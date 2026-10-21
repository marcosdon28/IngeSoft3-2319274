"""REGLA 4 — Validación de dominio en el borde de entrada (Pydantic).

Son los CASOS DE ERROR: una entrada inválida tiene que ser rechazada antes de
llegar a un service, y el mensaje tiene que decir qué campo falló.
"""
import pytest
from pydantic import ValidationError

from app.schemas.movimiento import MovimientoCrear
from app.schemas.producto import ProductoCrear


def test_un_movimiento_con_cantidad_cero_es_rechazado():
    # Arrange / Act
    with pytest.raises(ValidationError) as info:
        MovimientoCrear(producto_id=1, tipo="SALIDA", cantidad=0)
    # Assert: el error señala el campo y la condición (> 0)
    errores = info.value.errors()
    assert errores[0]["loc"] == ("cantidad",)
    assert "greater than 0" in errores[0]["msg"]


def test_un_producto_con_precio_negativo_es_rechazado():
    # Arrange / Act
    with pytest.raises(ValidationError) as info:
        ProductoCrear(sku="AB-1", nombre="Algo", precio=-1, stock=0, categoria_id=1)
    # Assert
    assert info.value.errors()[0]["loc"] == ("precio",)


def test_un_producto_con_stock_negativo_es_rechazado():
    with pytest.raises(ValidationError) as info:
        ProductoCrear(sku="AB-1", nombre="Algo", precio=10, stock=-5, categoria_id=1)
    assert info.value.errors()[0]["loc"] == ("stock",)


def test_un_producto_valido_tiene_stock_cero_por_defecto():
    # Arrange / Act: sin stock ni stock_minimo
    datos = ProductoCrear(sku="AB-1", nombre="Algo", precio=10, categoria_id=1)
    # Assert: los defaults existen y no son negativos
    assert datos.stock == 0
    assert datos.stock_minimo == 0
