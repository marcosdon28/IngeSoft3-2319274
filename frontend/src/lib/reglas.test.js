import { describe, expect, it } from 'vitest'
import {
  calcularTotal, estaBajoStock, formatearPrecio, motivoMovimientoInvalido,
} from './reglas.js'

describe('calcularTotal — regla 5, el descuento por cantidad', () => {
  // Parametrizado: el mismo comportamiento con varios datos, uno por fila.
  it.each([
    [9, 0, 16200],      // una unidad ANTES del umbral: sin descuento
    [10, 10, 16200],    // el umbral es INCLUSIVO: con 10 ya hay 10 %
    [11, 10, 17820],    // por encima del umbral
    [1, 0, 1800],
  ])('con %i unidades aplica %i %% y el total es %i', (cantidad, descuento, total) => {
    const resultado = calcularTotal(1800, cantidad)
    expect(resultado.descuento).toBe(descuento)
    expect(resultado.total).toBe(total)
  })

  it('con una cantidad que no es número el total es cero, no NaN', () => {
    // Caso de borde: el input vacío del formulario llega como '' antes de escribir
    expect(calcularTotal(1800, '')).toEqual({ descuento: 0, bruto: 0, total: 0 })
  })

  it('redondea a dos decimales', () => {
    expect(calcularTotal(33.333, 3).total).toBe(100)   // 99.999 → 100
  })
})

describe('estaBajoStock — regla 6', () => {
  it.each([
    [{ stock: 3, stock_minimo: 6 }, true],
    [{ stock: 6, stock_minimo: 6 }, true],     // igual al mínimo ya es bajo stock
    [{ stock: 7, stock_minimo: 6 }, false],
  ])('%o → %s', (producto, esperado) => {
    expect(estaBajoStock(producto)).toBe(esperado)
  })

  it('sin producto no está en bajo stock', () => {
    expect(estaBajoStock(null)).toBe(false)
  })
})

describe('motivoMovimientoInvalido — reglas 1, 4 y 7 en la vista', () => {
  const activo = { nombre: 'Gaseosa', activo: true, stock: 10 }

  // Casos de ERROR: cada regla tiene que explicar POR QUÉ no se puede.
  it('sin producto elegido pide elegir uno', () => {
    expect(motivoMovimientoInvalido({ producto: null, tipo: 'ENTRADA', cantidad: 1 }))
      .toBe('Elegí un producto.')
  })

  it('un producto inactivo no admite movimientos (regla 7)', () => {
    const motivo = motivoMovimientoInvalido({ producto: { ...activo, activo: false }, tipo: 'ENTRADA', cantidad: 1 })
    expect(motivo).toContain('"Gaseosa" está inactivo')
  })

  it.each([
    ['cero', 0], ['negativa', -3], ['decimal', 1.5], ['vacía', ''],
  ])('una cantidad %s es rechazada (regla 4)', (_caso, cantidad) => {
    expect(motivoMovimientoInvalido({ producto: activo, tipo: 'ENTRADA', cantidad }))
      .toBe('La cantidad tiene que ser un entero mayor a cero.')
  })

  it('una salida mayor al stock dice cuánto hay y cuánto se quiere sacar (regla 1)', () => {
    expect(motivoMovimientoInvalido({ producto: activo, tipo: 'SALIDA', cantidad: 11 }))
      .toBe('Stock insuficiente: hay 10 y querés sacar 11.')
  })

  it('una salida igual al stock es válida: el borde no es "superar"', () => {
    expect(motivoMovimientoInvalido({ producto: activo, tipo: 'SALIDA', cantidad: 10 })).toBeNull()
  })

  it('una entrada mayor al stock es válida: la regla 1 es sólo para salidas', () => {
    expect(motivoMovimientoInvalido({ producto: activo, tipo: 'ENTRADA', cantidad: 500 })).toBeNull()
  })
})

describe('formatearPrecio', () => {
  it('formatea en pesos argentinos con dos decimales', () => {
    expect(formatearPrecio(1800)).toMatch(/1\.800,00/)
  })
  it('un valor no numérico se muestra como cero', () => {
    expect(formatearPrecio('abc')).toMatch(/0,00/)
  })
})
