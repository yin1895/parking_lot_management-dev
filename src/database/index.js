const DatabaseManager = require('./DatabaseManager');

// 创建一个数据库管理实例
const dbManager = new DatabaseManager();

// 导出数据库管理实例，便于其他模块使用
module.exports = dbManager;
