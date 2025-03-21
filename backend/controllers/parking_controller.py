from flask import Blueprint, request, jsonify
from backend.services.parking_service import ParkingService

parking_bp = Blueprint('parking', __name__)
parking_service = ParkingService()

@parking_bp.route('/entry', methods=['POST'])
def vehicle_entry():
    """车辆入场接口"""
    data = request.json
    plate_number = data.get('plate_number')
    plate_color = data.get('plate_color', '蓝色')
    
    if not plate_number:
        return jsonify({'success': False, 'message': '车牌号不能为空'}), 400
    
    result = parking_service.record_entry(plate_number, plate_color)
    return jsonify(result)

@parking_bp.route('/exit', methods=['POST'])
def vehicle_exit():
    """车辆出场接口"""
    data = request.json
    plate_number = data.get('plate_number')
    
    if not plate_number:
        return jsonify({'success': False, 'message': '车牌号不能为空'}), 400
    
    result = parking_service.record_exit(plate_number)
    return jsonify(result)

@parking_bp.route('/status', methods=['GET'])
def parking_status():
    """获取停车场状态"""
    status = parking_service.get_status()
    return jsonify(status)
