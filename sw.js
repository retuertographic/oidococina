/* OídoCocina · service worker
   Su único trabajo: que el visitante nunca vea una página de error de GitHub.
   - Guarda en caché las páginas de error propias (503 y 404).
   - Las páginas siempre se piden a la red (nunca se sirve contenido viejo).
   - Si GitHub responde con un error de servidor (5xx) o de saturación (429),
     o si no hay conexión, muestra nuestra página 503 en su lugar. */
const CACHE = "oc-errors-v1";
const PAGES = ["503.html", "404.html"];
const url = p => new URL(p, self.registration.scope).href;

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(PAGES.map(url))).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k.startsWith("oc-") && k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

async function errorPage(){
  const cached = await caches.match(url("503.html"));
  if (cached) {
    return new Response(cached.body, { status: 503, statusText: "Service Unavailable", headers: { "Content-Type": "text/html; charset=utf-8", "Retry-After": "30" } });
  }
  return new Response("<!doctype html><meta charset=utf-8><title>OídoCocina</title><p style=\"font-family:sans-serif;padding:40px\">OídoCocina no está disponible ahora mismo. Vuelve a intentarlo en unos minutos.</p>", { status: 503, headers: { "Content-Type": "text/html; charset=utf-8" } });
}

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.mode !== "navigate" || new URL(req.url).origin !== self.location.origin) return;
  e.respondWith(
    fetch(req)
      .then(res => (res.status >= 500 || res.status === 429) ? errorPage() : res)
      .catch(errorPage)
  );
});
