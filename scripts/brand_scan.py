# "חדש מהמותגים": סריקה שבועית של חנויות רשמיות של מותגים נבחרים באלי אקספרס.
# ה-API לא ממיין לפי "הכי חדש", לכן משווים לרשימת המוצרים שכבר נראו (data/brand_seen.json):
# מוצר שלא נראה קודם, מהחנות הרשמית של המותג, עם דירוג סביר (או בלי דירוג עדיין) – מועמד ל"חדש".
# בהרצה הראשונה כל המוצרים נשמרים כ"נראו", ומועמדים הם רק מוצרים עם מעט מכירות (כנראה חדשים).
# התוצאה נכתבת ל-data/brand_new.json. היא לא מוצגת באתר: Claude בוחר ממנה פריטים לגיליון השבועי, ויורם מאשר.
import os, sys, json, time, hmac, hashlib, datetime, requests

APP_KEY = os.environ.get('ALI_APP_KEY', '553904')
APP_SECRET = os.environ.get('ALI_APP_SECRET', '').strip()
URL = 'https://api-sg.aliexpress.com/sync'
TRACKING = 'website'
SEEN = 'data/brand_seen.json'
OUT = 'data/brand_new.json'
# מותג -> מילה שחייבת להופיע בשם החנות (יחד עם "official")
BRANDS = {'PGYTECH': 'pgytech', 'SmallRig': 'smallrig', 'Ulanzi': 'ulanzi', 'K&F Concept': 'k&f',
          'Godox': 'godox', 'NEEWER': 'neewer', 'TELESIN': 'telesin', 'JJC': 'jjc', 'BOYA': 'boya',
          'Freewell': 'freewell', 'Fotopro': 'fotopro', 'TTArtisan': 'ttartisan', '7artisans': '7artisans',
          'Viltrox': 'viltrox'}
MAX_PER_BRAND = 4
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

try:
    seen = json.load(open(SEEN, encoding='utf-8'))
except Exception:
    seen = {}
first_run = not seen
today = datetime.date.today().isoformat()
cands, errors = [], []
for brand, key in BRANDS.items():
    found = {}
    for sort in ('LAST_VOLUME_ASC', 'LAST_VOLUME_DESC'):
        for page in (1, 2):
            res = call('aliexpress.affiliate.product.query', keywords=brand, ship_to_country='IL', target_currency='USD',
                       target_language='EN', page_size=50, page_no=page, sort=sort, tracking_id=TRACKING)
            root = res.get('aliexpress_affiliate_product_query_response', {}).get('resp_result', {})
            if root.get('resp_code') != 200:
                errors.append(f'{brand} {sort} {page}: {str(res)[:120]}'); break
            items = ((root.get('result') or {}).get('products') or {}).get('product', [])
            for x in items:
                shop = (x.get('shop_name') or '').lower()
                if key in shop and 'official' in shop:
                    found[str(x.get('product_id'))] = x
            if len(items) < 50:
                break
            time.sleep(0.4)
    new = []
    for pid, x in found.items():
        is_new = pid not in seen
        sold = int(num(x.get('lastest_volume')) or 0)
        rate = num(x.get('evaluate_rate'))
        if first_run:
            is_new = sold <= 20
        if is_new and (rate is None or rate >= 90):
            new.append((sold, pid, x, rate))
        seen.setdefault(pid, today)
    new.sort(key=lambda t: -t[0])
    for sold, pid, x, rate in new[:MAX_PER_BRAND]:
        cands.append({'id': pid, 'brand': brand, 'title': x.get('product_title', ''), 'shop': x.get('shop_name', ''),
                      'price': num(x.get('target_sale_price')), 'rating': rate, 'sold': sold,
                      'img': x.get('product_main_image_url'), 'url': (x.get('product_detail_url') or '').split('?')[0],
                      'video': x.get('product_video_url') or '', 'first_seen': seen[pid]})
    time.sleep(0.4)

urls = [c['url'] for c in cands if c['url']]
links = {}
for i in range(0, len(urls), 20):
    links.update(gen_links(urls[i:i + 20])); time.sleep(0.5)
for c in cands:
    c['link'] = links.get(c['url'])

json.dump(seen, open(SEEN, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
json.dump({'date': today, 'first_run': first_run, 'errors': errors, 'candidates': cands},
          open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(cands), 'candidates,', len(seen), 'seen,', len(errors), 'errors')
