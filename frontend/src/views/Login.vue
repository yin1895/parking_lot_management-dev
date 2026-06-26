<template>
  <div class="login-container">
    <div class="login-box">
      <h2 class="login-title">登录系统</h2>

      <el-form :model="loginForm" :rules="rules" ref="loginFormRef" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="loginForm.username" placeholder="请输入用户名"></el-input>
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" @keyup.enter="submitForm"></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm" :loading="loading">登录</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>

      <div class="login-tips">
        <p>默认管理员账号: admin</p>
        <p>默认密码: admin</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

const router = useRouter()
const store = useStore()
const loginFormRef = ref(null)
const loading = ref(false)

const loginForm = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

const submitForm = async () => {
  if (!loginForm.username || !loginForm.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }

  loading.value = true
  try {
    const result = await store.dispatch('login', {
      username: loginForm.username,
      password: loginForm.password
    })

    if (result.success) {
      ElMessage.success('登录成功')
      router.push('/management')
    } else {
      ElMessage.error(result.message || '登录失败，请检查用户名和密码')
    }
  } catch (error) {
    ElMessage.error('登录失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  if (loginFormRef.value) {
    loginFormRef.value.resetFields()
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.login-box {
  width: 400px;
  padding: 32px;
  background: var(--el-bg-color-overlay);
  border: 1px solid var(--el-border-color);
}

.login-title {
  font-family: var(--font-family-inter);
  font-weight: 600;
  font-size: 20px;
  letter-spacing: -0.01em;
  color: var(--el-color-primary);
  text-align: center;
  margin: 0 0 24px 0;
}

.login-tips {
  margin-top: 20px;
  padding-top: 12px;
  border-top: 1px solid var(--el-border-color);
  color: var(--el-text-color-placeholder);
  font-size: 13px;
  text-align: center;
}

.login-tips p {
  margin: 2px 0;
}
</style>
