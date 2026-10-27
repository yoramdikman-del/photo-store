// סטטיסטיקה לעמודי התוכן (מדריכים): Google Analytics 4, אותו מזהה כמו בחנות הראשית.
// סופר צפייה בעמוד, והקלקה על כל קישור רכישה (אלי אקספרס / אמזון) עם שם העמוד שממנו נלחץ.
(function () {
  var GA_ID = 'G-KY0G2JCNBM';
  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;
  var sc = document.createElement('script');
  sc.async = true;
  sc.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
  document.head.appendChild(sc);
  gtag('js', new Date());
  gtag('config', GA_ID);

  var page = (location.pathname.split('/').pop() || 'index.html').replace('.html', '');
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a) return;
    try {
      if (/aliexpress|amzn\.to|amazon\./i.test(a.href)) {
        gtag('event', 'click_buy', {
          item_id: a.dataset.id || '',
          item_brand: a.dataset.brand || '',
          item_category: a.dataset.coll || '',
          item_name: a.dataset.title || a.getAttribute('aria-label') || a.textContent.trim().slice(0, 80),
          section: 'guide:' + page,
          via: a.classList.contains('pimg') ? 'image' : 'button'
        });
      } else if (/facebook\.com|instagram\.com|chat\.whatsapp\.com/.test(a.href)) {
        gtag('event', 'click_social', { network: a.hostname, place: 'guide:' + page });
      }
    } catch (err) {}
  });
})();
