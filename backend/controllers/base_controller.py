"""
控制器基类
提供通用的控制器功能和代码复用
"""
from flask import Blueprint, request, jsonify
from backend.utils.response_utils import success_response, error_response
from backend.utils.validators import BaseValidator
from backend.utils.error_handler import (
    ValidationError, NotFoundError, ConflictError, DatabaseError,
    AuthenticationError, PermissionError
)
from backend.middleware.auth_middleware import token_required, admin_required
from backend.models import db_session


class BaseController:
    """控制器基类"""
    
    def __init__(self, blueprint_name: str):
        self.bp = Blueprint(blueprint_name, __name__)
        self.db_session = db_session
    
    def validate_required_fields(self, data: dict, required_fields: list) -> dict:
        """验证必填字段"""
        validated_data = {}
        for field in required_fields:
            if field not in data:
                raise ValidationError(f"缺少必需字段: {field}", field=field)
            validated_data[field] = data[field]
        return validated_data
    
    def handle_validation_error(self, func):
        """处理验证错误的装饰器"""
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValidationError as e:
                return error_response(e.message, "VALIDATION_ERROR", 400, e.details)
            except NotFoundError as e:
                return error_response(e.message, "NOT_FOUND_ERROR", 404, e.details)
            except ConflictError as e:
                return error_response(e.message, "CONFLICT_ERROR", 409, e.details)
            except (AuthenticationError, PermissionError) as e:
                return error_response(e.message, e.error_code, e.status_code)
            except DatabaseError as e:
                return error_response(e.message, "DATABASE_ERROR", 500)
            except Exception as e:
                return error_response(f"操作失败: {str(e)}", "INTERNAL_ERROR", 500)
        return wrapper
    
    def get_pagination_params(self) -> tuple:
        """获取分页参数"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # 限制每页最大数量
        if per_page > 100:
            per_page = 100
        
        return page, per_page
    
    def get_filter_params(self, allowed_filters: list) -> dict:
        """获取过滤参数"""
        filters = {}
        for param in allowed_filters:
            if param in request.args:
                filters[param] = request.args.get(param)
        return filters


class BaseResourceController(BaseController):
    """资源控制器基类"""
    
    def __init__(self, blueprint_name: str, model_class, validator_class=None):
        super().__init__(blueprint_name)
        self.model_class = model_class
        self.validator_class = validator_class
        self.setup_routes()
    
    def setup_routes(self):
        """设置默认路由"""
        # 这些方法需要在子类中实现
        pass
    
    def handle_get_list(self, get_items_func):
        """处理获取列表请求"""
        page, per_page = self.get_pagination_params()
        filters = self.get_filter_params(['plate_number', 'name', 'status'])
        
        items, total = get_items_func(page=page, per_page=per_page, **filters)
        
        return success_response({
            'items': [item.to_dict() if hasattr(item, 'to_dict') else item for item in items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        })
    
    def handle_get_one(self, get_item_func, item_id):
        """处理获取单个资源请求"""
        item = get_item_func(item_id)
        if not item:
            raise NotFoundError(f"ID为 {item_id} 的资源不存在")
        
        return success_response(item.to_dict() if hasattr(item, 'to_dict') else item)
    
    def handle_create(self, create_func, validate_func=None):
        """处理创建请求"""
        if not request.is_json:
            raise ValidationError("请求必须是JSON格式")
        
        data = request.get_json()
        if validate_func:
            validated_data = validate_func(data)
        else:
            validated_data = data
        
        result = create_func(validated_data)
        return success_response(result, "创建成功", 201)
    
    def handle_update(self, update_func, item_id, validate_func=None):
        """处理更新请求"""
        if not request.is_json:
            raise ValidationError("请求必须是JSON格式")
        
        data = request.get_json()
        if validate_func:
            validated_data = validate_func(data)
        else:
            validated_data = data
        
        result = update_func(item_id, validated_data)
        return success_response(result, "更新成功")
    
    def handle_delete(self, delete_func, item_id):
        """处理删除请求"""
        result = delete_func(item_id)
        return success_response(result, "删除成功")
    
    def protected_route(self, methods, handler, require_admin=False):
        """创建受保护的路由"""
        decorators = []
        if require_admin:
            decorators.append(admin_required)
        else:
            decorators.append(token_required)
        
        route_decorator = self.bp.route('/', methods=methods)
        for decorator in reversed(decorators):
            route_decorator = decorator(route_decorator)
        
        route_decorator(self.handle_validation_error(handler))
    
    def public_route(self, methods, handler):
        """创建公开的路由"""
        route_decorator = self.bp.route('/', methods=methods)
        route_decorator(self.handle_validation_error(handler))
