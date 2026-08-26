from pydantic import BaseModel, ConfigDict, Field


class CategoriaCrear(BaseModel):
    nombre: str = Field(min_length=2, max_length=80)


class CategoriaLeer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    cantidad_productos: int = 0
