"""Punto de entrada de la API — capa Controller del MVC.

Los routers traducen HTTP a llamadas a los services; los services tienen las
reglas de negocio y no saben nada de HTTP. Esa separación es lo que permite
testear las reglas sin levantar la API (TP5).
"""
import os

import sentry_sdk
from fastapi import FastAPI

from app.database import Base, engine
from app.routers import categorias, movimientos, productos

# Observabilidad de la aplicación (TP9): qué falla, qué tarda y qué se usa.
# El DSN llega por el entorno y SÓLO está cargado en el servicio de producción:
# sin la variable (local, tests, QA) la librería queda apagada y la app anda igual.
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN", ""),
    environment=os.getenv("SENTRY_ENVIRONMENT", "production"),
    release=os.getenv("APP_COMMIT") or None,   # el commit horneado en la imagen: cada error dice qué versión lo produjo
    traces_sample_rate=1.0,                    # medir todos los pedidos (para una app de cursada sobra)
    send_default_pii=False,
)

app = FastAPI(
    title="Inventario — IngSoft3 UCC 2026",
    description="Gestión de productos, categorías y movimientos de stock.",
    version="0.1.0",
)


@app.on_event("startup")
def crear_schema() -> None:
    """Crea las tablas al arrancar si no existen.

    Alcanza para la materia. En un proyecto real esto se resuelve con migraciones
    (Alembic): create_all no sabe modificar una tabla que ya existe.
    """
    Base.metadata.create_all(bind=engine)


# El commit que corre, con tres orígenes posibles y en este orden:
#   1. APP_COMMIT horneado en la imagen (ARG del Dockerfile, lo pasa el pipeline
#      con --build-arg): es la fuente de verdad cuando el entorno EJECUTA la
#      imagen del registry (TP7). Nunca va como variable del servicio: si el
#      entorno la pisara, /health dejaría de decir qué imagen corre de verdad.
#   2. RENDER_GIT_COMMIT, que Render inyecta cuando RECONSTRUYE desde el repo
#      (TP6): ahí mi imagen no es la que corre, y el ARG no llega.
#   3. "local": un build en la máquina, sin pipeline.
APP_COMMIT = os.getenv("APP_COMMIT") or os.getenv("RENDER_GIT_COMMIT") or "local"


# GET y HEAD: el plan gratuito de UptimeRobot (TP9) pregunta con HEAD, y FastAPI
# no lo deriva solo de un GET: sin esto el monitor marca Down con PROD vivo.
@app.api_route("/health", methods=["GET", "HEAD"], tags=["salud"])
def health():
    """Endpoint de salud: lo usan el healthcheck del compose y el smoke test del CD.

    Devuelve también el commit que corre: así el smoke puede comprobar desde
    afuera que lo desplegado es lo que la corrida verificó, y no la versión
    anterior que Render sigue sirviendo mientras construye (TP6/TP7).
    """
    return {"status": "ok", "commit": APP_COMMIT}


app.include_router(categorias.router)
app.include_router(productos.router)
app.include_router(movimientos.router)
