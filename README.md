# OídoCocina · web de producto

Landing de **OídoCocina** (oidococinapp.com): comandas y pantalla de cocina en tiempo real para pizzerías.
HTML plano, sin build ni framework, publicada en GitHub Pages. Español como idioma principal e inglés como segundo idioma (botón ES/EN; también `?lang=en`).

## Estructura

La web **se genera**: se editan las plantillas de `src/` y `scripts/build_site.py`
escribe las páginas finales en la raíz. Las de la raíz son el resultado y llevan
el aviso «Generado por scripts/build_site.py»: no se editan a mano.

```
src/pages/index.html             plantilla de la portada
src/pages/404.html               plantilla de «página no encontrada»
src/pages/503.html               plantilla de «servicio no disponible» / mantenimiento
src/partials/header.html         cabecera: saltar al contenido, logo, menú, ES/EN, Entrar, demo
src/partials/footer.html         pie: columnas Producto / Contacto / Legal y copyright
src/partials/legal-modal.html    aviso legal, privacidad y cookies (ES y EN)
src/partials/overlays.html       volver arriba, botón de WhatsApp y banner de cookies
src/partials/error-styles.html   estilos de las páginas de error (en línea, autónomos)
src/partials/error-header.html   cabecera mínima de las páginas de error
src/partials/error-footer.html   pie mínimo de las páginas de error
src/partials/error-script.html   idioma, enlaces en github.io y email de las páginas de error
scripts/build_site.py            plantillas + partials -> index.html, 404.html, 503.html

index.html, 404.html, 503.html   GENERADOS
sw.js                            service worker: muestra 503.html si GitHub da un error 5xx/429 o no hay conexión
assets/                          favicon, iconos de la app y og.png (imagen para compartir en redes)
site.webmanifest, robots.txt, sitemap.xml
.github/workflows/pages.yml      genera y publica en GitHub Pages en cada push
```

### Cómo funcionan los partials

Una plantilla incluye un partial con un marcador `<!--{{NOMBRE}}-->`:
`<!--{{HEADER}}-->` carga `src/partials/header.html`, `<!--{{LEGAL_MODAL}}-->`
carga `legal-modal.html` (mayúsculas y `_` pasan a minúsculas y `-`).
Dentro de los partials, `{{HOME}}` es la ruta a la portada (vacía en la portada),
así el menú sirve tal cual para cualquier página nueva.

```bash
python3 scripts/build_site.py          # genera las páginas
python3 scripts/build_site.py --check  # comprueba que la raíz está al día
```

El workflow de publicación ejecuta el script antes de desplegar, así que lo
publicado siempre corresponde a `src/`, aunque se olvide generar en local.
Para una página nueva: crea `src/pages/nueva.html` con los mismos marcadores.

## Qué hay que rellenar antes de publicar en serio

| Dato | Dónde |
|---|---|
| Email, teléfono, WhatsApp y URL de la app | bloque `CONFIG` del `<script>` final de `src/pages/index.html` (y el email también en `src/partials/error-script.html`) |
| Claves de EmailJS del formulario | `EMAILJS` en el mismo bloque |
| ID de Google Analytics (opcional) | `GA_ID`; solo se carga si el visitante acepta cookies |
| Precios | los `[PRECIO]` de la sección Precios |
| Titular, NIF y dirección | `src/partials/legal-modal.html` (`[TITULAR]`, `[NIF]`, `[DIRECCIÓN]`, `[EMAIL]`) |
| Biscotti u otro CMP | pega su script en el `<head>` y pon `ownCookieBanner: false` |

## Cómo se edita un texto

El español está escrito en las plantillas y partials de `src/`. Cada texto traducible lleva `data-i18n="clave"` y su versión en inglés está en el objeto `EN` del script. Si cambias un texto en español, cambia también su clave en `EN`.

## Publicación

El workflow `pages.yml` publica en GitHub Pages en cada push a `main` o a la rama de trabajo.
Si el primer despliegue falla por permisos: **Settings → Pages → Source: GitHub Actions**.
Dominio propio: **Settings → Pages → Custom domain** → `oidococinapp.com` y apunta el DNS a GitHub Pages.

## Páginas de error

- **404**: GitHub Pages sirve `404.html` para cualquier dirección que no exista.
- **503 y errores de servidor**: GitHub Pages no permite páginas propias para errores 5xx. Para que no se vea la página de GitHub, `sw.js` (se instala en la primera visita) intercepta la navegación y, si GitHub responde 5xx o 429, o no hay conexión, muestra `503.html`.
- Para cubrir también a quien entra por primera vez durante una caída de GitHub hace falta un proxy delante (por ejemplo Cloudflare con el dominio propio y sus páginas de error personalizadas apuntando a `503.html`).
- **Modo mantenimiento**: crea un archivo vacío llamado `MAINTENANCE` en la raíz y haz push; toda la web mostrará la página 503. Bórralo y haz push para volver.
- Los estilos de 404 y 503 se insertan en línea (partial `error-styles.html`) para que se vean bien aunque falle el resto del sitio. El email de contacto está en el `CONFIG` de `src/partials/error-script.html`.
