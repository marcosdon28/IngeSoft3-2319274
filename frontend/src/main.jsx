import React from 'react'
import ReactDOM from 'react-dom/client'
import * as Sentry from '@sentry/react'
import App from './App.jsx'

// Observabilidad del front (TP9). El DSN va escrito acá y no es un descuido: el
// DSN de un front sólo sirve para ENVIAR eventos, no para leerlos, y viaja en el
// JavaScript que baja cualquier navegador. No es una clave de API.
Sentry.init({
  dsn: 'https://0583fa25071a8867cadb0a987a1b64cb@o4512295556349952.ingest.us.sentry.io/4512295590363136',
  environment: window.location.hostname,   // de qué sitio vino: QA, producción o localhost
  integrations: [Sentry.browserTracingIntegration()],
  tracesSampleRate: 1.0,
})
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
