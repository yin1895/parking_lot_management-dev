from flask import Blueprint, request, jsonify
from backend.models.user import User
from backend.models import db_session
# 替换为 pbkdf2_sha256
from passlib.hash import pbkdf2_sha256
import datetime
import jwt
from backend.config.config import Config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': '用户名和密码不能为空'
            }), 400
            
        # 查询用户
        user = db_session.query(User).filter_by(username=username).first()
        
        # 验证密码 - 使用 pbkdf2_sha256
        if not user or not pbkdf2_sha256.verify(password, user.password):
            return jsonify({
                'success': False,
                'message': '用户名或密码错误'
            }), 401
            
        # 生成JWT令牌
        expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=Config.JWT_ACCESS_TOKEN_EXPIRES)
        payload = {
            'sub': user.id,
            'username': user.username,
            'role': user.role,
            'exp': expiration
        }
        token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')
        
        return jsonify({
            'success': True,
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'role': user.role
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'登录失败: {str(e)}'
        }), 500
        
@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': '用户名和密码不能为空'
            }), 400
            
        # 检查用户名是否已存在
        existing = db_session.query(User).filter_by(username=username).first()
        if existing:
            return jsonify({
                'success': False,
                'message': f'用户名 {username} 已存在'
            }), 400
            
        # 创建新用户 - 使用 pbkdf2_sha256
        hashed_password = pbkdf2_sha256.hash(password)
        user = User(
            username=username,
            password=hashed_password,
            email=email,
            role='user'  # 默认为普通用户
        )
        
        db_session.add(user)
        db_session.commit()
        
        return jsonify({
            'success': True,
            'message': '用户注册成功',
            'user': {
                'id': user.id,
                'username': user.username,
                'role': user.role
            }
        }), 201
    except Exception as e:
        db_session.rollback()
        return jsonify({
            'success': False,
            'message': f'注册失败: {str(e)}'
        }), 500
