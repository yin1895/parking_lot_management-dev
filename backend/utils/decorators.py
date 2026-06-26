import functools
import logging
from flask import request, g
from backend.utils.response import api_error

logger = logging.getLogger(__name__)


def require_auth(f):
    """要求用户已登录（检查 JWT）"""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        from backend.services.auth_service import AuthService
        token = _extract_token()
        if not token:
            return api_error("缺少认证令牌", 401)
        payload = AuthService.verify_token(token)
        if not payload:
            return api_error("令牌无效或已过期", 401)
        g.current_user = {
            "id": payload.get("sub"),
            "username": payload.get("username"),
            "role": payload.get("role", "user"),
        }
        return f(*args, **kwargs)
    return wrapper


def require_role(*roles):
    """要求指定角色"""
    def decorator(f):
        @functools.wraps(f)
        @require_auth
        def wrapper(*args, **kwargs):
            if g.current_user.get("role") not in roles:
                return api_error("权限不足", 403)
            return f(*args, **kwargs)
        return wrapper
    return decorator


def _extract_token():
    """从请求头提取令牌"""
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth[7:]
    return None
