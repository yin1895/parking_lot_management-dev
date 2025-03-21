const mysql = require('mysql');
const util = require('util');

/**
 * 数据库管理类 - 提供基础的数据库操作
 */
class DatabaseManager {
  constructor(config) {
    this.config = config || {
      host: process.env.DB_HOST || 'localhost',
      user: process.env.DB_USER || 'root',
      password: process.env.DB_PASSWORD || '',
      database: process.env.DB_NAME || 'parking_lot'
    };
    this.connection = null;
  }

  /**
   * 连接数据库
   */
  connect() {
    try {
      this.connection = mysql.createConnection(this.config);
      // 将callback形式的query转为Promise形式
      this.query = util.promisify(this.connection.query).bind(this.connection);
      console.log('数据库连接成功');
      return true;
    } catch (error) {
      console.error('数据库连接失败:', error);
      return false;
    }
  }

  /**
   * 关闭数据库连接
   */
  disconnect() {
    if (this.connection) {
      this.connection.end();
      console.log('数据库连接已关闭');
    }
  }

  /**
   * 执行查询
   * @param {string} sql SQL查询语句
   * @param {Array} params 查询参数
   * @returns {Promise} 查询结果
   */
  async executeQuery(sql, params = []) {
    try {
      if (!this.connection) {
        await this.connect();
      }
      const results = await this.query(sql, params);
      return results;
    } catch (error) {
      console.error('查询执行失败:', error);
      throw error;
    }
  }

  /**
   * 查询单条记录
   * @param {string} table 表名
   * @param {object} conditions 查询条件
   * @returns {Promise} 查询结果
   */
  async findOne(table, conditions) {
    const keys = Object.keys(conditions);
    const whereClause = keys.map(key => `${key} = ?`).join(' AND ');
    const params = keys.map(key => conditions[key]);
    
    const sql = `SELECT * FROM ${table} WHERE ${whereClause} LIMIT 1`;
    const results = await this.executeQuery(sql, params);
    return results[0];
  }

  /**
   * 查询多条记录
   * @param {string} table 表名
   * @param {object} conditions 查询条件
   * @returns {Promise} 查询结果
   */
  async findMany(table, conditions = {}) {
    let sql = `SELECT * FROM ${table}`;
    let params = [];
    
    const keys = Object.keys(conditions);
    if (keys.length > 0) {
      const whereClause = keys.map(key => `${key} = ?`).join(' AND ');
      params = keys.map(key => conditions[key]);
      sql += ` WHERE ${whereClause}`;
    }
    
    return await this.executeQuery(sql, params);
  }

  /**
   * 插入记录
   * @param {string} table 表名
   * @param {object} data 要插入的数据
   * @returns {Promise} 插入结果
   */
  async insert(table, data) {
    const keys = Object.keys(data);
    const values = keys.map(key => data[key]);
    const placeholders = Array(keys.length).fill('?').join(', ');
    
    const sql = `INSERT INTO ${table} (${keys.join(', ')}) VALUES (${placeholders})`;
    return await this.executeQuery(sql, values);
  }

  /**
   * 更新记录
   * @param {string} table 表名
   * @param {object} data 要更新的数据
   * @param {object} conditions 更新条件
   * @returns {Promise} 更新结果
   */
  async update(table, data, conditions) {
    const dataKeys = Object.keys(data);
    const setClause = dataKeys.map(key => `${key} = ?`).join(', ');
    const dataValues = dataKeys.map(key => data[key]);
    
    const conditionKeys = Object.keys(conditions);
    const whereClause = conditionKeys.map(key => `${key} = ?`).join(' AND ');
    const conditionValues = conditionKeys.map(key => conditions[key]);
    
    const sql = `UPDATE ${table} SET ${setClause} WHERE ${whereClause}`;
    return await this.executeQuery(sql, [...dataValues, ...conditionValues]);
  }

  /**
   * 删除记录
   * @param {string} table 表名
   * @param {object} conditions 删除条件
   * @returns {Promise} 删除结果
   */
  async delete(table, conditions) {
    const keys = Object.keys(conditions);
    const whereClause = keys.map(key => `${key} = ?`).join(' AND ');
    const params = keys.map(key => conditions[key]);
    
    const sql = `DELETE FROM ${table} WHERE ${whereClause}`;
    return await this.executeQuery(sql, params);
  }
}

module.exports = DatabaseManager;
