# בדיקת מוצרים לפי מספר: חנות, מחיר, דירוג ומכירות. למחקר בלבד (לא משנה את האתר).
# קורא את search/lookup.txt (מספר מוצר בכל שורה) וכותב את search/lookup.json.
import os, sys, json, time, hmac, hashlib, datetime, requests
APP_KEY = os.environ.get('ALI_APP_KEY', '553904')
APP_SECRET = os.environ.get('ALI_APP_SECRET', '').strip()
if not APP_SECRET:
    sys.exit('חסר הסוד ALI_APP_SECRET')

def call(method, **params):
    res = {}
    for attempt in range(4):
        p = {'app_key': APP_KEY, 'method': method, 'sign_method': 'sha256', 'timestamp': str(int(time.time() * 1000))}
        p.update({k: str(v) for k, v in params.items()})
        p['sign'] = hmac.new(APP_SECRET.encode(), ''.join(k + p[k] for k in sorted(p)).encode(), hashlib.sha256).hexdigest().upper()
        try:
            res = requests.post('https://api-sg.aliexpress.com/sync', data=p, timeout=30).json()
        except Exception as e:
            res = {'error': str(e)}
        if 'ApiCallLimit' in str(res)[:300]:
            time.sleep(2 + attempt * 2); continue
        return res
    return res

ids = [l.split('#')[0].strip() for l in open('search/lookup.txt', encoding='utf-8')]
ids = [i for i in ids if i.isdigit()]
out = []
for i in range(0, len(ids), 20):
    chunk = ids[i:i + 20]
    res = call('aliexpress.affiliate.productdetail.get', product_ids=','.join(chunk), target_currency='USD',
               target_language='EN', country='IL', tracking_id='website')
    root = res.get('aliexpress_affiliate_productdetail_get_response', {}).get('resp_result', {})
    prods = ((root.get('result') or {}).get('products') or {}).get('product', [])
    got = set()
    for x in prods:
        pid = str(x.get('product_id')); got.add(pid)
        out.append({'id': pid, 'title': x.get('product_title', ''), 'shop': x.get('shop_name', ''),
                    'shop_url': x.get('shop_url', ''), 'price': x.get('target_sale_price'),
                    'rating': x.get('evaluate_rate'), 'sold': x.get('lastest_volume'),
                    'commission': x.get('commission_rate'),
                    'category': x.get('second_level_category_name') or x.get('first_level_category_name')})
    for pid in chunk:
        if pid not in got:
            out.append({'id': pid, 'missing': 'לא נמצא בתוכנית השותפים'})
    time.sleep(0.5)
json.dump({'date': datetime.datetime.utcnow().isoformat(timespec='minutes'), 'products': out},
          open('search/lookup.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out), 'products')
