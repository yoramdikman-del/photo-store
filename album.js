// עיצוב "אלבום": פתיחה עם ערימת תמונות וקטגוריות כתמונות. מוצג רק בדף הבית (בלי # בכתובת).
(function(){
  const $ = id => document.getElementById(id);
  function ready(){ try { return DB && DB.collections && DB.products.length; } catch (e) { return false; } }
  function build(){
    if (!ready()) return setTimeout(build, 150);
    const shop = $('shop'); if (!shop || $('al-hero')) return;
    const top = DB.products.filter(p => p.img).slice().sort((a,b) => (b.sold||0) - (a.sold||0));
    const seen = new Set(), pics = [];
    for (const p of top) { if (!seen.has(p.collection)) { seen.add(p.collection); pics.push(p); } if (pics.length === 5) break; }
    const hero = document.createElement('section'); hero.id = 'al-hero'; hero.className = 'al-hero';
    hero.innerHTML = `<div class="al-copy"><h2>צילום מאהבה</h2><p>הציוד שאנחנו אוהבים, בדוק ומסודר בעברית. בוחרים את המצלמה שלכם ורואים מה מתאים לה.</p><a href="#cam" class="al-btn">מה מתאים למצלמה שלי</a></div>
      <div class="pile" aria-hidden="true">${pics.map((p,i) => `<figure class="pol p${i}"><img referrerpolicy="no-referrer" src="${esc(p.img)}" alt="" onerror="imgFail(this)"><figcaption>${esc(p.brand || '')}</figcaption></figure>`).join('')}</div>`;
    const tiles = document.createElement('nav'); tiles.id = 'al-tiles'; tiles.className = 'al-tiles'; tiles.setAttribute('aria-label', 'קטגוריות');
    tiles.innerHTML = DB.collections.map(c => {
      const items = DB.products.filter(p => p.collection === c.id);
      if (!items.length) return '';
      const p = items.filter(x => x.img).sort((a,b) => (b.sold||0) - (a.sold||0))[0] || {};
      return `<a href="#${c.id}" class="al-tile"><span class="ti"><img loading="lazy" referrerpolicy="no-referrer" src="${esc(p.img || 'logo.png')}" alt="" onerror="imgFail(this)"></span><b>${esc(c.name)}</b><small>${items.length} מוצרים</small></a>`;
    }).join('');
    shop.insertBefore(tiles, shop.firstChild); shop.insertBefore(hero, tiles);
    toggle();
  }
  function toggle(){ const home = !location.hash || location.hash === '#'; ['al-hero','al-tiles'].forEach(id => { const el = $(id); if (el) el.hidden = !home; }); const fb = document.querySelector('.finder-bar'); if (fb) fb.hidden = home; }
  window.addEventListener('hashchange', toggle);
  const rs = history.replaceState.bind(history); history.replaceState = function(){ rs.apply(null, arguments); toggle(); };
  build();
})();
