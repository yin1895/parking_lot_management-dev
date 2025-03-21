# NPM 警告处理指南

## webpack-chain 弃用警告

在运行 `npm install` 时，您可能会看到以下警告：

## ESLint 警告

在运行 `npm install` 或 `npm run lint` 时，您可能会看到以下警告：

### 警告内容

```
Warning: ESLint couldn't find the plugin "eslint-plugin-xxx".
```

### 解决方法

1. 确保您已经安装了所需的 ESLint 插件。
2. 检查您的 `.eslintrc` 配置文件，确保插件名称正确。
3. 如果问题仍然存在，请尝试重新安装 ESLint 及相关插件。

## 依赖冲突警告

### 警告内容

```
npm resolution error report

While resolving: frontend@1.0.0
Found: webpack@5.98.0
node_modules/webpack
  dev webpack@"^5.80.0" from the root project

Could not resolve dependency:
peer webpack@"^4.0.0" from cache-loader@4.1.0
node_modules/cache-loader
  dev cache-loader@"^4.1.0" from the root project
```

### 解决方法

1. 使用 `--legacy-peer-deps` 或 `--force` 标志安装依赖：
   ```bash
   npm install --legacy-peer-deps
   # 或
   npm install --force
   ```

2. 如果您遇到特定的cache-loader和webpack冲突，不用担心，我们已从package.json中移除了cache-loader，因为webpack 5已内置缓存功能。

3. 对于其他依赖冲突，可以在package.json的"resolutions"字段中指定特定版本。

