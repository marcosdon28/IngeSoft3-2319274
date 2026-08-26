"""Reglas de negocio de categorías."""
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Categoria, Producto
from app.services.errores import NoEncontradoError, ReglaDeNegocioError


def listar(db: Session) -> list[dict]:
    filas = db.execute(
        select(Categoria, func.count(Producto.id))
        .outerjoin(Producto, Producto.categoria_id == Categoria.id)
        .group_by(Categoria.id)
        .order_by(Categoria.nombre)
    ).all()
    return [
        {"id": c.id, "nombre": c.nombre, "cantidad_productos": n}
        for c, n in filas
    ]


def crear(db: Session, nombre: str) -> Categoria:
    nombre = nombre.strip()
    existente = db.scalar(select(Categoria).where(func.lower(Categoria.nombre) == nombre.lower()))
    if existente:
        raise ReglaDeNegocioError(f"Ya existe una categoría llamada '{nombre}'.")

    categoria = Categoria(nombre=nombre)
    db.add(categoria)
    db.commit()
    return categoria


def eliminar(db: Session, categoria_id: int) -> None:
    """REGLA 3 — No se puede eliminar una categoría que tenga productos asociados.

    Sin esta regla quedarían productos apuntando a una categoría inexistente. La
    alternativa (borrar en cascada) destruiría datos sin avisar: preferimos
    frenar y que la decisión la tome una persona.
    """
    categoria = db.get(Categoria, categoria_id)
    if categoria is None:
        raise NoEncontradoError("La categoría no existe.")

    cantidad = db.scalar(
        select(func.count(Producto.id)).where(Producto.categoria_id == categoria_id)
    )
    if cantidad:
        raise ReglaDeNegocioError(
            f"No se puede eliminar la categoría '{categoria.nombre}': "
            f"tiene {cantidad} producto(s) asociado(s)."
        )

    db.delete(categoria)
    db.commit()
