import axios from 'axios';

const MAX_RETRIES = 2;
const RETRY_DELAY = 500; // ms

// 创建带重试功能的axios请求
export const createApiRequest = async (method, url, data = null, config = {}, retries = 0) => {
  try {
    let response;
    
    if (method.toLowerCase() === 'get') {
      response = await axios.get(url, {
        ...config,
        params: {
          ...(config.params || {}),
          _t: Date.now() // 添加时间戳防止缓存
        }
      });
    } else if (method.toLowerCase() === 'post') {
      response = await axios.post(url, data, config);
    } else if (method.toLowerCase() === 'put') {
      response = await axios.put(url, data, config);
    } else if (method.toLowerCase() === 'delete') {
      response = await axios.delete(url, config);
    } else {
      throw new Error(`不支持的请求方法: ${method}`);
    }
    
    return response.data;
  } catch (error) {
    // 检查是否应该重试
    if (retries < MAX_RETRIES && isRetryableError(error)) {
      console.warn(`请求失败，尝试重试 (${retries + 1}/${MAX_RETRIES}): ${url}`);
      
      // 等待一段时间后重试
      await new Promise(resolve => setTimeout(resolve, RETRY_DELAY * (retries + 1)));
      
      // 递归重试
      return createApiRequest(method, url, data, config, retries + 1);
    }
    
    // 无法重试或已达到最大重试次数，向上抛出错误
    console.error('API请求失败:', {url, method, error});
    throw error;
  }
};

// 判断错误是否可以重试
const isRetryableError = (error) => {
  // 网络错误总是可以重试
  if (!error.response) return true;
  
  // 服务器错误(5xx)可以重试
  const status = error.response.status;
  return status >= 500 && status < 600;
};

export default {
  get: (url, config = {}) => createApiRequest('get', url, null, config),
  post: (url, data, config = {}) => createApiRequest('post', url, data, config),
  put: (url, data, config = {}) => createApiRequest('put', url, data, config),
  delete: (url, config = {}) => createApiRequest('delete', url, config)
};
