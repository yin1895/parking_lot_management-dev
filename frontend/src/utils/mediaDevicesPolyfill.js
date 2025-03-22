/**
 * 为旧浏览器提供navigator.mediaDevices的polyfill
 */
export function initMediaDevicesPolyfill() {
  // 确保navigator对象存在
  if (!navigator) return;
  
  // 旧版本浏览器适配
  if (!navigator.mediaDevices) {
    navigator.mediaDevices = {};
  }

  // 如果getUserMedia不存在，创建一个polyfill
  if (!navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia = function(constraints) {
      // 获取旧版本浏览器的getUserMedia实现
      const getUserMedia = navigator.getUserMedia ||
                          navigator.webkitGetUserMedia ||
                          navigator.mozGetUserMedia ||
                          navigator.msGetUserMedia;

      // 如果没有任何实现，返回一个rejected promise
      if (!getUserMedia) {
        return Promise.reject(new Error('此浏览器不支持摄像头访问'));
      }

      // 将老式回调包装为Promise
      return new Promise((resolve, reject) => {
        getUserMedia.call(navigator, constraints, resolve, reject);
      });
    };
  }
}

// 导出一个立即执行函数，以便在导入时立即应用polyfill
export default (function() {
  initMediaDevicesPolyfill();
  return { initiated: true };
})();
