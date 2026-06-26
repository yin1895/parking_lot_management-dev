import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from backend.models.parking_record import ParkingRecord
from backend.models import db
from backend.utils.exceptions import NotFoundError, ValidationError

logger = logging.getLogger(__name__)


class RecordService:
    """停车记录查询服务"""

    @staticmethod
    def query(
        plate_number: str = None,
        start_date: str = None,
        end_date: str = None,
        page: int = 1,
        limit: int = 20,
    ) -> dict:
        page = max(1, page)
        limit = min(max(1, limit), 200)
        offset = (page - 1) * limit

        query = db.session.query(ParkingRecord)

        if plate_number:
            query = query.filter(ParkingRecord.plate_number == plate_number)

        if start_date:
            query = query.filter(ParkingRecord.entry_time >= datetime.fromisoformat(start_date))

        if end_date:
            query = query.filter(ParkingRecord.entry_time <= datetime.fromisoformat(end_date))

        total = query.count()
        records = (
            query.order_by(ParkingRecord.entry_time.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        return {
            "records": [r.to_dict() for r in records],
            "total": total,
            "page": page,
            "limit": limit,
        }

    @staticmethod
    def get_by_id(record_id: int) -> dict:
        record = db.session.query(ParkingRecord).get(record_id)
        if not record:
            raise NotFoundError("记录不存在")
        return record.to_dict()

    @staticmethod
    def get_today_stats() -> dict:
        """获取今日统计（入场数、出场数、收入）"""
        tz = ZoneInfo("Asia/Shanghai")
        now = datetime.now(tz)
        today_start = datetime(now.year, now.month, now.day, tzinfo=tz)
        tomorrow_start = today_start + timedelta(days=1)

        # 数据库存储为 UTC naive datetime，做范围转换
        today_start_utc = today_start.astimezone(ZoneInfo("UTC")).replace(tzinfo=None)
        tomorrow_start_utc = tomorrow_start.astimezone(ZoneInfo("UTC")).replace(tzinfo=None)

        entries_count = (
            db.session.query(ParkingRecord)
            .filter(
                ParkingRecord.entry_time >= today_start_utc,
                ParkingRecord.entry_time < tomorrow_start_utc,
            )
            .count()
        )

        exits_today = (
            db.session.query(ParkingRecord)
            .filter(
                ParkingRecord.exit_time >= today_start_utc,
                ParkingRecord.exit_time < tomorrow_start_utc,
            )
            .all()
        )
        exits_count = len(exits_today)
        total_income = round(sum(r.parking_fee or 0 for r in exits_today), 2)

        logger.info(f"今日统计: 入场={entries_count}, 出场={exits_count}, 收入={total_income}")

        return {
            "entries": entries_count,
            "exits": exits_count,
            "income": total_income,
            "timestamp": datetime.now().timestamp(),
        }
