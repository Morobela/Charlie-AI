import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const apiTarget = process.env.VITE_API_TARGET || 'http://localhost:8000'
const wsTarget = process.env.VITE_WS_TARGET || 'ws://localhost:8000'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      '/api': apiTarget,
      '/ws': { target: wsTarget, ws: true },
      '/mcp': { target: wsTarget, ws: true },
      '/a2a': apiTarget
    }
  }
})
