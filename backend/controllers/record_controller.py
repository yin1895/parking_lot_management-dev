from flask import Blueprint, request, jsonify
from backend.models.parking_record import ParkingRecord
from backend.models import db_session
from datetime import datetime, timedelta

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

@record_bp.route('/stats/today', methods=['GET'])
def get_today_stats():
    """获取今日停车场统计数据"""
    try:
        # 使用UTC时区统一处理日期
        from datetime import datetime, timedelta, timezone
        
        # 获取当前服务器时区的今天日期范围
        local_tz = timezone(timedelta(hours=8))  # 假设服务器在东八区，根据实际情况调整
        now = datetime.now(local_tz)
        today_start = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=local_tz)
        tomorrow_start = today_start + timedelta(days=1)
        
        # 将时区信息转换为UTC进行数据库查询
        today_start_utc = today_start.astimezone(timezone.utc).replace(tzinfo=None)
        tomorrow_start_utc = tomorrow_start.astimezone(timezone.utc).replace(tzinfo=None)
        
        # 查询今日入场记录数
        entries_query = db_session.query(ParkingRecord).filter(
            ParkingRecord.entry_time >= today_start_utc,
            ParkingRecord.entry_time < tomorrow_start_utc
        )
        entries_count = entries_query.count()
        
        # 查询今日出场记录数
        exits_query = db_session.query(ParkingRecord).filter(
            ParkingRecord.exit_time >= today_start_utc,
            ParkingRecord.exit_time < tomorrow_start_utc
        )
        exits_count = exits_query.count()
        
        # 计算今日收入
        income_records = exits_query.all()
        total_income = sum(record.parking_fee or 0 for record in income_records)
        
        # 打印详细日志以便调试
        print(f"统计时间范围: {today_start_utc} 至 {tomorrow_start_utc}")
        print(f"今日入场: {entries_count}, 出场: {exits_count}, 收入: {total_income}")
        
        return jsonify({
            'success': True,
            'stats': {
                'entries': entries_count,
                'exits': exits_count,
                'income': round(total_income, 2),
                # 添加查询时间戳，前端可用来验证数据新鲜度
                'timestamp': datetime.now().timestamp()
            }
        })
    except Exception as e:
        import traceback
        print(f"获取今日统计数据异常: {str(e)}")
        print(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'message': f'获取统计数据失败: {str(e)}',
            'stats': {
                'entries': 0,
                'exits': 0,
                'income': 0,
                'timestamp': datetime.now().timestamp()
            }
        }), 500
