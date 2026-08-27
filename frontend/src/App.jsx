import { useCallback, useEffect, useState } from 'react'
import { api } from './api.js'
import Dashboard from './pages/Dashboard.jsx'
import Productos from './pages/Productos.jsx'
import Categorias from './pages/Categorias.jsx'
import Movimientos from './pages/Movimientos.jsx'

// Orden de las pestañas: el resumen primero, que es lo que más se mira.
const PESTANAS = [
  ['dashboard', 'Resumen'],
  ['productos', 'Productos'],
  ['categorias', 'Categorías'],
  ['movimientos', 'Movimientos'],
]

export default function App() {
  const [pestana, setPestana] = useState('dashboard')
  const [productos, setProductos] = useState([])
  const [categorias, setCategorias] = useState([])
  const [movimientos, setMovimientos] = useState([])
  const [error, setError] = useState(null)

  const recargar = useCallback(async () => {
    try {
      const [p, c, m] = await Promise.all([
        api.productos.listar(), api.categorias.listar(), api.movimientos.listar(),
      ])
      setProductos(p); setCategorias(c); setMovimientos(m); setError(null)
    } catch (e) {
      setError(e.message)
    }
  }, [])

  useEffect(() => { recargar() }, [recargar])

  const comun = { productos, categorias, movimientos, recargar, setError }

  return (
    <>
      <header>
        <h1>Inventario</h1>
        <p>Ingeniería del Software 3 · UCC 2026 · app del semestre</p>
        <nav>
          {PESTANAS.map(([id, rotulo]) => (
            <button key={id} className={pestana === id ? 'activa' : ''} onClick={() => setPestana(id)}>
              {rotulo}
            </button>
          ))}
        </nav>
      </header>
      <main>
        {error && <div className="error">{error}</div>}
        {pestana === 'dashboard' && <Dashboard {...comun} />}
        {pestana === 'productos' && <Productos {...comun} />}
        {pestana === 'categorias' && <Categorias {...comun} />}
        {pestana === 'movimientos' && <Movimientos {...comun} />}
      </main>
    </>
  )
}
