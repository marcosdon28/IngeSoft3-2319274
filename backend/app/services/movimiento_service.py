"""Reglas de negocio de los movimientos de stock.

Acá viven las reglas más interesantes del dominio, y son las que el TP5 va a
testear: son funciones puras sobre datos, sin HTTP en el medio.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import DESCUENTO_CANTIDAD_MINIMA, DESCUENTO_PORCENTAJE
from app.models import Movimiento, Producto, TipoMovimiento
from app.services.errores import NoEncontradoError, ReglaDeNegocioError


def calcular_descuento(cantidad: int, cantidad_minima: int = DESCUENTO_CANTIDAD_MINIMA,
                       porcentaje: float = DESCUENTO_PORCENTAJE) -> float:
    """REGLA 5 — Descuento por cantidad.

    A partir de `cantidad_minima` unidades la salida aplica `porcentaje` %. El
    borde es INCLUSIVO: con exactamente el mínimo ya corresponde el descuento.
    Función pura: se testea sin base de datos ni API.
    """
    if cantidad >= cantidad_minima:
        return porcentaje
    return 0.0


def calcular_total(precio_unitario: float, cantidad: int, descuento: float) -> float:
    """Total de un movimiento, con el descuento ya aplicado. Redondea a 2 decimales."""
    bruto = precio_unitario * cantidad
    return round(bruto * (1 - descuento / 100), 2)


def listar(db: Session) -> list[dict]:
    movimientos = db.scalars(
        select(Movimiento).order_by(Movimiento.fecha.desc(), Movimiento.id.desc())
    ).all()
    return [
        {
            "id": m.id,
            "producto_id": m.producto_id,
            "producto_nombre": m.producto.nombre if m.producto else None,
            "tipo": m.tipo,
            "cantidad": m.cantidad,
            "total": float(m.total),
            "descuento_aplicado": float(m.descuento_aplicado),
            "fecha": m.fecha,
        }
        for m in movimientos
    ]


def registrar(db: Session, datos) -> dict:
    producto = db.get(Producto, datos.producto_id)
    if producto is None:
        raise NoEncontradoError("El producto no existe.")

    # REGLA 7 — Un producto inactivo no admite nuevos movimientos.
    # Dar de baja un producto tiene que significar algo: si igual se le pueden
    # cargar movimientos, la baja es decorativa.
    if not producto.activo:
        raise ReglaDeNegocioError(
            f"El producto '{producto.nombre}' está inactivo: no admite movimientos."
        )

    # REGLA 1 — Una salida no puede superar el stock disponible.
    # Es la regla central del dominio: el stock nunca puede quedar negativo,
    # porque representa unidades físicas en un depósito.
    if datos.tipo == TipoMovimiento.SALIDA and datos.cantidad > producto.stock:
        raise ReglaDeNegocioError(
            f"Stock insuficiente: hay {producto.stock} unidades de "
            f"'{producto.nombre}' y se intentan sacar {datos.cantidad}."
        )

    # REGLA 5 — el descuento sólo tiene sentido en una salida (una venta).
    descuento = (
        calcular_descuento(datos.cantidad)
        if datos.tipo == TipoMovimiento.SALIDA
        else 0.0
    )
    total = calcular_total(float(producto.precio), datos.cantidad, descuento)

    if datos.tipo == TipoMovimiento.ENTRADA:
        producto.stock += datos.cantidad
    else:
        producto.stock -= datos.cantidad

    movimiento = Movimiento(
        producto_id=producto.id,
        tipo=datos.tipo,
        cantidad=datos.cantidad,
        total=total,
        descuento_aplicado=descuento,
    )
    db.add(movimiento)
    db.commit()

    return {
        "id": movimiento.id,
        "producto_id": producto.id,
        "producto_nombre": producto.nombre,
        "tipo": movimiento.tipo,
        "cantidad": movimiento.cantidad,
        "total": float(movimiento.total),
        "descuento_aplicado": float(movimiento.descuento_aplicado),
        "fecha": movimiento.fecha,
    }
