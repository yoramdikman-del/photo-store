# מוסיף את אוסף "מתאמי עדשות" (סבב 1, 19/10/2026) ל-data/products.json.
# הנתונים (מחיר, דירוג, הזמנות, תמונה) מסריקת search/results.json. הקישורים נוצרים ברענון (status=pending עד אז).
import json
S = {p['id']: p for p in json.load(open('search/results.json', encoding='utf-8'))['products']}
db = json.load(open('data/products.json', encoding='utf-8'))

COLL = {
    'id': 'adapters', 'name': 'מתאמי עדשות',
    'title': 'מתאמי עדשות: ממשיכים לצלם עם העדשות שלכם',
    'intro': 'החלפתם מצלמה? קניתם עדשה ממותג אחר? מתאם טוב מחבר עדשה למצלמה. יש מתאמים ידניים פשוטים, ויש מתאמים אלקטרוניים שמעבירים פוקוס אוטומטי, צמצם וייצוב. באיכות כאן לא מתפשרים.',
    'search': 'חיפוש: EF, RF, Sony E, Nikon Z, M42, Fuji X',
    'how': ['איך בוחרים מתאם?', 'בודקים שני דברים: מאיזו עדשה (למשל Canon EF) ולאיזו מצלמה (למשל Sony E). מתאם ידני לא מעביר חשמל, והפוקוס והצמצם ידניים. מתאם אלקטרוני מעביר פוקוס, צמצם וייצוב, אבל מהירות הפוקוס תלויה בעדשה ובמצלמה.'],
    'groups': [['same', 'אותו מותג, עם פוקוס אוטומטי'], ['cross', 'בין מותגים, עם פוקוס אוטומטי'],
               ['booster', 'מכווצי מוקד (Speed Booster)'], ['manual', "ידניים ועדשות וינטג'"]],
}
# (קבוצה, מספר, מותג, כותרת, קוד, סוג, מתאים ל, הערה, מותג מצלמה לחיפוש, הערת עדשה, בלי עמלה, חיפוש חלופה)
A = [
 ('same', '1005003721929534', 'K&F', 'מתאם עדשות Canon EF למצלמות Canon RF, עם פוקוס אוטומטי', 'EF → RF', 'מתאם אלקטרוני', 'Canon R50, R10, R8, R7, R6, R5, RP', 'מעביר פוקוס, צמצם וייצוב', 'canon', 'לעדשות Canon EF/EF-S', False, ''),
 ('same', '1005006304613402', 'K&F', 'מתאם עדשות Canon EF ל-RF, עם פוקוס אוטומטי – הנמכר ביותר', 'EF → RF', 'מתאם אלקטרוני', 'Canon R50, R10, R8, R7, R6, R5, RP', 'הכי נמכר בקטגוריה', 'canon', 'לעדשות Canon EF/EF-S', True, 'EF to RF adapter autofocus'),
 ('same', '4000106384086', 'JJC', 'מתאם עדשות Canon EF ל-RF, עם פוקוס אוטומטי', 'EF → RF', 'מתאם אלקטרוני', 'Canon R50, R10, R8, R7, R6, R5, RP', 'חנות רשמית של JJC', 'canon', 'לעדשות Canon EF/EF-S', False, ''),
 ('same', '1005004696775559', 'Meike', 'מתאם עדשות Canon EF ל-RF, עם פוקוס אוטומטי', 'EF → RF', 'מתאם אלקטרוני', 'Canon R50, R10, R8, R7, R6, R5, RP', '', 'canon', 'לעדשות Canon EF/EF-S', True, 'EF to RF adapter autofocus'),
 ('same', '1005011921899971', 'Shoten', 'מתאם אלקטרוני לעדשות Nikon F למצלמות Nikon Z', 'F → Z', 'מתאם אלקטרוני', 'Nikon Z5, Z6, Z7, Z8, Zf, Z50, Z fc', 'פוקוס אוטומטי בעדשות עם מנוע (AF-S/AF-P) – לבדוק בדף המוצר', 'nikon', 'לעדשות Nikon F', True, 'Nikon F to Z adapter autofocus'),
 ('cross', '1005006186166116', 'K&F', 'מתאם עדשות Canon EF למצלמות Sony E, עם פוקוס אוטומטי', 'EF → Sony E', 'מתאם אלקטרוני', 'Sony A7, A6000–A6700, ZV-E10, FX3', '', 'sony', 'לעדשות Canon EF', False, ''),
 ('cross', '1005008243776880', '7artisans', 'מתאם עדשות Canon EF ל-Sony E, עם פוקוס אוטומטי', 'EF → Sony E', 'מתאם אלקטרוני', 'Sony A7, A6000–A6700, ZV-E10, FX3', '', 'sony', 'לעדשות Canon EF', False, ''),
 ('cross', '1005009244271681', 'Viltrox', 'מתאם עדשות Nikon F ל-Sony E, עם פוקוס אוטומטי', 'F → Sony E', 'מתאם אלקטרוני', 'Sony A7, A6000–A6700, ZV-E10', 'פוקוס אוטומטי בעדשות עם מנוע (AF-S/AF-P)', 'sony', 'לעדשות Nikon F', True, 'Nikon F to Sony E adapter autofocus'),
 ('cross', '1005008365293017', 'Viltrox', 'מתאם עדשות Sony E למצלמות Nikon Z, עם פוקוס אוטומטי', 'Sony E → Z', 'מתאם אלקטרוני', 'Nikon Z5, Z6, Z7, Z8, Zf, Z50', '', 'nikon', 'לעדשות Sony E', True, 'Sony E to Nikon Z adapter autofocus'),
 ('cross', '1005007561939468', 'Megadap', 'מתאם ETZ21 Pro+ לעדשות Sony E (כולל Sigma ו-Tamron) למצלמות Nikon Z', 'Sony E → Z', 'מתאם אלקטרוני', 'Nikon Z5, Z6, Z7, Z8, Zf, ZR', 'דגם מקצועי', 'nikon', 'לעדשות Sony E', True, 'Sony E to Nikon Z adapter autofocus'),
 ('cross', '1005009667074868', 'Viltrox', 'מתאם עדשות Canon EF למצלמות Nikon Z, עם פוקוס אוטומטי', 'EF → Z', 'מתאם אלקטרוני', 'Nikon Z5, Z6, Z7, Z8, Zf, Z50', '', 'nikon', 'לעדשות Canon EF', True, 'EF to Nikon Z adapter autofocus'),
 ('cross', '1005004962235865', 'Meike', 'מתאם עדשות Canon EF ל-Nikon Z, עם פוקוס אוטומטי', 'EF → Z', 'מתאם אלקטרוני', 'Nikon Z5, Z6, Z7, Z8, Zf, Z50', '', 'nikon', 'לעדשות Canon EF', False, ''),
 ('cross', '1005011925026902', 'K&F', 'מתאם עדשות Canon EF למצלמות Fuji X, עם פוקוס אוטומטי', 'EF → Fuji X', 'מתאם אלקטרוני', 'Fujifilm X-T30, X-T50, X-S10, X-E4, X-H2', 'דגם חדש', 'fuji', 'לעדשות Canon EF', False, ''),
 ('cross', '1005007937952410', 'Fringer', 'מתאם EF-FX Pro III לעדשות Canon EF למצלמות Fuji X', 'EF → Fuji X', 'מתאם אלקטרוני', 'Fujifilm X-T30, X-T50, X-S10, X-E4, X-H2', 'דגם מקצועי', 'fuji', 'לעדשות Canon EF', True, 'EF to Fuji X adapter autofocus'),
 ('cross', '4001156708662', 'Fringer', 'מתאם NF-FX II לעדשות Nikon F למצלמות Fuji X', 'F → Fuji X', 'מתאם אלקטרוני', 'Fujifilm X-T30, X-T50, X-S10, X-E4, X-H2', 'פוקוס אוטומטי בעדשות AF-S/AF-P', 'fuji', 'לעדשות Nikon F', True, 'Nikon F to Fuji X adapter autofocus'),
 ('cross', '1005008548031525', 'Viltrox', 'מתאם EF-L Pro לעדשות Canon EF למצלמות L-Mount', 'EF → L', 'מתאם אלקטרוני', 'Panasonic S5, S1, Sigma fp, Leica SL', '', '', '', True, 'EF to L mount adapter autofocus'),
 ('booster', '1005009514083250', 'Viltrox', 'מכווץ מוקד 0.71x לעדשות Canon EF למצלמות Sony E', 'EF → Sony E', 'Speed Booster', 'Sony A6000–A6700, ZV-E10, FX30', 'בחיישן APS-C: שדה ראייה קרוב לפול פריים, ועוד כ-1 סטופ אור', 'sony', 'לעדשות Canon EF', True, 'Viltrox speed booster'),
 ('booster', '1005008548063264', 'Viltrox', 'מכווץ מוקד 0.71x לעדשות Canon EF למצלמות Canon EOS M', 'EF → EOS M', 'Speed Booster', 'Canon M50, M6, M200', 'שדה ראייה רחב יותר ועוד כ-1 סטופ אור', '', '', True, 'Canon EF to EOS M speed booster'),
 ('booster', '1005008548035908', 'Viltrox', 'מכווץ מוקד לעדשות Canon EF למצלמות Micro 4/3', 'EF → M4/3', 'Speed Booster', 'Panasonic GH5, GH6, G9, Olympus OM-D', 'שדה ראייה רחב יותר ועוד כ-1 סטופ אור', '', '', True, 'EF to M43 speed booster'),
 ('manual', '1005008239138047', 'K&F', 'מתאם לעדשות וינטג\' M42 לכל המצלמות', 'M42', 'מתאם ידני', 'Sony E, Canon RF/EF/M, Nikon F/Z, Fuji X – בוחרים בדף המוצר', 'הכי נמכר בקטגוריה', '', '', False, ''),
 ('manual', '1005004383481162', 'K&F', 'מתאם M42 ל-Sony E, דגם PRO', 'M42 → Sony E', 'מתאם ידני', 'Sony A7, A6000–A6700, ZV-E10', '', 'sony', 'לעדשות M42', False, ''),
 ('manual', '1005010217006000', 'K&F', 'מתאם לעדשות Nikon F/G ל-Sony E, עם טבעת צמצם', 'F → Sony E', 'מתאם ידני', 'Sony A7, A6000–A6700, ZV-E10', 'מתאים גם לעדשות G בלי טבעת צמצם', 'sony', 'לעדשות Nikon F/G', False, ''),
 ('manual', '1005001525023186', 'K&F', 'מתאם לעדשות Canon FD ל-Sony E', 'FD → Sony E', 'מתאם ידני', 'Sony A7, A6000–A6700, ZV-E10', '', 'sony', 'לעדשות Canon FD', False, ''),
 ('manual', '1005008832919209', 'K&F', 'מתאם לעדשות Minolta MD ל-Sony E', 'MD → Sony E', 'מתאם ידני', 'Sony A7, A6000–A6700, ZV-E10', '', 'sony', 'לעדשות Minolta MD', False, ''),
 ('manual', '1005009050524454', 'K&F', 'מתאם לעדשות Pentax K ל-Sony E', 'PK → Sony E', 'מתאם ידני', 'Sony A7, A6000–A6700, ZV-E10', '', 'sony', 'לעדשות Pentax K', False, ''),
 ('manual', '1005008709634841', 'K&F', 'מתאם לעדשות Leica M למצלמות מירורלס', 'Leica M', 'מתאם ידני', 'Canon RF, Sony E, Nikon Z, Fuji X – בוחרים בדף המוצר', '', '', '', False, ''),
 ('manual', '1005010209722673', 'K&F', 'מתאם לעדשות Nikon F/G ל-Fuji X, עם טבעת צמצם', 'F → Fuji X', 'מתאם ידני', 'Fujifilm X-T30, X-T50, X-S10, X-E4', '', 'fuji', 'לעדשות Nikon F/G', False, ''),
 ('manual', '1005002483049242', 'K&F', 'מתאם לעדשות Canon FD ל-Fuji X', 'FD → Fuji X', 'מתאם ידני', 'Fujifilm X-T30, X-T50, X-S10, X-E4', '', 'fuji', 'לעדשות Canon FD', False, ''),
 ('manual', '1005007354058729', 'K&F', 'מתאם M42 ל-Fuji X', 'M42 → Fuji X', 'מתאם ידני', 'Fujifilm X-T30, X-T50, X-S10, X-E4', '', 'fuji', 'לעדשות M42', False, ''),
 ('manual', '1005007354380569', 'K&F', 'מתאם לעדשות Nikon F ידניות (AI/AIS) למצלמות Nikon Z', 'F → Z', 'מתאם ידני', 'Nikon Z5, Z6, Z7, Z8, Zf, Z50', 'לעדשות ידניות', 'nikon', 'לעדשות Nikon F ידניות', False, ''),
 ('manual', '1005006850214410', 'K&F', 'מתאם לעדשות Nikon F למצלמות Canon EF (רפלקס)', 'F → EF', 'מתאם ידני', 'Canon 5D, 6D, 80D, 90D, 250D', '', 'canon', 'לעדשות Nikon F', False, ''),
]
num = lambda x: float(str(x or 0).replace('%', '') or 0)
have = {p['id'] for p in db['products']}
added = 0
for g, pid, brand, title, code, kind, fits, note, cb, lens, nocomm, alt in A:
    if pid in have:
        continue
    s = S[pid]
    p = dict(collection='adapters', group=g, id=pid, brand=brand, title=title, code=code, kind=kind, fits=fits, note=note,
             price=round(num(s['price']), 2), rating=num(s['rating']) or None, sold=int(num(s['sold'])),
             link=s['url'], img=s['img'], tid='pending', status='pending')
    if nocomm:
        p['no_commission'] = True
        p['alt_query'] = alt
    if cb:
        p['brand_for'] = cb; p['for'] = ['M', 'D'] if code.endswith('EF') else ['M']
        p['lens_note'] = lens
    elif 'בוחרים בדף המוצר' in fits:
        p['for'] = ['M']
    db['products'].append(p); added += 1
if not any(c['id'] == 'adapters' for c in db['collections']):
    db['collections'].append(COLL)
json.dump(db, open('data/products.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('added', added)
