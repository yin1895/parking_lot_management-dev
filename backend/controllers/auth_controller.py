from flask import Blueprint, request
from backend.services.auth_service import AuthService
from backend.utils.response import api_success, api_error
from backend.utils.limiter import limiter

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    """用户登录，返回 access + refresh 令牌对"""
    data = request.json or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return api_error("用户名和密码不能为空", 400)

    user_info = AuthService.authenticate(username, password)
    if not user_info:
        return api_error("用户名或密码错误", 401)

    tokens = AuthService.create_tokens(user_info)
    return api_success({
        **tokens,
        "user": user_info,
    }, "登录成功")


@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    from backend.models.user import User
    from backend.models import db
    from passlib.hash import pbkdf2_sha256

    data = request.json or {}
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if not username or not password:
        return api_error("用户名和密码不能为空", 400)

    existing = db.session.query(User).filter_by(username=username).first()
    if existing:
        return api_error(f"用户名 {username} 已存在", 400)

    user = User(
        username=username,
        password=pbkdf2_sha256.hash(password),
        email=email,
        role="user",
    )
    db.session.add(user)
    db.session.commit()
    return api_success({
        "id": user.id,
        "username": user.username,
        "role": user.role,
    }, "用户注册成功", 201)


@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    """用 refresh token 换取新的 access token"""
    data = request.json or {}
    refresh_token = data.get("refresh_token")
    if not refresh_token:
        return api_error("缺少 refresh_token", 400)

    tokens = AuthService.refresh_access(refresh_token)
    if not tokens:
        return api_error("refresh_token 无效或已过期", 401)
    return api_success(tokens, "令牌刷新成功")
