"""测试 认证/权限装饰器 (decorators.py)"""
import pytest
from flask import Flask, g, jsonify
from unittest.mock import patch

from backend.utils.decorators import require_auth, require_role


def _make_test_app():
    """构建一个使用装饰器的测试路由"""
    app = Flask(__name__)
    app.config["TESTING"] = True

    @app.route("/protected")
    @require_auth
    def protected_view():
        return jsonify({"user": g.get("current_user")})

    @app.route("/admin")
    @require_role("admin")
    def admin_view():
        return jsonify({"role": g.get("current_user", {}).get("role")})

    return app


class TestRequireAuth:
    def test_no_token(self):
        app = _make_test_app()
        with app.test_client() as c:
            resp = c.get("/protected")
            assert resp.status_code == 401

    def test_malformed_header(self):
        app = _make_test_app()
        with app.test_client() as c:
            resp = c.get("/protected", headers={"Authorization": "NotBearer xyz"})
            assert resp.status_code == 401

    def test_invalid_token(self):
        app = _make_test_app()
        with patch("backend.services.auth_service.AuthService.verify_token", return_value=None):
            with app.test_client() as c:
                resp = c.get("/protected", headers={"Authorization": "Bearer fake-token"})
                assert resp.status_code == 401

    def test_valid_token(self):
        app = _make_test_app()
        fake_payload = {"sub": "1", "username": "alice", "role": "admin"}
        with patch("backend.services.auth_service.AuthService.verify_token", return_value=fake_payload):
            with app.test_client() as c:
                resp = c.get("/protected", headers={"Authorization": "Bearer good-token"})
                assert resp.status_code == 200


class TestRequireRole:
    def test_forbidden_when_wrong_role(self):
        app = _make_test_app()
        fake_payload = {"sub": "2", "username": "bob", "role": "user"}
        with patch("backend.services.auth_service.AuthService.verify_token", return_value=fake_payload):
            with app.test_client() as c:
                resp = c.get("/admin", headers={"Authorization": "Bearer good-token"})
                assert resp.status_code == 403

    def test_allowed_with_correct_role(self):
        app = _make_test_app()
        fake_payload = {"sub": "1", "username": "admin", "role": "admin"}
        with patch("backend.services.auth_service.AuthService.verify_token", return_value=fake_payload):
            with app.test_client() as c:
                resp = c.get("/admin", headers={"Authorization": "Bearer good-token"})
                assert resp.status_code == 200
