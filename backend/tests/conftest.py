"""Fixtures compartidas por la suite del backend.

Los tests NO levantan la API ni tocan PostgreSQL: las reglas viven en los
services y en funciones puras, así que se prueban llamando a una función.
Cuando un service necesita la base, se le pasa un DOBLE de la Session.
"""
from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from app.models import Categoria, Producto


@pytest.fixture
def db():
    """Un doble de la Session de SQLAlchemy.

    `spec=Session` hace que el doble sólo acepte los métodos que la Session real
    tiene: un typo (`db.comit()`) explota en el test en vez de pasar en silencio.
    """
    return Mock(spec=Session)


@pytest.fixture
def categoria():
    return Categoria(id=1, nombre="Bebidas")


@pytest.fixture
def producto(categoria):
    """Un producto activo con 10 unidades: el punto de partida de casi todos los casos."""
    return Producto(
        id=1, sku="BEB-001", nombre="Gaseosa 1.5L", precio=1800,
        stock=10, stock_minimo=4, activo=True, categoria_id=1, categoria=categoria,
    )
