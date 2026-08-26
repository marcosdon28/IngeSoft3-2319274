# Informes

Un informe por trabajo práctico, en PDF, con las capturas embebidas.

| Archivo | Qué es |
|---|---|
| `TP1-informe.pdf` / `.html` | TP1 — Git colaborativo (18 páginas) |
| `TP2-informe.pdf` / `.html` | TP2 — Contenedores: la app del semestre (21 páginas) |
| `build-informe.py` | Regenera el HTML del TP1 a partir de las imágenes de `../img/` |
| `build-informe-tp2.py` | Ídem para el TP2 |
| `render-terminal.py` | Renderiza la salida **real** de una terminal como imagen, para las evidencias |

El `.html` es la fuente: texto versionable y diffeable, con las imágenes embebidas en base64. El
`.pdf` es el artefacto que se lee.

## Cómo regenerar un informe

```bash
python3 informes/build-informe-tp2.py

"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$PWD/informes/TP2-informe.pdf" \
  "file://$PWD/informes/TP2-informe.html"
```

No hace falta instalar nada: el HTML se imprime a PDF con el Chrome que ya está en la máquina.

## Cómo se produce una evidencia de terminal

La salida del comando se captura **literal** a un archivo de texto, y después se renderiza:

```bash
python3 informes/render-terminal.py salida.txt salida.html "título de la ventana"
# y se captura el HTML con Playwright
```

El script sólo agrega colores: **no inventa ni edita la salida**. En `evidencias.md`, donde
corresponde, se aclara que la imagen es un render y se transcribe el texto original al lado.
