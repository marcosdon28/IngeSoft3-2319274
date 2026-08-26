import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    // En desarrollo, /api se proxea al backend local (uvicorn → :8000).
    // En el contenedor, ese mismo rol lo cumple el proxy_pass de nginx.
    // El front NUNCA escribe el host del backend: llama a rutas relativas.
    proxy: { '/api': 'http://localhost:8000' },
  },
})
