# Informes

Un informe por trabajo práctico, en PDF, con las capturas embebidas.

| Archivo | Qué es |
|---|---|
| `TP1-informe.html` | La **fuente** del informe: texto versionable y diffeable, con las imágenes de `../img/` embebidas en base64 |
| `TP1-informe.pdf` | El artefacto que se lee y se entrega |
| `build-informe.py` | Regenera el `.html` a partir de las imágenes de `../img/` |

## Cómo regenerarlo

```bash
python3 informes/build-informe.py

"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$PWD/informes/TP1-informe.pdf" \
  "file://$PWD/informes/TP1-informe.html"
```

No hace falta instalar nada: el HTML se imprime a PDF con el Chrome que ya está en la máquina.
