import './utils/mediaDevicesPolyfill';
import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import store from './store'
import zhCn from 'element-plus/es/locale/lang/zh-cn';
import * as ElementPlusIconsVue from '@element-plus/icons-vue' // 导入所有图标

// 添加全局错误处理，防止ResizeObserver警告在控制台显示
const originalConsoleError = console.error;
console.error = (...args) => {
  if (args[0] && args[0].includes && args[0].includes('ResizeObserver')) {
    return; // 忽略ResizeObserver警告
  }
  originalConsoleError(...args);
};

const app = createApp(App)

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(ElementPlus, {
  locale: zhCn
});
app.use(store)
app.use(router)

app.mount('#app')
