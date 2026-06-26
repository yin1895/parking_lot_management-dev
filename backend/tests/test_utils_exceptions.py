"""测试 自定义异常类 (exceptions.py)"""
from backend.utils.exceptions import (
    AppError, NotFoundError, ValidationError, AuthError,
    ForbiddenError, ConflictError, ServiceUnavailableError,
)


class TestAppError:
    def test_defaults(self):
        err = AppError()
        assert err.message == "应用异常"
        assert err.status_code == 500
        assert err.payload == {}

    def test_custom(self):
        err = AppError("自定义", 418, {"detail": "teapot"})
        assert err.message == "自定义"
        assert err.status_code == 418
        assert err.payload["detail"] == "teapot"


class TestSpecificErrors:
    def test_not_found(self):
        err = NotFoundError()
        assert err.status_code == 404
        assert err.message == "资源不存在"

    def test_validation(self):
        err = ValidationError("参数错")
        assert err.status_code == 400
        assert err.message == "参数错"

    def test_auth(self):
        err = AuthError()
        assert err.status_code == 401
        assert err.message == "认证失败"

    def test_forbidden(self):
        err = ForbiddenError("没权限")
        assert err.status_code == 403
        assert err.message == "没权限"

    def test_conflict(self):
        err = ConflictError("已存在")
        assert err.status_code == 409
        assert err.message == "已存在"

    def test_service_unavailable(self):
        err = ServiceUnavailableError()
        assert err.status_code == 503
        assert err.message == "服务暂不可用"
