import logging
from flask import jsonify
from werkzeug.exceptions import HTTPException
from backend.utils.exceptions import AppError
from backend.utils.response import api_error

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    """注册全局错误处理器"""

    @app.errorhandler(AppError)
    def handle_app_error(error):
        logger.warning(f"AppError [{error.status_code}]: {error.message}")
        return api_error(message=error.message, status_code=error.status_code, errors=error.payload or None)

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        logger.warning(f"HTTPError [{error.code}]: {error.description}")
        return api_error(message=error.description or error.name, status_code=error.code)

    @app.errorhandler(Exception)
    def handle_generic_error(error):
        logger.exception(f"未捕获异常: {str(error)}")
        return api_error(message="服务器内部错误", status_code=500)
