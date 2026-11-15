/* İngilizce tanıtım turu (?lang=en ile açılır, ?lang=tr ile kapanır).
 * Uygulama Türkçe konuşanlara İngilizce öğretmek için yazıldı ve Türkçe kalır. Tur, İngilizce okuyan bir ziyaretçiye
 * (ör. işveren) her bölümün ne işe yaradığını anlatan bir panel ve menü/başlıkların altında küçük İngilizce karşılıklar ekler.
 * İçerik CONFIG'tedir; altındaki motor bütün Kesit uygulamalarında ve İngilizce Atölyesi'nde aynıdır.
 * Ayrıntı: docs/INGILIZCE-TUR.md */
(function (root) {
  'use strict';
  const HUB = {
    kelimeler: ['Words', 'Vocabulary lessons by level, phrasal verbs and irregular verbs. New words enter spaced repetition automatically.'],
    kaliplar: ['Collocations', 'Word partnerships such as “make a decision” or “heavy rain”, taught as sets because Turkish speakers often translate them word by word.'],
    aileler: ['Word families', 'decide → decision → decisive: one root, several word forms, practised together.'],
    idioms: ['Idioms', '835 idioms and proverbs, each with a short story so the meaning sticks.'],
    grammar: ['Grammar', '193 grammar topics from A1 to C2, explained in Turkish with exercises and level tests. The explanations compare English with Turkish structures.'],
    hatalar: ['Common mistakes', 'The errors Turkish speakers make most often (for example “I am agree”), with the reason and the fix.'],
    konusma: ['Speaking', 'Functional language and speaking tasks: asking for help, disagreeing politely, giving opinions.'],
    strateji: ['Strategies', 'Reading and listening strategies: skimming, scanning, predicting.'],
    stories: ['Reading', '155 graded stories and reading passages with comprehension questions.'],
    dinle: ['Listening', 'Listen and answer, plus dictation, using the browser’s speech engine.'],
    diyaloglar: ['Dialogues', '175 real-life dialogues with role play: at the doctor, in a shop, at work.'],
    yazma: ['Writing', 'Guided writing practice: e-mails, essays and reports.'],
    telaffuz: ['Pronunciation', 'Sounds that are hard for Turkish speakers: th, w/v, ship/sheep, word stress.'],
    sinav: ['Exam centre', 'Original practice tests for YDS, e-YDS and YÖKDİL, the national English exams in Turkey used for academic posts and civil-service pay. Includes a 4,702-entry exam dictionary.'],
    ceviri: ['Translation (YDS)', 'English↔Turkish translation practice in the YDS format: multiple choice and written.'],
    ukus: ['UK / US', 'British and American differences in vocabulary and spelling.'],
    sayilar: ['Numbers and time', 'Telling the time, dates, prices and phone numbers.'],
    yolculuk: ['Map', 'The grammar journey as a map of steps.'],
    practice: ['Free practice', 'Mixed practice outside the units.'],
  };
  const CONFIG = {
    key: 'ia_lang',
    bg: '#23305a',
    accent: '#ffcf6b',
    intro:
      'İngilizce Atölyesi teaches English to Turkish speakers from A1 to C2 and prepares them for Turkey’s national English exams (YDS, e-YDS, YÖKDİL). Explanations are in Turkish on purpose — they contrast English with Turkish — so the interface stays Turkish. This guide explains each section.',
    glossSelector: 'nav.tb button, .hbt > b, .gal, main .big, .scard b, main .tabs button, main .seg button',
    blockGloss: '.hbt > b, main .big, .gal',
    gloss: {
      Bugün: 'Today',
      Üniteler: 'Units',
      Tekrar: 'Review',
      Keşfet: 'Explore',
      Profil: 'Profile',
      'Kelime bilgisi': 'Vocabulary',
      Dilbilgisi: 'Grammar',
      Beceriler: 'Skills',
      Ekstralar: 'Extras',
      'Seviye seç': 'Choose a level',
      Özet: 'Summary',
      Rozetler: 'Badges',
      Ayarlar: 'Settings',
      'İngilizce karnem': 'My English report card',
      'Merhaba! Ben Mavi.': 'Hi! I’m Mavi (the guide character).',
      ...Object.fromEntries(
        Object.entries({
          kelimeler: 'Kelimeler', kaliplar: 'Kalıplar', aileler: 'Kelime aileleri', idioms: 'Deyimler',
          hatalar: 'Sık hatalar', konusma: 'Konuşma', strateji: 'Stratejiler', stories: 'Okuma', dinle: 'Dinleme',
          diyaloglar: 'Diyaloglar', yazma: 'Yazma', telaffuz: 'Telaffuz', sinav: 'Sınav merkezi', ceviri: 'Çeviri (YDS)',
          sayilar: 'Sayılar ve zaman', yolculuk: 'Harita', practice: 'Serbest pratik',
        }).map(([k, tr]) => [tr, HUB[k][0]])
      ),
    },
    clickRoute(el) {
      const m = el.closest('[data-m]');
      if (m) return m.dataset.m;
      const h = el.closest('[data-hb]');
      if (h && HUB[h.dataset.hb]) return h.dataset.hb;
      return null;
    },
    route: clicked => clicked,
    guide: {
      home: {
        t: 'Today',
        p: 'The daily screen: one “continue” button, today’s lesson and the review queue. Mavi, the guide character, suggests the next step. Progress is stored in the browser — no account needed.',
        try: 'Press “Seviye seç” (Choose a level) or start the first word lesson to see how a lesson works.',
      },
      uniteler: {
        t: 'Units',
        p: '75 themed units from A1 to C2 (“Hello!”, “My family and home”, “Daily life”…). Each unit has seven core steps and a unit test that needs 70% to pass. Every three units unlock a mixed review.',
      },
      tekrar: {
        t: 'Spaced repetition',
        p: 'Wrong answers and new words come back after 10 minutes, then 1, 3, 7 and 21 days. Each correct answer lengthens the interval; after the fifth correct answer the item leaves the list.',
      },
      dersler: {
        t: 'Explore',
        p: 'Every section outside the unit path, grouped as vocabulary, grammar, skills and extras. The numbers on each card show progress at the chosen level.',
        try: 'Open “Sık hatalar” (Common mistakes) or “Sınav merkezi” (Exam centre) — the two sections most specific to Turkish learners.',
      },
      stats: {
        t: 'Profile',
        p: 'XP, streaks, a weekly chart, the daily goal and the word-learning funnel (new → learning → consolidating → learned → permanent). The shareable “English report card” summarises the level. Backups are exported to a file from here.',
      },
      ...Object.fromEntries(Object.entries(HUB).map(([k, [t, p]]) => [k, { t, p }])),
    },
  };
