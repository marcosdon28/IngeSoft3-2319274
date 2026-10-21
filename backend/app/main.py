"""Punto de entrada de la API — capa Controller del MVC.

Los routers traducen HTTP a llamadas a los services; los services tienen las
reglas de negocio y no saben nada de HTTP. Esa separación es lo que permite
testear las reglas sin levantar la API (TP5).
"""
import os

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import categorias, movimientos, productos

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


# El commit con el que se construyó la imagen: lo pone el pipeline como argumento
# de build (ARG APP_COMMIT en el Dockerfile). Nunca va como variable del servicio:
# si el entorno la pisara, /health dejaría de decir qué imagen corre de verdad.
APP_COMMIT = os.getenv("APP_COMMIT", "desconocido")


@app.get("/health", tags=["salud"])
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
