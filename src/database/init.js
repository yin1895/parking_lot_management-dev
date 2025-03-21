const dbManager = require('./index');
const path = require('path');
const fs = require('fs');
const dotenv = require('dotenv');

// 加载环境变量
dotenv.config();

/**
 * 初始化数据库连接和表结构
 */
async function initDatabase() {
  try {
    console.log('正在初始化数据库...');
    
    // 连接数据库
    const connected = await dbManager.connect();
    if (!connected) {
      console.error('数据库连接失败，请检查配置');
      return false;
    }
    
    // 创建必要的表
    await createTables();
    
    console.log('数据库初始化完成');
    return true;
  } catch (error) {
    console.error('数据库初始化失败:', error);
    return false;
  }
}

/**
 * 创建必要的数据库表
 */
async function createTables() {
  // 读取SQL文件
  const sqlFilePath = path.join(__dirname, 'schema.sql');
  
  // 检查文件是否存在
  if (!fs.existsSync(sqlFilePath)) {
    console.warn('未找到schema.sql文件，跳过表创建');
    return;
  }
  
  // 读取SQL语句
  const sql = fs.readFileSync(sqlFilePath, 'utf8');
  
  // 分割多条SQL语句
  const statements = sql.split(';').filter(stmt => stmt.trim() !== '');
  
  // 执行每条SQL语句
  for (const statement of statements) {
    await dbManager.executeQuery(statement);
  }
  
  console.log('数据库表创建完成');
}

// 导出初始化函数
module.exports = initDatabase;
