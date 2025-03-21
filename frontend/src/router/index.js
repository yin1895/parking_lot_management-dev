import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import store from '../store'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/About.vue')
  },
  {
    path: '/management',
    name: 'management',
    component: () => import('../views/Management.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// 简单的路由守卫，保护需要认证的页面
router.beforeEach((to, from, next) => {
  // 检查用户认证状态
  store.dispatch('checkAuth')
  
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 如果路由需要认证，检查是否已登录
    if (!store.getters.isAuthenticated) {
      // 未登录，重定向到登录页
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      // 已登录，允许访问
      next()
    }
  } else {
    // 不需要认证的路由，直接放行
    next()
  }
})

export default router
