import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // IMPORTANT: listen on all interfaces so it's accessible from host
    port: 5173,
    watch: {
      usePolling: true, // Better file watching in Docker
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true
  }
})