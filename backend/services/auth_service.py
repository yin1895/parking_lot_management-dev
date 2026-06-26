import logging
from datetime import datetime, timedelta

import jwt
from passlib.hash import pbkdf2_sha256

from backend.config.config import Config
from backend.models.user import User
from backend.models import db

logger = logging.getLogger(__name__)


class AuthService:
    """认证服务：注册、登录、令牌管理"""

    @staticmethod
    def authenticate(username: str, password: str) -> dict:
        """验证用户凭据，返回用户信息"""
        user = db.session.query(User).filter_by(username=username).first()
        if not user or not pbkdf2_sha256.verify(password, user.password):
            logger.warning(f"登录失败: 用户名={username}")
            return None
        return {"id": user.id, "username": user.username, "role": user.role}

    @staticmethod
    def create_tokens(user_info: dict) -> dict:
        """生成 access + refresh 令牌对"""
        now = datetime.utcnow()
        access_payload = {
            "sub": str(user_info["id"]),
            "username": user_info["username"],
            "role": user_info["role"],
            "type": "access",
            "iat": now,
            "exp": now + timedelta(seconds=Config.JWT_ACCESS_TOKEN_EXPIRES),
        }
        refresh_payload = {
            "sub": str(user_info["id"]),
            "type": "refresh",
            "iat": now,
            "exp": now + timedelta(seconds=Config.JWT_REFRESH_TOKEN_EXPIRES),
        }
        return {
            "access_token": jwt.encode(access_payload, Config.JWT_SECRET_KEY, algorithm="HS256"),
            "refresh_token": jwt.encode(refresh_payload, Config.JWT_SECRET_KEY, algorithm="HS256"),
            "token_type": "Bearer",
            "expires_in": Config.JWT_ACCESS_TOKEN_EXPIRES,
        }

    @staticmethod
    def verify_token(token: str) -> dict:
        """验证并解码令牌"""
        try:
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            logger.debug("令牌已过期")
            return None
        except jwt.InvalidTokenError as e:
            logger.debug(f"令牌无效: {e}")
            return None

    @staticmethod
    def refresh_access(refresh_token: str) -> dict:
        """用 refresh token 换取新的 access token"""
        payload = AuthService.verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            return None
        user_info = {"id": int(payload["sub"])}
        user = db.session.query(User).get(user_info["id"])
        if not user:
            return None
        return AuthService.create_tokens({
            "id": user.id,
            "username": user.username,
            "role": user.role,
        })
