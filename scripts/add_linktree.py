# סבב 1 מהחנות הישנה בלינקטרי (25/10/2026, אושר ע"י יורם): מוסיף 43 מוצרים לאוספים באתר ופותח אוסף "שלט, טיימר וטיימלאפס".
# רץ ב-GitHub Actions: מושך נתונים עדכניים ויוצר קישורי שותפים במזהה website.
import os, sys, json, time, hmac, hashlib, requests
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

def pct(s):
    try: return float(str(s).replace('%', ''))
    except Exception: return 0.0

ALL = ['M', 'D', 'C']
NEW_COLL = {'id': 'remote', 'name': 'שלט, טיימר וטיימלאפס', 'title': 'שלטים, טיימרים וטיימלאפס',
            'intro': 'צילום בלי לגעת במצלמה: בלי רעידות בחשיפה ארוכה, צילומי טיימלאפס של שקיעה או עננים, ותמונה קבוצתית שגם אתם בה. ויש גם טריק: להפוך את המצלמה למצלמת רשת.',
            'groups': []}
# (אוסף, מספר, מותג, כותרת, מתאים ל, הערה)
P = [
 ('cards', '32832711883', 'UGREEN', 'קורא כרטיסי זיכרון לטייפ-סי ולחיבור רגיל', ALL + ['P'], 'נמכר באלפים'),
 ('cards', '4000594534315', 'Netac', 'כרטיס זיכרון מיקרו מהיר', ['A', 'P', 'R'], ''),
 ('batteries', '1005005982265490', '', 'סוללה EN-EL14a לניקון D3000 ו-D5000', ['D'], 'סוללה תואמת'),
 ('bags', '32820718193', 'JJC', 'נרתיק מרופד לעדשה', ALL, ''),
 ('straps', '1005007624531237', 'PGYTECH', 'מחברים מהירים לרצועת מצלמה', ALL, ''),
 ('straps', '1005010634788498', 'PGYTECH', 'רצועת יד דקה עם שחרור מהיר', ALL, ''),
 ('straps', '1005009419105594', 'PGYTECH', 'רצועה קלועה לטלפון', ['P'], ''),
 ('straps', '1005005975868053', 'PGYTECH', 'תושבת צוואר למצלמת אקסטרים', ['A', 'P'], 'צילום מנקודת המבט שלכם'),
 ('straps', '1005008683628199', 'PGYTECH', 'קלמפ ופלטה לשחרור מהיר בתקן ארקה', ALL, ''),
 ('straps', '1005006476883955', 'JJC', 'רצועה לתליית ציוד על רגלי החצובה', ALL, ''),
 ('straps', '1005006039565570', '', 'פלטת שחרור מהיר אוניברסלית בתקן ארקה', ALL, 'נמכר מאוד'),
 ('tripods', '4000295965415', 'Ulanzi', 'חצובת שולחן קטנה שהיא גם ידית אחיזה', ALL + ['P'], ''),
 ('tripods', '1005007621087158', 'Ulanzi', 'בסיס טעינה וחצובה למצלמת הכיס של די ג׳יי איי', ['K'], ''),
 ('tripods', '1005007505914091', 'Ulanzi', 'חצובה עם שחרור מהיר בלחיצה אחת', ALL, ''),
 ('filters', '1005005358517125', 'K&F', 'פילטר אפור משתנה לחשיפה ארוכה ביום', ALL, 'נמכר באלפים'),
 ('filters', '1005002218348425', 'K&F', 'פילטר מקטב: שמיים כחולים ובלי השתקפויות', ALL, 'נמכר באלפים'),
 ('filters', '1005004754351276', '', 'טבעות מתאם לפילטרים בין קטרים', ALL, 'פילטר אחד לכמה עדשות'),
 ('filters', '1005002566769965', '', 'מכסה עדשה ממתכת לעדשות גדולות', ALL, ''),
 ('filters', '4001234644220', 'Hoya', 'פילטר הגנה לעדשה', ALL, ''),
 ('filters', '1005003658922855', '', 'פילטר הגנה למצלמת Canon G7X', ['C'], ''),
 ('filters', '1005006280445673', 'JJC', 'דיסק לאיזון לבן מדויק', ALL, ''),
 ('adapters', '1005007218550542', 'Andoer', 'מתאם עדשות Canon EF ל-RF, עם פוקוס אוטומטי', ['M'], ''),
 ('cleaning', '1005007003455573', '', 'ערכת ניקוי למצלמה ולמסכים', ALL + ['P'], 'נמכר באלפים'),
 ('cleaning', '1005005401605542', '', 'מגן מסך מזכוכית למצלמות Canon R8, R7, R6, R50', ['M'], 'נמכר באלפים'),
 ('cleaning', '1005004836333410', 'K&F', 'מקלוני ניקוי לחיישן המצלמה', ['M', 'D'], ''),
 ('cleaning', '1005010494951357', 'K&F', 'מפוח אוויר חשמלי לניקוי ציוד', ALL + ['P'], 'גאדג׳ט וואו'),
 ('cleaning', '1005008091338918', 'K&F', 'מפוח אוויר ידני עם פיה מתחלפת', ALL, ''),
 ('lighting', '1005007038803141', '', 'פנל תאורה צבעוני קטן', ALL + ['P'], ''),
 ('product', '1005006692082506', '', 'כדור זכוכית לצילום יצירתי', ALL + ['P'], 'רעיון לצילום שונה'),
 ('phone', '1005006394370045', 'Ulanzi', 'כלוב לאייפון לצילום ווידאו', ['P'], ''),
 ('video', '1005006124935243', 'Minifocus', 'תושבת למסך חיצוני על נעל המצלמה', ['M', 'D'], ''),
 ('video', '32853039475', 'SmallRig', 'מחבר מוטות לריג וידאו', ['M', 'D'], ''),
 ('video', '1005006896677162', '', 'מארז צלילה למצלמת Insta360 X4', ['A'], ''),
 ('video', '1005002996786975', 'Ulanzi', 'זרוע קסם עם קלמפ', ALL + ['P', 'A'], ''),
 ('video', '32854699427', 'SmallRig', 'מוט קרבון לריג וידאו', ['M', 'D'], ''),
 ('video', '4001192739625', 'SmallRig', 'מחזיק סוללה ניידת לריג', ALL + ['P'], ''),
 ('video', '1005006924581539', 'Ulanzi', 'פנס קטן עמיד למים', ['A', 'P'], ''),
 ('nature', '1005006090960903', '', 'מעיל הסוואה שקט ועמיד למים', [], 'לצילום ציפורים מהמסתור'),
 ('nature', '1005005779638769', 'Selens', 'שק הסוואה לתמיכה בעדשה', ALL, ''),
 ('remote', '1005003290313156', 'AODELAN', 'שלט טיימלאפס עם טיימר', ['M', 'D'], 'לבדוק התאמה לדגם בדף המוצר'),
 ('remote', '1005004747576016', '', 'שלט טיימלאפס עם מסך', ['M', 'D'], 'לבדוק התאמה לדגם בדף המוצר'),
 ('remote', '4001244652610', 'JJC', 'שלט בלוטות׳ למצלמות סוני', ['M'], ''),
 ('remote', '1005005874070478', '', 'כרטיס לכידה: המצלמה הופכת למצלמת רשת', ALL, 'רעיון יצירתי'),
]
ids = [p[1] for p in P]
info = {}
for i in range(0, len(ids), 20):
    res = call('aliexpress.affiliate.productdetail.get', product_ids=','.join(ids[i:i + 20]), target_currency='USD',
               target_language='EN', country='IL', tracking_id='website')
    root = (res.get('aliexpress_affiliate_productdetail_get_response') or {}).get('resp_result') or {}
    for x in ((root.get('result') or {}).get('products') or {}).get('product', []):
        info[str(x['product_id'])] = x
    time.sleep(0.5)
