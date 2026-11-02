/* Kelime Atölyesi: önce ağ, ağ yoksa son kaydedilen kopya. */
const CACHE='kelime-atolyesi-v1';
const CORE=['./','index.html','app.js','config.js','hakkinda.html','vendor/fonts.css','favicon.svg','vendor/fonts/nunito-latin-wght-normal.woff2','vendor/fonts/nunito-latin-ext-wght-normal.woff2','vendor/fonts/baloo-2-latin-wght-normal.woff2','vendor/fonts/baloo-2-latin-ext-wght-normal.woff2'];
self.addEventListener('install',e=>{self.skipWaiting();e.waitUntil(caches.open(CACHE).then(c=>c.addAll(CORE)).catch(()=>{}))});
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',e=>{const q=e.request;if(q.method!=='GET'||new URL(q.url).origin!==self.location.origin)return;
e.respondWith(fetch(q).then(r=>{if(r&&r.ok){const c=r.clone();caches.open(CACHE).then(x=>x.put(q,c)).catch(()=>{})}return r}).catch(()=>caches.match(q).then(r=>r||caches.match('index.html'))))});
