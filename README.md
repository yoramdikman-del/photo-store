# צילום בכל גיל – חנות ציוד צילום

אתר סטטי (GitHub Pages) שמציג ציוד צילום מחנויות רשמיות באלי אקספרס, עם קישורי שותפים.

- `index.html` – האתר. קורא את המוצרים מ-`data/products.json`.
- `data/products.json` – כל המוצרים והאוספים. עדכון מוצרים = עדכון הקובץ הזה בלבד.
- `scripts/refresh.py` + `.github/workflows/refresh.yml` – בדיקה שבועית מול אלי אקספרס (מחיר, דירוג, מוצרים שנעלמו). התוצאה נפתחת כבקשת שינוי שמחכה לאישור.
- הסוד של ה-API נשמר רק ב-Settings → Secrets → Actions בשם `ALI_APP_SECRET`.
