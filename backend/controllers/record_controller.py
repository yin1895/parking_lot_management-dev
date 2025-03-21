from flask import Blueprint, request, jsonify
from backend.models.parking_record import ParkingRecord
from backend.models import db_session
from datetime import datetime

record_bp = Blueprint('records', __name__)

@record_bp.route('', methods=['GET'])
def get_records():
    """获取停车记录"""
    try:
        # 获取查询参数
        plate_number = request.args.get('plate_number')
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 100))
        
        # 构建查询
        query = db_session.query(ParkingRecord)
        
        if plate_number:
            query = query.filter(ParkingRecord.plate_number == plate_number)
            
        if start_date_str:
            start_date = datetime.fromisoformat(start_date_str)
            query = query.filter(ParkingRecord.entry_time >= start_date)
            
        if end_date_str:
            end_date = datetime.fromisoformat(end_date_str)
            query = query.filter(ParkingRecord.entry_time <= end_date)
        
        # 获取总记录数
        total = query.count()
        
        # 分页
        records = query.order_by(ParkingRecord.entry_time.desc()).offset(skip).limit(limit).all()
        
        return jsonify({
            'success': True,
            'total': total,
            'records': [record.to_dict() for record in records],
            'page': skip // limit + 1 if limit > 0 else 1,
            'limit': limit,
            'pages': (total + limit - 1) // limit if limit > 0 else 1
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取停车记录失败: {str(e)}'
        }), 500

@record_bp.route('/<int:record_id>', methods=['GET'])
def get_record(record_id):
    """获取特定停车记录"""
    try:
        record = db_session.query(ParkingRecord).get(record_id)
        
        if not record:
            return jsonify({
                'success': False,
                'message': '记录不存在'
            }), 404
            
        return jsonify({
            'success': True,
            'record': record.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取停车记录失败: {str(e)}'
        }), 500
