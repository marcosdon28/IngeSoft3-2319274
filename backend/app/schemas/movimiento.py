from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.movimiento import TipoMovimiento


class MovimientoCrear(BaseModel):
    producto_id: int
    tipo: TipoMovimiento
    # Regla 4: la cantidad de un movimiento debe ser mayor a cero.
    cantidad: int = Field(gt=0)


class MovimientoLeer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    producto_id: int
    producto_nombre: str | None = None
    tipo: TipoMovimiento
    cantidad: int
    total: float
    descuento_aplicado: float
    fecha: datetime
