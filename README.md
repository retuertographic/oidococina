# OídoCocina · web de producto

Landing de **OídoCocina** (oidococinapp.com): comandas y pantalla de cocina en tiempo real para pizzerías.
HTML plano, sin build ni framework, publicada en GitHub Pages. Español como idioma principal e inglés como segundo idioma (botón ES/EN; también `?lang=en`).

## Estructura

```
index.html            la página (estilos, textos en español, traducciones EN y scripts)
404.html              página de error
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
