# 智能停车场管理系统

一个基于Python Flask的智能停车场管理系统，集成了车牌识别功能，支持实时车牌识别、会员管理和停车记录管理。

## ✨ 功能特点

- 🚗 **实时车牌识别**
  - 支持图片上传识别
  - 支持车牌颜色识别

- 📊 **停车场管理**
  - 车位状态实时监控
  - 智能分段计费系统
    - 支持普通用户和会员差别计费
    - 支持会员状态变更自动分段计费
  - 车辆进出记录管理

- 👥 **会员管理**
  - 会员添加与删除
  - 会员状态管理
  - 会员优惠价格设置

- 📈 **数据管理**
  - 历史记录查询
    - 支持日期范围筛选
    - 支持车牌号筛选
  - 停车时长统计
  - 费用明细查看

- 💻 **用户界面**
  - 直观的图形界面
  - 实时显示停车场状态
  - 支持手动输入和自动识别
  - 管理员控制面板

## 🛡️ 安全特性

- **JWT认证**: 完整的身份验证和权限管理系统
- **输入验证**: 严格的参数验证和XSS防护
- **错误处理**: 统一的异常处理和安全错误响应
- **CORS配置**: 安全的跨域请求控制
- **密码安全**: PBKDF2加密存储

## 🏗️ 架构优化

- **统一响应格式**: 标准化的API响应格式
- **缓存机制**: 内存缓存提升性能
- **性能监控**: 实时性能指标追踪
- **数据库优化**: 索引优化和查询优化
- **测试框架**: 完整的单元测试覆盖

## 🚀 部署方式

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

4. **配置环境变量**
- 复制环境变量示例文件:
```bash
cp .env.example .env
```
- 根据实际情况修改.env文件中的配置

5. **初始化数据库**
```bash
python scripts/init_db.py
```

6. **启动项目**
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

1. **使用Docker Compose部署**
```bash
docker-compose -f docker-compose.hub.yml up -d
```

2. **访问系统**
- 前端界面: http://localhost:8080
- 后端API: http://localhost:5001

## 🔧 API接口

| 接口 | 方法 | 描述 | 认证 |
|------|------|------|------|
| /api/auth/login | POST | 管理员登录 | 否 |
| /api/parking/entry | POST | 车辆入场记录 | 可选 |
| /api/parking/exit | POST | 车辆出场及计费 | 可选 |
| /api/parking/status | GET | 获取停车场状态 | 需要管理员 |
| /api/members | GET | 获取会员列表 | 需要认证 |
| /api/members | POST | 添加会员 | 需要管理员 |
| /api/members/{id} | PUT | 更新会员信息 | 需要管理员 |
| /api/members/{id} | DELETE | 删除会员 | 需要管理员 |
| /api/records | GET | 获取停车记录 | 需要认证 |
| /api/recognition/plate | POST | 上传图片识别车牌 | 可选 |

详细API文档见 `/docs/api.md`

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=backend tests/

# 运行特定测试
pytest tests/test_validators.py
```

## 📊 监控和日志

- **性能监控**: 实时追踪API响应时间
- **请求日志**: 完整的HTTP请求记录
- **错误追踪**: 详细的错误日志和堆栈跟踪
- **缓存监控**: 缓存命中率和性能统计

## 🔒 安全最佳实践

- 使用强密码策略
- 定期更新JWT密钥
- 启用HTTPS
- 配置防火墙规则
- 定期备份数据库

## 📈 性能优化

- 数据库索引优化
- 内存缓存机制
- 分页查询优化
- 连接池管理

## 🛠️ 开发工具

- **代码格式化**: Black
- **代码检查**: Flake8
- **测试覆盖率**: Coverage
- **依赖管理**: pip-tools

## 📞 技术支持

如有问题或建议，请通过以下方式联系：
- Email: 3023001549@tju.edu.cn

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 🎯 路线图

- [ ] Redis缓存集成
- [ ] 消息队列支持
- [ ] 微服务架构
- [ ] 移动端APP
- [ ] 高级数据分析
