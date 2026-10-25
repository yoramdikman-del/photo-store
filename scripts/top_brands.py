# המוצרים הנמכרים והמדורגים ביותר של מותגי הצילום (מחקר בלבד, לא משנה את האתר).
# קורא את search/top_brands.txt, כותב ל-search/top_brands.json ול-search/top_brands.csv.
# סינון: חנות שהשם שלה כולל את המותג, 100+ הזמנות, דירוג חיובי 94%+ (ה-API לא מחזיר כוכבים ולא דירוג חנות).
import os, sys, json, time, hmac, hashlib, datetime, csv, re, requests

APP_KEY = os.environ.get('ALI_APP_KEY', '553904')
APP_SECRET = os.environ.get('ALI_APP_SECRET', '').strip()
URL = 'https://api-sg.aliexpress.com/sync'
TRACKING = 'website'
MIN_SOLD, MIN_RATE, TOP_N, PAGES = 100, 94.0, 6, 3
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
    try: return float(str(s).replace('%', '').strip())
    except Exception: return 0.0

try:
    store_ids = set(re.findall(r'(\d{13,17})', open('data/products.json', encoding='utf-8').read()))
except Exception:
    store_ids = set()

brands = []
for l in open('search/top_brands.txt', encoding='utf-8'):
    if l.strip() and not l.startswith('#'):
        b, k, c = [x.strip() for x in l.split('|')]
        brands.append((b, k.lower(), c))

out, summary, errors = [], [], []
for brand, key, cat in brands:
    found = {}
    shops = {}
    for method in ('aliexpress.affiliate.product.query', 'aliexpress.affiliate.hotproduct.query'):
        for page in range(1, PAGES + 1):
            res = call(method, keywords=brand, ship_to_country='IL', target_currency='USD', target_language='EN',
                       page_size=50, page_no=page, sort='LAST_VOLUME_DESC', tracking_id=TRACKING)
            root = (res.get(method.replace('.', '_') + '_response') or {}).get('resp_result') or {}
            if root.get('resp_code') != 200:
                if page == 1:
                    errors.append(f'{brand} {method.split(".")[-2]}: {str(res)[:150]}')
                break
            items = ((root.get('result') or {}).get('products') or {}).get('product', [])
            for x in items:
                shop = (x.get('shop_name') or '')
                if key not in shop.lower().replace(' ', '') and key not in shop.lower():
                    continue
                shops[shop] = shops.get(shop, 0) + 1
                pid = str(x.get('product_id'))
                comm = max(num(x.get('commission_rate')), num(x.get('hot_product_commission_rate')))
                imgs = [x.get('product_main_image_url')] + (((x.get('product_small_image_urls') or {}).get('string')) or [])
                r = found.setdefault(pid, {
                    'brand': brand, 'category': cat, 'id': pid, 'title': x.get('product_title', ''),
                    'shop': shop, 'official': any(w in shop.lower() for w in ('official', 'flagship')),
                    'price': num(x.get('target_sale_price')), 'orig_price': num(x.get('target_original_price')),
                    'rating': num(x.get('evaluate_rate')), 'sold': int(num(x.get('lastest_volume'))),
                    'commission': comm, 'hot': method.endswith('hotproduct.query'),
                    'cat_path': ' > '.join(v for v in (x.get('first_level_category_name'), x.get('second_level_category_name')) if v),
                    'images': [i for i in dict.fromkeys(imgs) if i][:4],
                    'url': (x.get('product_detail_url') or '').split('?')[0], 'in_store': pid in store_ids})
                r['commission'] = max(r['commission'], comm)
                r['hot'] = r['hot'] or method.endswith('hotproduct.query')
            if len(items) < 50:
                break
            time.sleep(0.4)
    total = len(found)
    good = [r for r in found.values() if r['sold'] >= MIN_SOLD and r['rating'] >= MIN_RATE]
    for r in good:
        r['est_month_usd'] = round(r['price'] * r['commission'] / 100 * r['sold'], 1)
        r['score'] = r['est_month_usd'] * (1.15 if r['official'] else 1)
    good.sort(key=lambda r: -r['score'])
    top = good[:TOP_N]
    out += top
    summary.append({'brand': brand, 'category': cat, 'brand_items': total, 'passed': len(good),
                    'shops': sorted(shops, key=lambda s: -shops[s])[:3]})
    time.sleep(0.4)

urls = [r['url'] for r in out if r['url']]
links = {}
for i in range(0, len(urls), 20):
    res = call('aliexpress.affiliate.link.generate', promotion_link_type=0, source_values=','.join(urls[i:i + 20]), tracking_id=TRACKING)
    root = (res.get('aliexpress_affiliate_link_generate_response') or {}).get('resp_result') or {}
    for l in ((root.get('result') or {}).get('promotion_links') or {}).get('promotion_link', []):
        links[str(l.get('source_value', '')).split('?')[0]] = l.get('promotion_link')
    time.sleep(0.5)
for r in out:
    r['link'] = links.get(r['url'])

json.dump({'date': datetime.datetime.utcnow().isoformat(timespec='minutes'),
           'filters': {'min_sold': MIN_SOLD, 'min_positive_rate': MIN_RATE, 'top_per_brand': TOP_N, 'tracking': TRACKING},
           'summary': summary, 'errors': errors, 'products': out},
          open('search/top_brands.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
cols = ['brand', 'category', 'id', 'title', 'shop', 'official', 'price', 'orig_price', 'rating', 'sold', 'commission',
        'hot', 'est_month_usd', 'in_store', 'cat_path', 'link', 'url', 'images']
with open('search/top_brands.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f); w.writerow(cols)
    for r in out:
        w.writerow([' | '.join(r[c]) if c == 'images' else r.get(c, '') for c in cols])
print(len(out), 'products,', len(errors), 'errors')
