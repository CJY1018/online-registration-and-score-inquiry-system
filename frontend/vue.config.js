const {defineConfig} = require('@vue/cli-service')
const AutoImport = require('unplugin-auto-import/webpack')
const Components = require('unplugin-vue-components/webpack')
const {ElementPlusResolver} = require('unplugin-vue-components/resolvers')

module.exports = defineConfig({
    transpileDependencies: true,
    // 打包路径
    // publicPath: './',
    // 导入element-plus
    configureWebpack: {
        plugins: [
            AutoImport({
                resolvers: [ElementPlusResolver()],
            }),
            Components({
                resolvers: [ElementPlusResolver()],
            }),
        ],
    },
    // 解决跨域问题
    devServer: {
        proxy: {
            '/api': {
                target: 'https://api.zjzw.cn/',
                changeOrigin: true,
                pathRewrite: {
                    '^/api': ''
                }
            },
            '/static-data': {
                target: 'https://static-data.gaokao.cn/',
                changeOrigin: true,
                pathRewrite: {
                    '^/static-data': ''
                }
            }
        }
    }
})
