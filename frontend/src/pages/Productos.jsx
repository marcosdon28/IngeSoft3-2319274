import { useState } from 'react'
import { api } from '../api.js'
import { estaBajoStock, formatearPrecio } from '../lib/reglas.js'

const VACIO = { sku: '', nombre: '', precio: '', stock: '', stock_minimo: '', categoria_id: '' }

export default function Productos({ productos, categorias, recargar, setError }) {
  const [f, setF] = useState(VACIO)

  const set = (campo) => (e) => setF({ ...f, [campo]: e.target.value })

  const completo = f.sku.trim().length >= 2 && f.nombre.trim().length >= 2 &&
                   f.precio !== '' && Number(f.precio) >= 0 && f.categoria_id !== ''

  async function crear(e) {
    e.preventDefault()
    try {
      await api.productos.crear({
        sku: f.sku.trim(),
        nombre: f.nombre.trim(),
        precio: Number(f.precio),
        stock: Number(f.stock || 0),
        stock_minimo: Number(f.stock_minimo || 0),
        categoria_id: Number(f.categoria_id),
      })
      setF(VACIO); setError(null); recargar()
    } catch (err) { setError(err.message) }
  }

  async function alternarActivo(p) {
    try {
      await api.productos.actualizar(p.id, { activo: !p.activo })
      setError(null); recargar()
    } catch (err) { setError(err.message) }
  }

  return (
    <>
      <div className="panel">
        <h2>Nuevo producto</h2>
        {categorias.length === 0
          ? <p className="aviso">Primero creá una categoría: un producto siempre pertenece a una.</p>
          : (
            <form className="fila" onSubmit={crear}>
              <label>SKU<input value={f.sku} onChange={set('sku')} placeholder="BEB-001" required /></label>
              <label>Nombre<input value={f.nombre} onChange={set('nombre')} placeholder="Gaseosa 1.5L" required /></label>
              <label>Precio<input type="number" min="0" step="0.01" value={f.precio} onChange={set('precio')} required style={{ width: 110 }} /></label>
              <label>Stock inicial<input type="number" min="0" value={f.stock} onChange={set('stock')} placeholder="0" style={{ width: 100 }} /></label>
              <label>Stock mínimo<input type="number" min="0" value={f.stock_minimo} onChange={set('stock_minimo')} placeholder="0" style={{ width: 105 }} /></label>
              <label>
                Categoría
                <select value={f.categoria_id} onChange={set('categoria_id')} required>
                  <option value="">Elegir…</option>
                  {categorias.map((c) => <option key={c.id} value={c.id}>{c.nombre}</option>)}
                </select>
              </label>
              <button className="accion" type="submit" disabled={!completo}>Agregar</button>
            </form>
          )}
      </div>

      <div className="panel">
        <h2>Productos</h2>
        {productos.length === 0
          ? <p className="vacio">Todavía no hay productos cargados.</p>
          : (
            <table>
              <thead>
                <tr>
                  <th>SKU</th><th>Producto</th><th>Categoría</th>
                  <th className="num">Precio</th><th className="num">Stock</th>
                  <th>Estado</th><th></th>
                </tr>
              </thead>
              <tbody>
                {productos.map((p) => (
                  <tr key={p.id}>
                    <td>{p.sku}</td>
                    <td>{p.nombre}</td>
                    <td>{p.categoria_nombre}</td>
                    <td className="num">{formatearPrecio(p.precio)}</td>
                    <td className="num">
                      {/* Regla 6: bajo stock cuando stock <= stock_minimo */}
                      <span className={`chip ${estaBajoStock(p) ? 'bajo' : 'ok'}`}>{p.stock}</span>
                    </td>
                    <td>{p.activo ? '—' : <span className="chip inactivo">inactivo</span>}</td>
                    <td style={{ textAlign: 'right' }}>
                      <button className="link" style={{ color: 'var(--acento)' }}
                              onClick={() => alternarActivo(p)}>
                        {p.activo ? 'Dar de baja' : 'Reactivar'}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
      </div>
    </>
  )
}
