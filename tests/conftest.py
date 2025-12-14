"""
测试配置文件
提供测试所需的公共fixtures和配置
"""
import pytest
import tempfile
import os
from unittest.mock import Mock, patch

# 测试配置
@pytest.fixture
def test_config():
    """测试配置"""
    return {
        'SECRET_KEY': 'test-secret-key-for-unit-tests',
        'JWT_ACCESS_TOKEN_EXPIRES': 3600,
        'DATABASE_URL': 'sqlite:///:memory:',
        'TESTING': True
    }

@pytest.fixture
def mock_db_session():
    """模拟数据库会话"""
    session = Mock()
    session.query.return_value = Mock()
    session.add.return_value = None
    session.commit.return_value = None
    session.rollback.return_value = None
    return session

@pytest.fixture
def sample_user_data():
    """示例用户数据"""
    return {
        'username': 'testuser',
        'password': 'TestPassword123',
        'email': 'test@example.com'
    }

@pytest.fixture
def sample_member_data():
    """示例会员数据"""
    return {
        'name': '张三',
        'plate_number': '京A12345',
        'phone': '13812345678',
        'status': 'active'
    }

@pytest.fixture
def sample_parking_data():
    """示例停车数据"""
    return {
        'plate_number': '京A12345',
        'plate_color': '蓝色'
    }

@pytest.fixture
def valid_jwt_token():
    """有效的JWT令牌"""
    import jwt
    from backend.config.config import Config
    
    payload = {
        'sub': 1,
        'username': 'testuser',
        'role': 'user',
        'exp': 9999999999  # 过期时间设置为很远
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

@pytest.fixture
def admin_jwt_token():
    """管理员JWT令牌"""
    import jwt
    from backend.config.config import Config
    
    payload = {
        'sub': 1,
        'username': 'admin',
        'role': 'admin',
        'exp': 9999999999
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

@pytest.fixture
def test_app():
    """测试应用实例"""
    from backend.app import app
    
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['JWT_SECRET_KEY'] = 'test-jwt-secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        # 在应用上下文中创建所有表
        from backend.models import db
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(test_app):
    """测试客户端"""
    return test_app.test_client()
