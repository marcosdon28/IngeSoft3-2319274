from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Producto(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    precio: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    stock_minimo: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"), nullable=False)
    categoria: Mapped["Categoria"] = relationship(back_populates="productos")  # noqa: F821

    @property
    def bajo_stock(self) -> bool:
        """Regla 6: un producto está en bajo stock cuando stock <= stock_minimo.

        Es una propiedad derivada, no una columna: no puede quedar desincronizada
        del stock real porque se calcula cada vez que se lee.
        """
        return self.stock <= self.stock_minimo
