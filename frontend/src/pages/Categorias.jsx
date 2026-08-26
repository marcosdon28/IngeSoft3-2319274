import { useState } from 'react'
import { api } from '../api.js'

export default function Categorias({ categorias, recargar, setError }) {
  const [nombre, setNombre] = useState('')

  async function crear(e) {
    e.preventDefault()
    try {
      await api.categorias.crear(nombre.trim())
      setNombre(''); setError(null); recargar()
    } catch (err) { setError(err.message) }
  }

  async function eliminar(id) {
    try {
      await api.categorias.eliminar(id)
      setError(null); recargar()
    } catch (err) { setError(err.message) }
  }

  return (
    <>
      <div className="panel">
        <h2>Nueva categoría</h2>
        <form className="fila" onSubmit={crear}>
          <label>
            Nombre
            <input value={nombre} onChange={(e) => setNombre(e.target.value)}
                   placeholder="Bebidas" minLength={2} required />
          </label>
          <button className="accion" type="submit" disabled={nombre.trim().length < 2}>Agregar</button>
        </form>
      </div>

      <div className="panel">
        <h2>Categorías</h2>
        {categorias.length === 0
          ? <p className="vacio">Todavía no hay categorías. Creá una para poder cargar productos.</p>
          : (
            <table>
              <thead>
                <tr><th>Nombre</th><th className="num">Productos</th><th></th></tr>
              </thead>
              <tbody>
                {categorias.map((c) => (
                  <tr key={c.id}>
                    <td>{c.nombre}</td>
                    <td className="num">{c.cantidad_productos}</td>
                    <td style={{ textAlign: 'right' }}>
                      {/* Regla 3: con productos asociados no se puede borrar.
                          El botón se deshabilita acá, y el backend lo rechaza igual. */}
                      <button className="link" onClick={() => eliminar(c.id)}
                              disabled={c.cantidad_productos > 0}
                              title={c.cantidad_productos > 0
                                ? 'Tiene productos asociados: no se puede eliminar'
                                : 'Eliminar categoría'}
                              style={c.cantidad_productos > 0 ? { color: 'var(--suave)', cursor: 'not-allowed' } : {}}>
                        Eliminar
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
