self.addEventListener('install', event => event.waitUntil(self.skipWaiting()));
self.addEventListener('activate', event => {
  event.waitUntil(Promise.all([
    caches.delete('dilkusu-v1'),
    self.clients.claim(),
    self.registration.unregister()
  ]));
});
