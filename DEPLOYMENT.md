# 智能停车场管理系统部署指南

本文档提供智能停车场管理系统的完整部署步骤。

## 系统要求

### 硬件要求
- CPU: 2核或以上
- 内存: 4GB或以上
- 硬盘: 20GB或以上

### 软件环境
- Node.js v14+
- Python 3.8+
- MySQL 5.7+
- npm/yarn
- pip

## 部署步骤

### 1. 克隆代码仓库

```bash
git clone https://github.com/your-repo/parking_lot_management.git
cd parking_lot_management
```

### 2. 环境配置

#### 2.1 配置环境变量

复制示例环境变量文件并编辑：

```bash
cp .env.example .env
```

编辑`.env`文件，配置以下关键参数：

## 3. 更新DEPLOYMENT.md文档

将ESLint相关配置添加到部署文档中：

## 4. 前端安装注意事项

安装前端依赖时，使用以下命令避免依赖冲突：

```bash
cd frontend
npm install --legacy-peer-deps
# 或者使用
npm install --force
```

这是因为一些旧版本的依赖可能与webpack 5不兼容。如果安装过程中遇到依赖冲突问题，可以查看 `docs/npm-warnings.md` 了解更多信息。

