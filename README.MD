# 智能停车场管理系统

一个基于Python的智能停车场管理系统，集成了车牌识别功能，支持实时车牌识别、会员管理和停车记录管理。

## 功能特点

- 🚗 实时车牌识别
  - 支持图片上传识别
  - 支持车牌颜色识别

- 📊 停车场管理
  - 车位状态实时监控
  - 智能分段计费系统
    - 支持普通用户和会员差别计费
    - 支持会员状态变更自动分段计费
  - 车辆进出记录管理

- 👥 会员管理
  - 会员添加与删除
  - 会员状态管理
  - 会员优惠价格设置

- 📈 数据管理
  - 历史记录查询
    - 支持日期范围筛选
    - 支持车牌号筛选
  - 停车时长统计
  - 费用明细查看

- 💻 用户界面
  - 直观的图形界面
  - 实时显示停车场状态
  - 支持手动输入和自动识别
  - 管理员控制面板

## 系统要求

- Python 3.8+
- OpenCV
- Flask (后端API服务)
- Vue (前端界面)
- SQLAlchemy (数据库ORM)
- ONNX Runtime
- Pandas
- 其他依赖见 requirements.txt

## 安装与启动

### 1. 克隆仓库
```bash     
git clone https://github.com/yin1895/parking-management.git
cd parking-management
```

### 2. 创建虚拟环境（推荐使用anaconda）
```bash
conda create -n parking python=3.8
conda activate parking
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 启动后端服务

```bash
# 在项目根目录下运行
python backend/app.py

# 或者使用项目主入口
python main.py
```

> **注意**: 请在项目根目录下运行后端服务，如果在backend目录内运行可能会遇到模块导入错误。

### 5. 启动前端应用
```bash
cd frontend
npm install
npm start  # 或者使用 npm run serve
```

> **注意**：如果 npm install 显示依赖项存在安全漏洞，可以运行 `npm run audit-fix` 尝试修复。对于无法自动修复的问题，可能需要手动更新特定依赖或等待依赖项更新。请谨慎使用 `npm audit fix --force`，因为它可能破坏应用功能。

## 使用说明

### 基本操作
1. 启动系统
```bash
python main.py
```

2. 车牌识别
- 点击"开启摄像头"按钮启动识别
- 系统将在5秒内进行连续识别
- 自动选择最佳识别结果

3. 车辆管理
- 车辆入场：输入车牌号或使用识别结果，点击"车辆入场"
- 车辆出场：输入车牌号或使用识别结果，点击"车辆出场"
- 系统自动记录时间并计算费用

### 管理员功能
1. 登录管理界面
- 点击"管理员入口"
- 默认账号：admin
- 默认密码：1234

2. 会员管理
- 添加/删除会员
- 查看会员列表
- 设置会员价格

3. 历史记录查询
- 按日期范围查询
- 按车牌号筛选
- 查看详细停车记录

## 架构说明

本系统采用前后端分离架构:

### 后端 (Backend)
- RESTful API服务
- 车牌识别核心算法
- 数据库管理
- 业务逻辑处理

### 前端 (Frontend)
- Web界面 (Vue + Element Plus)
- 通过API与后端通信

## API文档

系统提供以下主要API接口:

| 接口                   | 方法   | 描述                 |
|------------------------|--------|---------------------|
| /api/auth/login        | POST   | 管理员登录           |
| /api/parking/entry     | POST   | 车辆入场记录         |
| /api/parking/exit      | POST   | 车辆出场及计费       |
| /api/parking/status    | GET    | 获取停车场状态       |
| /api/members           | GET    | 获取会员列表         |
| /api/members           | POST   | 添加会员             |
| /api/members/{id}      | PUT    | 更新会员信息         |
| /api/members/{id}      | DELETE | 删除会员             |
| /api/records           | GET    | 获取停车记录         |
| /api/recognition/plate | POST   | 上传图片识别车牌     |

详细API文档见 `/docs/api.md`

## 项目结构

```
parking_management/
├── backend/           # 后端API服务
│   ├── app.py         # Flask后端入口点
│   ├── config/        # 配置文件
│   ├── models/        # 数据库模型
│   ├── controllers/   # API控制器
│   ├── services/      # 业务服务
│   ├── utils/         # 工具函数
│   └── recognition/   # 车牌识别模块
├── frontend/          # 前端Web应用
│   ├── public/        # 静态资源
│   ├── src/           # 源代码
│   ├── package.json   # 依赖配置
│   └── README.md      # 前端说明
├── docs/              # 文档
│   └── api.md         # API文档
├── weights/           # 模型文件
└── requirements.txt   # 项目依赖
```

## 配置说明

系统配置文件位于 `data/config.json`，可以修改以下参数：
- 停车场容量
- 计费标准（普通/会员）
- 界面刷新率
- 其他系统参数

## 常见问题

1. 摄像头无法打开
   - 检查摄像头连接
   - 确认摄像头未被其他程序占用
   - 检查摄像头驱动是否正确安装
   - 请检查摄像头物理开关是否打开

2. 车牌识别不准确
   - 确保光线充足
   - 调整摄像头角度
   - 确保车牌在画面中清晰可见

3. 管理员登录问题
   - 确认使用默认账号密码
   - 检查输入是否正确
   - 注意大小写

## 开发计划

- [x] 添加会员管理功能
- [x] 实现分段计费系统
- [x] 添加历史记录查询
- [ ] 添加数据统计和报表功能
- [ ] 优化车牌识别准确率
- [ ] 添加更多用户权限管理
- [ ] 支持多摄像头接入

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 联系方式

如有问题或建议，请通过以下方式联系：
- Email: 3023001549@tju.edu.cn