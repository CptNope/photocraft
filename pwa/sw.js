/* PhotoCraft PWA: generated from the fork's compiled static build.
 * Application WASM/JS assets are precached for offline launch after install.
 * Only same-origin files inside the GitHub Pages project path are handled.
 */
const CACHE_NAME = 'photocraft-pwa-__BUILD_VERSION__';
const CORE = __PRECACHE_ASSETS__;

self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE_NAME);
    try {
      await cache.addAll(CORE);
    } catch (error) {
      // On a device with a strict storage quota, allow the online app
      // to install; full offline support cannot be guaranteed.
      console.warn('PhotoCraft offline precache was incomplete', error);
      await cache.addAll(['./', './manifest.webmanifest', './icons/icon-192.png']);
    }
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const cacheNames = await caches.keys();
    await Promise.all(cacheNames
      .filter(name => name.startsWith('photocraft-pwa-') && name !== CACHE_NAME)
      .map(name => caches.delete(name)));
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', event => {
  const request = event.request;
  const url = new URL(request.url);
  const scopePath = new URL(self.registration.scope).pathname;
  if (request.method !== 'GET' ||
      url.origin !== self.location.origin ||
      !url.pathname.startsWith(scopePath)) return;

  if (request.mode === 'navigate') {
    event.respondWith((async () => {
      const cache = await caches.open(CACHE_NAME);
      try {
        const response = await fetch(request);
        if (response.ok) await cache.put('./index.html', response.clone());
        return response;
      } catch {
        return await cache.match('./index.html') || Response.error();
      }
    })());
    return;
  }

  event.respondWith((async () => {
    const cache = await caches.open(CACHE_NAME);
    const stored = await cache.match(request);
    if (stored) return stored;
    const response = await fetch(request);
    if (response.ok && response.type === 'basic') {
      try { await cache.put(request, response.clone()); }
      catch (error) { console.warn('PhotoCraft cache write skipped', error); }
    }
    return response;
  })());
});
