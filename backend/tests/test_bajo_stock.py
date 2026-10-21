"""REGLA 6 — Bajo stock: propiedad DERIVADA del modelo, stock <= stock_minimo."""
import pytest

from app.models import Producto


@pytest.mark.parametrize(
    ("stock", "stock_minimo", "esperado"),
    [
        (3, 6, True),    # por debajo del mínimo
        (6, 6, True),    # borde: IGUAL al mínimo ya es bajo stock (<=, no <)
        (7, 6, False),   # una unidad arriba del mínimo
        (0, 0, True),    # sin stock y sin mínimo: hay que reponer igual
    ],
)
def test_bajo_stock_cuando_el_stock_no_supera_el_minimo(stock, stock_minimo, esperado):
    # Arrange
    producto = Producto(sku="X-1", nombre="x", precio=1, stock=stock, stock_minimo=stock_minimo)
    # Act / Assert: es una propiedad, no una columna — no puede desincronizarse
    assert producto.bajo_stock is esperado
