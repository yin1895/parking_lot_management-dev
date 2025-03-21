const FeeCalculator = require('./fee_calculator');
const DatabaseAdapter = require('./db_adapter');
const { DateTime } = require('luxon');

/**
 * 停车场服务类 - 处理车辆进出与费用计算
 */
class ParkingService {
    constructor() {
        this.feeCalculator = new FeeCalculator();
    }
    
    /**
     * 记录车辆入场
     * @param {string} plateNumber - 车牌号
     * @param {string} plateColor - 车牌颜色
     * @returns {Object} 入场记录结果
     */
    async recordEntry(plateNumber, plateColor='蓝色') {
        try {
            // 使用新的数据库适配器检查车辆是否已在场内
            const existingRecord = await DatabaseAdapter.getActiveVehicle(plateNumber);
            if (existingRecord) {
                return {
                    'success': false,
                    'message': `车辆 ${plateNumber} 已在停车场内`,
                    'record': existingRecord
                };
            }
            
            // 创建新记录
            const entryTime = new Date();
            const record = await DatabaseAdapter.addParkingRecord({
                plate_number: plateNumber,
                plate_color: plateColor,
                entry_time: entryTime
            });
            
            return {
                'success': true,
                'message': `车辆 ${plateNumber} 成功入场`,
                'record': {
                    id: record.insertId,
                    plate_number: plateNumber,
                    plate_color: plateColor,
                    entry_time: entryTime
                }
            };
        } catch (e) {
            console.error('记录入场失败:', e);
            return {
                'success': false,
                'message': `记录入场失败: ${e.message}`
            };
        }
    }
    
    /**
     * 获取停车场状态
     * @returns {Object} 停车场状态信息
     */
    async getStatus() {
        try {
            // 获取当前在场车辆数量
            const activeVehicles = await DatabaseAdapter.countActiveVehicles();
            // 假设总车位为100
            const totalSpaces = 100;
            const availableSpaces = totalSpaces - activeVehicles;
            
            return {
                'success': true,
                'total_spaces': totalSpaces,
                'occupied_spaces': activeVehicles,
                'available_spaces': availableSpaces,
                'occupancy_rate': (activeVehicles / totalSpaces) * 100
            };
        } catch (e) {
            console.error('获取停车场状态失败:', e);
            return {
                'success': false,
                'message': `获取停车场状态失败: ${e.message}`
            };
        }
    }
}

module.exports = ParkingService;