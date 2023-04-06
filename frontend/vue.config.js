const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: [
    'vuetify'
  ],
  devServer: {
    proxy: 'http://127.0.0.1:3000',
    host: 'localhost'
  },
  assetsDir: "static" // for flask static folder
})
