# Proyecto IngSoft3 — Inventario de productos (UCC 2026)

[![CI](https://github.com/marcosdon28/IngeSoft3-2319274/actions/workflows/ci.yml/badge.svg)](https://github.com/marcosdon28/IngeSoft3-2319274/actions/workflows/ci.yml)
Ingeniería del Software 3 - UCC 2026 | Repo del semestre: TP1..TP9 + Integrador

Sistema de gestión de inventario: productos, categorías y movimientos de stock, con las reglas de
negocio del dominio (stock que no puede quedar negativo, SKU único, descuentos por cantidad, alertas
de reposición). Es la **app del semestre**: cada trabajo práctico le agrega una capa.

| | |
|---|---|
| **Frontend** | React 18 + Vite, servido por nginx |
| **Backend** | FastAPI (Python 3.12) + SQLAlchemy 2, organizado en MVC |
| **Base de datos** | PostgreSQL 16 |

---

## Arranque desde cero

Requisitos: **sólo Docker**. No hace falta tener instalado Python, Node ni PostgreSQL.

```bash
git clone https://github.com/marcosdon28/IngeSoft3-2319274.git
cd IngeSoft3-2319274

cp .env.example .env        # ⚠️ PRIMERO esto: el .env no viaja en el repo
docker compose up -d --build
```

Son **dos comandos, no uno**, y eso es a propósito: el secreto de la base es lo único que no puede
estar versionado, así que el arranque necesita ese paso manual. El `.env.example` documenta qué
variables hacen falta, sin traer ningún valor real.

Cuando termine:

| Servicio | URL |
|---|---|
| Aplicación | <http://localhost:3000> |
| API | <http://localhost:8000> |
| Documentación de la API (OpenAPI) | <http://localhost:8000/docs> |
| Salud del backend | <http://localhost:8000/health> |

Para ver la app con contenido: `./scripts/datos-demo.sh`

Para apagar: `docker compose down` (los datos quedan) · `docker compose down -v` (los datos se borran).

### Levantarlo sin el código, desde el registry

Las imágenes están publicadas en GitHub Container Registry. Con sólo el compose y el `.env` alcanza:

```bash
cp .env.example .env
docker compose -f docker-compose.registry.yml up -d
```

- `ghcr.io/marcosdon28/inventario-backend:v0.1.0`
- `ghcr.io/marcosdon28/inventario-frontend:v0.1.0`

---

## Cómo está organizado

```
backend/                 FastAPI, en capas MVC
  app/models/            SQLAlchemy — las entidades y su persistencia
  app/schemas/           Pydantic — el contrato de entrada y salida de la API
  app/services/          las REGLAS DE NEGOCIO, sin nada de HTTP adentro
  app/routers/           los endpoints: traducen HTTP a llamadas a los services
frontend/                React + Vite
  src/lib/reglas.js      reglas de la vista, funciones puras y testeables
  src/pages/             Resumen · Productos · Categorías · Movimientos
scripts/datos-demo.sh    carga datos de ejemplo contra la API
```

Los services no importan FastAPI: las reglas se pueden testear sin levantar la API. El frontend llama
a `/api/...` con **ruta relativa** — no sabe dónde vive el backend, y por eso la misma imagen sirve en
cualquier entorno (en desarrollo lo resuelve el proxy de Vite; en el contenedor, nginx).

## Las reglas de negocio

| # | Regla | Dónde vive |
|---|---|---|
| 1 | Una salida no puede superar el stock disponible | `services/movimiento_service.py` |
| 2 | El SKU de un producto es único | `services/producto_service.py` |
| 3 | No se puede eliminar una categoría con productos asociados | `services/categoria_service.py` |
| 4 | Precio y stock no negativos; cantidad de movimiento > 0 | `schemas/` (Pydantic) |
| 5 | Descuento por cantidad a partir de un umbral | `services/movimiento_service.py` |
| 6 | Un producto con `stock <= stock_minimo` está en bajo stock | `models/producto.py` |
| 7 | Un producto inactivo no admite movimientos | `services/movimiento_service.py` |

---

## Contenido del repositorio

| Archivo | Qué es |
|---|---|
| [`decisiones.md`](decisiones.md) | Bitácora de decisiones técnicas, problemas resueltos y declaración de uso de IA. Se acumula TP a TP |
| [`evidencias.md`](evidencias.md) | Las capturas de cada TP, con una explicación de qué se está viendo |
| [`CLAUDE.md`](CLAUDE.md) | Las reglas de trabajo del repositorio: todo por PR, cuándo se actualiza cada archivo, cómo se cierra cada TP |
| [`informes/`](informes/) | Un informe en PDF por trabajo práctico, paso a paso |
| [`img/`](img/) | Las imágenes de las evidencias |

## Trabajos prácticos

Planificación y tablero: **[IngSoft3 — Inventario DevOps](https://github.com/users/marcosdon28/projects/2)** (público)


| TP | Tema | Versión |
|---|---|---|
| TP1 | Git colaborativo | [`v1.0.0`](https://github.com/marcosdon28/IngeSoft3-2319274/releases/tag/v1.0.0) |
| TP2 | Contenedores: la app del semestre | [`v2.0.0`](https://github.com/marcosdon28/IngeSoft3-2319274/releases/tag/v2.0.0) |
| TP3 | Planificación y trazabilidad | [`v3.0.0`](https://github.com/marcosdon28/IngeSoft3-2319274/releases/tag/v3.0.0) |

Cada práctico se cierra con su tag y su release: el tag marca el commit exacto con el que quedó
entregado.
