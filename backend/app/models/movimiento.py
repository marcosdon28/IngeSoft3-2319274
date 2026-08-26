import enum
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class TipoMovimiento(str, enum.Enum):
    ENTRADA = "ENTRADA"
    SALIDA = "SALIDA"


class Movimiento(Base):
    __tablename__ = "movimientos"

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[TipoMovimiento] = mapped_column(
        Enum(TipoMovimiento, name="tipo_movimiento"), nullable=False
    )
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)

    # Se guarda el total ya calculado: el precio del producto puede cambiar
    # después, y el movimiento tiene que seguir contando lo que pasó ese día.
    total: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    descuento_aplicado: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False, default=0)

    fecha: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    producto_id: Mapped[int] = mapped_column(ForeignKey("productos.id"), nullable=False)
    producto: Mapped["Producto"] = relationship()  # noqa: F821
