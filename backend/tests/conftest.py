import pytest
from flask import Flask
from passlib.hash import pbkdf2_sha256

from backend.models import init_db, db
from backend.models.user import User
from backend.models.member import Member


@pytest.fixture(scope="function")
def app():
    """创建测试用 Flask 应用（SQLite 内存）"""
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "test-secret-key"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 86400
    app.config["PARKING_CAPACITY"] = 100

    init_db(app)
    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture(scope="function")
def db_session(app):
    """提供测试用的数据库会话"""
    with app.app_context():
        yield db.session
        db.session.rollback()


@pytest.fixture(scope="function")
def client(app):
    """Flask 测试客户端"""
    return app.test_client()


@pytest.fixture(scope="function")
def sample_user(db_session):
    """创建一个测试用户"""
    user = User(
        username="testuser",
        password=pbkdf2_sha256.hash("testpass"),
        email="test@example.com",
        role="admin",
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture(scope="function")
def sample_member(db_session):
    """创建一个测试会员"""
    member = Member(
        name="张三",
        plate_number="京A12345",
        phone="13800138000",
        status="active",
    )
    db_session.add(member)
    db_session.commit()
    return member


@pytest.fixture(scope="function", autouse=True)
def _clean_tables(db_session):
    """每个测试前清空所有表（除了每个 fixture 自己创建的数据）"""
    yield
