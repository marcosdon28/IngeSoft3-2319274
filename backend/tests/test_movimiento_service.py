"""REGLAS 1 y 7 — registrar un movimiento, con la base reemplazada por un DOBLE.

`db` es un Mock(spec=Session): `db.get` contesta lo que el test le diga (stub) y
después el test mira QUÉ le pidieron a la base (mock): si la regla frenó, no
tiene que haber ni `add` ni `commit`; si el movimiento es válido, exactamente uno.
"""
import pytest

from app.models import Movimiento, TipoMovimiento
from app.schemas.movimiento import MovimientoCrear
from app.services import movimiento_service
from app.services.errores import NoEncontradoError, ReglaDeNegocioError


def test_una_salida_mayor_al_stock_es_rechazada_y_no_toca_la_base(db, producto):
    # Arrange: hay 10 unidades y se intentan sacar 11
    db.get.return_value = producto
    datos = MovimientoCrear(producto_id=1, tipo=TipoMovimiento.SALIDA, cantidad=11)

    # Act
    with pytest.raises(ReglaDeNegocioError) as info:
        movimiento_service.registrar(db, datos)

    # Assert: el mensaje explica cuánto hay y cuánto se pidió, y la base quedó intacta
    assert "hay 10 unidades" in info.value.mensaje
    assert "sacar 11" in info.value.mensaje
    db.add.assert_not_called()
    db.commit.assert_not_called()
    assert producto.stock == 10


def test_una_salida_igual_al_stock_se_permite_y_deja_el_stock_en_cero(db, producto):
    # Arrange: borde de la regla 1 — sacar EXACTAMENTE lo que hay no es "superar"
    db.get.return_value = producto
    datos = MovimientoCrear(producto_id=1, tipo=TipoMovimiento.SALIDA, cantidad=10)

    # Act
    resultado = movimiento_service.registrar(db, datos)

    # Assert
    assert producto.stock == 0
    assert resultado["cantidad"] == 10
    assert resultado["descuento_aplicado"] == 10.0   # y además, 10 unidades → descuento (regla 5)


def test_un_producto_inactivo_no_admite_movimientos(db, producto):
    # Arrange: dado de baja
    producto.activo = False
    db.get.return_value = producto
    datos = MovimientoCrear(producto_id=1, tipo=TipoMovimiento.ENTRADA, cantidad=1)

    # Act / Assert
    with pytest.raises(ReglaDeNegocioError, match="inactivo"):
        movimiento_service.registrar(db, datos)
    db.commit.assert_not_called()


def test_un_producto_inexistente_devuelve_no_encontrado(db):
    # Arrange: la base no tiene ese id
    db.get.return_value = None
    datos = MovimientoCrear(producto_id=999, tipo=TipoMovimiento.ENTRADA, cantidad=1)

    # Act / Assert
    with pytest.raises(NoEncontradoError):
        movimiento_service.registrar(db, datos)


def test_una_entrada_valida_persiste_un_movimiento_una_sola_vez(db, producto):
    """El test con MOCK: no mira el valor devuelto, mira la INTERACCIÓN con la base."""
    # Arrange
    db.get.return_value = producto
    datos = MovimientoCrear(producto_id=1, tipo=TipoMovimiento.ENTRADA, cantidad=5)

    # Act
    movimiento_service.registrar(db, datos)

    # Assert: se agregó exactamente UN Movimiento, con los datos correctos, y se commiteó una vez.
    # Si mañana alguien duplica el add por error, este test se pone rojo.
    db.add.assert_called_once()
    guardado = db.add.call_args.args[0]
    assert isinstance(guardado, Movimiento)
    assert guardado.cantidad == 5
    assert guardado.tipo == TipoMovimiento.ENTRADA
    assert guardado.descuento_aplicado == 0.0     # una entrada nunca lleva descuento
    db.commit.assert_called_once()
    assert producto.stock == 15


def _con_movimiento(db, producto, tipo, cantidad):
    """El doble contesta el movimiento y después el producto, en ese orden (dos db.get)."""
    movimiento = Movimiento(id=7, producto_id=producto.id, tipo=tipo, cantidad=cantidad,
                            total=0, descuento_aplicado=0)
    db.get.side_effect = [movimiento, producto]
    return movimiento


def test_anular_una_salida_devuelve_las_unidades_al_stock(db, producto):
    # Arrange: stock 10, una salida de 4 registrada
    movimiento = _con_movimiento(db, producto, TipoMovimiento.SALIDA, 4)

    # Act
    movimiento_service.anular(db, 7)

    # Assert: el stock vuelve, el movimiento se borra, un solo commit
    assert producto.stock == 14
    db.delete.assert_called_once_with(movimiento)
    db.commit.assert_called_once()


def test_anular_una_entrada_resta_lo_que_habia_sumado(db, producto):
    _con_movimiento(db, producto, TipoMovimiento.ENTRADA, 4)

    movimiento_service.anular(db, 7)

    assert producto.stock == 6


def test_no_se_anula_una_entrada_cuyas_unidades_ya_salieron(db, producto):
    # Arrange: stock 10, pero la entrada fue de 25: deshacerla dejaría -15 (regla 1)
    _con_movimiento(db, producto, TipoMovimiento.ENTRADA, 25)

    with pytest.raises(ReglaDeNegocioError, match="quedarían -15"):
        movimiento_service.anular(db, 7)
    db.delete.assert_not_called()
    assert producto.stock == 10


def test_anular_un_movimiento_inexistente_devuelve_no_encontrado(db):
    db.get.return_value = None
    with pytest.raises(NoEncontradoError):
        movimiento_service.anular(db, 99)
