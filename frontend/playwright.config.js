import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',                // los DOS archivos; cada job del pipeline corre el suyo por nombre
  timeout: 60_000,                 // tope de CADA test: generoso para las e2e, de sobra para la api
  expect: { timeout: 15_000 },     // tope de CADA aserción (el default es 5 s)
  use: {
    // El FRONT. La api tiene la suya: API_BASE_URL, que leen los specs.
    baseURL: process.env.E2E_BASE_URL || 'http://localhost:3000',
    // Tope de CADA acción (click, fill, selectOption). Sin esto una acción espera hasta
    // el tope del test entero (60 s), el test muere por timeout y el `finally` que
    // limpia QA no llega a correr: lo vi en la corrida roja 39644611792, que dejó
    // dos categorías y dos productos «e2e …» en la base de QA.
    actionTimeout: 15_000,
    trace: 'on-first-retry',         // la traza se graba en el retry de un fallo
    screenshot: 'only-on-failure',
  },
  retries: 1,                      // absorbe una demora suelta; si pasa recién ahí, sale «flaky»
  reporter: [['html', { open: 'never' }], ['list']],
})
