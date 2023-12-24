import Components from 'unplugin-vue-components/vite'
import { DevUiResolver } from 'unplugin-vue-components/resolvers'
export default defineConfig({
  plugins: [
    vue(),
    // 新增
    Components({
      resolvers: [
        DevUiResolver()
      ]
    })
  ]
})