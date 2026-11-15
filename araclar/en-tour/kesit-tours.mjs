// Kesit uygulamaları ve Kesit ana sayfası için en-tour.js dosyalarını üretir.
// Kullanım: node kesit-tours.mjs  → /home/claude/arac/out/<uygulama>/en-tour.js
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';

const ENGINE = readFileSync(new URL('./en-tour-engine.js', import.meta.url), 'utf8');

const COMMON_GLOSS = {
  'Ana sayfa': 'Home',
  'Öğrenme yolları': 'Learning paths',
  Dersler: 'Lessons',
  Tekrar: 'Review',
  'Seviye testi': 'Placement test',
  Pratik: 'Practice',
  Sınavlar: 'Exams',
  Mülakat: 'Interview',
  'Mülakat hazırlığı': 'Interview prep',
  'Bitirme projeleri': 'Capstone projects',
  Belgelerim: 'My certificates',
  'Veri setleri': 'Datasets',
  'Sık hatalar': 'Common mistakes',
  'Sık hatalar ve ipuçları': 'Common mistakes and tips',
  Sözlük: 'Glossary',
  Profil: 'Profile',
  Hakkında: 'About',
  Menü: 'Menu',
  'Nereden başlayalım?': 'Where shall we start?',
  'Hedefine göre yol seç': 'Pick a path for your goal',
  'Uygula ve hazırlan': 'Apply and get ready',
  'Bilgini sına': 'Test yourself',
  ÖĞREN: 'Learn',
  PRATİK: 'Practice',
  ARAÇLAR: 'Tools',
  KARİYER: 'Career',
  REFERANS: 'Reference',
};

const COMMON_GUIDE = {
  paths: {
    t: 'Learning paths',
    p: 'Role-based routes (data analyst, BI developer, data engineer…) that pick and order the lessons, with stages, an exam and a job-readiness checklist.',
  },
  review: {
    t: 'Review',
    p: 'Spaced repetition: questions you got wrong come back after increasing intervals until you answer them correctly several times.',
  },
  test: {
    t: 'Placement test',
    p: 'A short test that marks the levels you already know, so the “next lesson” skips them. Skipped lessons are not counted as completed.',
  },
  profile: {
    t: 'Profile',
    p: 'Progress, streaks and settings. Progress lives only in this browser; it can be exported to a file and loaded on another device. No personal data is collected.',
  },
  hakkinda: {
    t: 'About',
    p: 'How the app was built and verified, its known limits, and the licence. Product decisions are Yusuf Durak’s; code and content were developed with AI (Claude) and checked by automated tests.',
  },
  belgeler: {
    t: 'My certificates',
    p: 'A completion certificate generated in the browser after finishing a path. It is not verifiable and is not an official certificate — the app says so on the page.',
  },
  hatalar: { t: 'Common mistakes', p: 'Typical errors learners make and how to fix them.' },
  dict: { t: 'Glossary', p: 'Key terms with short Turkish explanations.' },
  data: {
    t: 'Datasets',
    p: 'The shared fictional datasets used across all four Kesit apps (e-commerce, bank, airline, food delivery, HR, bike sharing). The same company data runs through SQL, Power BI, Python and statistics, so one story connects the skills. Known quirks left in on purpose are listed here.',
  },
  projeler: { t: 'Capstone projects', p: 'End-of-path projects on the shared datasets.' },
  lesson: {
    t: 'Inside a lesson',
    p: 'Explanation in Turkish, examples and exercises that are checked instantly. Code and technical terms stay in English, as they are at work.',
  },
};

const INTRO = name =>
  `${name} is one of four Kesit apps that teach data skills — SQL, Power BI, Python and statistics — <b>in Turkish</b>, in the browser, with no setup or account. Teaching data work in Turkish is the point of the project, so the interface stays Turkish; code, functions and technical terms are in English as at work. This guide explains each screen.`;

const hashKey = (alias = {}) =>
  `() => {
      const h = location.hash.replace(/^#\\/?/, '').split(/[/?&]/)[0];
      if (!h) return 'home';
      if (/^ders-|^lesson$|^l$/.test(h)) return 'lesson';
      const a = ${JSON.stringify(alias)};
      return a[h] || h;
    }`;

