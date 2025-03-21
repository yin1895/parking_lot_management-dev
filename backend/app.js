const express = require('express');
const cors = require('cors');
const initDatabase = require('../src/database/init');
const parkingController = require('./controllers/parking_controller');
const recognitionController = require('./controllers/recognition_controller');
const errorHandler = require('./utils/error_handler');

// 创建Express应用
const app = express();
app.use(cors());
app.use(express.json());

// 初始化数据库
(async () => {
  try {
    const dbInitialized = await initDatabase();
    if (!dbInitialized) {
      console.warn('数据库初始化失败，某些功能可能不可用');
    }
  } catch (error) {
    console.error('数据库初始化错误:', error);
  }
})();

// 注册路由
app.use('/api/parking', parkingController);
app.use('/api/recognition', recognitionController);

// 状态检查端点
app.get('/api/status', (req, res) => {
  res.json({
    status: 'running',
    database: 'connected'
  });
});

// 注册错误处理中间件
app.use(errorHandler);

// 启动服务器
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`服务器运行在端口: ${PORT}`);
});
