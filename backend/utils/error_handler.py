"""
统一错误处理机制
提供标准化的错误响应和日志记录
"""
import logging
import datetime
from flask import jsonify, request
from werkzeug.exceptions import HTTPException, BadRequest, Unauthorized, Forbidden, NotFound, MethodNotAllowed, InternalServerError


# 配置日志
error_logger = logging.getLogger('parking_errors')
error_handler_logger = logging.getLogger('error_handler')


class ParkingError(Exception):
    """停车场系统自定义异常基类"""
    def __init__(self, message, error_code=None, status_code=400, details=None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or 'PARKING_ERROR'
        self.status_code = status_code
        self.details = details or {}


class ValidationError(ParkingError):
    """数据验证错误"""
    def __init__(self, message, field=None, details=None):
        super().__init__(message, 'VALIDATION_ERROR', 400, details or {})
        self.details['field'] = field


class AuthenticationError(ParkingError):
    """认证错误"""
    def __init__(self, message='认证失败', details=None):
        super().__init__(message, 'AUTHENTICATION_ERROR', 401, details or {})


class PermissionError(ParkingError):
    """权限错误"""
    def __init__(self, message='权限不足', details=None):
        super().__init__(message, 'PERMISSION_ERROR', 403, details or {})


class NotFoundError(ParkingError):
    """资源不存在错误"""
    def __init__(self, message='资源不存在', resource=None, details=None):
        super().__init__(message, 'NOT_FOUND_ERROR', 404, details or {})
        self.details['resource'] = resource


class ConflictError(ParkingError):
    """资源冲突错误"""
    def __init__(self, message='资源冲突', resource=None, details=None):
        super().__init__(message, 'CONFLICT_ERROR', 409, details or {})
        self.details['resource'] = resource


class DatabaseError(ParkingError):
    """数据库错误"""
    def __init__(self, message='数据库操作失败', details=None):
        super().__init__(message, 'DATABASE_ERROR', 500, details or {})


def create_error_response(error_code, message, status_code=400, details=None):
    """创建标准化错误响应"""
    response = {
        'success': False,
        'error': {
            'code': error_code,
            'message': message,
            'status_code': status_code,
            'timestamp': datetime.datetime.now().isoformat()
        }
    }
    
    if details:
        response['error']['details'] = details
    
    return response, status_code


def log_error(error, context=None):
    """记录错误日志"""
    error_info = {
        'error_type': type(error).__name__,
        'error_message': str(error),
        'request_url': request.url if request else None,
        'request_method': request.method if request else None,
        'request_headers': dict(request.headers) if request else None,
        'context': context or {}
    }
    
    # 记录不同级别的日志
    if isinstance(error, (ValidationError, NotFoundError, ConflictError)):
        error_logger.warning(f"业务错误: {error_info}")
    elif isinstance(error, (AuthenticationError, PermissionError)):
        error_logger.warning(f"权限错误: {error_info}")
    elif isinstance(error, DatabaseError):
        error_logger.error(f"数据库错误: {error_info}")
    else:
        error_logger.error(f"系统错误: {error_info}")
    
    # 同时记录到error_handler logger
    error_handler_logger.error(f"Error details: {error_info}")


def register_error_handlers(app):
    """注册所有错误处理器"""
    
    # HTTP异常处理
    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        # 记录HTTP错误
        error_info = {
            'http_status': error.code,
            'error_name': error.name,
            'description': error.description,
            'request_url': request.url,
            'request_method': request.method
        }
        error_logger.warning(f"HTTP错误: {error_info}")
        
        response = {
            'success': False,
            'error': {
                'code': f'HTTP_{error.code}',
                'message': error.description,
                'status_code': error.code,
                'name': error.name
            }
        }
        return jsonify(response), error.code
    
    # 自定义业务异常处理
    @app.errorhandler(ParkingError)
    def handle_parking_error(error):
        log_error(error)
        return create_error_response(
            error.error_code, 
            error.message, 
            error.status_code, 
            error.details
        )
    
    # 通用异常处理
    @app.errorhandler(Exception)
    def handle_generic_error(error):
        log_error(error, {'exception_type': 'generic'})
        
        # 在生产环境中隐藏具体错误信息
        if app.config.get('DEBUG'):
            error_message = str(error)
            error_details = {'traceback': str(error.__traceback__)}
        else:
            error_message = '系统内部错误'
            error_details = None
        
        return create_error_response(
            'INTERNAL_SERVER_ERROR',
            error_message,
            500,
            error_details
        )
    
    # 404错误处理
    @app.errorhandler(404)
    def handle_not_found(error):
        log_error(NotFoundError('请求的资源不存在'), {'path': request.path})
        return create_error_response(
            'NOT_FOUND',
            '请求的资源不存在',
            404,
            {'path': request.path}
        )
    
    # 405错误处理
    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        log_error(error, {'method': request.method, 'path': request.path})
        return create_error_response(
            'METHOD_NOT_ALLOWED',
            f'不支持的HTTP方法: {request.method}',
            405,
            {'method': request.method, 'path': request.path}
        )
    
    # 400错误处理
    @app.errorhandler(400)
    def handle_bad_request(error):
        log_error(error, {'description': str(error)})
        return create_error_response(
            'BAD_REQUEST',
            '请求参数错误',
            400,
            {'description': str(error)}
        )
    
    # 500错误处理
    @app.errorhandler(500)
    def handle_internal_server_error(error):
        log_error(error, {'error': str(error)})
        return create_error_response(
            'INTERNAL_SERVER_ERROR',
            '服务器内部错误',
            500,
            {'error': '服务器遇到了一个意外情况，无法完成请求'}
        )
