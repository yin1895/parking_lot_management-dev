<template>
  <div id="app">
    <div class="ambient-bg-layer"></div>
    <el-container>
      <el-header>
        <div class="header-content">
          <h1 class="app-logo">停车场管理系统</h1>
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
            <el-button
              size="small"
              :icon="isDarkTheme ? 'Sunny' : 'Moon'"
              @click="toggleTheme"
              class="theme-toggle"
            ></el-button>
            <template v-if="isAuthenticated">
              <span class="welcome-msg">欢迎, {{ username }}</span>
              <el-button size="small" plain @click="handleLogout">登出</el-button>
            </template>
            <template v-else>
              <el-button size="small" plain @click="goToLogin">登录</el-button>
            </template>
          </div>
        </div>
        <div class="header-separator"></div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
      <el-footer>
        <div class="footer-separator"></div>
        <span class="footer-text">&copy; 2025 停车场管理系统</span>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus';
import { Moon, SunnyBeach } from '@element-plus/icons-vue';

export default {
  name: 'App',
  components: {
    Moon,
    SunnyBeach
  },
  data() {
    return {
      activeIndex: '/',
      _rafId: null
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
    this.$store.dispatch('checkAuth');
    this.$store.dispatch('initTheme');
    this.$nextTick(() => {
        this.initCursorTracking();
      });
  },
  beforeUnmount() {
    this.cleanupCursorTracking();
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
    },
    initCursorTracking() {
      let targetX = 50;
      let targetY = 50;
      let currentX = 50;
      let currentY = 50;
      this._onMouseMove = (e) => {
        targetX = (e.clientX / window.innerWidth) * 100;
        targetY = (e.clientY / window.innerHeight) * 100;
      };
      document.addEventListener('mousemove', this._onMouseMove);

      const smoothFactor = 0.08;
      const animate = () => {
        currentX += (targetX - currentX) * smoothFactor;
        currentY += (targetY - currentY) * smoothFactor;
        document.documentElement.style.setProperty('--cursor-x', currentX + '%');
        document.documentElement.style.setProperty('--cursor-y', currentY + '%');
        this._rafId = requestAnimationFrame(animate);
      };
      this._rafId = requestAnimationFrame(animate);
    },
    cleanupCursorTracking() {
      if (this._onMouseMove) {
        document.removeEventListener('mousemove', this._onMouseMove);
      }
      if (this._rafId) {
        cancelAnimationFrame(this._rafId);
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
/* ============ Element Plus 变量覆写（暗色默认 = :root） ============ */
:root {
  --font-family-inter: "Inter", "Microsoft YaHei", -apple-system, sans-serif;
  --font-family-mono: "JetBrains Mono", "Cascadia Code", monospace;

  --el-color-primary: #c4883c;
  --el-color-primary-light-3: #d49e4e;
  --el-color-primary-dark-2: #a06e2e;
  --el-color-success: #5a8a6a;
  --el-color-warning: #c4883c;
  --el-color-danger: #a04040;
  --el-color-info: #666666;

  --el-bg-color: #141310;
  --el-bg-color-overlay: #22201b;
  --el-bg-color-page: #0f0f0d;
  --el-text-color-primary: #e8e6e3;
  --el-text-color-regular: #c0bcb8;
  --el-text-color-secondary: #888888;
  --el-text-color-placeholder: #666666;
  --el-border-color: #3a3a3a;
  --el-border-color-light: #3a3a3a;
  --el-border-color-lighter: #2a2a2a;
  --el-border-color-extra-light: #2a2a2a;
  --el-border-radius-base: 0px;
  --el-border-radius-small: 0px;
  --el-border-radius-round: 0px;
  --el-border-radius-circle: 0px;
  --el-fill-color: #2a2a2a;
  --el-fill-color-light: #2a2a2a;
  --el-fill-color-lighter: #333333;
  --el-fill-color-blank: #1a1a1a;
  --el-fill-color-dark: #222222;
  --el-mask-color: rgba(0, 0, 0, 0.7);
  --el-box-shadow: none;
  --el-box-shadow-light: none;
  --el-box-shadow-lighter: none;
  --el-font-size-base: 14px;
  --el-font-weight-primary: 500;
  --el-font-line-height-primary: 1.6;

  --el-color-white: #e8e6e3;
  --el-color-black: #1a1a1a;
  --cursor-x: 50%;
  --cursor-y: 50%;
}

/* ============ Light theme overrides ============ */
[data-theme="light"] {
  --el-color-primary: #c4883c;
  --el-color-success: #5a8a6a;
  --el-color-warning: #c4883c;
  --el-color-danger: #a04040;

  --el-bg-color: #f5f2ed;
  --el-bg-color-overlay: #ffffff;
  --el-bg-color-page: #edeae5;
  --el-text-color-primary: #2a2a2a;
  --el-text-color-regular: #555;
  --el-text-color-secondary: #888;
  --el-text-color-placeholder: #aaa;
  --el-border-color: #ddd;
  --el-border-color-light: #e5e5e5;
  --el-border-color-lighter: #eee;
  --el-fill-color: #f0f0f0;
  --el-fill-color-light: #f5f5f5;
  --el-fill-color-lighter: #fafafa;
  --el-fill-color-blank: #ffffff;
  --el-mask-color: rgba(0, 0, 0, 0.4);
  --el-box-shadow: none;
  --el-box-shadow-light: none;
  --el-box-shadow-lighter: none;

  --el-color-white: #ffffff;
  --el-color-black: #000000;
}

/* ============ Reset & Base ============ */
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  font-family: var(--font-family-inter);
  background: linear-gradient(180deg, #1a1712 0%, #0d0c0a 100%);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  font-family: var(--font-family-inter);
  font-size: var(--el-font-size-base);
  text-align: center;
  color: var(--el-text-color-primary);
  margin: 0;
  padding: 0;
  min-height: 100vh;
  background: transparent;
  display: flex;
  flex-direction: column;
}

/* ============ Layout ============ */
.el-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.el-header {
  background: linear-gradient(180deg, rgba(255,255,255,0.03) 0%, transparent 100%);
  color: var(--el-text-color-primary);
  padding: 0 24px;
  height: 56px !important;
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: relative;
}

.el-header::after {
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.06) 20%, rgba(255,255,255,0.06) 80%, transparent 100%);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 56px;
}

.header-separator {
  height: 1px;
  background: linear-gradient(90deg, transparent 0%, rgba(196, 136, 60, 0.3) 20%, rgba(196, 136, 60, 0.3) 50%, rgba(196, 136, 60, 0.15) 80%, transparent 100%);
  box-shadow: 0 0 8px rgba(196, 136, 60, 0.1);
}

.app-logo {
  font-family: var(--font-family-inter);
  font-weight: 700;
  font-size: 15px;
  letter-spacing: 0.06em;
  color: var(--el-text-color-primary);
  margin: 0;
  white-space: nowrap;
  text-transform: uppercase;
}

.el-main {
  flex: 1;
  padding: 48px;
  background: transparent;
  overflow-x: hidden;
}

.el-footer {
  background: transparent;
  color: var(--el-text-color-secondary);
  padding: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.footer-separator {
  width: 100%;
  height: 1px;
  background: var(--el-border-color);
}

.footer-text {
  font-size: 12px;
  padding: 16px 0;
  color: var(--el-text-color-secondary);
}

/* ============ Navigation Menu ============ */
.nav-menu {
  background: transparent !important;
  border-bottom: none !important;
  flex: 1;
  display: flex;
  justify-content: center;
}

.el-menu--horizontal {
  border-bottom: none !important;
}

.el-menu--horizontal .el-menu-item {
  color: var(--el-text-color-secondary) !important;
  border-bottom: none !important;
  padding: 0 16px;
  height: 56px;
  line-height: 56px;
  font-size: 13px;
  letter-spacing: 0.02em;
  transition: color 150ms ease;
  background: transparent !important;
}

.el-menu--horizontal .el-menu-item.is-active {
  color: var(--el-color-primary) !important;
  font-weight: 600;
  border-bottom: none !important;
  position: relative;
}

.el-menu--horizontal .el-menu-item.is-active::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 24px;
  height: 2px;
  background: var(--el-color-primary);
  box-shadow: 0 0 12px rgba(196, 136, 60, 0.4);
}

.el-menu--horizontal .el-menu-item:not(.is-active):hover {
  color: var(--el-color-primary) !important;
  background: transparent !important;
}

.el-menu--horizontal .el-menu-item::after {
  display: none !important;
}

/* ============ User Actions ============ */
.user-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.welcome-msg {
  font-size: 13px;
  color: var(--el-text-color-secondary);
  margin-right: 4px;
}

.theme-toggle {
  margin-right: 4px;
}

/* ============ Button Overrides ============ */
.el-button {
  border-radius: 0 !important;
  transition: all 150ms ease !important;
}

.el-button:hover {
  transform: none !important;
  box-shadow: none !important;
}

.el-button--primary {
  --el-button-hover-bg-color: var(--el-color-primary-light-3);
  --el-button-active-bg-color: var(--el-color-primary-dark-2);
  transition: all 200ms ease !important;
}

.el-button--primary:not(.is-plain):hover {
  box-shadow: 0 0 20px rgba(196, 136, 60, 0.25) !important;
}

.el-button--danger {
  --el-button-hover-bg-color: #b05050;
  --el-button-active-bg-color: #803030;
}

.el-button--default {
  --el-button-hover-bg-color: var(--el-fill-color-light);
  --el-button-active-bg-color: var(--el-fill-color);
}

.el-button.is-plain:hover {
  background: transparent;
  color: var(--el-color-primary);
  border-color: var(--el-color-primary);
}

/* ============ Card Overrides ============ */
.el-card {
  border-radius: 0 !important;
  border: 1px solid rgba(196, 136, 60, 0.08) !important;
  background: linear-gradient(
    135deg,
    rgba(255,255,255,0.03) 0%,
    rgba(255,255,255,0.005) 40%,
    rgba(0,0,0,0.02) 60%,
    rgba(0,0,0,0.04) 100%
  ) !important;
  backdrop-filter: blur(20px) !important;
  -webkit-backdrop-filter: blur(20px) !important;
  box-shadow: 0 8px 32px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.04) !important;
  transition: all 250ms ease;
}

.el-card:hover {
  border-color: rgba(196, 136, 60, 0.2) !important;
  background: linear-gradient(
    135deg,
    rgba(255,255,255,0.04) 0%,
    rgba(255,255,255,0.01) 40%,
    rgba(0,0,0,0.02) 60%,
    rgba(0,0,0,0.04) 100%
  ) !important;
  box-shadow: 0 12px 48px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.04), 0 0 20px rgba(196,136,60,0.05) !important;
}

