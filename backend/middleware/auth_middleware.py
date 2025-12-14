"""
API身份验证中间件
用于保护需要认证的API端点
"""
import jwt
from functools import wraps
from flask import request
from backend.config.config import Config
from backend.models.user import User
from backend.models import db_session
from backend.utils.response_utils import unauthorized_response, forbidden_response


def token_required(f):
    """JWT令牌验证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # 从请求头获取令牌
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                # 支持 "Bearer <token>" 格式
                if auth_header.startswith('Bearer '):
                    token = auth_header.split(' ')[1]
                else:
                    token = auth_header
            except Exception:
                return unauthorized_response('令牌格式无效')
        
        if not token:
            return unauthorized_response('缺少认证令牌')
        
        try:
            # 验证令牌
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
            
            # 从数据库获取用户信息
            current_user = db_session.query(User).filter_by(id=payload['sub']).first()
            if not current_user:
                return unauthorized_response('用户不存在')
            
            # 将用户信息传递给被装饰的函数
            return f(current_user=current_user, *args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            return unauthorized_response('令牌已过期')
        except jwt.InvalidTokenError:
            return unauthorized_response('令牌无效')
        except Exception as e:
            return unauthorized_response(f'认证失败: {str(e)}')
    
    return decorated


def admin_required(f):
    """管理员权限验证装饰器"""
    @wraps(f)
    @token_required
    def decorated(current_user, *args, **kwargs):
        if current_user.role != 'admin':
            return forbidden_response('需要管理员权限')
        
        return f(*args, **kwargs)
    
    return decorated


def validate_jwt_optional(f):
    """可选的JWT验证装饰器（不强制要求认证）"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        current_user = None
        
        # 从请求头获取令牌（如果存在）
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                if auth_header.startswith('Bearer '):
                    token = auth_header.split(' ')[1]
                else:
                    token = auth_header
                
                if token:
                    # 验证令牌
                    payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
                    current_user = db_session.query(User).filter_by(id=payload['sub']).first()
                    
            except jwt.ExpiredSignatureError:
                # 令牌过期，返回空用户但不阻止请求
                current_user = None
            except jwt.InvalidTokenError:
                # 令牌无效，返回空用户但不阻止请求
                current_user = None
            except Exception:
                # 其他错误，返回空用户但不阻止请求
                current_user = None
        
        # 将用户信息传递给被装饰的函数（可能为None）
        return f(current_user=current_user, *args, **kwargs)
    
    return decorated
