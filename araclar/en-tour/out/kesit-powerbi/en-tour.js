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
    intro: "Kesit Power BI is one of five Kesit apps that teach data skills — Excel, SQL, Power BI, Python and statistics — <b>in Turkish</b>, in the browser, with no setup or account. Teaching data work in Turkish is the point of the project, so the interface stays Turkish; code, functions and technical terms are in English as at work. This guide explains each screen.",
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
      "DAX Arena": "DAX Arena",
      "DAX Playground": "DAX Playground",
      "Power Query Lab": "Power Query Lab",
      "Measure Lab": "Measure Lab",
      "Örnek raporlar": "Sample reports",
      "DAX fonksiyonları": "DAX functions",
      "Power BI arayüzü": "Power BI interface",
      "Görseller ve biçim": "Visuals and formatting",
      "Anadolu Market modeli": "Anadolu Market model",
      "Sıfırdan işe hazır Power BI uzmanlığına.": "From zero to job-ready Power BI.",
      "Hangi işi yapmak istiyorsun?": "Which job do you want to do?",
      "Üç seviye, her birinin sonunda “yapabilirim”": "Three levels, each ending in “I can do this”",
      "Okumanın ötesi": "Beyond reading"
    },
    route: () => {
      const h = location.hash.replace(/^#\/?/, '').split(/[/?&]/)[0];
      if (!h) return 'home';
      if (/^ders-|^lesson$|^l$/.test(h)) return 'lesson';
      const a = {"patikalar":"paths","dersler":"curr","tekrar":"review","alistirma":"pratik","sinavlar":"sinav","studyo":"studio","dashboard":"dash","kariyer":"iv","sertifika":"belgeler","veriler":"data","formuller":"formulas","menuler":"menus","gorseller":"visuals","sozluk":"dict","profil":"profile"};
      return a[h] || h;
    },
    guide: {
      "paths": {
        "t": "Learning paths",
        "p": "12 paths, e.g. data analyst, BI developer, PL-300, DP-600 / Fabric, DAX mastery and Excel to Power BI, each with stages and a job-readiness checklist."
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
        "p": "Typical errors learners make and how to fix them."
      },
      "dict": {
        "t": "Glossary",
        "p": "Key terms with short Turkish explanations."
      },
      "data": {
        "t": "Datasets",
        "p": "Anadolu Market plus 5 case packs for Power BI Desktop (Ilgaz Bank, Kanat Airlines, Lezzet Courier, Pusula HR, Pedal İzmir), each with CSVs, a model plan, a measure library and tasks with expected results."
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
        "t": "Kesit Power BI",
        "p": "158 lessons, 1,438 in-lesson exercises (including building visuals and models) and 117 practice tasks on Power BI, DAX and Fabric. Measures are written against a DAX-emulating engine that runs in the browser, so every exercise is checked instantly without installing Power BI.",
        "try": "Open “Dersler” (Lessons) and start “1 dakikada ilk ölçün” — your first measure in one minute."
      },
      "curr": {
        "t": "Lessons",
        "p": "From the first measure to expanded tables, calculation groups and Direct Lake, in Basic, Intermediate and Advanced levels."
      },
      "pratik": {
        "t": "Practice",
        "p": "117 practice tasks."
      },
      "arena": {
        "t": "DAX Arena",
        "p": "DAX challenges checked by the in-browser engine."
      },
      "sinav": {
        "t": "Exams",
        "p": "262 question-bank items for Microsoft’s PL-300 and DP-600 exams; a coverage map links each official exam objective to lessons and questions."
      },
      "studio": {
        "t": "DAX Playground",
        "p": "Write any DAX measure against the sample model and see the result table."
      },
      "pq": {
        "t": "Power Query Lab",
        "p": "Data preparation with Power Query in the browser."
      },
      "lab": {
        "t": "Measure Lab",
        "p": "A workspace for building and testing measures."
      },
      "dash": {
        "t": "Sample reports",
        "p": "24 sample reports, 104 pages, explained step by step: bookmarks, tooltip pages, drill-through, field parameters and mobile layout."
      },
      "iv": {
        "t": "Interview",
        "p": "185 interview questions with weak and strong answer examples, a live DAX coding round and take-home tasks."
      },
      "formulas": {
        "t": "DAX functions",
        "p": "Reference for DAX functions."
      },
      "menus": {
        "t": "Power BI interface",
        "p": "A bilingual (Turkish and English) list of Power BI commands, so learners can follow either interface language."
      },
      "visuals": {
        "t": "Visuals and formatting",
        "p": "Reference for Power BI visuals and formatting options."
      },
      "model": {
        "t": "Anadolu Market model",
        "p": "The data model used throughout the lessons."
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
