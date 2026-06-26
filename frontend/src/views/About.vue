<template>
  <div class="about">
    <h2 class="about-heading">关于停车场管理系统</h2>
    <div class="about-separator"></div>
    <p>本系统用于管理停车场的车辆进出、费用计算和会员管理等功能。</p>
    <p>使用技术栈: Vue.js, Element Plus, Flask, MySQL</p>
  </div>
</template>

<script>
export default {
  name: 'AboutView'
}
</script>

<style scoped>
.about {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  text-align: left;
}

.about-heading {
  font-family: var(--font-family-inter);
  font-weight: 600;
  font-size: 20px;
  letter-spacing: -0.01em;
  color: var(--el-text-color-primary);
  margin: 0 0 8px 0;
}

.about-separator {
  height: 1px;
  background: var(--el-border-color);
  margin-bottom: 20px;
}

.about p {
  font-size: 14px;
  line-height: 1.6;
  color: var(--el-text-color-regular);
  margin: 8px 0;
}
</style>
