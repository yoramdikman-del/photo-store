# מיפוי החנות הישנה בלינקטרי: פותח כל קישור קצר, מוצא את מספר המוצר, ומושך נתונים עדכניים מה-API.
# קורא את search/linktree.txt (אוסף | קוד), כותב את search/linktree.json. למחקר בלבד, לא משנה את האתר.
import os, sys, re, json, time, hmac, hashlib, datetime, requests
from urllib.parse import unquote
APP_KEY = os.environ.get('ALI_APP_KEY', '553904')
APP_SECRET = os.environ.get('ALI_APP_SECRET', '').strip()
if not APP_SECRET:
    sys.exit('חסר הסוד ALI_APP_SECRET')
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36'}

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

def resolve(code):
    url = 'https://s.click.aliexpress.com/e/' + code
    try:
        r = requests.get(url, headers=UA, timeout=25, allow_redirects=True)
        blobs = [h.headers.get('Location', '') for h in r.history] + [r.url, r.text[:20000]]
        for b in blobs:
            b = unquote(unquote(b or ''))
            m = re.search(r'/item/(\d{10,17})', b) or re.search(r'productIds?=(\d{10,17})', b) or re.search(r'"productId"\s*:\s*"?(\d{10,17})', b)
            if m:
                return m.group(1)
    except Exception:
        pass
    return None

def pct(s):
    try: return float(str(s).replace('%', ''))
    except Exception: return 0.0

rows = []
for l in open('search/linktree.txt', encoding='utf-8'):
    if l.strip() and not l.startswith('#'):
        col, code = [x.strip() for x in l.split('|')]
        rows.append({'old_collection': col, 'code': code, 'id': resolve(code)})
        time.sleep(0.3)

store = set(re.findall(r'(\d{13,17})', open('data/products.json', encoding='utf-8').read()))
ids = sorted({r['id'] for r in rows if r['id']})
info = {}
for i in range(0, len(ids), 20):
    res = call('aliexpress.affiliate.productdetail.get', product_ids=','.join(ids[i:i + 20]), target_currency='USD',
               target_language='EN', country='IL', tracking_id='website')
    root = (res.get('aliexpress_affiliate_productdetail_get_response') or {}).get('resp_result') or {}
    for x in ((root.get('result') or {}).get('products') or {}).get('product', []):
        info[str(x.get('product_id'))] = {
            'title': x.get('product_title'), 'shop': x.get('shop_name'), 'price': pct(x.get('target_sale_price')),
            'rating': pct(x.get('evaluate_rate')), 'sold': int(pct(x.get('lastest_volume'))),
            'commission': max(pct(x.get('commission_rate')), pct(x.get('hot_product_commission_rate'))),
            'img': x.get('product_main_image_url'), 'cat': x.get('second_level_category_name') or x.get('first_level_category_name')}
    time.sleep(0.5)
for r in rows:
    r['in_store'] = bool(r['id'] and r['id'] in store)
    r['alive'] = bool(r['id'] and r['id'] in info)
    r.update(info.get(r['id'] or '', {}))
json.dump({'date': datetime.datetime.utcnow().isoformat(timespec='minutes'), 'rows': rows},
          open('search/linktree.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(rows), 'rows,', sum(1 for r in rows if r['id']), 'resolved,', sum(r['alive'] for r in rows), 'alive,', sum(r['in_store'] for r in rows), 'in store')
