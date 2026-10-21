// Suite de INTEGRACIÓN (amplia): le habla a la api de QA ya desplegada, con su
// base de verdad detrás. Sin navegador (fixture `request`) y sin dobles.
import { expect, test } from '@playwright/test'

// La api tiene su propia dirección: NO es la del front. Sin barra al final.
const API = process.env.API_BASE_URL || 'http://localhost:8000'

async function listar(request, recurso) {
  const r = await request.get(`${API}/api/${recurso}`)
  expect(r.status()).toBe(200)
  return r.json()
}

test('el alta de una categoría guarda en la base de verdad, y el borrado la saca', async ({ request }) => {
  const nombre = `api ${Date.now()}`                      // único: no choca con otra corrida
  const alta = await request.post(`${API}/api/categorias`, { data: { nombre } })
  expect(alta.status()).toBe(201)                         // la api dice «creada»
  const creada = await alta.json()

  const lista = await listar(request, 'categorias')       // y la BASE la devuelve: no es un doble
  expect(lista.some((c) => c.nombre === nombre)).toBe(true)

  const borrado = await request.delete(`${API}/api/categorias/${creada.id}`)
  expect(borrado.status()).toBe(204)

  const despues = await listar(request, 'categorias')     // y el borrado, comprobado
  expect(despues.some((c) => c.nombre === nombre)).toBe(false)
})

test('una categoría con nombre vacío la rechaza la api, y no crea nada', async ({ request }) => {
  const antes = await listar(request, 'categorias')

  const alta = await request.post(`${API}/api/categorias`, { data: { nombre: '' } })
  expect(alta.status()).toBe(422)                         // el contrato del error: validación de entrada

  const despues = await listar(request, 'categorias')
  expect(despues.length).toBe(antes.length)               // y de verdad no se creó nada
})

test('la regla 1 se cumple contra la base: una salida mayor al stock no mueve nada', async ({ request }) => {
  // Arrange: una categoría y un producto propios, con nombres que no se repiten
  const marca = Date.now()
  const categoria = await (await request.post(`${API}/api/categorias`, { data: { nombre: `api cat ${marca}` } })).json()
  const alta = await request.post(`${API}/api/productos`, {
    data: { sku: `API-${marca}`, nombre: `api prod ${marca}`, precio: 100, stock: 5, categoria_id: categoria.id },
  })
  expect(alta.status()).toBe(201)
  const producto = await alta.json()

  // Act: sacar 6 habiendo 5
  const salida = await request.post(`${API}/api/movimientos`, {
    data: { producto_id: producto.id, tipo: 'SALIDA', cantidad: 6 },
  })

  // Assert: 400 con el motivo, y el stock en la base sigue en 5
  expect(salida.status()).toBe(400)
  expect((await salida.json()).detail).toContain('Stock insuficiente')
  const leido = await (await request.get(`${API}/api/productos/${producto.id}`)).json()
  expect(leido.stock).toBe(5)

  // Limpieza, comprobada: QA es uno solo y lo comparten todas las corridas
  expect((await request.delete(`${API}/api/productos/${producto.id}`)).status()).toBe(204)
  expect((await request.delete(`${API}/api/categorias/${categoria.id}`)).status()).toBe(204)
  expect((await listar(request, 'productos')).some((p) => p.id === producto.id)).toBe(false)
})
