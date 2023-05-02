const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: [
    'vuetify'
  ],
  devServer: {
    proxy: {
      '^/': {
        target: 'http://127.0.0.1:3000',
        host: 'localhost',
        ws: false
      },
      
    }
  },
  assetsDir: "static" // for flask static folder
})
