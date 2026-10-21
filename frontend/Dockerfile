# ---- Etapa 1: build (Node compila la SPA a estáticos) ----
FROM node:22-alpine AS build
WORKDIR /app

# package.json + lockfile primero: la capa de dependencias se cachea aparte.
COPY package*.json ./
RUN npm ci                 # ci, no install: respeta el lockfile exacto

COPY . .
RUN npm run build          # Vite emite a /app/dist

# ---- Etapa 2: tests (parte del build: ya tiene Node y las dependencias de desarrollo) ----
# `npm ci` de arriba instaló TAMBIÉN las devDependencies (vitest, coverage-v8):
# no lleva --omit=dev justamente para que esta etapa pueda testear. La imagen
# final (nginx) no se lleva nada de esto: sólo copia el dist/ compilado.
# El umbral que frena vive en vite.config.js (coverage.thresholds): una receta.
FROM build AS test
ENTRYPOINT ["npm", "run", "test:ci"]

# ---- Etapa 3: nginx sirve los estáticos (queda ÚLTIMA: es la imagen que se despliega) ----
# Node no viaja a producción: la imagen final sólo tiene nginx y archivos.
FROM nginx:alpine

# Linkea la imagen publicada con este repositorio en la pestaña Packages.
LABEL org.opencontainers.image.source=https://github.com/marcosdon28/IngeSoft3-2319274
# La configuración es una PLANTILLA: nginx reemplaza ${BACKEND_URL} y ${DNS_RESOLVER}
# al arrancar (en templates/, no en conf.d/: ahí la leería tal cual y no levantaría).
COPY default.conf.template /etc/nginx/templates/default.conf.template
# Defaults = los de compose. Render los pisa con las variables del servicio.
ENV BACKEND_URL=http://backend:8000 \
    DNS_RESOLVER=127.0.0.11
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
