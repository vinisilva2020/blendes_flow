import { fileURLToPath, URL } from 'node:url'

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const projectRoot = fileURLToPath(new URL('..', import.meta.url))
  const environment = { ...loadEnv(mode, projectRoot, ''), ...process.env }

  return {
    envDir: projectRoot,
    define: {
      'import.meta.env.VITE_GOOGLE_OAUTH_CLIENT_ID': JSON.stringify(
        environment.GOOGLE_OAUTH_CLIENT_ID ?? '',
      ),
    },
    plugins: [vue(), vueDevTools(), tailwindcss()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
  }
})
