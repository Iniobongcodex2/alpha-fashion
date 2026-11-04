// This is a basic service worker that allows the PWA to be installable.
self.addEventListener('install', (e) => {
  console.log('[Service Worker] Install');
});
self.addEventListener('fetch', (e) => {
  // We will leave this empty for now. It is used for offline caching later.
});
