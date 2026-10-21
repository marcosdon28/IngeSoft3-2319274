import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    // En desarrollo, /api se proxea al backend local (uvicorn → :8000).
    // En el contenedor, ese mismo rol lo cumple el proxy_pass de nginx.
    // El front NUNCA escribe el host del backend: llama a rutas relativas.
    proxy: { '/api': 'http://localhost:8000' },
  },
  test: {
    coverage: {
      provider: 'v8',
      // json-summary deja coverage-summary.json: es lo que el pipeline lee para el resumen.
      reporter: ['text', 'html', 'lcov', 'json-summary'],
      // Qué ENTRA en la cuenta: la lógica pura (lib/) y el cliente de la API.
      // Quedan afuera los componentes de React (pegamento de UI, se verifican
      // end-to-end en el TP7) y main.jsx (el arranque).
      include: ['src/lib/**', 'src/api.js'],
      // El umbral que FRENA el build: sobre líneas Y ramas (la rama es la más honesta).
      thresholds: { lines: 90, branches: 85 },
    },
  },
})
