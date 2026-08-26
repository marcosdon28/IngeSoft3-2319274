# ---- Etapa 1: build (Node compila la SPA a estáticos) ----
FROM node:22-alpine AS build
WORKDIR /app

# package.json + lockfile primero: la capa de dependencias se cachea aparte.
COPY package*.json ./
RUN npm ci                 # ci, no install: respeta el lockfile exacto

COPY . .
RUN npm run build          # Vite emite a /app/dist

# ---- Etapa 2: nginx sirve los estáticos ----
# Node no viaja a producción: la imagen final sólo tiene nginx y archivos.
FROM nginx:alpine

# Linkea la imagen publicada con este repositorio en la pestaña Packages.
LABEL org.opencontainers.image.source=https://github.com/marcosdon28/IngeSoft3-2319274
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
