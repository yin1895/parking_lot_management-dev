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

## 部署方式

系统提供两种部署方式，请根据需求选择：

### 方式一：手动部署

#### 系统要求

- Python 3.8+
- MySQL 5.7+ 
- Node.js 和 npm (前端部署)

#### 部署步骤

1. **克隆仓库**
```bash     
git clone https://github.com/yin1895/parking-management-dev.git
cd parking-management-dev
```

2. **创建虚拟环境**
```bash
conda create -n parking python=3.8
conda activate parking
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **安装并配置MySQL**
- 创建数据库：
  ```sql
  CREATE DATABASE parking_lot_management;
  ```
- 创建用户并授权：
  ```sql
  CREATE USER 'parking_user'@'localhost' IDENTIFIED BY 'your_password';
  GRANT ALL PRIVILEGES ON parking_lot_management.* TO 'parking_user'@'localhost';
  FLUSH PRIVILEGES;
  ```

5. **配置环境变量**
- 复制环境变量示例文件:
  ```bash
  cp .env.example .env
  ```
- 或者根据实际情况修改.env文件中的配置:
  ```
  DB_HOST=localhost
  DB_PORT=3306
  DB_NAME=parking_lot_management
  DB_USER=parking_user
  DB_PASSWORD=your_password
  JWT_SECRET_KEY=your_secret_key
  PARKING_CAPACITY=100
  ```

6. **初始化数据库**
```bash
python scripts/init_db.py
```

7. **启动项目**
```bash
run.bat
```
或分别启动前后端：
```bash
# 启动后端
python backend/app.py

# 启动前端
cd frontend
npm install
npm start
```

### 方式二：Docker部署

#### 系统要求

- Docker
- Docker Compose

#### 部署步骤

1. **克隆仓库**
```bash     
git clone https://github.com/yin1895/parking-management-dev.git
cd parking-management-dev
```

2. **使用Docker Compose部署**
- 作者的docker username是yinth,如果你使用one-click-deploy.bat快捷脚本可能会用到，这个脚本是提供给不熟悉docker的用户使用的，如果你对docker有所了解，可以使用下面命令
```bash
docker-compose -f docker-compose.hub.yml up -d
```
- 注意后端启动后会等待20秒以便数据库彻底启动，这个过程前端是链接不到后端的哦

3. **访问系统**
- 前端界面: http://localhost:8080
- 后端API: http://localhost:5001

4. **故障排除**
- 如果Docker部署后遇到服务间通信问题(如前端无法连接后端，或后端无法连接数据库)，可以运行检查脚本:
```bash
./check_docker_connectivity.sh
```
- 该脚本会检查容器网络、端口映射和服务状态，并提供修复建议
- 常见问题包括:
  - 防火墙阻止容器通信
  - 端口冲突(如3307或8080端口已被占用)
  - Docker网络配置不正确

- 在docker中数据库我已经默认使用root，因为懒得设置用户和权限，有需要的自己搞QWQ

5. **停止服务**
```bash
docker-compose -f docker-compose.hub.yml down
```

## 默认管理员账号

- 用户名：`admin`
- 密码：`admin`

## 使用说明

1. 停车场管理
   - 车辆入场：记录车牌和入场时间
   - 车辆出场：计算停车费用并记录
   - 查看车位状态

2. 会员管理
   - 添加/删除会员
   - 查看会员列表
   - 设置会员价格

3. 历史记录查询
   - 按日期范围查询
   - 按车牌号筛选
   - 查看详细停车记录

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

## 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 联系方式

如有问题或建议，请通过以下方式联系：
- Email: 3023001549@tju.edu.cn