.el-card__header {
  border-bottom: 1px solid var(--el-border-color) !important;
  padding: 12px 16px !important;
}

/* ============ Dialog Overrides ============ */
.el-dialog {
  --el-dialog-border-radius: 0px;
  --el-dialog-bg-color: transparent;
  background: linear-gradient(
    135deg,
    rgba(255,255,255,0.04) 0%,
    rgba(255,255,255,0.01) 30%,
    rgba(255,255,255,0) 50%,
    rgba(0,0,0,0.02) 60%,
    rgba(0,0,0,0.06) 100%
  );
  backdrop-filter: blur(40px);
  -webkit-backdrop-filter: blur(40px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-top: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow: 0 24px 80px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.06);
}

.el-dialog__header {
  border-bottom: 1px solid var(--el-border-color);
  padding: 16px 20px;
  margin-right: 0 !important;
}

.el-dialog__title {
  font-size: 15px;
  font-weight: 600;
}

.el-dialog__body {
  padding: 20px;
}

.el-dialog__footer {
  border-top: 1px solid var(--el-border-color);
  padding: 12px 20px;
}

.el-overlay {
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

/* ============ Form / Input Overrides ============ */
.el-input__wrapper {
  border-radius: 0 !important;
  box-shadow: 0 0 0 1px var(--el-border-color) inset !important;
  background: var(--el-fill-color-blank) !important;
}

.el-input__wrapper.is-focus {
  box-shadow: 0 0 0 1px var(--el-color-primary) inset, 0 0 12px rgba(196, 136, 60, 0.1) !important;
}

.el-input__inner {
  font-family: var(--font-family-inter);
}

.el-textarea__inner {
  border-radius: 0 !important;
  box-shadow: 0 0 0 1px var(--el-border-color) inset !important;
  font-family: var(--font-family-inter);
}

.el-select .el-input__wrapper {
  border-radius: 0 !important;
}

/* ============ Table Overrides ============ */
.el-table {
  --el-table-border-radius: 0px !important;
  --el-table-header-bg-color: transparent !important;
  --el-table-row-hover-bg-color: var(--el-fill-color-lighter) !important;
  --el-table-border-color: var(--el-border-color) !important;
  --el-table-bg-color: transparent !important;
  --el-table-tr-bg-color: transparent !important;
  font-size: 13px;
}

.el-table th.el-table__cell {
  font-weight: 600;
  color: var(--el-text-color-secondary);
  border-bottom: 1px solid var(--el-border-color);
}

.el-table td.el-table__cell {
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell {
  background: var(--el-fill-color);
}

/* ============ Tabs Overrides ============ */
.el-tabs__item {
  font-size: 13px;
  color: var(--el-text-color-secondary);
  transition: color 150ms ease;
}

.el-tabs__item.is-active {
  color: var(--el-color-primary);
  font-weight: 600;
}

.el-tabs__active-bar {
  background: var(--el-color-primary);
  height: 2px;
}

.el-tabs__header {
  border-bottom: 1px solid var(--el-border-color);
  margin-bottom: 24px;
}

/* ============ Tag Overrides ============ */
.el-tag {
  border-radius: 0 !important;
}

/* ============ Alert Overrides ============ */
.el-alert {
  border-radius: 0 !important;
  border: 1px solid var(--el-border-color);
}

/* ============ Pagination Overrides ============ */
.el-pagination {
  --el-pagination-button-border-radius: 0px;
  --el-pagination-bg-color: transparent;
  font-family: var(--font-family-inter);
}

.el-pagination .btn-prev,
.el-pagination .btn-next,
.el-pagination .el-pager li {
  border-radius: 0 !important;
  background: transparent !important;
  border: 1px solid transparent;
}

.el-pagination .el-pager li.active {
  color: var(--el-color-primary);
  font-weight: 600;
  border-color: var(--el-border-color);
}

.el-pagination .el-pager li:hover {
  color: var(--el-color-primary);
}

/* ============ Progress Overrides ============ */
.el-progress {
  --el-progress-border-radius: 0px;
}

/* ============ Upload Overrides ============ */
.el-upload {
  border-radius: 0 !important;
}

.el-upload-dragger {
  border-radius: 0 !important;
  border: 1px dashed var(--el-border-color) !important;
  background: transparent !important;
}

.el-upload-dragger:hover {
  border-color: var(--el-color-primary) !important;
}

/* ============ Menu Overrides ============ */
.el-sub-menu__title {
  border-radius: 0 !important;
}

/* ============ Custom Scrollbar ============ */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: linear-gradient(180deg, #1a1712 0%, #0d0c0a 100%);
}

::-webkit-scrollbar-thumb {
  background: var(--el-border-color);
}

::-webkit-scrollbar-thumb:hover {
  background: var(--el-text-color-secondary);
}

/* ============ Selection ============ */
::selection {
  background: var(--el-color-primary);
  color: var(--el-bg-color);
}

::-moz-selection {
  background: var(--el-color-primary);
  color: var(--el-bg-color);
}

/* ============ Transition timings ============ */
:root {
  --el-transition-duration: 0.15s;
  --el-transition-function-ease-in-out-bezier: cubic-bezier(0.4, 0, 0.2, 1);
}

/* ============ GPU hints (keep) ============ */
.el-dialog,
.el-drawer,
.el-popover {
  transform: translateZ(0);
  will-change: transform, opacity;
}

.el-table,
.el-form {
  contain: content;
}

.el-main {
  overflow-x: hidden;
}

/* ============ Responsive ============ */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    height: auto;
    padding: 8px;
    gap: 4px;
  }

  .nav-menu {
    margin: 4px 0;
  }

  .el-header {
    height: auto !important;
  }

  .app-logo {
    font-size: 14px;
  }

  .el-main {
    padding: 16px;
  }
}

