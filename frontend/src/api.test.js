import { describe, expect, it, vi } from 'vitest'
import { crearApi } from './api.js'

// Fabrica una respuesta mínima con la forma que `pedir` necesita de un fetch.
const respuesta = ({ status = 200, ok = status < 400, cuerpo = null, sinJson = false } = {}) => ({
  status, ok,
  json: sinJson ? () => Promise.reject(new Error('sin cuerpo')) : () => Promise.resolve(cuerpo),
})

describe('crearApi — el cliente HTTP entra desde afuera', () => {
  it('listar productos devuelve lo que contestó la API', async () => {
    // Arrange: el doble actúa como STUB — sólo contesta
    const fetchImpl = vi.fn().mockResolvedValue(respuesta({ cuerpo: [{ id: 1, sku: 'BEB-001' }] }))
    const api = crearApi(fetchImpl)
    // Act
    const productos = await api.productos.listar()
    // Assert
    expect(productos).toEqual([{ id: 1, sku: 'BEB-001' }])
  })

  it('listar sólo bajo stock le pide a la API la ruta con el filtro', async () => {
    // Arrange: acá el doble actúa como MOCK — el assert mira la INTERACCIÓN
    const fetchImpl = vi.fn().mockResolvedValue(respuesta({ cuerpo: [] }))
    const api = crearApi(fetchImpl)
    // Act
    await api.productos.listar(true)
    // Assert: qué URL se pidió y cuántas veces. Si alguien cambia la ruta sin querer, se pone rojo.
    expect(fetchImpl).toHaveBeenCalledTimes(1)
    expect(fetchImpl).toHaveBeenCalledWith('/api/productos?bajo_stock=true', expect.objectContaining({
      headers: { 'Content-Type': 'application/json' },
    }))
  })

  it('registrar un movimiento manda un POST con el cuerpo en JSON', async () => {
    const fetchImpl = vi.fn().mockResolvedValue(respuesta({ status: 201, cuerpo: { id: 7 } }))
    const api = crearApi(fetchImpl)

    const creado = await api.movimientos.registrar({ producto_id: 1, tipo: 'SALIDA', cantidad: 10 })

    expect(creado).toEqual({ id: 7 })
    const [url, opciones] = fetchImpl.mock.calls[0]
    expect(url).toBe('/api/movimientos')
    expect(opciones.method).toBe('POST')
    expect(JSON.parse(opciones.body)).toEqual({ producto_id: 1, tipo: 'SALIDA', cantidad: 10 })
  })

  // Caso de ERROR: el mensaje que ve el usuario sale del `detail` del backend.
  it('un 400 se convierte en un Error con el motivo que mandó el backend', async () => {
    const fetchImpl = vi.fn().mockResolvedValue(respuesta({
      status: 400, cuerpo: { detail: 'Stock insuficiente: hay 10 unidades.' },
    }))
    const api = crearApi(fetchImpl)

    await expect(api.movimientos.registrar({})).rejects.toThrow('Stock insuficiente: hay 10 unidades.')
  })

  it('un error sin cuerpo JSON se informa con el código de estado', async () => {
    const fetchImpl = vi.fn().mockResolvedValue(respuesta({ status: 502, sinJson: true }))
    const api = crearApi(fetchImpl)

    await expect(api.categorias.listar()).rejects.toThrow('Error 502')
  })

  it('un 204 (eliminar) devuelve null sin intentar leer un cuerpo', async () => {
    const fetchImpl = vi.fn().mockResolvedValue(respuesta({ status: 204, sinJson: true }))
    const api = crearApi(fetchImpl)

    expect(await api.categorias.eliminar(3)).toBeNull()
    expect(fetchImpl).toHaveBeenCalledWith('/api/categorias/3', expect.objectContaining({ method: 'DELETE' }))
  })
})
