#!/usr/bin/env python3
"""Genera las páginas de la web a partir de las plantillas de src/.

    python3 scripts/build_site.py          escribe index.html, 404.html y no-disponible.html en la raíz
    python3 scripts/build_site.py --check  no escribe nada; falla si la raíz no está al día
    python3 scripts/build_site.py --strict además falla si quedan datos sin rellenar ([EMAIL], [NIF]…)

Cada plantilla de src/pages/ puede incluir partials de src/partials/ con un
marcador <!--{{NOMBRE}}-->: {{HEADER}} carga header.html, {{LEGAL_MODAL}}
carga legal-modal.html, etc. (mayúsculas y _ -> minúsculas y -).

Dentro de los partials, {{HOME}} es la ruta a la portada desde cada página
(vacía en la propia portada), para que los enlaces del menú (#precios...)
funcionen igual si mañana se añade otra página.

Sin dependencias: solo la biblioteca estándar de Python.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "src" / "pages"
PARTIALS = ROOT / "src" / "partials"

# Variables por página. Las páginas que no aparecen usan DEFAULT_VARS.
DEFAULT_VARS = {"HOME": "./"}
PAGE_VARS = {
    "index.html": {"HOME": ""},
}

MARKER = re.compile(r"<!--\{\{([A-Z0-9_]+)\}\}-->")
VAR = re.compile(r"\{\{([A-Z0-9_]+)\}\}")
# Datos de ejemplo que no deben publicarse: se avisa siempre y --strict impide publicar
PLACEHOLDER = re.compile(r"\[(?:EMAIL|TEL[EÉ]FONO|PRECIO|NIF|TITULAR|DIRECCI[OÓ]N|URL-DE-LA-APP|TU_[A-Z_]+|NOMBRE[^\]]*|NAME[^\]]*|OWNER|ADDRESS)\]")
BANNER = "<!-- Generado por scripts/build_site.py desde src/pages/{name}: no se edita a mano. -->\n"


def partial(name: str, page: str) -> str:
    path = PARTIALS / (name.lower().replace("_", "-") + ".html")
    if not path.exists():
        sys.exit(f"ERROR: {page} usa <!--{{{{{name}}}}}--> pero no existe {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8").rstrip("\n")


def render(src: Path) -> str:
    html = src.read_text(encoding="utf-8")
    # Los partials pueden incluir otros partials (hasta 5 niveles)
    for _ in range(5):
        new = MARKER.sub(lambda m: partial(m.group(1), src.name), html)
        if new == html:
            break
        html = new
    if MARKER.search(html):
        sys.exit(f"ERROR: {src.name}: partials anidados demasiado profundo")
    variables = {**DEFAULT_VARS, **PAGE_VARS.get(src.name, {})}
    html = VAR.sub(lambda m: variables.get(m.group(1), m.group(0)), html)
    left = set(VAR.findall(html))
    if left:
        sys.exit(f"ERROR: {src.name}: variables sin valor: {', '.join(sorted(left))}")
    # El aviso va justo después del <!doctype html>
    first, rest = html.split("\n", 1)
    return first + "\n" + BANNER.format(name=src.name) + rest


def main() -> None:
    check = "--check" in sys.argv[1:]
    strict = "--strict" in sys.argv[1:]
    stale, pending = [], {}
    for src in sorted(PAGES.glob("*.html")):
        out = ROOT / src.name
        html = render(src)
        found = sorted(set(PLACEHOLDER.findall(html)))
        if found:
            pending[src.name] = found
        current = out.read_text(encoding="utf-8") if out.exists() else None
        if current == html:
            print(f"  = {src.name}")
            continue
        if check:
            stale.append(src.name)
            print(f"  ! {src.name} no está al día")
        else:
            out.write_text(html, encoding="utf-8")
            print(f"  ✓ {src.name}")
    for name, found in pending.items():
        print(f"  ⚠ {name}: datos sin rellenar: {', '.join(found)}")
    if pending and strict:
        sys.exit("Hay datos sin rellenar: no se publica (quita --strict para publicar igualmente).")
    if stale:
        sys.exit("Ejecuta: python3 scripts/build_site.py")


if __name__ == "__main__":
    main()
