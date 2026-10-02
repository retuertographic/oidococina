# OídoCocina · web de producto

Landing de **OídoCocina** (oidococinapp.com): comandas y pantalla de cocina en tiempo real para pizzerías.
HTML plano, sin build ni framework, publicada en GitHub Pages. Español como idioma principal e inglés como segundo idioma (botón ES/EN; también `?lang=en`).

## Estructura

```
index.html            la página (estilos, textos en español, traducciones EN y scripts)
404.html              página no encontrada (ES/EN, con la identidad de la web)
503.html              servicio no disponible / mantenimiento (ES/EN, reintenta sola cada 30 s)
sw.js                 service worker: muestra 503.html si GitHub da un error 5xx/429 o no hay conexión
assets/               favicon, iconos de la app y og.png (imagen para compartir en redes)
site.webmanifest      manifiesto (icono al añadir a la pantalla de inicio)
robots.txt, sitemap.xml
.github/workflows/pages.yml   publica en GitHub Pages en cada push
```

## Qué hay que rellenar antes de publicar en serio

| Dato | Dónde |
|---|---|
| Email, teléfono, WhatsApp y URL de la app | bloque `CONFIG` al principio del `<script>` final de `index.html` (se aplica en toda la página) |
| Claves de EmailJS del formulario | `EMAILJS` en el mismo bloque |
| ID de Google Analytics (opcional) | `GA_ID`; solo se carga si el visitante acepta cookies |
| Precios | los `[PRECIO]` de la sección Precios |
| Titular, NIF y dirección | textos legales del modal (`[TITULAR]`, `[NIF]`, `[DIRECCIÓN]`, `[EMAIL]`) |
| Biscotti u otro CMP | pega su script en el `<head>` y pon `ownCookieBanner: false` |

## Cómo se edita un texto

El español está escrito en el propio HTML. Cada texto traducible lleva `data-i18n="clave"` y su versión en inglés está en el objeto `EN` del script. Si cambias un texto en español, cambia también su clave en `EN`.

## Publicación

El workflow `pages.yml` publica en GitHub Pages en cada push a `main` o a la rama de trabajo.
Si el primer despliegue falla por permisos: **Settings → Pages → Source: GitHub Actions**.
Dominio propio: **Settings → Pages → Custom domain** → `oidococinapp.com` y apunta el DNS a GitHub Pages.

## Páginas de error

- **404**: GitHub Pages sirve `404.html` para cualquier dirección que no exista.
- **503 y errores de servidor**: GitHub Pages no permite páginas propias para errores 5xx. Para que no se vea la página de GitHub, `sw.js` (se instala en la primera visita) intercepta la navegación y, si GitHub responde 5xx o 429, o no hay conexión, muestra `503.html`.
- Para cubrir también a quien entra por primera vez durante una caída de GitHub hace falta un proxy delante (por ejemplo Cloudflare con el dominio propio y sus páginas de error personalizadas apuntando a `503.html`).
- **Modo mantenimiento**: crea un archivo vacío llamado `MAINTENANCE` en la raíz y haz push; toda la web mostrará la página 503. Bórralo y haz push para volver.
- Los textos y estilos de 404 y 503 están en línea dentro de cada archivo para que se vean bien aunque falle el resto del sitio. El email de contacto del 503 está en su `CONFIG`.
