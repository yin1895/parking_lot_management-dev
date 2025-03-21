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
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
      <el-footer>
        &copy; 2023 停车场管理系统
      </el-footer>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      activeIndex: '/'
    };
  },
  mounted() {
    this.activeIndex = this.$route.path;
  },
  methods: {
    handleSelect(key) {
      this.activeIndex = key;
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
</style>
