// Service Worker para CoworkSpace KC PWA
const CACHE_NAME = 'coworkspace-kc-v1';
const OFFLINE_URL = '/';

// Archivos a cachear para funcionamiento offline
const urlsToCache = [
  '/',
  '/static/css/style.css',
  '/static/css/custom-colors.css',
  '/static/css/spacing-fix.css',
  '/static/images/icon-192.png',
  '/static/images/icon-512.png',
];

// Instalación del Service Worker
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('PWA: Cache abierto');
        return cache.addAll(urlsToCache);
      })
      .then(() => self.skipWaiting())
  );
});

// Activación del Service Worker
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('PWA: Borrando caché antiguo:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Estrategia: Network First, luego Cache (para datos dinámicos)
self.addEventListener('fetch', (event) => {
  // Ignorar requests que no sean GET
  if (event.request.method !== 'GET') {
    return;
  }

  event.respondWith(
    fetch(event.request)
      .then((response) => {
        // Si la respuesta es válida, guardarla en caché
        if (response && response.status === 200) {
          const responseToCache = response.clone();
          caches.open(CACHE_NAME)
            .then((cache) => {
              cache.put(event.request, responseToCache);
            });
        }
        return response;
      })
      .catch(() => {
        // Si falla la red, intentar servir desde caché
        return caches.match(event.request)
          .then((response) => {
            if (response) {
              return response;
            }
            // Si no hay caché, mostrar página offline
            if (event.request.mode === 'navigate') {
              return caches.match(OFFLINE_URL);
            }
          });
      })
  );
});

// Sincronización en segundo plano (Background Sync)
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-data') {
    event.waitUntil(syncData());
  }
});

async function syncData() {
  try {
    // Aquí se sincronizarían los datos pendientes cuando vuelva la conexión
    console.log('PWA: Sincronizando datos con el servidor...');
    
    // Obtener datos pendientes del IndexedDB
    const pendingRequests = await getPendingRequests();
    
    // Enviar cada request pendiente
    for (const request of pendingRequests) {
      try {
        await fetch(request.url, {
          method: request.method,
          headers: request.headers,
          body: request.body
        });
        // Si se envió correctamente, eliminarlo de pendientes
        await removePendingRequest(request.id);
      } catch (error) {
        console.log('PWA: Error al sincronizar request:', error);
      }
    }
  } catch (error) {
    console.log('PWA: Error en sincronización:', error);
  }
}

// Funciones auxiliares para IndexedDB (simuladas)
async function getPendingRequests() {
  // Aquí iría la lógica para obtener requests pendientes de IndexedDB
  return [];
}

async function removePendingRequest(id) {
  // Aquí iría la lógica para eliminar request de IndexedDB
  return true;
}

// Notificar al cliente cuando hay actualizaciones
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
