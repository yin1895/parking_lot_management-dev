class AppError(Exception):
    """应用基础异常"""
    def __init__(self, message: str = "应用异常", status_code: int = 500, payload: dict = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload or {}


class NotFoundError(AppError):
    def __init__(self, message: str = "资源不存在", payload: dict = None):
        super().__init__(message, status_code=404, payload=payload)


class ValidationError(AppError):
    def __init__(self, message: str = "参数校验失败", payload: dict = None):
        super().__init__(message, status_code=400, payload=payload)


class AuthError(AppError):
    def __init__(self, message: str = "认证失败", payload: dict = None):
        super().__init__(message, status_code=401, payload=payload)


class ForbiddenError(AppError):
    def __init__(self, message: str = "权限不足", payload: dict = None):
        super().__init__(message, status_code=403, payload=payload)


class ConflictError(AppError):
    def __init__(self, message: str = "资源冲突", payload: dict = None):
        super().__init__(message, status_code=409, payload=payload)


class ServiceUnavailableError(AppError):
    def __init__(self, message: str = "服务暂不可用", payload: dict = None):
        super().__init__(message, status_code=503, payload=payload)
