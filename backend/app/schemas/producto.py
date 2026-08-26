from pydantic import BaseModel, ConfigDict, Field


class ProductoCrear(BaseModel):
    # Regla 4: precio y stock no pueden ser negativos. La validación de tipo y de
    # rango la hace Pydantic acá; las reglas que necesitan mirar la BASE viven en
    # los services.
    sku: str = Field(min_length=2, max_length=40)
    nombre: str = Field(min_length=2, max_length=120)
    precio: float = Field(ge=0)
    stock: int = Field(ge=0, default=0)
    stock_minimo: int = Field(ge=0, default=0)
    categoria_id: int


class ProductoActualizar(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=120)
    precio: float | None = Field(default=None, ge=0)
    stock_minimo: int | None = Field(default=None, ge=0)
    activo: bool | None = None


class ProductoLeer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sku: str
    nombre: str
    precio: float
    stock: int
    stock_minimo: int
    activo: bool
    categoria_id: int
    categoria_nombre: str | None = None
    bajo_stock: bool
