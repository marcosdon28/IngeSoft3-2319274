"""Sesión y engine de SQLAlchemy — la infraestructura de la capa Model."""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    """Base declarativa de la que heredan todos los modelos."""


def get_db():
    """Dependencia de FastAPI: abre una sesión por request y la cierra siempre."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
