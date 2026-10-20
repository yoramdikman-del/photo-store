# "מועמדים לחנות": סריקה שבועית לכל אוסף לפי data/collection_queries.json.
# כל אוסף מגדיר מילות חיפוש (q) ומילים שחייבות להופיע בשם המוצר (must), כדי לסנן מוצרים לא קשורים.
# מסננים לפי הכללים של יורם: חנות רשמית, דירוג 94% ומעלה, 100 מכירות לפחות, עד 200$, משלוח לישראל, עם עמלה,
# ורק מוצרים שעוד לא בחנות. לכל אוסף נשמרים עד 3 מועמדים. מסמנים גם מוצרים חלשים בחנות (דירוג ירד או נעלמו).
# התוצאה ב-data/store_candidates.json. לא מוצגת באתר: Claude ממליץ על עד 5 מוצרים בשבוע, ויורם מאשר.
import os, sys, json, time, hmac, hashlib, datetime, requests

APP_KEY = os.environ.get('ALI_APP_KEY', '553904')
APP_SECRET = os.environ.get('ALI_APP_SECRET', '').strip()
URL = 'https://api-sg.aliexpress.com/sync'
TRACKING = 'website'
MIN_RATE, MIN_SOLD, MAX_PRICE, PER_COLL = 94, 100, 200, 3
WEAK_RATE = 92
if not APP_SECRET:
    sys.exit('חסר הסוד ALI_APP_SECRET')

def call(method, **params):
    res = {}
    for attempt in range(4):
        p = {'app_key': APP_KEY, 'method': method, 'sign_method': 'sha256', 'timestamp': str(int(time.time() * 1000))}
        p.update({k: str(v) for k, v in params.items()})
        base = ''.join(k + p[k] for k in sorted(p))
        p['sign'] = hmac.new(APP_SECRET.encode(), base.encode(), hashlib.sha256).hexdigest().upper()
        try:
            res = requests.post(URL, data=p, timeout=30).json()
        except Exception as e:
            res = {'error': str(e)}
        if 'ApiCallLimit' in str(res)[:300]:
            time.sleep(2 + attempt * 2); continue
        return res
    return res

def num(s):
    try: return float(str(s).replace('%', ''))
    except Exception: return None

def gen_links(urls):
    res = call('aliexpress.affiliate.link.generate', promotion_link_type=0, source_values=','.join(urls), tracking_id=TRACKING)
    root = res.get('aliexpress_affiliate_link_generate_response', {}).get('resp_result', {})
    return {str(l.get('source_value', '')).split('?')[0]: l.get('promotion_link') for l in
            ((root.get('result') or {}).get('promotion_links') or {}).get('promotion_link', [])}

db = json.load(open('data/products.json', encoding='utf-8'))
have = {p['id'] for p in db['products']}
queries = json.load(open('data/collection_queries.json', encoding='utf-8'))
out, errors, taken = {}, [], set()
EXCLUDE = ['dash cam', 'lash', 'controller', 'earbud', 'headphone', 'car phone holder', 'car charger', 'baby monitor', 'aux', 'nvme', 'glue', 'watch', 'drone propeller']
for coll, spec in queries.items():
    qs, must = spec['q'], spec.get('must', [])
    cand = {}
    for q in qs:
        res = call('aliexpress.affiliate.product.query', keywords=q, ship_to_country='IL', target_currency='USD',
                   target_language='EN', page_size=50, page_no=1, sort='LAST_VOLUME_DESC', tracking_id=TRACKING)
        root = res.get('aliexpress_affiliate_product_query_response', {}).get('resp_result', {})
        if root.get('resp_code') != 200:
            errors.append(f'{coll} | {q}: {str(res)[:120]}'); continue
        for x in ((root.get('result') or {}).get('products') or {}).get('product', []):
            pid = str(x.get('product_id'))
            shop = (x.get('shop_name') or '').lower()
            rate, sold, price = num(x.get('evaluate_rate')) or 0, int(num(x.get('lastest_volume')) or 0), num(x.get('target_sale_price')) or 0
            comm = max(num(x.get('hot_product_commission_rate')) or 0, num(x.get('commission_rate')) or 0)
            title = (x.get('product_title') or '').lower()
            if pid in have or pid in taken or 'official' not in shop:
                continue
            if any(w in title for w in EXCLUDE) or not all(any(w in title for w in grp) for grp in must):
                continue
            if rate < MIN_RATE or sold < MIN_SOLD or not price or price > MAX_PRICE or comm <= 0:
                continue
            cand[pid] = {'id': pid, 'collection': coll, 'query': q, 'title': x.get('product_title', ''),
                         'shop': x.get('shop_name', ''), 'price': price, 'rating': rate, 'sold': sold, 'commission': comm,
                         'img': x.get('product_main_image_url'), 'url': (x.get('product_detail_url') or '').split('?')[0]}
        time.sleep(0.4)
    best = sorted(cand.values(), key=lambda c: -c['sold'])[:PER_COLL]
    taken.update(c['id'] for c in best)
    out[coll] = best

allc = [c for cs in out.values() for c in cs]
links = {}
urls = [c['url'] for c in allc if c['url']]
for i in range(0, len(urls), 20):
    links.update(gen_links(urls[i:i + 20])); time.sleep(0.5)
for c in allc:
    c['link'] = links.get(c['url'])

weak = [{'id': p['id'], 'collection': p['collection'], 'brand': p.get('brand'), 'title': p.get('title'),
         'rating': p.get('rating'), 'status': p.get('status')}
        for p in db['products'] if p.get('status') == 'missing' or (p.get('rating') and p['rating'] < WEAK_RATE)]

json.dump({'date': datetime.date.today().isoformat(), 'rules': {'min_rating': MIN_RATE, 'min_sold': MIN_SOLD,
           'max_price': MAX_PRICE, 'official_store': True}, 'errors': errors, 'candidates': out, 'weak': weak},
          open('data/store_candidates.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(allc), 'candidates,', len(weak), 'weak,', len(errors), 'errors')
