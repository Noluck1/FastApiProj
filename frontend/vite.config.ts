import { fileURLToPath, URL } from 'node:url'

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import vueDevTools from 'vite-plugin-vue-devtools'

const normalizeBasePath = (value?: string) => {
  const normalized = value?.trim()

  if (!normalized || normalized === '/') {
    return '/'
  }

  const trimmed = normalized.replace(/^\/+|\/+$/g, '')

  return `/${trimmed}/`
}

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const configuredDevPort = env.VITE_DEV_PORT ? Number(env.VITE_DEV_PORT) : undefined
  const devPort = configuredDevPort && Number.isFinite(configuredDevPort) ? configuredDevPort : 8002

  return {
    base: normalizeBasePath(env.VITE_BASE_PATH),
    plugins: [vue(), tailwindcss(), vueDevTools()],
    server: {
      ...(env.VITE_DEV_HOST ? { host: env.VITE_DEV_HOST } : {}),
      port: devPort,
      strictPort: true,
      proxy: {
        '/auth': {
          target: 'http://localhost:8001',
          changeOrigin: true,
        },
        '/books': {
          target: 'http://localhost:8010',
          changeOrigin: true,
        },
        '/favorite': {
          target: 'http://localhost:8010',
          changeOrigin: true,
        },
      },
    },
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
  }
})