const APPS = {
  'kesit-sql': {
    name: 'Kesit SQL',
    gloss: {
      'SQL Arena': 'SQL Arena',
      'Sorgu editörü': 'Query editor',
      "Her sorgu bir adım. Sıfırdan ileri SQL'e.": 'Every query is a step. From zero to advanced SQL.',
      'Temelden ileriye üç basamak': 'Three steps from basics to advanced',
    },
    alias: {},
    guide: {
      home: {
        t: 'Kesit SQL',
        p: '295 lessons, 1,944 exercises and 578 practice tasks, from the first SELECT to window functions, query optimisation and data warehousing. A real SQLite database runs in the browser (sql.js); every query is checked instantly.',
        try: 'Open “Dersler” (Lessons) and start “1 dakikada ilk sorgun” — your first query in one minute.',
      },
      curr: {
        t: 'Lessons',
        p: 'All lessons by level. Six SQL dialects — SQL Server, PostgreSQL, MySQL, Oracle, BigQuery and SQLite: examples are shown in the dialect you choose and exercises are checked against its rules (the other five are emulated on top of SQLite).',
      },
      pratik: { t: 'Practice', p: '578 practice tasks on the shared datasets, grouped by topic and difficulty.' },
      play: {
        t: 'SQL Arena',
        p: 'Challenges with hidden tests, SQL detective cases, result prediction, query puzzles and a weekly tournament.',
      },
      sinav: { t: 'Exams', p: 'Exams by level and path.' },
      serbest: { t: 'Query editor', p: 'A free SQL editor on the bundled databases.' },
      mulakat: { t: 'Interview', p: 'SQL interview questions and patterns.' },
      paths: {
        t: 'Learning paths',
        p: '21 paths: 9 role paths (data analyst, IT business analyst, data engineer, data scientist, BI, DBA, backend, SQL Server, SQL basics), 9 topic paths and 3 certification-prep paths.',
      },
    },
  },
  'kesit-powerbi': {
    name: 'Kesit Power BI',
    gloss: {
      'DAX Arena': 'DAX Arena',
      'DAX Playground': 'DAX Playground',
      'Power Query Lab': 'Power Query Lab',
      'Measure Lab': 'Measure Lab',
      'Örnek raporlar': 'Sample reports',
      'DAX fonksiyonları': 'DAX functions',
      'Power BI arayüzü': 'Power BI interface',
      'Görseller ve biçim': 'Visuals and formatting',
      'Anadolu Market modeli': 'Anadolu Market model',
      'Sıfırdan işe hazır Power BI uzmanlığına.': 'From zero to job-ready Power BI.',
      'Hangi işi yapmak istiyorsun?': 'Which job do you want to do?',
      'Üç seviye, her birinin sonunda “yapabilirim”': 'Three levels, each ending in “I can do this”',
      'Okumanın ötesi': 'Beyond reading',
    },
    alias: {
      patikalar: 'paths', dersler: 'curr', tekrar: 'review', alistirma: 'pratik', sinavlar: 'sinav', studyo: 'studio',
      dashboard: 'dash', kariyer: 'iv', sertifika: 'belgeler', veriler: 'data', formuller: 'formulas', menuler: 'menus',
      gorseller: 'visuals', sozluk: 'dict', profil: 'profile',
    },
    guide: {
      home: {
        t: 'Kesit Power BI',
        p: '150 lessons, 1,250 in-lesson exercises and 117 practice tasks on Power BI, DAX and Fabric. Measures are written against a DAX-emulating engine that runs in the browser, so every exercise is checked instantly without installing Power BI.',
        try: 'Open “Dersler” (Lessons) and start “1 dakikada ilk ölçün” — your first measure in one minute.',
      },
      curr: { t: 'Lessons', p: 'From the first measure to expanded tables, calculation groups and Direct Lake, in Basic, Intermediate and Advanced levels.' },
      paths: {
        t: 'Learning paths',
        p: '12 paths, e.g. data analyst, BI developer, PL-300, DP-600 / Fabric, DAX mastery and Excel to Power BI, each with stages and a job-readiness checklist.',
      },
      pratik: { t: 'Practice', p: '117 practice tasks.' },
      arena: { t: 'DAX Arena', p: 'DAX challenges checked by the in-browser engine.' },
      sinav: { t: 'Exams', p: '262 question-bank items for Microsoft’s PL-300 and DP-600 exams; a coverage map links each official exam objective to lessons and questions.' },
      studio: { t: 'DAX Playground', p: 'Write any DAX measure against the sample model and see the result table.' },
      pq: { t: 'Power Query Lab', p: 'Data preparation with Power Query in the browser.' },
      lab: { t: 'Measure Lab', p: 'A workspace for building and testing measures.' },
      dash: {
        t: 'Sample reports',
        p: '24 sample reports, 104 pages, explained step by step: bookmarks, tooltip pages, drill-through, field parameters and mobile layout.',
      },
      iv: { t: 'Interview', p: '185 interview questions with weak and strong answer examples, a live DAX coding round and take-home tasks.' },
      formulas: { t: 'DAX functions', p: 'Reference for DAX functions.' },
      menus: { t: 'Power BI interface', p: 'A bilingual (Turkish and English) list of Power BI commands, so learners can follow either interface language.' },
      visuals: { t: 'Visuals and formatting', p: 'Reference for Power BI visuals and formatting options.' },
      model: { t: 'Anadolu Market model', p: 'The data model used throughout the lessons.' },
      data: {
        t: 'Datasets',
        p: 'Anadolu Market plus 5 case packs for Power BI Desktop (Ilgaz Bank, Kanat Airlines, Lezzet Courier, Pusula HR, Pedal İzmir), each with CSVs, a model plan, a measure library and tasks with expected results.',
      },
    },
  },
  'kesit-python': {
    name: 'Kesit Python',
    gloss: {
      'Yapay Zekâ': 'AI',
      'Python Arena': 'Python Arena',
      'Kod editörü': 'Code editor',
      'Kopya kâğıdı': 'Cheat sheet',
      "Python'ı tarayıcında çalıştırarak öğren.": 'Learn Python by running it in your browser.',
      'Üç seviye, tek yol': 'Three levels, one path',
      'Nasıl çalışır?': 'How it works',
    },
    alias: { lessons: 'curr', exam: 'test', exams: 'sinav', practice: 'pratik', interview: 'mulakat', projects: 'projeler', mistakes: 'hatalar', ref: 'dict' },
    guide: {
      home: {
        t: 'Kesit Python',
        p: '156 lessons, 3,240 in-lesson exercises and 562 practice tasks. Real Python (CPython compiled to WebAssembly via Pyodide) runs in a Web Worker in the browser; exercises are checked by automated tests. An infinite loop does not freeze the page — Stop and a 60-second limit restart the engine.',
        try: 'Open “Dersler” (Lessons) and start “İlk kodun” — your first code in a few minutes.',
      },
      curr: { t: 'Lessons', p: 'From the basics to automation, data analysis, web, machine learning and LLM applications, in three levels.' },
      paths: {
        t: 'Learning paths',
        p: '11 paths: data analyst, data scientist, data engineer, backend, web, machine learning, AI, automation and more — each with prerequisites, an exam, role-filtered interview questions and portfolio ideas.',
      },
      ai: { t: 'AI', p: 'Lessons on using Python with AI and LLM applications.' },
      pratik: { t: 'Practice', p: '562 practice tasks checked by tests.' },
      arena: { t: 'Python Arena', p: '250 problems with hidden tests.' },
      sinav: { t: 'Exams', p: '18 exams by level and path.' },
      play: { t: 'Code editor', p: 'A free Python editor running in the browser.' },
      mulakat: { t: 'Interview', p: '292 Python interview questions, filtered by role.' },
      hatalar: { t: 'Common mistakes', p: '160 common-mistake entries: the error, why it happens and the fix.' },
      dict: { t: 'Cheat sheet and glossary', p: 'Quick syntax reference and terms.' },
      data: { t: 'Datasets', p: '8 fictional datasets: e-commerce, bank, HR, food delivery, airline, bike sharing, the Power BI model and a deliberately dirty dataset for cleaning practice.' },
    },
  },
  'kesit-istatistik': {
    name: 'Kesit İstatistik',
    gloss: {
      'Başlangıç rehberi': 'Getting started',
      'İş problemi çöz': 'Solve a business problem',
      'Kavramı gör': 'See the concept',
      'Konu panoları': 'Topic boards',
      İlerlemem: 'My progress',
      'Kapsam ve kalite': 'Scope and quality',
      'Kesit verileriyle': 'With Kesit data',
      'Alıştırma atölyesi': 'Practice workshop',
      'Formülden önce neyi gördüğünü anla.': 'Understand what you see before the formula.',
      'Şu an neye ihtiyacın var?': 'What do you need right now?',
      'İstatistiği hangi iş için kullanacaksın?': 'What will you use statistics for?',
    },
    alias: { path: 'paths', library: 'curr', placement: 'test', progress: 'profile', mistakes: 'hatalar', interview: 'mulakat' },
    guide: {
      home: {
        t: 'Kesit İstatistik',
        p: '120 lessons in 30 modules plus 8 elective method lessons, from population and sample to tests, regression, experiments, time series, Bayes, quality, statistical learning and causal inference. Calculators are checked against SciPy references; case results are computed with pandas, SciPy and statsmodels.',
        try: 'Open “Kesit verileriyle” (With Kesit data) to see a statistics question answered with SQL, Python and DAX on the shared datasets.',
      },
      start: { t: 'Getting started', p: 'Where to begin depending on your background and goal.' },
      paths: { t: 'Learning paths', p: '4 paths: data analysis and BI, data science, machine learning, process and quality analysis.' },
      curr: { t: 'Lessons', p: 'All modules in Basic, Intermediate and Advanced levels.' },
      lesson: {
        t: 'Inside a lesson',
        p: 'What the concept means before the formula, with applied examples. Related lessons end with the SQL, DAX and Python equivalent of the concept.',
      },
      lab: { t: 'Solve a business problem', p: 'Business cases: choose the method, run it and turn the result into a decision with its limits.' },
      explore: { t: 'See the concept', p: '50 visual concept explorations.' },
      infographics: { t: 'Topic boards', p: 'One-page visual summaries of each topic.' },
      profile: { t: 'My progress', p: 'Progress, saved to a file and merged on another device; includes practice, case and interview records.' },
      quality: { t: 'Scope and quality', p: 'What the curriculum covers and how the results were verified.' },
      data: {
        t: 'With Kesit data',
        p: '13 cases on the datasets shared with Kesit SQL, Power BI and Python. Each case: a prediction, choice of method, SQL + Python + DAX code, the result computed from the real data, a chart, the decision and its limits.',
      },
      practice: { t: 'Practice workshop', p: '33 question types that generate new numbers each time, with formula hints, step-by-step solutions and a list of weak topics.' },
      test: { t: 'Placement test', p: 'Places you at the right level.' },
      hatalar: { t: 'Common mistakes', p: '32 common statistical mistakes with the correct reasoning.' },
      mulakat: { t: 'Interview prep', p: '48 statistics interview questions by role: what a strong answer contains, a weak example and a follow-up question.' },
    },
  },
};

