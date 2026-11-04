const CACHE_NAME = 'smartmyanmarfonts-cache-v3';
const STATIC_ASSETS = [
    './',
    './index.html',
    './davinci-plugins.html',
    './ae-plugins.html',
    './sound-effects.html',
    './premium-fonts.html',
    './w-art-house-capcut-converter.html',
    './ad_slot_300x250.html',
    './manifest.json',
    './favicon.ico',
    './icons/icon-192.png',
    './icons/icon-512.png',
    './icons/apple-touch-icon.png',
    './icons/favicon-32.png'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(STATIC_ASSETS).catch(() => {});
        }).then(() => self.skipWaiting())
    );
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
            );
        }).then(() => self.clients.claim())
    );
});

self.addEventListener('fetch', (event) => {
    if (event.request.method !== 'GET') return;

    const url = new URL(event.request.url);

    // Bypass caching for ad scripts, adsterra, googlesyndication, and analytics
    if (url.hostname.includes('adsterra') ||
        url.hostname.includes('highperformanceformat') ||
        url.hostname.includes('bellnewyork') ||
        url.hostname.includes('googlesyndication') ||
        url.hostname.includes('google-analytics') ||
        url.hostname.includes('doubleclick')) {
        return;
    }

    if (url.pathname.endsWith('.html') || url.pathname.endsWith('/')) {
        event.respondWith(
            fetch(event.request).then((response) => {
                if (response && response.status === 200) {
                    const clone = response.clone();
                    caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
                }
                return response;
            }).catch(() => {
                return caches.match(event.request).then((cached) => {
                    if (cached) return cached;
                    if (url.pathname.includes('davinci')) return caches.match('./davinci-plugins.html');
                    if (url.pathname.includes('ae-plugin')) return caches.match('./ae-plugins.html');
                    if (url.pathname.includes('sound')) return caches.match('./sound-effects.html');
                    return caches.match('./index.html');
                });
            })
        );
    } else {
        event.respondWith(
            caches.match(event.request).then((cached) => {
                return cached || fetch(event.request).then((response) => {
                    return response;
                });
            })
        );
    }
});
