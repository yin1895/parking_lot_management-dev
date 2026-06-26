"""测试 认证服务 (auth_service.py)"""
import jwt
import pytest
from flask import Flask
from passlib.hash import pbkdf2_sha256

from backend.services.auth_service import AuthService
from backend.config.config import Config
from backend.models import init_db, db
from backend.models.user import User


@pytest.fixture
def auth_app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "test-key-which-is-long-enough-32b"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 86400
    init_db(app)
    with app.app_context():
        u = User(username="alice", password=pbkdf2_sha256.hash("secret"), role="user")
        db.session.add(u)
        db.session.commit()
    # Override JWT secret in Config for the scope of auth tests
    orig_key = Config.JWT_SECRET_KEY
    Config.JWT_SECRET_KEY = "test-key-which-is-long-enough-32b"
    yield app
    Config.JWT_SECRET_KEY = orig_key


class TestAuthenticate:
    def test_success(self, auth_app):
        with auth_app.app_context():
            result = AuthService.authenticate("alice", "secret")
        assert result is not None
        assert result["username"] == "alice"
        assert result["role"] == "user"

    def test_wrong_password(self, auth_app):
        with auth_app.app_context():
            result = AuthService.authenticate("alice", "wrong")
        assert result is None

    def test_unknown_user(self, auth_app):
        with auth_app.app_context():
            result = AuthService.authenticate("nobody", "x")
        assert result is None

    def test_empty_credentials(self, auth_app):
        with auth_app.app_context():
            assert AuthService.authenticate("", "") is None
            assert AuthService.authenticate("alice", "") is None


class TestCreateTokens:
    def test_returns_both_tokens(self):
        tokens = AuthService.create_tokens({"id": 1, "username": "alice", "role": "admin"})
        assert "access_token" in tokens
        assert "refresh_token" in tokens
        assert tokens["token_type"] == "Bearer"
        assert tokens["expires_in"] > 0

    def test_access_token_contains_claims(self):
        info = {"id": 42, "username": "bob", "role": "viewer"}
        tokens = AuthService.create_tokens(info)
        payload = AuthService.verify_token(tokens["access_token"])
        assert payload["sub"] == "42"
        assert payload["username"] == "bob"
        assert payload["role"] == "viewer"
        assert payload["type"] == "access"


class TestVerifyToken:
    def test_valid_token(self):
        tokens = AuthService.create_tokens({"id": 1, "username": "x", "role": "user"})
        payload = AuthService.verify_token(tokens["access_token"])
        assert payload is not None

    def test_expired_token_returns_none(self):
        expired = jwt.encode(
            {"sub": "1", "exp": 0},
            Config.JWT_SECRET_KEY, algorithm="HS256",
        )
        assert AuthService.verify_token(expired) is None

    def test_garbage_token_returns_none(self):
        assert AuthService.verify_token("not.a.token") is None


class TestRefreshAccess:
    def test_success(self, auth_app):
        with auth_app.app_context():
            tokens = AuthService.create_tokens({"id": 1, "username": "alice", "role": "user"})
            new_tokens = AuthService.refresh_access(tokens["refresh_token"])
        assert new_tokens is not None
        assert new_tokens is not None
        assert "access_token" in new_tokens

    def test_invalid_refresh_token_returns_none(self):
        tokens = AuthService.create_tokens({"id": 1, "username": "alice", "role": "user"})
        result = AuthService.refresh_access(tokens["access_token"])
        assert result is None

    def test_refresh_user_not_found(self, auth_app):
        tokens = AuthService.create_tokens({"id": 9999, "username": "ghost", "role": "user"})
        with auth_app.app_context():
            result = AuthService.refresh_access(tokens["refresh_token"])
        assert result is None
