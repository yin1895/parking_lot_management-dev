/**
 * 全局错误处理中间件
 * @param {Error} err - 错误对象
 * @param {Request} req - 请求对象
 * @param {Response} res - 响应对象
 * @param {Function} next - 下一个中间件
 */
function errorHandler(err, req, res, next) {
  console.error('应用错误:', err);
  
  // 区分不同类型的错误
  if (err.type === 'validation') {
    return res.status(400).json({
      success: false,
      error: {
        code: 'VALIDATION_ERROR',
        message: err.message
      }
    });
  }
  
  if (err.type === 'authentication') {
    return res.status(401).json({
      success: false,
      error: {
        code: 'AUTH_ERROR',
        message: err.message || '认证失败'
      }
    });
  }
  
  // 默认服务器错误
  const statusCode = err.statusCode || 500;
  res.status(statusCode).json({
    success: false,
    error: {
      code: err.code || 'SERVER_ERROR',
      message: process.env.NODE_ENV === 'production' 
        ? '服务器内部错误' 
        : (err.message || '未知错误')
    }
  });
}

module.exports = errorHandler;
