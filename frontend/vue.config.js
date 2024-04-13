const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  assetsSubDirectory:'static',
  assetsPublicPath:'/',
  proxyTable:{
    'api':{
      target:'http://localhost:8080',
      changeOrigin:true,
      pathRewrite:{
        '^/api':''
      }
    }
  },
  transpileDependencies: true
})
