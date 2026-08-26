from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.movimiento import MovimientoCrear, MovimientoLeer
from app.services import movimiento_service
from app.services.errores import NoEncontradoError, ReglaDeNegocioError

router = APIRouter(prefix="/api/movimientos", tags=["movimientos"])


@router.get("", response_model=list[MovimientoLeer])
def listar(db: Session = Depends(get_db)):
    return movimiento_service.listar(db)


@router.post("", response_model=MovimientoLeer, status_code=status.HTTP_201_CREATED)
def registrar(datos: MovimientoCrear, db: Session = Depends(get_db)):
    try:
        return movimiento_service.registrar(db, datos)
    except NoEncontradoError as e:
        raise HTTPException(status_code=404, detail=e.mensaje)
    except ReglaDeNegocioError as e:
        raise HTTPException(status_code=400, detail=e.mensaje)