APPS['kesit-ana'] = {
  name: 'Kesit',
  intro:
    'Kesit is a free set of four browser apps that teach the core data skills — SQL, Power BI, Python and statistics — <b>in Turkish</b>, by doing, with no setup or account. Teaching data work in Turkish is the point of the project, so the apps stay Turkish; code, functions and technical terms are in English as at work. This guide explains each app; it stays on when you open one.',
  sel: 'h1, main h2, h2, main b, .go',
  block: 'h1, h2',
  nav: null,
  route: "() => 'home'",
  gloss: {
    'Veri işinin temel araçları ve istatistik, Türkçe ve yaparak.': 'The core tools of data work, and statistics — in Turkish, by doing.',
    'Hangi işi yapmak istiyorsun?': 'Which job do you want to do?',
    'Nasıl çalışır?': 'How it works',
    'Bu proje hakkında': 'About this project',
    'Veri analisti': 'Data analyst',
    'BT iş analisti': 'IT business analyst',
    'İş zekâsı uzmanı': 'BI specialist',
    'Veri mühendisi': 'Data engineer',
    'Veri bilimci': 'Data scientist',
    'Süreç ve kalite analisti': 'Process and quality analyst',
    Otomasyon: 'Automation',
    'Yapay zekâ': 'AI',
    'Kurulum yok': 'No setup',
    'Hesap yok': 'No account',
    'Ortak veri setleri': 'Shared datasets',
    "SQL'e başla →": 'Start SQL',
    "Power BI'a başla →": 'Start Power BI',
    "Python'a başla →": 'Start Python',
    'İstatistiğe başla →': 'Start statistics',
  },
  guide: {
    home: {
      t: 'Kesit — data skills in Turkish',
      p: 'Four apps share the same fictional company data (e-commerce, bank, HR, courier, airline, bike sharing), so one story connects the skills: query with SQL → test with Python → report with Power BI → interpret with statistics. Code runs in the browser and exercises are checked instantly; progress stays in the browser.',
      try: 'Pick a role under “Hangi işi yapmak istiyorsun?” (Which job do you want to do?) to see the suggested order of apps, or open Kesit SQL.',
    },
  },
};

