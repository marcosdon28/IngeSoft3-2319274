// Suite E2E: un navegador real usando la app desplegada en QA, contra su api y
// su base de verdad. Sin mocks, sin page.route: si el navegador no le pega a
// la API, no es end-to-end.
import { expect, test } from '@playwright/test'

const API = process.env.API_BASE_URL || 'http://localhost:8000'

// Datos propios de cada test, con la hora adentro para no chocar con otra corrida.
async function armarProducto(request, marca, { stock, precio = 1000 }) {
  const categoria = await (await request.post(`${API}/api/categorias`, { data: { nombre: `e2e cat ${marca}` } })).json()
  const producto = await (await request.post(`${API}/api/productos`, {
    data: { sku: `E2E-${marca}`, nombre: `e2e prod ${marca}`, precio, stock, categoria_id: categoria.id },
  })).json()
  return { categoria, producto }
}

async function limpiar(request, { categoria, producto }) {
  // Primero los movimientos del producto (anularlos), después el producto, después la categoría.
  const movimientos = await (await request.get(`${API}/api/movimientos`)).json()
  for (const m of movimientos.filter((m) => m.producto_id === producto.id)) {
    expect((await request.delete(`${API}/api/movimientos/${m.id}`)).status()).toBe(204)
  }
  expect((await request.delete(`${API}/api/productos/${producto.id}`)).status()).toBe(204)
  expect((await request.delete(`${API}/api/categorias/${categoria.id}`)).status()).toBe(204)
  const productos = await (await request.get(`${API}/api/productos`)).json()
  expect(productos.some((p) => p.id === producto.id)).toBe(false)   // la limpieza, comprobada
}

test('crear una categoría la muestra en la lista, y borrarla la saca', async ({ page, request }) => {
  const nombre = `e2e ${Date.now()}`
  try {
    await page.goto('/')
    await page.getByRole('button', { name: 'Categorías' }).click()
    await page.getByLabel('Nombre').fill(nombre)
    await page.getByRole('button', { name: 'Agregar' }).click()
    // exact: la celda del botón «Eliminar <nombre>» también contiene el nombre
    await expect(page.getByRole('cell', { name: nombre, exact: true })).toBeVisible()   // el dato que ESTE test creó
    await page.getByRole('button', { name: `Eliminar ${nombre}` }).click()
    await expect(page.getByRole('cell', { name: nombre, exact: true })).toHaveCount(0)  // y el borrado, comprobado
  } finally {
    // Si el test falló a mitad de camino, que no deje basura en QA: borra por API lo que quede.
    const restos = (await (await request.get(`${API}/api/categorias`)).json()).filter((c) => c.nombre === nombre)
    for (const c of restos) await request.delete(`${API}/api/categorias/${c.id}`)
  }
})

test('una salida mayor al stock muestra el motivo, deshabilita el botón y no registra nada', async ({ page, request }) => {
  const marca = Date.now()
  const datos = await armarProducto(request, marca, { stock: 5 })
  try {
    await page.goto('/')
    await page.getByRole('button', { name: 'Movimientos' }).click()
    await page.getByLabel('Producto').selectOption({ label: `e2e prod ${marca} (5 u.)` })
    await page.getByLabel('Tipo').selectOption('SALIDA')
    await page.getByLabel('Cantidad').fill('6')

    await expect(page.getByRole('status')).toHaveText('Stock insuficiente: hay 5 y querés sacar 6.')  // el usuario ve el error…
    await expect(page.getByRole('button', { name: 'Registrar' })).toBeDisabled()
    await expect(page.getByRole('cell', { name: `e2e prod ${marca}` })).toHaveCount(0)             // …y en el historial no apareció nada
    const movimientos = await (await request.get(`${API}/api/movimientos`)).json()
    expect(movimientos.some((m) => m.producto_id === datos.producto.id)).toBe(false)              // ni en la base
  } finally {
    await limpiar(request, datos)
  }
})

test('el flujo de todos los días: registrar una salida con descuento y verla en el historial', async ({ page, request }) => {
  const marca = Date.now()
  const datos = await armarProducto(request, marca, { stock: 20, precio: 1000 })
  try {
    await page.goto('/')
    await page.getByRole('button', { name: 'Movimientos' }).click()
    await page.getByLabel('Producto').selectOption({ label: `e2e prod ${marca} (20 u.)` })
    await page.getByLabel('Tipo').selectOption('SALIDA')
    await page.getByLabel('Cantidad').fill('10')                                   // el borde: con 10 ya hay descuento
    await expect(page.getByText('10% de descuento por cantidad')).toBeVisible()  // regla 5 en vivo, antes de confirmar
    await page.getByRole('button', { name: 'Registrar' }).click()

    const fila = page.getByRole('row', { name: new RegExp(`e2e prod ${marca}`) })
    await expect(fila).toBeVisible()
    await expect(fila).toContainText('SALIDA')
    await expect(fila).toContainText('10%')                                      // el descuento que la api calculó
    await expect(fila).toContainText('9.000,00')                                 // 10 × 1000 − 10 %

    const leido = await (await request.get(`${API}/api/productos/${datos.producto.id}`)).json()
    expect(leido.stock).toBe(10)                                                 // y el stock bajó en la base
  } finally {
    await limpiar(request, datos)
  }
})
