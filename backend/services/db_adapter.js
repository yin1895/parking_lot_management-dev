/**
 * 数据库适配器 - 将DatabaseManager与现有服务整合
 */
const dbManager = require('../../src/database');

/**
 * 将现有数据库操作适配到新的DatabaseManager
 * 该类提供数据访问接口，隔离底层数据库操作
 */
class DatabaseAdapter {
  /**
   * 通过车牌号获取会员
   * @param {string} plateNumber 车牌号
   * @returns {Promise<Object>} 会员信息
   */
  static async getMemberByPlate(plateNumber) {
    return await dbManager.findOne('members', { plate_number: plateNumber });
  }

  /**
   * 获取当前在场的车辆记录
   * @param {string} plateNumber 车牌号
   * @returns {Promise<Object>} 停车记录
   */
  static async getActiveVehicle(plateNumber) {
    return await dbManager.findOne('parking_records', { 
      plate_number: plateNumber,
      exit_time: null
    });
  }

  /**
   * 统计当前在场车辆数量
   * @returns {Promise<number>} 在场车辆数量
   */
  static async countActiveVehicles() {
    const records = await dbManager.findMany('parking_records', { exit_time: null });
    return records.length;
  }

  /**
   * 添加停车记录
   * @param {Object} recordData 停车记录数据
   * @returns {Promise<Object>} 添加结果
   */
  static async addParkingRecord(recordData) {
    return await dbManager.insert('parking_records', recordData);
  }

  /**
   * 更新停车记录
   * @param {number} recordId 记录ID
   * @param {Object} updateData 更新数据
   * @returns {Promise<Object>} 更新结果
   */
  static async updateParkingRecord(recordId, updateData) {
    return await dbManager.update('parking_records', updateData, { id: recordId });
  }

  /**
   * 保存会员信息
   * @param {Object} memberData 会员数据
   * @returns {Promise<Object>} 保存结果
   */
  static async saveMember(memberData) {
    if (memberData.id) {
      return await dbManager.update('members', memberData, { id: memberData.id });
    } else {
      return await dbManager.insert('members', memberData);
    }
  }
}

module.exports = DatabaseAdapter;
