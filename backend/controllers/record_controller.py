from flask import Blueprint, request
from backend.services.record_service import RecordService
from backend.utils.response import api_success, api_error, api_paginated

record_bp = Blueprint('records', __name__)


@record_bp.route('', methods=['GET'])
def get_records():
    """获取停车记录（分页+筛选）"""
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 20))
    result = RecordService.query(
        plate_number=request.args.get("plate_number"),
        start_date=request.args.get("start_date"),
        end_date=request.args.get("end_date"),
        page=page,
        limit=limit,
    )
    return api_paginated(
        items=result["records"],
        total=result["total"],
        page=result["page"],
        limit=result["limit"],
    )


@record_bp.route('/<int:record_id>', methods=['GET'])
def get_record(record_id):
    """获取特定停车记录"""
    try:
        record = RecordService.get_by_id(record_id)
        return api_success({"record": record})
    except Exception as e:
        return api_error(str(e), getattr(e, "status_code", 500))


@record_bp.route('/stats/today', methods=['GET'])
def get_today_stats():
    """获取今日停车场统计数据"""
    try:
        stats = RecordService.get_today_stats()
        return api_success({"stats": stats})
    except Exception as e:
        return api_error(f"获取统计数据失败: {str(e)}", 500)
