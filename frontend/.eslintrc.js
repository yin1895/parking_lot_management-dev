module.exports = {
  root: true,
  env: {
    node: true,
    browser: true,
    es2021: true
  },
  extends: [
    'plugin:vue/vue3-essential',
    'eslint:recommended'
  ],
  parserOptions: {
    ecmaVersion: 2020,
    sourceType: 'module'
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    // 允许未使用的变量
    'no-unused-vars': 'warn',
    // 缩进设置为2个空格
    'indent': ['warn', 2],
    // 允许开发环境使用console
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off'
  }
}
