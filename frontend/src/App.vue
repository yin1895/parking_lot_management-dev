<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>停车场管理系统</h1>
          <el-menu
            :default-active="activeIndex"
            class="nav-menu"
            mode="horizontal"
            router
            @select="handleSelect"
          >
            <el-menu-item index="/">首页</el-menu-item>
            <el-menu-item index="/management">管理</el-menu-item>
            <el-menu-item index="/about">关于</el-menu-item>
          </el-menu>
          <div class="user-actions">
            <template v-if="isAuthenticated">
              <span class="welcome-msg">欢迎, {{ username }}</span>
              <el-button size="small" type="danger" @click="handleLogout">登出</el-button>
            </template>
            <template v-else>
              <el-button size="small" type="primary" @click="goToLogin">登录</el-button>
            </template>
          </div>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
      <el-footer>
        &copy; 2025 停车场管理系统
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus';
import { computed } from 'vue';
import { useStore } from 'vuex';

export default {
  name: 'App',
  data() {
    return {
      activeIndex: '/'
    };
  },
  computed: {
    isAuthenticated() {
      return this.$store.getters.isAuthenticated;
    },
    username() {
      return this.$store.getters.user?.username || '用户';
    }
  },
  mounted() {
    this.activeIndex = this.$route.path;
    // 初始化时检查用户认证状态
    this.$store.dispatch('checkAuth');
  },
  methods: {
    handleSelect(key) {
      this.activeIndex = key;
    },
    goToLogin() {
      this.$router.push('/login');
    },
    handleLogout() {
      this.$store.dispatch('logout');
      ElMessage.success('已成功登出');
      if (this.$route.meta.requiresAuth) {
        this.$router.push('/');
      }
    }
  },
  watch: {
    '$route.path'(newPath) {
      this.activeIndex = newPath;
    }
  }
};
</script>

<style>
#app {
  font-family: 'Microsoft YaHei', sans-serif;
  text-align: center;
  color: #2c3e50;
  margin: 0;
  padding: 0;
  height: 100vh;
}
.el-header {
  background-color: #409EFF;
  color: white;
  padding: 0;
}
.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  padding: 0 20px;
}
.nav-menu {
  background-color: transparent;
  border-bottom: none;
  flex: 1; /* 让菜单占据中间区域 */
}
.el-menu--horizontal .el-menu-item {
  color: white;
  border-bottom: none;
}
.el-menu--horizontal .el-menu-item.is-active {
  color: #ffffff;
  font-weight: bold;
  background-color: rgba(255, 255, 255, 0.2);
}
.el-menu--horizontal .el-menu-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}
.el-footer {
  background-color: #f5f7fa;
  color: #606266;
  padding: 20px 0;
}
.user-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}
.welcome-msg {
  color: white;
  margin-right: 10px;
}
</style>
