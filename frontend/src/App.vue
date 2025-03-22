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
            <!-- 添加主题切换按钮 -->
            <el-button
              size="small"
              :icon="isDarkTheme ? 'SunnyBeach' : 'Moon'"
              circle
              @click="toggleTheme"
              class="theme-toggle"
            ></el-button>
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
import { Moon, SunnyBeach } from '@element-plus/icons-vue';
import { computed } from 'vue';
import { useStore } from 'vuex';

export default {
  name: 'App',
  components: {
    Moon,
    SunnyBeach
  },
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
    },
    isDarkTheme() {
      return this.$store.getters.theme === 'dark';
    }
  },
  mounted() {
    this.activeIndex = this.$route.path;
    // 初始化时检查用户认证状态
    this.$store.dispatch('checkAuth');
    // 初始化主题
    this.$store.dispatch('initTheme');
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
    },
    toggleTheme() {
      this.$store.dispatch('toggleTheme');
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
  background-color: var(--bg-color);
  color: var(--text-color);
}
.el-header {
  background-color: var(--header-bg);
  color: var(--header-text);
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
  background-color: var(--footer-bg);
  color: var(--footer-text);
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
.theme-toggle {
  margin-right: 10px;
}

/* 添加支持暗色主题的变量 */
:root {
  --bg-color: #ffffff;
  --text-color: #2c3e50;
  --header-bg: #409EFF;
  --header-text: #ffffff;
  --footer-bg: #f5f7fa;
  --footer-text: #606266;
  --card-bg: #ffffff;
  --border-color: #e4e7ed;
}

[data-theme="dark"] {
  --bg-color: #1a1a1a;
  --text-color: #f0f0f0;
  --header-bg: #1e3a8a;
  --header-text: #f0f0f0;
  --footer-bg: #1f2937;
  --footer-text: #d1d5db;
  --card-bg: #2c3e50;
  --border-color: #4b5563;
}

/* 使暗色模式下的卡片更易于阅读 */
[data-theme="dark"] .el-card {
  background-color: var(--card-bg);
  border-color: var(--border-color);
  color: var(--text-color);
}

/* 添加响应式支持 */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    padding: 10px;
  }
  
  .nav-menu {
    margin: 10px 0;
  }
  
  .user-actions {
    margin-top: 10px;
  }
  
  h1 {
    font-size: 1.5rem;
  }
  
  .el-header {
    height: auto !important;
    padding: 10px 0;
  }
}

/* 基础样式优化 */
.el-button {
  transition: all 0.3s ease;
}

.el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

/* 暗色模式下的输入框样式 */
[data-theme="dark"] .el-input__inner {
  background-color: #374151;
  border-color: #4b5563;
  color: #f3f4f6;
}

[data-theme="dark"] .el-button--default {
  background-color: #374151;
  border-color: #4b5563;
  color: #f3f4f6;
}

/* 添加性能优化相关样式 */
/* 减少页面的重排和重绘 */
.el-card, .el-button, .el-menu-item {
  will-change: transform;
  transform: translateZ(0);
}

/* 对于动画元素使用GPU加速 */
.el-dialog, .el-drawer, .el-popover {
  transform: translateZ(0);
  will-change: transform, opacity;
}

/* 对固定尺寸的容器使用缓存 */
.el-table, .el-form {
  contain: content;
}

/* 避免不必要的布局重计算 */
.el-main {
  overflow-x: hidden;
}
</style>
