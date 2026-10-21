// Todas las llamadas usan RUTA RELATIVA (/api/...): el frontend no sabe dónde
// vive el backend. En dev lo resuelve el proxy de Vite; en el contenedor, nginx.
// Gracias a eso la misma imagen sirve en cualquier entorno y no hay CORS.
//
// El cliente HTTP ENTRA DESDE AFUERA (TP5): `crearApi` recibe la función que
// hace el pedido. La app real le pasa el `fetch` del navegador; los tests le
// pasan un doble (`vi.fn()`) y así se prueba la traducción de respuestas y de
// errores sin salir a la red.
export function crearApi(fetchImpl = (...args) => fetch(...args)) {
  async function pedir(url, opciones = {}) {
    const res = await fetchImpl(url, {
      headers: { 'Content-Type': 'application/json' },
      ...opciones,
    })
    if (res.status === 204) return null
    const cuerpo = await res.json().catch(() => null)
    if (!res.ok) {
      throw new Error(cuerpo?.detail ?? `Error ${res.status}`)
    }
    return cuerpo
  }

  return {
    categorias: {
      listar: () => pedir('/api/categorias'),
      crear: (nombre) => pedir('/api/categorias', { method: 'POST', body: JSON.stringify({ nombre }) }),
      eliminar: (id) => pedir(`/api/categorias/${id}`, { method: 'DELETE' }),
    },
    productos: {
      listar: (bajoStock = false) => pedir(`/api/productos${bajoStock ? '?bajo_stock=true' : ''}`),
      crear: (datos) => pedir('/api/productos', { method: 'POST', body: JSON.stringify(datos) }),
      actualizar: (id, datos) => pedir(`/api/productos/${id}`, { method: 'PATCH', body: JSON.stringify(datos) }),
    },
    movimientos: {
      listar: () => pedir('/api/movimientos'),
      registrar: (datos) => pedir('/api/movimientos', { method: 'POST', body: JSON.stringify(datos) }),
    },
  }
}

// El cliente que usa la app: con el fetch real del navegador.
export const api = crearApi()
