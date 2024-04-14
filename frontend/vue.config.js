const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      "/api": {
        target: "http://127.0.0.1:5000", // 后端接口
        changeOrigin: true, // 是否跨域
        pathRewrite: {
          "/api": "",
        },
      },
    },
  },
});
