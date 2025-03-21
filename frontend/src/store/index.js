import { createStore } from 'vuex'
import parkingApi from '../api/parkingApi'

export default createStore({
  state: {
    isAuthenticated: false,
    user: null,
    token: localStorage.getItem('token') || null
  },
  getters: {
    isAuthenticated: state => state.isAuthenticated,
    user: state => state.user,
    token: state => state.token
  },
  mutations: {
    setAuth(state, auth) {
      state.isAuthenticated = auth
    },
    setUser(state, user) {
      state.user = user
    },
    setToken(state, token) {
      state.token = token
      if (token) {
        localStorage.setItem('token', token)
      } else {
        localStorage.removeItem('token')
      }
    }
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const result = await parkingApi.login(credentials.username, credentials.password)
        
        if (result.success) {
          commit('setAuth', true)
          commit('setUser', result.user)
          commit('setToken', result.token)
          return { success: true }
        } else {
          return { success: false, message: result.message }
        }
      } catch (error) {
        console.error('登录失败:', error)
        return { success: false, message: error.message }
      }
    },
    
    logout({ commit }) {
      commit('setAuth', false)
      commit('setUser', null)
      commit('setToken', null)
    },
    
    // 检查用户是否已登录（从localStorage恢复会话）
    checkAuth({ commit, state }) {
      if (state.token) {
        // 如果有token，尝试恢复登录状态
        commit('setAuth', true)
        // 这里可以添加验证token有效性的请求
      }
    }
  }
})
