import { createStore } from 'vuex'

export default createStore({
  state: {
    isAuthenticated: false,
    user: null
  },
  getters: {
    isAuthenticated: state => state.isAuthenticated,
    user: state => state.user
  },
  mutations: {
    setAuth(state, auth) {
      state.isAuthenticated = auth
    },
    setUser(state, user) {
      state.user = user
    }
  },
  actions: {
    login({ commit }, userData) {
      // 实际项目中，这里会调用API
      commit('setAuth', true)
      commit('setUser', userData)
    },
    logout({ commit }) {
      commit('setAuth', false)
      commit('setUser', null)
    }
  }
})
