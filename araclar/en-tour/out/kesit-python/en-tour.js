/* İngilizce tanıtım turu (?lang=en ile açılır, ?lang=tr ile kapanır; aynı sekmede bütün Kesit uygulamalarında sürer).
 * Kesit Türkçe veri eğitimidir ve Türkçe kalır. Tur, İngilizce okuyan ziyaretçiye her ekranın ne işe yaradığını anlatan
 * bir panel ve menü/başlıkların altında küçük İngilizce karşılıklar ekler. Uygulamaya özel içerik CONFIG'tedir; altındaki
 * motor bütün Kesit uygulamalarında ve İngilizce Atölyesi'nde aynıdır. Bu dosya ana sayfa deposundaki
 * araclar/en-tour/ betiğiyle üretilir. */
(function (root) {
  'use strict';
  const CONFIG = {
    key: 'kesit_lang',
    bg: '#16323a',
    accent: '#9fe0c9',
    intro: "Kesit Python is one of five Kesit apps that teach data skills — Excel, SQL, Power BI, Python and statistics — <b>in Turkish</b>, in the browser, with no setup or account. Teaching data work in Turkish is the point of the project, so the interface stays Turkish; code, functions and technical terms are in English as at work. This guide explains each screen.",
    glossSelector: "nav button, aside button, aside a[data-page], .side a[data-page], h1, main h2",
    blockGloss: "h1, main h2",
    navGloss: "nav button, aside button, aside a[data-page], .side a[data-page]",
    gloss: {
      "Ana sayfa": "Home",
      "Öğrenme yolları": "Learning paths",
      "Dersler": "Lessons",
      "Tekrar": "Review",
      "Seviye testi": "Placement test",
      "Pratik": "Practice",
      "Sınavlar": "Exams",
      "Mülakat": "Interview",
      "Mülakat hazırlığı": "Interview prep",
      "Bitirme projeleri": "Capstone projects",
      "Belgelerim": "My certificates",
      "Veri setleri": "Datasets",
      "Sık hatalar": "Common mistakes",
      "Sık hatalar ve ipuçları": "Common mistakes and tips",
      "Sözlük": "Glossary",
      "Profil": "Profile",
      "Hakkında": "About",
      "Menü": "Menu",
      "Nereden başlayalım?": "Where shall we start?",
      "Hedefine göre yol seç": "Pick a path for your goal",
      "Uygula ve hazırlan": "Apply and get ready",
      "Bilgini sına": "Test yourself",
      "ÖĞREN": "Learn",
      "PRATİK": "Practice",
      "ARAÇLAR": "Tools",
      "KARİYER": "Career",
      "REFERANS": "Reference",
      "Yapay Zekâ": "AI",
      "Python Arena": "Python Arena",
      "Kod editörü": "Code editor",
      "Kopya kâğıdı": "Cheat sheet",
      "Python'ı tarayıcında çalıştırarak öğren.": "Learn Python by running it in your browser.",
      "Üç seviye, tek yol": "Three levels, one path",
      "Nasıl çalışır?": "How it works"
    },
    route: () => {
      const h = location.hash.replace(/^#\/?/, '').split(/[/?&]/)[0];
      if (!h) return 'home';
      if (/^ders-|^lesson$|^l$/.test(h)) return 'lesson';
      const a = {"lessons":"curr","exam":"test","exams":"sinav","practice":"pratik","interview":"mulakat","projects":"projeler","mistakes":"hatalar","ref":"dict"};
      return a[h] || h;
    },
    guide: {
      "paths": {
        "t": "Learning paths",
        "p": "11 paths: data analyst, data scientist, data engineer, backend, web, machine learning, AI, automation and more — each with prerequisites, an exam, role-filtered interview questions and portfolio ideas."
      },
      "review": {
        "t": "Review",
        "p": "Spaced repetition: questions you got wrong come back after increasing intervals until you answer them correctly several times."
      },
      "test": {
        "t": "Placement test",
        "p": "A short test that marks the levels you already know, so the “next lesson” skips them. Skipped lessons are not counted as completed."
      },
      "profile": {
        "t": "Profile",
        "p": "Progress, streaks and settings. Progress lives only in this browser; it can be exported to a file and loaded on another device. No personal data is collected."
      },
      "hakkinda": {
        "t": "About",
        "p": "How the app was built and verified, its known limits, and the licence. Product decisions are Yusuf Durak’s; code and content were developed with AI (Claude) and checked by automated tests."
      },
      "belgeler": {
        "t": "My certificates",
        "p": "A completion certificate generated in the browser after finishing a path. It is not verifiable and is not an official certificate — the app says so on the page."
      },
      "hatalar": {
        "t": "Common mistakes",
        "p": "160 common-mistake entries: the error, why it happens and the fix."
      },
      "dict": {
        "t": "Cheat sheet and glossary",
        "p": "Quick syntax reference and terms."
      },
      "data": {
        "t": "Datasets",
        "p": "8 fictional datasets: e-commerce, bank, HR, food delivery, airline, bike sharing, the Power BI model and a deliberately dirty dataset for cleaning practice."
      },
      "projeler": {
        "t": "Capstone projects",
        "p": "End-of-path projects on the shared datasets."
      },
      "lesson": {
        "t": "Inside a lesson",
        "p": "Explanation in Turkish, examples and exercises that are checked instantly. Code and technical terms stay in English, as they are at work."
      },
      "home": {
        "t": "Kesit Python",
        "p": "156 lessons, 3,240 in-lesson exercises and 562 practice tasks. Real Python (CPython compiled to WebAssembly via Pyodide) runs in a Web Worker in the browser; exercises are checked by automated tests. An infinite loop does not freeze the page — Stop and a 60-second limit restart the engine.",
        "try": "Open “Dersler” (Lessons) and start “İlk kodun” — your first code in a few minutes."
      },
      "curr": {
        "t": "Lessons",
        "p": "From the basics to automation, data analysis, web, machine learning and LLM applications, in three levels."
      },
      "ai": {
        "t": "AI",
        "p": "Lessons on using Python with AI and LLM applications."
      },
      "pratik": {
        "t": "Practice",
        "p": "562 practice tasks checked by tests."
      },
      "arena": {
        "t": "Python Arena",
        "p": "250 problems with hidden tests."
      },
      "sinav": {
        "t": "Exams",
        "p": "18 exams by level and path."
      },
      "play": {
        "t": "Code editor",
        "p": "A free Python editor running in the browser."
      },
      "mulakat": {
        "t": "Interview",
        "p": "292 Python interview questions, filtered by role."
      }
    },
  };
  /* ---------- Tur motoru (bütün uygulamalarda aynı; içerik yukarıdaki CONFIG'tedir) ---------- */
  const C = CONFIG;
  // Tur yalnızca bu sekmede açık kalır (sessionStorage): ?lang=en ile açılır, aynı sekmede gezerken sürer,
  // yeni bir ziyarette uygulama yine Türkçe açılır. Eski sürüm seçimi kalıcı tuttuğu için o kayıt silinir.
  let on = false;
  try {
    localStorage.removeItem(C.key);
    const q = new URLSearchParams(location.search).get('lang');
    if (q === 'en') sessionStorage.setItem(C.key, 'en');
    if (q === 'tr') sessionStorage.removeItem(C.key);
    on = sessionStorage.getItem(C.key) === 'en';
  } catch {}
  if (!on) return;
  root.EN_TOUR = true;
  let clicked = null; // URL'si değişmeyen uygulamalarda son tıklanan bölüm
  const norm = s => (s || '').replace(/\s+/g, ' ').trim();
  const strip = s => norm(s).replace(/^[^\p{L}\p{N}]+/u, '').replace(/\s*[›→↗»]$/, '');

  function glossAll() {
    document.querySelectorAll(C.glossSelector).forEach(el => {
      if (el.dataset.enGloss || el.closest('#en-tour')) return;
      const own = C.glossText ? C.glossText(el) : el.innerText;
      const en = C.gloss[norm(own)] || C.gloss[strip(own)];
      if (!en || en === strip(own)) return;
      el.dataset.enGloss = '1';
      const s = document.createElement('span');
      s.className = 'en-gloss';
      s.lang = 'en';
      s.textContent = en;
      if (C.blockGloss && el.matches(C.blockGloss)) s.classList.add('en-block');
      else if (C.navGloss && el.matches(C.navGloss)) el.classList.add('en-nav');
      el.appendChild(s);
    });
  }

  const CSS = `
  .en-gloss{display:inline-block;margin-left:6px;font-size:11px;font-weight:500;letter-spacing:0;text-transform:none;opacity:.7;font-style:italic}
  .en-nav{flex-wrap:wrap!important}
  .en-nav>.en-gloss{display:block;flex-basis:100%;margin:1px 0 0 ${C.navIndent || '28px'};font-size:10.5px;line-height:1.2}
  .en-gloss.en-block{display:block;margin:2px 0 0;font-size:12px;line-height:1.3}
  #en-tour{position:fixed;right:16px;bottom:16px;z-index:2147483000;width:min(360px,calc(100vw - 32px));max-height:calc(100vh - 32px);overflow:auto;background:${C.bg || '#1f2a44'};color:#f4f6fb;border-radius:14px;box-shadow:0 14px 40px rgba(0,0,0,.28);font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;text-align:left}
  #en-tour header{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:11px 14px 0}
  #en-tour header b{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:${C.accent || '#ffd479'}}
  #en-tour header button{all:unset;cursor:pointer;border:1px solid rgba(255,255,255,.35);border-radius:8px;padding:1px 8px;font-size:12px}
  #en-tour .en-body{padding:4px 14px 13px}
  #en-tour h3{margin:4px 0 6px;font-size:16px;color:#fff;font-weight:700}
  #en-tour p{margin:0 0 8px}
  #en-tour .en-try{background:rgba(255,255,255,.08);border-left:3px solid ${C.accent || '#ffd479'};padding:7px 10px;border-radius:6px}
  #en-tour a{color:${C.accent || '#ffd479'}}
  #en-tour .en-foot{font-size:12px;opacity:.75;margin:6px 0 0}
  #en-tour.en-min .en-body{display:none}
  #en-tour.en-min{width:auto}
  #en-tour.en-min header{padding:9px 12px}
  @media (max-width:640px){#en-tour{right:8px;left:8px;bottom:8px;width:auto;max-height:45vh}}
  @media print{#en-tour,.en-gloss{display:none!important}}
  ${C.css || ''}`;

  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
  let panel, btn, lastKey;
  function render(force) {
    const k = C.route(clicked) || 'home';
    if (k === lastKey && !force) return;
    lastKey = k;
    const g = C.guide[k] || C.guide.home;
    let first = false;
    try {
      first = !sessionStorage.getItem(C.key + '_seen');
      sessionStorage.setItem(C.key + '_seen', '1');
    } catch {}
    panel.querySelector('.en-body').innerHTML = `
      ${first ? `<p>${C.intro}</p>` : ''}
      <h3>${esc(g.t)}</h3>
      <p>${g.p}</p>
      ${g.try ? `<p class="en-try"><b>Try this:</b> ${g.try}</p>` : ''}
      <p class="en-foot">${C.foot || 'Small English labels under menus and headings are part of this guide.'} <a href="?lang=tr">Turn off</a></p>`;
  }
  function setMin(min, remember) {
    panel.classList.toggle('en-min', min);
    btn.textContent = min ? 'Show' : 'Hide';
    btn.setAttribute('aria-expanded', String(!min));
    if (remember)
      try {
        localStorage.setItem(C.key + '_min', min ? '1' : '');
      } catch {}
  }
  function mount() {
    const style = document.createElement('style');
    style.textContent = CSS;
    document.head.appendChild(style);
    panel = document.createElement('aside');
    panel.id = 'en-tour';
    panel.lang = 'en';
    panel.setAttribute('aria-label', 'English guide');
    panel.innerHTML = '<header><b>English guide</b><button type="button">Hide</button></header><div class="en-body"></div>';
    btn = panel.querySelector('button');
    btn.addEventListener('click', () => setMin(!panel.classList.contains('en-min'), true));
    document.body.appendChild(panel);
    let min = false;
    try {
      min = localStorage.getItem(C.key + '_min') === '1';
    } catch {}
    setMin(min);
    render(true);
    glossAll();
    // Kullanıcı yazmaya başlayınca panel küçülür, içeriği kapatmaz.
    document.addEventListener('focusin', e => {
      if (!panel.contains(e.target) && e.target.matches('input:not([type=checkbox]):not([type=radio]), textarea, select'))
        setMin(true);
    });
    document.addEventListener(
      'click',
      e => {
        if (panel.contains(e.target) || !C.clickRoute) return;
        const r = C.clickRoute(e.target);
        if (r) clicked = r;
      },
      true
    );
    let t;
    new MutationObserver(() => {
      clearTimeout(t);
      t = setTimeout(() => {
        glossAll();
        render();
      }, 80);
    }).observe(document.body, { childList: true, subtree: true });
    addEventListener('hashchange', () => setTimeout(render, 60));
    addEventListener('popstate', () => setTimeout(render, 60));
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
  else mount();
})(window);
