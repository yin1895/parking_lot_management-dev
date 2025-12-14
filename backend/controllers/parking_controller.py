from flask import Blueprint, request, jsonify
from backend.services.parking_service import ParkingService
from backend.middleware.auth_middleware import validate_jwt_optional, admin_required

parking_bp = Blueprint('parking', __name__)
parking_service = ParkingService()

@parking_bp.route('/entry', methods=['POST'])
@validate_jwt_optional
def vehicle_entry(current_user):
    """车辆入场接口 - 支持可选认证"""
    data = request.json
    plate_number = data.get('plate_number')
    plate_color = data.get('plate_color', '蓝色')
    
    if not plate_number:
        return jsonify({'success': False, 'message': '车牌号不能为空'}), 400
    
    # 记录操作员信息（如果已认证）
    operator_info = f" (操作员: {current_user.username})" if current_user else ""
    
    result = parking_service.record_entry(plate_number, plate_color)
    if result['success']:
        result['message'] += operator_info
    
    return jsonify(result)

@parking_bp.route('/exit', methods=['POST'])
@validate_jwt_optional
def vehicle_exit(current_user):
    """车辆出场接口 - 支持可选认证"""
    data = request.json
    plate_number = data.get('plate_number')
    
    if not plate_number:
        return jsonify({'success': False, 'message': '车牌号不能为空'}), 400
    
    # 记录操作员信息（如果已认证）
    operator_info = f" (操作员: {current_user.username})" if current_user else ""
    
    result = parking_service.record_exit(plate_number)
    if result['success']:
        result['message'] += operator_info
    
    return jsonify(result)

@parking_bp.route('/status', methods=['GET'])
@admin_required
def parking_status(current_user):
    """获取停车场状态 - 需要管理员权限"""
    status = parking_service.get_status()
    return jsonify(status)
