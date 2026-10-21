"""REGLA 5 — Descuento por cantidad (función pura, sin base ni API)."""
import pytest

from app.services.movimiento_service import calcular_descuento, calcular_total


@pytest.mark.parametrize(
    ("cantidad", "descuento_esperado"),
    [
        (1, 0.0),     # muy por debajo del umbral
        (9, 0.0),     # borde: una unidad ANTES del umbral, todavía sin descuento
        (10, 10.0),   # borde: el umbral es INCLUSIVO, con 10 ya corresponde
        (11, 10.0),   # por encima del umbral
    ],
)
def test_descuento_por_cantidad_aplica_desde_el_umbral_inclusive(cantidad, descuento_esperado):
    # Arrange: el umbral y el porcentaje se pasan explícitos para no depender del entorno
    # Act
    descuento = calcular_descuento(cantidad, cantidad_minima=10, porcentaje=10)
    # Assert
    assert descuento == descuento_esperado


def test_el_umbral_y_el_porcentaje_son_parametrizables():
    # Arrange: otro depósito, con descuento del 15 % a partir de 50 unidades
    # Act
    con_descuento = calcular_descuento(50, cantidad_minima=50, porcentaje=15)
    sin_descuento = calcular_descuento(49, cantidad_minima=50, porcentaje=15)
    # Assert
    assert con_descuento == 15
    assert sin_descuento == 0


def test_total_con_descuento_redondea_a_dos_decimales():
    # Arrange: 3 unidades a $33,333 con 10 % → 89.9991, que NO puede llegar así a un remito
    # Act
    total = calcular_total(precio_unitario=33.333, cantidad=3, descuento=10)
    # Assert
    assert total == 90.0


def test_nueve_unidades_cuestan_lo_mismo_que_diez_en_el_borde():
    """El caso que salió de probar la regla en el TP2: no es un bug, es lo que la regla dice."""
    # Arrange
    precio = 1800
    # Act
    total_nueve = calcular_total(precio, 9, calcular_descuento(9, 10, 10))
    total_diez = calcular_total(precio, 10, calcular_descuento(10, 10, 10))
    # Assert
    assert total_nueve == total_diez == 16200.0
