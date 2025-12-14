"""
响应工具
提供标准化的API响应格式
"""
from flask import jsonify
from typing import Any, Dict, Optional, List


def success_response(data: Any = None, message: str = "操作成功", status_code: int = 200) -> tuple:
    """创建成功响应"""
    response = {
        'success': True,
        'message': message
    }
    
    if data is not None:
        response['data'] = data
    
    return jsonify(response), status_code


def error_response(message: str, error_code: str = "ERROR", status_code: int = 400, details: Optional[Dict] = None) -> tuple:
    """创建错误响应"""
    response = {
        'success': False,
        'error': {
            'code': error_code,
            'message': message,
            'status_code': status_code
        }
    }
    
    if details:
        response['error']['details'] = details
    
    return jsonify(response), status_code


def paginated_response(items: List, page: int, per_page: int, total: int, message: str = "查询成功") -> tuple:
    """创建分页响应"""
    pages = (total + per_page - 1) // per_page
    
    response = {
        'success': True,
        'message': message,
        'data': items,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': pages,
            'has_next': page < pages,
            'has_prev': page > 1
        }
    }
    
    return jsonify(response), 200


def validation_error_response(field: str, message: str) -> tuple:
    """创建验证错误响应"""
    response = {
        'success': False,
        'error': {
            'code': 'VALIDATION_ERROR',
            'message': f'{field}: {message}',
            'status_code': 400,
            'field': field
        }
    }
    
    return jsonify(response), 400


def not_found_response(resource: str = "资源") -> tuple:
    """创建资源不存在响应"""
    return error_response(
        f"{resource}不存在", 
        "NOT_FOUND", 
        404
    )


def unauthorized_response(message: str = "未授权访问") -> tuple:
    """创建未授权响应"""
    return error_response(
        message, 
        "UNAUTHORIZED", 
        401
    )


def forbidden_response(message: str = "权限不足") -> tuple:
    """创建权限不足响应"""
    return error_response(
        message, 
        "FORBIDDEN", 
        403
    )


def conflict_response(message: str, details: Optional[Dict] = None) -> tuple:
    """创建冲突响应"""
    return error_response(
        message, 
        "CONFLICT", 
        409, 
        details
    )


def internal_error_response(message: str = "内部服务器错误", details: Optional[Dict] = None) -> tuple:
    """创建内部服务器错误响应"""
    return error_response(
        message, 
        "INTERNAL_ERROR", 
        500, 
        details
    )
