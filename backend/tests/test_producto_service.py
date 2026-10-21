"""REGLA 2 — El SKU es único."""
import pytest

from app.schemas.producto import ProductoCrear
from app.services import producto_service
from app.services.errores import NoEncontradoError, ReglaDeNegocioError


def test_un_sku_repetido_es_rechazado_sin_insertar(db, producto):
    # Arrange: la base ya tiene un producto con ese SKU (en minúscula: la regla no distingue)
    db.scalar.return_value = producto
    datos = ProductoCrear(sku="beb-001", nombre="Otra gaseosa", precio=100, categoria_id=1)

    # Act
    with pytest.raises(ReglaDeNegocioError) as info:
        producto_service.crear(db, datos)

    # Assert: el mensaje nombra el SKU normalizado, y no hubo add ni commit
    assert "BEB-001" in info.value.mensaje
    db.add.assert_not_called()
    db.commit.assert_not_called()


def test_un_sku_nuevo_con_categoria_inexistente_devuelve_no_encontrado(db):
    # Arrange: no hay SKU repetido, pero la categoría 42 no existe
    db.scalar.return_value = None
    db.get.return_value = None
    datos = ProductoCrear(sku="NEW-1", nombre="Nuevo", precio=100, categoria_id=42)

    # Act / Assert
    with pytest.raises(NoEncontradoError):
        producto_service.crear(db, datos)
    db.add.assert_not_called()


def test_un_producto_nuevo_se_guarda_con_el_sku_en_mayusculas(db, categoria):
    # Arrange
    db.scalar.return_value = None
    db.get.return_value = categoria
    datos = ProductoCrear(sku=" new-1 ", nombre="  Nuevo  ", precio=100, stock=3, categoria_id=1)

    # Act
    producto_service.crear(db, datos)

    # Assert: lo que llegó a la base está normalizado
    guardado = db.add.call_args.args[0]
    assert guardado.sku == "NEW-1"
    assert guardado.nombre == "Nuevo"
    assert guardado.activo is True
    db.commit.assert_called_once()


def test_listar_solo_bajo_stock_filtra_por_la_regla_6(db, producto, categoria):
    # Arrange: dos productos, uno en bajo stock (3 <= 6) y otro no (10 > 4)
    from app.models import Producto
    escaso = Producto(id=2, sku="LIM-001", nombre="Detergente", precio=2400, stock=3,
                      stock_minimo=6, activo=True, categoria_id=1, categoria=categoria)
    db.scalars.return_value.all.return_value = [producto, escaso]

    # Act
    todos = producto_service.listar(db)
    reponer = producto_service.listar(db, solo_bajo_stock=True)

    # Assert
    assert [p["sku"] for p in todos] == ["BEB-001", "LIM-001"]
    assert [p["sku"] for p in reponer] == ["LIM-001"]
    assert reponer[0]["bajo_stock"] is True


def test_dar_de_baja_un_producto_lo_deja_inactivo_sin_tocar_lo_demas(db, producto):
    # Arrange: un PATCH que sólo trae `activo` y un nombre nuevo
    from app.schemas.producto import ProductoActualizar
    db.get.return_value = producto
    datos = ProductoActualizar(nombre="Gaseosa 1.5L (baja)", activo=False)

    # Act
    resultado = producto_service.actualizar(db, 1, datos)

    # Assert: cambió lo pedido, el precio y el mínimo quedaron como estaban
    assert resultado["activo"] is False
    assert resultado["nombre"] == "Gaseosa 1.5L (baja)"
    assert resultado["precio"] == 1800.0
    assert producto.stock_minimo == 4
    db.commit.assert_called_once()


def test_obtener_un_producto_inexistente_devuelve_no_encontrado(db):
    db.get.return_value = None
    with pytest.raises(NoEncontradoError):
        producto_service.obtener(db, 404)
