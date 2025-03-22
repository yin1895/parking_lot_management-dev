import apiClient from '../utils/apiClient';
import axios from 'axios';

const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:5000/api';

/**
 * 统一处理API错误
 * @param {Error} error - 捕获的错误
 * @param {string} operation - 操作描述
 * @throws {Error} 处理后的错误
 */
const handleApiError = (error, operation) => {
  console.error(`API错误 (${operation}):`, error);
  
  // 提取错误信息
  let errorMessage = '操作失败，请稍后重试';
  
  if (error.response) {
    // 服务器返回了错误状态码
    const status = error.response.status;
    const data = error.response.data;
    
    if (data && data.message) {
      errorMessage = data.message;
    } else if (status === 401) {
      errorMessage = '未授权，请重新登录';
    } else if (status === 400) {
      errorMessage = '请求参数错误';
    } else if (status === 404) {
      errorMessage = '请求的资源不存在';
    } else if (status >= 500) {
      errorMessage = '服务器错误，请稍后重试';
    }
  } else if (error.request) {
    // 请求已发送但未收到响应
    errorMessage = '无法连接到服务器，请检查网络连接';
  }
  
  const enhancedError = new Error(errorMessage);
  enhancedError.originalError = error;
  enhancedError.isApiError = true;
  
  throw enhancedError;
};

const parkingApi = {
  // 车辆入场
  recordEntry: async (plateNumber, plateColor) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/parking/entry`, {
        plate_number: plateNumber,
        plate_color: plateColor
      });
      return response.data;
    } catch (error) {
      return handleApiError(error, '记录车辆入场');
    }
  },

  // 车辆出场
  recordExit: async (plateNumber) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/parking/exit`, {
        plate_number: plateNumber
      });
      return response.data;
    } catch (error) {
      return handleApiError(error, '记录车辆出场');
    }
  },

  // 获取停车场状态
  getParkingStatus: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/parking/status`);
      return response.data;
    } catch (error) {
      return handleApiError(error, '获取停车场状态');
    }
  },

  // 获取停车记录
  getParkingRecords: async (params) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/records`, { params });
      return response.data;
    } catch (error) {
      return handleApiError(error, '获取停车记录');
    }
  },

  // 识别车牌
  recognizePlate: async (imageFile) => {
    try {
      const formData = new FormData();
      formData.append('image', imageFile);
      
      const response = await axios.post(
        `${API_BASE_URL}/recognition/plate`, 
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      );
      return response.data;
    } catch (error) {
      return handleApiError(error, '识别车牌');
    }
  },

  // 处理视频帧识别
  processVideoFrame: async (frameData) => {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/auto-parking/process-frame`, 
        { frame_data: frameData }
      );
      return response.data;
    } catch (error) {
      return handleApiError(error, '处理视频帧');
    }
  },

  // 认证相关API
  login: async (username, password) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/login`, {
        username,
        password
      });
      return response.data;
    } catch (error) {
      return handleApiError(error, '用户登录');
    }
  },

  register: async (userData) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/register`, userData);
      return response.data;
    } catch (error) {
      return handleApiError(error, '用户注册');
    }
  },

  // 会员管理API
  getMembers: async (params) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/members`, { params });
      return response.data;
    } catch (error) {
      return handleApiError(error, '获取会员列表');
    }
  },

  getMemberById: async (id) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/members/${id}`);
      return response.data;
    } catch (error) {
      return handleApiError(error, '获取会员详情');
    }
  },

  createMember: async (memberData) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/members`, memberData);
      return response.data;
    } catch (error) {
      return handleApiError(error, '创建会员');
    }
  },

  updateMember: async (id, memberData) => {
    try {
      const response = await axios.put(`${API_BASE_URL}/members/${id}`, memberData);
      return response.data;
    } catch (error) {
      return handleApiError(error, '更新会员');
    }
  },

  deleteMember: async (id) => {
    try {
      const response = await axios.delete(`${API_BASE_URL}/members/${id}`);
      return response.data;
    } catch (error) {
      return handleApiError(error, '删除会员');
    }
  },

  // 停车记录详情API
  getRecordById: async (id) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/records/${id}`);
      return response.data;
    } catch (error) {
      return handleApiError(error, '获取停车记录详情');
    }
  },

  // 获取今日统计数据
  getTodayStats: async () => {
    try {
      const url = `${API_BASE_URL}/records/stats/today?_t=${Date.now()}`;
      const response = await axios.get(url);
      return response.data;
    } catch (error) {
      const fallbackResponse = {
        success: false,
        message: error.message || '获取今日统计数据失败',
        stats: {
          entries: 0,
          exits: 0,
          income: 0,
          timestamp: Date.now()
        }
      };
      console.error('获取今日统计数据失败:', error);
      return fallbackResponse;
    }
  }
};

export default parkingApi;
