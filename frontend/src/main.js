import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import store from './store'
import zhCn from 'element-plus/es/locale/lang/zh-cn';

const app = createApp(App)

app.use(ElementPlus, {
  locale: zhCn
});
app.use(store)
app.use(router)

app.mount('#app')