/* ============ Premium refinements ============ */
body::before {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9998;
  background-image:
    linear-gradient(rgba(196, 136, 60, 0.045) 1px, transparent 1px),
    linear-gradient(90deg, rgba(196, 136, 60, 0.045) 1px, transparent 1px);
  background-size: 32px 32px;
  mask-image: radial-gradient(
    ellipse at var(--cursor-x, 50%) var(--cursor-y, 50%),
    rgba(0, 0, 0, 0.55) 0%,
    rgba(0, 0, 0, 0.22) 25%,
    rgba(0, 0, 0, 0) 60%
  );
  -webkit-mask-image: radial-gradient(
    ellipse at var(--cursor-x, 50%) var(--cursor-y, 50%),
    rgba(0, 0, 0, 0.55) 0%,
    rgba(0, 0, 0, 0.22) 25%,
    rgba(0, 0, 0, 0) 60%
  );
}

body::after {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9997;
  background:
    radial-gradient(circle at var(--cursor-x, 50%) var(--cursor-y, 50%),
    rgba(196, 136, 60, 0.08) 0%,
    rgba(196, 136, 60, 0.035) 15%,
    transparent 40%),
    radial-gradient(circle at var(--cursor-x, 50%) var(--cursor-y, 50%),
    rgba(196, 136, 60, 0.03) 0%,
    rgba(255, 255, 255, 0.012) 22%,
    transparent 50%),
    radial-gradient(circle at var(--cursor-x, 50%) var(--cursor-y, 50%),
    rgba(255, 255, 255, 0.015) 0%,
    transparent 60%);
}


/* ambient background layer – noise + corner glow */
.ambient-bg-layer {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9996;
  background:
    radial-gradient(ellipse at 5% 5%, rgba(196, 136, 60, 0.06) 0%, transparent 45%),
    radial-gradient(ellipse at 95% 5%, rgba(196, 136, 60, 0.03) 0%, transparent 45%),
    radial-gradient(ellipse at 50% 100%, rgba(255, 255, 255, 0.015) 0%, transparent 45%);
}

.ambient-bg-layer::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-repeat: repeat;
  background-size: 160px 160px;
  mix-blend-mode: overlay;
  opacity: 0.15;
}

</style>
