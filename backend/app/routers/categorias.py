from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.categoria import CategoriaCrear, CategoriaLeer
from app.services import categoria_service
from app.services.errores import NoEncontradoError, ReglaDeNegocioError

router = APIRouter(prefix="/api/categorias", tags=["categorias"])


@router.get("", response_model=list[CategoriaLeer])
def listar(db: Session = Depends(get_db)):
    return categoria_service.listar(db)


@router.post("", response_model=CategoriaLeer, status_code=status.HTTP_201_CREATED)
def crear(datos: CategoriaCrear, db: Session = Depends(get_db)):
    try:
        categoria = categoria_service.crear(db, datos.nombre)
    except ReglaDeNegocioError as e:
        raise HTTPException(status_code=400, detail=e.mensaje)
    return {"id": categoria.id, "nombre": categoria.nombre, "cantidad_productos": 0}


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(categoria_id: int, db: Session = Depends(get_db)):
    try:
        categoria_service.eliminar(db, categoria_id)
    except NoEncontradoError as e:
        raise HTTPException(status_code=404, detail=e.mensaje)
    except ReglaDeNegocioError as e:
        raise HTTPException(status_code=400, detail=e.mensaje)
