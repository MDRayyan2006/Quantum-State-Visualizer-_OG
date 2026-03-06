import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'
import { fileURLToPath, URL } from 'node:url'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    port: 3000,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8003',  // All APIs including chat on main backend
        changeOrigin: true,
        secure: false,
      },
      '/dash': {
        target: 'http://localhost:8003',  // Dash on main backend
        changeOrigin: true,
        secure: false,
      },
    },
  },
})