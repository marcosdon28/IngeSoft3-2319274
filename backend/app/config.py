"""Configuración leída del entorno.

Regla del proyecto: la conexión a la base NUNCA va hardcodeada. Se lee de
DATABASE_URL, que es lo que permite que la MISMA imagen corra en local, en QA y
en producción cambiando solo una variable (TP6).
"""
import os

# El default apunta al servicio 'db' del compose: dentro de la red de compose los
# servicios se encuentran por NOMBRE, no por IP ni por localhost.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@db:5432/inventario",
)

# Regla de negocio 5: umbral y porcentaje del descuento por cantidad.
# Parametrizables por entorno para poder cambiarlos sin tocar el código.
DESCUENTO_CANTIDAD_MINIMA = int(os.getenv("DESCUENTO_CANTIDAD_MINIMA", "10"))
DESCUENTO_PORCENTAJE = float(os.getenv("DESCUENTO_PORCENTAJE", "10"))
