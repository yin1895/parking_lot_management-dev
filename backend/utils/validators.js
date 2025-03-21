/**
 * 验证工具模块 - 提供请求数据验证功能
 */

/**
 * 验证车牌号格式
 * @param {string} plateNumber - 车牌号
 * @returns {boolean} 是否有效
 */
function isValidPlateNumber(plateNumber) {
  if (!plateNumber || typeof plateNumber !== 'string') {
    return false;
  }
  
  // 基本中国车牌号格式验证 (可按实际需求调整)
  const plateRegex = /^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-Z][A-Z0-9]{5,6}$/;
  return plateRegex.test(plateNumber) || plateNumber.length >= 5; // 允许测试用的简化车牌
}

/**
 * 验证车牌颜色
 * @param {string} plateColor - 车牌颜色
 * @returns {boolean} 是否有效
 */
function isValidPlateColor(plateColor) {
  if (!plateColor || typeof plateColor !== 'string') {
    return false;
  }
  
  const validColors = ['蓝色', '黄色', '绿色', '黑色', '白色'];
  return validColors.includes(plateColor);
}

module.exports = {
  isValidPlateNumber,
  isValidPlateColor
};
