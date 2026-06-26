import { createStore } from 'vuex'
import parkingApi from '../api/parkingApi'

export default createStore({
  state: {
    isAuthenticated: false,
    user: null,
    token: localStorage.getItem('token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
    theme: localStorage.getItem('theme') || 'dark'
  },
  getters: {
    isAuthenticated: state => state.isAuthenticated,
    user: state => state.user,
    token: state => state.token,
    refreshToken: state => state.refreshToken,
    theme: state => state.theme
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
    },
    setRefreshToken(state, refreshToken) {
      state.refreshToken = refreshToken
      if (refreshToken) {
        localStorage.setItem('refresh_token', refreshToken)
      } else {
        localStorage.removeItem('refresh_token')
      }
    },
    setTheme(state, theme) {
      state.theme = theme
      localStorage.setItem('theme', theme)
      document.documentElement.setAttribute('data-theme', theme)
    }
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const result = await parkingApi.login(credentials.username, credentials.password)
        
        if (result.success) {
          const data = result.data || result
          commit('setAuth', true)
          commit('setUser', data.user)
          commit('setToken', data.access_token)
          commit('setRefreshToken', data.refresh_token)
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
      commit('setRefreshToken', null)
    },
    
    checkAuth({ commit, state }) {
      if (state.token) {
        commit('setAuth', true)
      }
    },
    toggleTheme({ commit, state }) {
      const newTheme = state.theme === 'light' ? 'dark' : 'light'
      commit('setTheme', newTheme)
    },
    initTheme({ commit, state }) {
      document.documentElement.setAttribute('data-theme', state.theme)
    }
  }
})
