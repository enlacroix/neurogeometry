const {defineConfig} = require('@vue/cli-service')
module.exports = defineConfig({
  css: {
    loaderOptions: {
      sass: {
        additionalData: `@import "@/assets/_variables.sass"`
      }
    }
  },
  transpileDependencies: true,
  publicPath: process.env.NODE_ENV === 'production' ? '/../static' : '/',
  outputDir: process.env.NODE_ENV === 'production' ? '../static' : 'dist/',
  indexPath: process.env.NODE_ENV === 'production' ? '../templates/_base_vue.html' : 'index.html',
  configureWebpack: {
    devServer: {
      devMiddleware: {
        writeToDisk: true
      }
    }
  }
});

// const {defineConfig} = require('@vue/cli-service')
// module.exports = defineConfig({
//   css: {
//     loaderOptions: {
//       sass: {
//         additionalData: `@import "@/assets/_variables.sass"`
//       }
//     }
//   },
//   transpileDependencies: true,
// });

