/**
 * 防抖函数 - 限制函数在一定时间内的重复调用
 * @param {Function} func 需要防抖的函数
 * @param {Number} wait 延迟时间(毫秒)
 * @param {Boolean} immediate 是否立即执行
 * @returns {Function} 防抖后的函数
 */
export function debounce(func, wait = 300, immediate = false) {
  let timeout;
  
  return function(...args) {
    const context = this;
    
    const later = function() {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    
    const callNow = immediate && !timeout;
    
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    
    if (callNow) func.apply(context, args);
  };
}

/**
 * 节流函数 - 限制函数在一定时间内只能执行一次
 * @param {Function} func 需要节流的函数
 * @param {Number} limit 限制的时间(毫秒)
 * @returns {Function} 节流后的函数
 */
export function throttle(func, limit = 300) {
  let inThrottle;
  
  return function(...args) {
    const context = this;
    
    if (!inThrottle) {
      func.apply(context, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}
