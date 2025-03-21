/**
 * 统一配置文件 - 集中管理应用配置
 * 注意: 当前各模块仍使用自己的配置，这是一个用于将来迁移的配置模板
 */
require('dotenv').config();

module.exports = {
  // 应用环境
  env: process.env.NODE_ENV || 'development',
  
  // 服务器配置
  server: {
    port: parseInt(process.env.PORT || '5000', 10),
    host: process.env.HOST || 'localhost',
  },
  
  // 数据库配置
  database: {
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT || '3306', 10),
    name: process.env.DB_NAME || 'parking_management',
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || '',
  },
  
  // 停车场配置
  parking: {
    capacity: parseInt(process.env.PARKING_CAPACITY || '100', 10),
    normalRate: parseFloat(process.env.NORMAL_RATE || '10'),
    memberRate: parseFloat(process.env.MEMBER_RATE || '8'),
    memberDiscount: parseFloat(process.env.MEMBER_DISCOUNT || '0.8'),
  },
  
  // JWT配置
  jwt: {
    secret: process.env.JWT_SECRET_KEY || 'your-secret-key-here',
    expiresIn: parseInt(process.env.JWT_ACCESS_TOKEN_EXPIRES || '86400', 10),
  }
};
