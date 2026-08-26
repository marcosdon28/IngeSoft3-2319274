#!/usr/bin/env bash
# Carga datos de ejemplo en la API para poder ver la app con contenido.
# Uso:  ./scripts/datos-demo.sh   (con el sistema levantado)
set -euo pipefail

API="${API:-http://localhost:8000/api}"

post() { curl -sf -X POST "$API/$1" -H 'Content-Type: application/json' -d "$2" > /dev/null; }

echo "Esperando a que la API responda…"
until curl -sf -o /dev/null "${API%/api}/health"; do sleep 1; done

echo "Categorías…"
post categorias '{"nombre":"Bebidas"}'
post categorias '{"nombre":"Almacen"}'
post categorias '{"nombre":"Limpieza"}'

echo "Productos…"
post productos '{"sku":"BEB-001","nombre":"Gaseosa 1.5L","precio":1800,"stock":40,"stock_minimo":10,"categoria_id":1}'
post productos '{"sku":"BEB-002","nombre":"Agua mineral 500ml","precio":900,"stock":8,"stock_minimo":12,"categoria_id":1}'
post productos '{"sku":"ALM-001","nombre":"Yerba mate 1kg","precio":6200,"stock":25,"stock_minimo":5,"categoria_id":2}'
post productos '{"sku":"LIM-001","nombre":"Detergente 750ml","precio":2400,"stock":3,"stock_minimo":6,"categoria_id":3}'

echo "Movimientos…"
post movimientos '{"producto_id":1,"tipo":"SALIDA","cantidad":9}'    # sin descuento
post movimientos '{"producto_id":1,"tipo":"SALIDA","cantidad":10}'   # con descuento (borde)
post movimientos '{"producto_id":2,"tipo":"ENTRADA","cantidad":24}'   # reposición
post movimientos '{"producto_id":3,"tipo":"SALIDA","cantidad":21}'    # deja ALM-001 bajo su mínimo

# LIM-001 queda a propósito en 3 unidades con mínimo 6: así se ve la alerta de
# bajo stock (regla 6) funcionando en el tablero.

echo "Listo. Abrí http://localhost:3000"
