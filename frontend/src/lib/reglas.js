// Reglas del frontend: funciones PURAS, sin React ni fetch adentro.
// Están separadas a propósito — son las que el TP5 va a testear con Vitest.

export const DESCUENTO_CANTIDAD_MINIMA = 10
export const DESCUENTO_PORCENTAJE = 10

/** Regla 6 (vista): un producto está en bajo stock cuando stock <= stock_minimo. */
export function estaBajoStock(producto) {
  if (!producto) return false
  return producto.stock <= producto.stock_minimo
}

/**
 * Regla 5 (vista): el total que ve el usuario ANTES de confirmar la salida.
 * Replica el cálculo del backend para poder mostrarlo en vivo; el backend
 * sigue siendo la fuente de verdad y vuelve a calcularlo al guardar.
 */
export function calcularTotal(precio, cantidad) {
  const p = Number(precio) || 0
  const c = Number(cantidad) || 0
  const descuento = c >= DESCUENTO_CANTIDAD_MINIMA ? DESCUENTO_PORCENTAJE : 0
  const bruto = p * c
  return {
    descuento,
    bruto: Math.round(bruto * 100) / 100,
    total: Math.round(bruto * (1 - descuento / 100) * 100) / 100,
  }
}

/**
 * Reglas 1, 4 y 7 (vista): por qué el botón de registrar movimiento está
 * deshabilitado. Devuelve null si el movimiento es válido, o el motivo.
 * Es validación de UX, no de seguridad: el backend valida igual.
 */
export function motivoMovimientoInvalido({ producto, tipo, cantidad }) {
  if (!producto) return 'Elegí un producto.'
  if (!producto.activo) return `"${producto.nombre}" está inactivo: no admite movimientos.`
  const c = Number(cantidad)
  if (!Number.isInteger(c) || c <= 0) return 'La cantidad tiene que ser un entero mayor a cero.'
  if (tipo === 'SALIDA' && c > producto.stock) {
    return `Stock insuficiente: hay ${producto.stock} y querés sacar ${c}.`
  }
  return null
}

/** Formatea un importe en pesos, para que el formato viva en un solo lugar. */
export function formatearPrecio(valor) {
  return new Intl.NumberFormat('es-AR', {
    style: 'currency', currency: 'ARS', minimumFractionDigits: 2,
  }).format(Number(valor) || 0)
}

/**
 * Prioridad de reposición de un producto en bajo stock, para ordenar la lista
 * del tablero. Mira cuánto falta para el mínimo y cuántas unidades salieron
 * en los últimos movimientos: un producto que se vende y ya no tiene stock es
 * más urgente que uno quieto.
 *   - 'sin-stock'     : no queda nada
 *   - 'urgente'       : menos de la mitad del mínimo y con salidas recientes
 *   - 'pronto'        : menos de la mitad del mínimo sin salidas, o en el mínimo con salidas
 *   - 'puede-esperar' : en o por debajo del mínimo, pero nadie lo está pidiendo
 *   - 'normal'        : por encima del mínimo (no hace falta reponer)
 */
export function prioridadDeReposicion(producto, movimientos = []) {
  if (!producto) return 'normal'
  if (producto.stock <= 0) return 'sin-stock'
  if (!estaBajoStock(producto)) return 'normal'

  const salidas = movimientos
    .filter((m) => m.producto_id === producto.id && m.tipo === 'SALIDA')
    .reduce((acc, m) => acc + m.cantidad, 0)
  const mitadDelMinimo = producto.stock_minimo / 2

  if (producto.stock < mitadDelMinimo) return salidas > 0 ? 'urgente' : 'pronto'
  return salidas > 0 ? 'pronto' : 'puede-esperar'
}

const ORDEN_PRIORIDAD = ['sin-stock', 'urgente', 'pronto', 'puede-esperar', 'normal']

/**
 * Ordena los productos por reponer: primero los más urgentes y, a igual
 * prioridad, por nombre. Devuelve pares { producto, prioridad } listos para
 * la tabla del tablero.
 */
export function ordenarPorPrioridad(productos, movimientos = []) {
  return productos
    .map((producto) => ({ producto, prioridad: prioridadDeReposicion(producto, movimientos) }))
    .sort((a, b) => (
      ORDEN_PRIORIDAD.indexOf(a.prioridad) - ORDEN_PRIORIDAD.indexOf(b.prioridad)
      || a.producto.nombre.localeCompare(b.producto.nombre)
    ))
}
