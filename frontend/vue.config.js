const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: [], 
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  },
  // 禁用保存时的lint检查，提高开发体验
  lintOnSave: false,
  
  // 添加自定义webpack配置来解决Progress Plugin问题
  configureWebpack: {
    plugins: []
  },
  chainWebpack: config => {
    // 移除progress插件以避免配置冲突
    config.plugins.delete('progress');
    
    // 如果需要，可以重新添加一个没有任何选项的progress插件
    // const webpack = require('webpack');
    // config.plugin('progress').use(new webpack.ProgressPlugin());
  }
})
