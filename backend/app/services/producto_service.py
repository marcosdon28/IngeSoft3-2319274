"""Reglas de negocio de productos."""
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Categoria, Producto
from app.services.errores import NoEncontradoError, ReglaDeNegocioError


def _a_dict(p: Producto) -> dict:
    return {
        "id": p.id,
        "sku": p.sku,
        "nombre": p.nombre,
        "precio": float(p.precio),
        "stock": p.stock,
        "stock_minimo": p.stock_minimo,
        "activo": p.activo,
        "categoria_id": p.categoria_id,
        "categoria_nombre": p.categoria.nombre if p.categoria else None,
        "bajo_stock": p.bajo_stock,
    }


def listar(db: Session, solo_bajo_stock: bool = False) -> list[dict]:
    productos = db.scalars(select(Producto).order_by(Producto.nombre)).all()
    if solo_bajo_stock:
        productos = [p for p in productos if p.bajo_stock]
    return [_a_dict(p) for p in productos]


def obtener(db: Session, producto_id: int) -> dict:
    producto = db.get(Producto, producto_id)
    if producto is None:
        raise NoEncontradoError("El producto no existe.")
    return _a_dict(producto)


def crear(db: Session, datos) -> dict:
    """REGLA 2 — El SKU es único.

    El SKU identifica el producto en el depósito y en los remitos. Dos productos
    con el mismo SKU hacen imposible saber cuál se movió. La base tiene además un
    UNIQUE, pero acá se valida antes para devolver un mensaje entendible en vez
    de un error de integridad.
    """
    sku = datos.sku.strip().upper()

    if db.scalar(select(Producto).where(func.upper(Producto.sku) == sku)):
        raise ReglaDeNegocioError(f"Ya existe un producto con el SKU '{sku}'.")

    if db.get(Categoria, datos.categoria_id) is None:
        raise NoEncontradoError("La categoría indicada no existe.")

    producto = Producto(
        sku=sku,
        nombre=datos.nombre.strip(),
        precio=datos.precio,
        stock=datos.stock,
        stock_minimo=datos.stock_minimo,
        categoria_id=datos.categoria_id,
        activo=True,
    )
    db.add(producto)
    db.commit()
    return _a_dict(producto)


def actualizar(db: Session, producto_id: int, datos) -> dict:
    producto = db.get(Producto, producto_id)
    if producto is None:
        raise NoEncontradoError("El producto no existe.")

    if datos.nombre is not None:
        producto.nombre = datos.nombre.strip()
    if datos.precio is not None:
        producto.precio = datos.precio
    if datos.stock_minimo is not None:
        producto.stock_minimo = datos.stock_minimo
    if datos.activo is not None:
        producto.activo = datos.activo

    db.commit()
    return _a_dict(producto)
