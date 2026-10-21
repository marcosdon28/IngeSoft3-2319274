#!/usr/bin/env bash
# Despliega UN servicio de Render por su API y espera a que ese deploy esté live.
#
# Uso:  RENDER_API_KEY=… ./scripts/render-deploy.sh <service-id> <imagen|commit-sha>
#   - con una IMAGEN (ghcr.io/…:sha-…), el servicio EJECUTA esa imagen (TP7:
#     build once, deploy many — lo que corre es bit a bit lo que se verificó);
#   - con un commit, Render reconstruye desde el repo (TP6; queda por compatibilidad).
#
# Por qué la API y no el Deploy Hook (TP6):
#   - El hook contesta al instante y Render construye en background; mientras
#     construye —o si el build falla— sigue sirviendo la versión anterior, así
#     que un smoke test puede dar verde contra la versión VIEJA. Con la API el
#     deploy tiene un id, y se le puede preguntar en qué estado está: este
#     script no termina hasta que figure `live`, y falla si el build falla.
#   - El commit va explícito (`commitId`), igual que el `&ref=` del hook: se
#     despliega lo que esta corrida verificó, no la punta de la rama.
#   - El id del servicio queda a la vista (variable del environment); la
#     credencial, no (secret del environment).
set -euo pipefail

SERVICIO="${1:?falta el id del servicio (srv-…)}"
QUE="${2:?falta la imagen (ghcr.io/…:sha-…) o el sha del commit}"
: "${RENDER_API_KEY:?falta RENDER_API_KEY en el entorno}"
API="https://api.render.com/v1"
ESPERA_MAX="${ESPERA_MAX:-900}"      # segundos: los builds del plan gratuito tardan 2-5 min por servicio

auth=(-H "Authorization: Bearer $RENDER_API_KEY" -H "Content-Type: application/json" -H "Accept: application/json")

if [[ "$QUE" == */* ]]; then
  echo "→ deploy de $SERVICIO con la IMAGEN $QUE"
  cuerpo="{\"imageUrl\":\"$QUE\"}"
else
  echo "→ deploy de $SERVICIO con el commit $QUE (Render reconstruye desde el repo)"
  cuerpo="{\"commitId\":\"$QUE\",\"clearCache\":\"do_not_clear\"}"
fi
respuesta=$(curl -fsS --max-time 30 -X POST "${auth[@]}" "$API/services/$SERVICIO/deploys" -d "$cuerpo")
DEPLOY=$(python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])' <<<"$respuesta")
echo "  deploy $DEPLOY creado"

inicio=$(date +%s)
anterior=""
while :; do
  estado=$(curl -fsS --max-time 30 "${auth[@]}" "$API/services/$SERVICIO/deploys/$DEPLOY" \
    | python3 -c 'import sys,json; print(json.load(sys.stdin)["status"])')
  [[ "$estado" != "$anterior" ]] && echo "  $(( $(date +%s) - inicio ))s · $estado"
  anterior=$estado
  case "$estado" in
    live)
      echo "✅ $SERVICIO live con $QUE ($(( $(date +%s) - inicio )) s)"; exit 0 ;;
    build_failed|update_failed|pre_deploy_failed|canceled|deactivated)
      echo "❌ el deploy terminó en '$estado'"; exit 1 ;;
  esac
  if (( $(date +%s) - inicio > ESPERA_MAX )); then
    echo "❌ el deploy no llegó a live en $ESPERA_MAX s (último estado: $estado)"; exit 1
  fi
  sleep 15
done
