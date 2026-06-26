from typing import Any, Optional
from flask import jsonify


def api_success(data: Any = None, message: str = "操作成功", status_code: int = 200):
    """统一成功响应"""
    body = {"success": True, "message": message}
    if data is not None:
        body["data"] = data
    return jsonify(body), status_code


def api_error(message: str = "操作失败", status_code: int = 400, errors: Optional[dict] = None):
    """统一错误响应"""
    body = {"success": False, "message": message}
    if errors:
        body["errors"] = errors
    return jsonify(body), status_code


def api_paginated(
    items: list,
    total: int,
    page: int,
    limit: int,
    extra: Optional[dict] = None,
):
    """统一分页响应"""
    pages = max(1, (total + limit - 1) // limit) if limit > 0 else 1
    body = {
        "success": True,
        "data": items,
        "pagination": {
            "total": total,
            "page": page,
            "limit": limit,
            "pages": pages,
            "has_next": page < pages,
            "has_prev": page > 1,
        },
    }
    if extra:
        body.update(extra)
    return jsonify(body), 200
