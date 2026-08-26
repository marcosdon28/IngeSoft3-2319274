import { estaBajoStock, formatearPrecio } from '../lib/reglas.js'

export default function Dashboard({ productos, categorias, movimientos }) {
  const bajos = productos.filter(estaBajoStock)
  const valorizado = productos.reduce((acc, p) => acc + p.precio * p.stock, 0)

  return (
    <>
      <div className="tarjetas">
        <div className="tarjeta">
          <div className="rotulo">Productos</div>
          <div className="valor">{productos.length}</div>
        </div>
        <div className="tarjeta">
          <div className="rotulo">Categorías</div>
          <div className="valor">{categorias.length}</div>
        </div>
        <div className="tarjeta">
          <div className="rotulo">Bajo stock</div>
          <div className="valor" style={{ color: bajos.length ? 'var(--alerta)' : 'var(--ok)' }}>
            {bajos.length}
          </div>
        </div>
        <div className="tarjeta">
          <div className="rotulo">Stock valorizado</div>
          <div className="valor" style={{ fontSize: 21 }}>{formatearPrecio(valorizado)}</div>
        </div>
      </div>

      <div className="panel" style={{ marginTop: 20 }}>
        <h2>Productos por reponer</h2>
        {bajos.length === 0
          ? <p className="vacio">Ningún producto está en o por debajo de su stock mínimo.</p>
          : (
            <table>
              <thead>
                <tr><th>SKU</th><th>Producto</th><th className="num">Stock</th><th className="num">Mínimo</th></tr>
              </thead>
              <tbody>
                {bajos.map((p) => (
                  <tr key={p.id}>
                    <td>{p.sku}</td>
                    <td>{p.nombre}</td>
                    <td className="num"><span className="chip bajo">{p.stock}</span></td>
                    <td className="num">{p.stock_minimo}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
      </div>

      <div className="panel">
        <h2>Últimos movimientos</h2>
        {movimientos.length === 0
          ? <p className="vacio">Todavía no se registró ningún movimiento.</p>
          : (
            <table>
              <thead>
                <tr><th>Producto</th><th>Tipo</th><th className="num">Cantidad</th><th className="num">Total</th></tr>
              </thead>
              <tbody>
                {movimientos.slice(0, 5).map((m) => (
                  <tr key={m.id}>
                    <td>{m.producto_nombre}</td>
                    <td><span className={`chip ${m.tipo.toLowerCase()}`}>{m.tipo}</span></td>
                    <td className="num">{m.cantidad}</td>
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
