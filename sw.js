// Psyched Luxuries — unified PWA service worker
const CACHE_VERSION = 'v5';
const CACHE = 'pl-shell-' + CACHE_VERSION;
const SHELL = [
  './', './index.html',
  './codex.html', './drops.html', './outreach.html', './seeds.html',
  './Seeds_Ledger.html',
  './Manifest_Study.html',
  './manifest.webmanifest',
  './icons/apple-touch-icon.png',
  './icons/icon-192.png', './icons/icon-512.png',
  './icons/tile-codex.png', './icons/tile-drops.png',
  './icons/tile-outreach.png', './icons/tile-seeds.png',
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k !== CACHE && k.startsWith('pl-shell-')).map(k => caches.delete(k)));
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  const isDoc = req.mode === 'navigate' || req.destination === 'document';
  if (isDoc) {
    e.respondWith((async () => {
      try {
        const fresh = await fetch(req);
        const c = await caches.open(CACHE);
        c.put(req, fresh.clone());
        return fresh;
      } catch {
        return (await caches.match(req)) || (await caches.match('./index.html')) ||
               new Response('Offline', { status: 503 });
      }
    })());
    return;
  }
  e.respondWith((async () => {
    const cached = await caches.match(req);
    if (cached) return cached;
    try {
      const fresh = await fetch(req);
      if (fresh.ok && (url.origin === location.origin || url.host.includes('fonts.g'))) {
        const c = await caches.open(CACHE);
        c.put(req, fresh.clone());
      }
      return fresh;
    } catch { return cached || new Response('Offline', { status: 503 }); }
  })());
});
