import { useState } from 'react'
import { api } from '../api.js'
import { calcularTotal, formatearPrecio, motivoMovimientoInvalido } from '../lib/reglas.js'

export default function Movimientos({ productos, movimientos, recargar, setError }) {
  const [productoId, setProductoId] = useState('')
  const [tipo, setTipo] = useState('ENTRADA')
  const [cantidad, setCantidad] = useState('')

  const producto = productos.find((p) => String(p.id) === String(productoId)) || null

  // Reglas 1, 4 y 7 en la vista: el botón dice POR QUÉ no se puede.
  const motivo = motivoMovimientoInvalido({ producto, tipo, cantidad })

  // Regla 5 en la vista: el total se recalcula mientras escribís.
  const calculo = producto ? calcularTotal(producto.precio, cantidad) : null

  async function registrar(e) {
    e.preventDefault()
    try {
      await api.movimientos.registrar({
        producto_id: Number(productoId), tipo, cantidad: Number(cantidad),
      })
      setCantidad(''); setError(null); recargar()
    } catch (err) { setError(err.message) }
  }

  return (
    <>
      <div className="panel">
        <h2>Registrar movimiento</h2>
        {productos.length === 0
          ? <p className="aviso">Cargá al menos un producto para poder registrar movimientos.</p>
          : (
            <>
              <form className="fila" onSubmit={registrar}>
                <label>
                  Producto
                  <select value={productoId} onChange={(e) => setProductoId(e.target.value)} required>
                    <option value="">Elegir…</option>
                    {productos.map((p) => (
                      <option key={p.id} value={p.id}>
                        {p.nombre} ({p.stock} u.){p.activo ? '' : ' — inactivo'}
                      </option>
                    ))}
                  </select>
                </label>
                <label>
                  Tipo
                  <select value={tipo} onChange={(e) => setTipo(e.target.value)}>
                    <option value="ENTRADA">Entrada</option>
                    <option value="SALIDA">Salida</option>
                  </select>
                </label>
                <label>
                  Cantidad
                  <input type="number" min="1" value={cantidad}
                         onChange={(e) => setCantidad(e.target.value)} style={{ width: 110 }} required />
                </label>
                <button className="accion" type="submit" disabled={motivo !== null}>Registrar</button>
              </form>

              {motivo && <p className="aviso" style={{ marginTop: 12 }}>{motivo}</p>}

              {!motivo && calculo && tipo === 'SALIDA' && (
                <p style={{ marginTop: 12, fontSize: 14 }}>
                  Total: <strong>{formatearPrecio(calculo.total)}</strong>
                  {calculo.descuento > 0 && (
                    <> — {calculo.descuento}% de descuento por cantidad
                      (antes {formatearPrecio(calculo.bruto)})</>
                  )}
                </p>
              )}
            </>
          )}
      </div>

      <div className="panel">
        <h2>Historial</h2>
        {movimientos.length === 0
          ? <p className="vacio">Todavía no se registró ningún movimiento.</p>
          : (
            <table>
              <thead>
                <tr>
                  <th>Fecha</th><th>Producto</th><th>Tipo</th>
                  <th className="num">Cantidad</th><th className="num">Descuento</th><th className="num">Total</th>
                </tr>
              </thead>
              <tbody>
                {movimientos.map((m) => (
                  <tr key={m.id}>
                    <td>{new Date(m.fecha).toLocaleString('es-AR')}</td>
                    <td>{m.producto_nombre}</td>
                    <td><span className={`chip ${m.tipo.toLowerCase()}`}>{m.tipo}</span></td>
                    <td className="num">{m.cantidad}</td>
                    <td className="num">{m.descuento_aplicado > 0 ? `${m.descuento_aplicado}%` : '—'}</td>
                    <td className="num">{formatearPrecio(m.total)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
      </div>
    </>
  )
}