links = {}
urls = [f'https://www.aliexpress.com/item/{i}.html' for i in ids]
for i in range(0, len(urls), 20):
    res = call('aliexpress.affiliate.link.generate', promotion_link_type=0, source_values=','.join(urls[i:i + 20]), tracking_id='website')
    root = (res.get('aliexpress_affiliate_link_generate_response') or {}).get('resp_result') or {}
    for l in ((root.get('result') or {}).get('promotion_links') or {}).get('promotion_link', []):
        m = str(l.get('source_value', '')).split('/item/')[-1].split('.')[0]
        links[m] = l.get('promotion_link')
    time.sleep(0.5)

db = json.load(open('data/products.json', encoding='utf-8'))
if not any(c['id'] == 'remote' for c in db['collections']):
    db['collections'].append(NEW_COLL)
have = {p['id'] for p in db['products']}
added, skipped = 0, []
for coll, pid, brand, title, fr, note in P:
    x = info.get(pid)
    if pid in have or not x or not links.get(pid):
        skipped.append(pid); continue
    db['products'].append({'collection': coll, 'group': '', 'id': pid, 'brand': brand, 'title': title, 'code': '', 'kind': '',
                           'fits': '', 'note': note, 'price': pct(x.get('target_sale_price')), 'rating': pct(x.get('evaluate_rate')),
                           'sold': int(pct(x.get('lastest_volume'))), 'link': links[pid], 'img': x.get('product_main_image_url'),
                           'tid': 'website', 'for': fr})
    added += 1
db['updated'] = time.strftime('%Y-%m-%d')
json.dump(db, open('data/products.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('added', added, 'skipped', skipped)
