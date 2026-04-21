import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

const apiProxyTarget = process.env.VITE_API_PROXY_TARGET || 'http://127.0.0.1:8000'
const apiProxy = {
  '/api': {
    target: apiProxyTarget,
    changeOrigin: true,
  },
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    AutoImport({
      resolvers: [ElementPlusResolver()],
      dts: false,
    }),
    Components({
      resolvers: [ElementPlusResolver()],
      dts: false,
    }),
  ],
  build: {
    chunkSizeWarningLimit: 600,
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (!id.includes('node_modules')) {
            return
          }

          if (id.includes('echarts')) {
            if (id.includes('/echarts/core')) {
              return 'vendor-echarts-core'
            }

            if (id.includes('/echarts/charts')) {
              return 'vendor-echarts-charts'
            }

            if (id.includes('/echarts/components')) {
              return 'vendor-echarts-components'
            }

            if (id.includes('/echarts/renderers')) {
              return 'vendor-echarts-renderers'
            }

            return 'vendor-echarts'
          }

          if (id.includes('@element-plus/icons-vue')) {
            return 'vendor-element-plus-icons'
          }

          if (id.includes('element-plus')) {
            if (id.includes('/components/table') || id.includes('/components/pagination')) {
              return 'vendor-element-plus-table'
            }

            if (id.includes('/components/form') || id.includes('/components/input') || id.includes('/components/select') || id.includes('/components/date-picker')) {
              return 'vendor-element-plus-form'
            }

            if (id.includes('/components/dialog') || id.includes('/components/message') || id.includes('/components/message-box') || id.includes('/components/notification')) {
              return 'vendor-element-plus-feedback'
            }

            return 'vendor-element-plus-core'
          }

          if (id.includes('axios')) {
            return 'vendor-axios'
          }

          if (id.includes('vue-router') || id.includes('pinia') || id.includes('/vue/')) {
            return 'vendor-vue'
          }

          return 'vendor-misc'
        },
      },
    },
  },
  server: {
    proxy: apiProxy,
  },
  preview: {
    proxy: apiProxy,
  },
})