const SEL = 'nav button, aside button, aside a[data-page], .side a[data-page], h1, main h2';

function file(id, a) {
  const guide = a.route ? a.guide : { ...COMMON_GUIDE, ...a.guide };
  return `/* İngilizce tanıtım turu (?lang=en ile açılır, ?lang=tr ile kapanır; seçim bütün Kesit uygulamalarında ortaktır).
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
    intro: ${JSON.stringify(a.intro || INTRO(a.name))},
    glossSelector: ${JSON.stringify(a.sel || SEL)},
    blockGloss: ${JSON.stringify(a.block || 'h1, main h2')},
    navGloss: ${JSON.stringify(a.nav === null ? '' : 'nav button, aside button, aside a[data-page], .side a[data-page]')},
    gloss: ${JSON.stringify(a.route ? a.gloss : { ...COMMON_GLOSS, ...a.gloss }, null, 2).replace(/\n/g, '\n    ')},
    route: ${a.route || hashKey(a.alias)},
    guide: ${JSON.stringify(guide, null, 2).replace(/\n/g, '\n    ')},
  };
${ENGINE}`;
}

for (const [id, a] of Object.entries(APPS)) {
  mkdirSync(new URL(`./out/${id}/`, import.meta.url), { recursive: true });
  writeFileSync(new URL(`./out/${id}/en-tour.js`, import.meta.url), file(id, a));
}
console.log('ok', Object.keys(APPS).join(', '));
