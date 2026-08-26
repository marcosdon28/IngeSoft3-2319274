from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.producto import ProductoActualizar, ProductoCrear, ProductoLeer
from app.services import producto_service
from app.services.errores import NoEncontradoError, ReglaDeNegocioError

router = APIRouter(prefix="/api/productos", tags=["productos"])


@router.get("", response_model=list[ProductoLeer])
def listar(bajo_stock: bool = False, db: Session = Depends(get_db)):
    return producto_service.listar(db, solo_bajo_stock=bajo_stock)


@router.get("/{producto_id}", response_model=ProductoLeer)
def obtener(producto_id: int, db: Session = Depends(get_db)):
    try:
        return producto_service.obtener(db, producto_id)
    except NoEncontradoError as e:
        raise HTTPException(status_code=404, detail=e.mensaje)


@router.post("", response_model=ProductoLeer, status_code=status.HTTP_201_CREATED)
def crear(datos: ProductoCrear, db: Session = Depends(get_db)):
    try:
        return producto_service.crear(db, datos)
    except NoEncontradoError as e:
        raise HTTPException(status_code=404, detail=e.mensaje)
    except ReglaDeNegocioError as e:
        raise HTTPException(status_code=400, detail=e.mensaje)


@router.patch("/{producto_id}", response_model=ProductoLeer)
def actualizar(producto_id: int, datos: ProductoActualizar, db: Session = Depends(get_db)):
    try:
        return producto_service.actualizar(db, producto_id, datos)
    except NoEncontradoError as e:
        raise HTTPException(status_code=404, detail=e.mensaje)
