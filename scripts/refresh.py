# רענון שבועי של מוצרי החנות "צילום בכל גיל".
# רץ אוטומטית ב-GitHub Actions. לכל מוצר בודק באלי אקספרס: שהוא עדיין קיים ונשלח לישראל,
# ומעדכן מחיר, דירוג ומספר הזמנות. מוצר שלא נמצא מסומן "missing" ומוסתר באתר עד שיורם מאשר להסיר אותו.
# כלום לא עולה לאתר בלי אישור: התוצאה נפתחת כבקשת שינוי (Pull Request) שמחכה לאישור.
# הסוד נקרא ממשתנה הסביבה ALI_APP_SECRET שנשמר ב-GitHub Secrets – לא בקוד.
import os, sys, json, time, hmac, hashlib, datetime, requests

APP_KEY = os.environ.get('ALI_APP_KEY', '553904')
APP_SECRET = os.environ.get('ALI_APP_SECRET', '').strip()
URL = 'https://api-sg.aliexpress.com/sync'
DATA = 'data/products.json'
REPORT = 'data/refresh_report.md'
PRICE_ALERT = 0.15   # שינוי מחיר של יותר מ-15% מופיע בדוח

if not APP_SECRET:
    sys.exit('חסר הסוד ALI_APP_SECRET ב-GitHub Secrets')

def call(method, **params):
    res = {}
    for attempt in range(4):
        p = {'app_key': APP_KEY, 'method': method, 'sign_method': 'sha256',
             'timestamp': str(int(time.time() * 1000))}
        p.update({k: str(v) for k, v in params.items()})
        base = ''.join(k + p[k] for k in sorted(p))
        p['sign'] = hmac.new(APP_SECRET.encode(), base.encode(), hashlib.sha256).hexdigest().upper()
        try:
            res = requests.post(URL, data=p, timeout=30).json()
        except Exception as e:
            res = {'error': str(e)}
        if 'ApiCallLimit' in str(res)[:300]:
            time.sleep(2 + attempt * 2)
            continue
        return res
    return res

def num(s):
    try: return float(str(s).replace('%', ''))
    except Exception: return None

db = json.load(open(DATA, encoding='utf-8'))
prods = db['products']
ids = [p['id'] for p in prods]
found = {}
for i in range(0, len(ids), 20):
    res = call('aliexpress.affiliate.productdetail.get', product_ids=','.join(ids[i:i + 20]),
               target_currency='USD', target_language='EN', country='IL', tracking_id='linktree')
    if 'error_response' in res:
        sys.exit(f"שגיאת API: {res['error_response'].get('code')}")
    root = res.get('aliexpress_affiliate_productdetail_get_response', {}).get('resp_result', {})
    for x in ((root.get('result') or {}).get('products') or {}).get('product', []):
        found[str(x.get('product_id'))] = x
    time.sleep(0.5)

missing, price_moves, back = [], [], []
for p in prods:
    x = found.get(p['id'])
    if not x:
        if p.get('status') != 'missing':
            missing.append(p)
        p['status'] = 'missing'
        continue
    if p.get('status') == 'missing':
        back.append(p)
    p.pop('status', None)
    new_price, new_rate, new_sold = num(x.get('target_sale_price')), num(x.get('evaluate_rate')), num(x.get('lastest_volume'))
    if new_price and p.get('price') and abs(new_price - p['price']) / p['price'] > PRICE_ALERT:
        price_moves.append((p, p['price'], new_price))
    if new_price: p['price'] = round(new_price, 2)
    if new_rate: p['rating'] = new_rate
    if new_sold is not None: p['sold'] = int(new_sold)
    if x.get('product_main_image_url'): p['img'] = x['product_main_image_url']

# קישורי שותפים עם מזהה המעקב website לכל מוצר שעדיין אין לו
TRACKING = 'website'
new_links = 0
todo = [p for p in prods if p.get('tid') != TRACKING and p['id'] in found]
for i in range(0, len(todo), 20):
    part = todo[i:i + 20]
    urls = [(found[p['id']].get('product_detail_url') or f"https://www.aliexpress.com/item/{p['id']}.html").split('?')[0] for p in part]
    res = call('aliexpress.affiliate.link.generate', promotion_link_type=0, source_values=','.join(urls), tracking_id=TRACKING)
    root = res.get('aliexpress_affiliate_link_generate_response', {}).get('resp_result', {})
    got = {str(l.get('source_value', '')).split('?')[0]: l.get('promotion_link') for l in
           ((root.get('result') or {}).get('promotion_links') or {}).get('promotion_link', [])}
    for p, u in zip(part, urls):
        if got.get(u):
            p['link'] = got[u]; p['tid'] = TRACKING; new_links += 1
    time.sleep(0.5)

today = datetime.date.today().isoformat()
db['updated'] = today
json.dump(db, open(DATA, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

name = lambda p: f"{p['brand']} – {p['title']} {p.get('code', '')}".strip()
lines = [f'# רענון מוצרים – {today}', '',
         f'נבדקו {len(prods)} מוצרים. נמצאו {len(found)}. קישורי website חדשים: {new_links}.', '']
lines += ['## מוצרים שלא נמצאו (מוסתרים באתר עד החלטה)'] + ([f'- {name(p)} ({p["id"]})' for p in missing] or ['- אין']) + ['']
lines += ['## מוצרים שחזרו'] + ([f'- {name(p)}' for p in back] or ['- אין']) + ['']
lines += [f'## שינויי מחיר מעל {int(PRICE_ALERT * 100)}%'] + ([f'- {name(p)}: {a}$ → {b}$' for p, a, b in price_moves] or ['- אין']) + ['']
open(REPORT, 'w', encoding='utf-8').write('\n'.join(lines))
print('\n'.join(lines))
