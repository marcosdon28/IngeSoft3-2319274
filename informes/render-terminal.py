#!/usr/bin/env python3
"""Renderiza la salida REAL de una terminal como imagen, para evidencias.

Uso:  python3 informes/render-terminal.py <transcript.txt> <salida.html> "<titulo>"

Después se captura el HTML con Playwright (ver informes/README.md). El texto de
entrada es la salida literal del comando: este script sólo le pone colores.
"""
import html
import sys

CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#1c1c1e; padding:26px; }
.win { background:#161617; border-radius:10px; overflow:hidden; box-shadow:0 10px 40px rgba(0,0,0,.5); }
.bar { background:#2c2c2e; height:38px; display:flex; align-items:center; padding:0 14px; gap:8px;
       border-bottom:1px solid #000; }
.dot { width:12px; height:12px; border-radius:50%; }
.r{background:#ff5f57} .y{background:#febc2e} .g{background:#28c840}
.title { flex:1; text-align:center; color:#9b9b9f; font:600 13px -apple-system,Segoe UI,sans-serif;
         margin-right:56px; }
pre { padding:20px 22px 24px; font:14px/1.55 "SF Mono",Menlo,Consolas,monospace;
      color:#e4e4e7; white-space:pre-wrap; }
.p{color:#7ee787} .pc{color:#79c0ff} .c{color:#fff;font-weight:600}
.err{color:#ff7b72} .ok{color:#7ee787} .cm{color:#8b96a5}
"""


def colorear(linea: str) -> str:
    e = html.escape(linea)
    if linea.startswith("marco@") and " % " in linea:
        host, cmd = linea.split(" % ", 1)
        return (f'<span class="p">{html.escape(host)}</span> '
                f'<span class="pc">%</span> <span class="c">{html.escape(cmd)}</span>')
    if linea.startswith("#"):
        return f'<span class="cm">{e}</span>'
    if any(k in linea for k in ("error", "Error", "rejected", "declined", "insuficiente")):
        return f'<span class="err">{e}</span>'
    if any(k in linea for k in ("Healthy", "healthy", "Started", "OK", "ok")):
        return f'<span class="ok">{e}</span>'
    return e


def main() -> None:
    entrada, salida, titulo = sys.argv[1], sys.argv[2], sys.argv[3]
    texto = open(entrada, encoding="utf-8").read().rstrip("\n")
    cuerpo = "\n".join(colorear(l) for l in texto.split("\n"))
    doc = (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
           f'<div class="win"><div class="bar">'
           f'<span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>'
           f'<span class="title">{html.escape(titulo)}</span></div>'
           f'<pre>{cuerpo}</pre></div></body></html>')
    open(salida, "w", encoding="utf-8").write(doc)
    print("HTML escrito:", salida)


if __name__ == "__main__":
    main()
