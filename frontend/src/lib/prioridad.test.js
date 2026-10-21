import { describe, expect, it } from 'vitest'
import { ordenarPorPrioridad, prioridadDeReposicion } from './reglas.js'

// Un test por camino que la función declara: cinco salidas, cinco entradas que las recorren.
describe('prioridadDeReposicion', () => {
  const salidaDe = (producto_id, cantidad) => ({ producto_id, tipo: 'SALIDA', cantidad })
  const entradaDe = (producto_id, cantidad) => ({ producto_id, tipo: 'ENTRADA', cantidad })

  it('sin producto es normal', () => {
    expect(prioridadDeReposicion(null)).toBe('normal')
  })

  it('con stock cero es sin-stock, haya o no movimientos', () => {
    expect(prioridadDeReposicion({ id: 1, stock: 0, stock_minimo: 6 })).toBe('sin-stock')
  })

  it('por encima del mínimo es normal aunque tenga salidas', () => {
    expect(prioridadDeReposicion({ id: 1, stock: 20, stock_minimo: 6 }, [salidaDe(1, 5)])).toBe('normal')
  })

  it('con menos de la mitad del mínimo y salidas recientes es urgente', () => {
    // mínimo 10 → mitad 5; stock 2; una salida de ese producto
    expect(prioridadDeReposicion({ id: 1, stock: 2, stock_minimo: 10 }, [salidaDe(1, 3)])).toBe('urgente')
  })

  it('con menos de la mitad del mínimo pero sin salidas es pronto', () => {
    // las ENTRADAS y las salidas de OTRO producto no cuentan
    const movimientos = [entradaDe(1, 3), salidaDe(2, 9)]
    expect(prioridadDeReposicion({ id: 1, stock: 2, stock_minimo: 10 }, movimientos)).toBe('pronto')
  })

  it('en el mínimo con salidas es pronto', () => {
    expect(prioridadDeReposicion({ id: 1, stock: 6, stock_minimo: 6 }, [salidaDe(1, 1)])).toBe('pronto')
  })

  it('en el mínimo sin salidas puede esperar', () => {
    expect(prioridadDeReposicion({ id: 1, stock: 6, stock_minimo: 6 }, [])).toBe('puede-esperar')
  })

  it('exactamente la mitad del mínimo NO es "menos de la mitad" (borde)', () => {
    // mínimo 10 → mitad 5; stock 5 con salidas: pronto, no urgente
    expect(prioridadDeReposicion({ id: 1, stock: 5, stock_minimo: 10 }, [salidaDe(1, 1)])).toBe('pronto')
  })
})

describe('ordenarPorPrioridad', () => {
  it('pone primero lo más urgente y desempata por nombre', () => {
    const productos = [
      { id: 1, nombre: 'Yerba', stock: 6, stock_minimo: 6 },        // puede-esperar
      { id: 2, nombre: 'Gaseosa', stock: 0, stock_minimo: 10 },     // sin-stock
      { id: 3, nombre: 'Detergente', stock: 1, stock_minimo: 10 },  // urgente
      { id: 4, nombre: 'Agua', stock: 1, stock_minimo: 10 },        // urgente, antes por nombre
    ]
    const movimientos = [{ producto_id: 3, tipo: 'SALIDA', cantidad: 2 }, { producto_id: 4, tipo: 'SALIDA', cantidad: 2 }]

    const orden = ordenarPorPrioridad(productos, movimientos)

    expect(orden.map((o) => `${o.producto.nombre}:${o.prioridad}`)).toEqual([
      'Gaseosa:sin-stock', 'Agua:urgente', 'Detergente:urgente', 'Yerba:puede-esperar',
    ])
  })

  it('no modifica la lista original', () => {
    const productos = [{ id: 1, nombre: 'B', stock: 0, stock_minimo: 1 }, { id: 2, nombre: 'A', stock: 0, stock_minimo: 1 }]
    ordenarPorPrioridad(productos)
    expect(productos.map((p) => p.nombre)).toEqual(['B', 'A'])
  })
})
