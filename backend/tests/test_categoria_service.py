"""REGLA 3 — No se elimina una categoría con productos asociados."""
import pytest

from app.services import categoria_service
from app.services.errores import NoEncontradoError, ReglaDeNegocioError


def test_una_categoria_con_productos_no_se_puede_eliminar(db, categoria):
    # Arrange: existe, y la cuenta de productos asociados da 2
    db.get.return_value = categoria
    db.scalar.return_value = 2

    # Act
    with pytest.raises(ReglaDeNegocioError) as info:
        categoria_service.eliminar(db, 1)

    # Assert: el mensaje dice cuántos, y no se borró nada
    assert "2 producto(s)" in info.value.mensaje
    db.delete.assert_not_called()
    db.commit.assert_not_called()


def test_una_categoria_vacia_se_elimina(db, categoria):
    # Arrange: existe y no tiene productos
    db.get.return_value = categoria
    db.scalar.return_value = 0

    # Act
    categoria_service.eliminar(db, 1)

    # Assert
    db.delete.assert_called_once_with(categoria)
    db.commit.assert_called_once()


def test_eliminar_una_categoria_inexistente_devuelve_no_encontrado(db):
    db.get.return_value = None
    with pytest.raises(NoEncontradoError):
        categoria_service.eliminar(db, 99)


def test_un_nombre_de_categoria_repetido_es_rechazado_sin_distinguir_mayusculas(db, categoria):
    # Arrange: ya existe "Bebidas"; se intenta crear "  bebidas "
    db.scalar.return_value = categoria

    # Act / Assert
    with pytest.raises(ReglaDeNegocioError, match="Ya existe una categoría"):
        categoria_service.crear(db, "  bebidas ")
    db.add.assert_not_called()


def test_una_categoria_nueva_se_guarda_con_el_nombre_recortado(db):
    # Arrange
    db.scalar.return_value = None

    # Act
    creada = categoria_service.crear(db, "  Limpieza  ")

    # Assert
    assert creada.nombre == "Limpieza"
    db.add.assert_called_once_with(creada)
    db.commit.assert_called_once()
