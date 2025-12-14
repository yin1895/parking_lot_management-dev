from sqlalchemy import Column, String, Float, DateTime, Index
from sqlalchemy.orm import joinedload
from backend.models.base import BaseModel
from backend.models import db_session

class ParkingRecord(BaseModel):
    __tablename__ = 'parking_records'

    plate_number = Column(String(20), nullable=False)
    plate_color = Column(String(10), default='蓝色')
    entry_time = Column(DateTime, nullable=False)
    exit_time = Column(DateTime, nullable=True)
    parking_fee = Column(Float, nullable=True)
    
    # 创建索引优化查询性能
    __table_args__ = (
        Index('idx_plate_number_active', 'plate_number', 'exit_time'),
        Index('idx_entry_time', 'entry_time'),
        Index('idx_exit_time', 'exit_time'),
        Index('idx_plate_number_entry', 'plate_number', 'entry_time'),
    )

    @staticmethod
    def get_active_by_plate(plate_number):
        """获取当前在场的车辆记录"""
        try:
            return db_session.query(ParkingRecord)\
                .filter_by(plate_number=plate_number, exit_time=None)\
                .first()
        except Exception:
            return None

    @staticmethod
    def count_active():
        """统计当前在场车辆数量"""
        try:
            return db_session.query(ParkingRecord)\
                .filter_by(exit_time=None)\
                .count()
        except Exception:
            return 0
            
    @staticmethod
    def get_active_with_member_info(plate_number):
        """获取当前在场车辆记录并包含会员信息 - 优化查询"""
        try:
            # 使用联表查询，一次性获取车辆记录和会员信息
            from backend.models.member import Member
            
            # 先查询车辆记录
            record = db_session.query(ParkingRecord)\
                .filter_by(plate_number=plate_number, exit_time=None)\
                .first()
            
            if not record:
                return None, None
            
            # 查询会员信息
            member = db_session.query(Member)\
                .filter_by(plate_number=plate_number, status='active')\
                .first()
            
            return record, member
        except Exception:
            return None, None
    
    @staticmethod
    def get_parking_records_with_pagination(page=1, per_page=20, plate_number=None, start_date=None, end_date=None):
        """分页查询停车记录 - 优化查询"""
        try:
            query = db_session.query(ParkingRecord)
            
            # 添加过滤条件
            if plate_number:
                query = query.filter(ParkingRecord.plate_number.contains(plate_number))
            
            if start_date:
                query = query.filter(ParkingRecord.entry_time >= start_date)
                
            if end_date:
                query = query.filter(ParkingRecord.entry_time <= end_date)
            
            # 按入场时间降序排列
            query = query.order_by(ParkingRecord.entry_time.desc())
            
            # 分页查询
            records = query.limit(per_page).offset((page - 1) * per_page).all()
            
            # 获取总记录数
            total = query.count()
            
            return records, total
        except Exception:
            return [], 0
    
    @staticmethod
    def get_parking_statistics(start_date=None, end_date=None):
        """获取停车统计信息 - 优化查询"""
        try:
            from sqlalchemy import func
            
            query = db_session.query(ParkingRecord)
            
            # 添加时间范围过滤
            if start_date:
                query = query.filter(ParkingRecord.entry_time >= start_date)
            if end_date:
                query = query.filter(ParkingRecord.entry_time <= end_date)
            
            # 统计总车辆数、平均停车时间、总收入等
            active_records_count = db_session.query(ParkingRecord)\
                .filter(ParkingRecord.exit_time.is_(None))\
                .count()
                
            completed_records_count = db_session.query(ParkingRecord)\
                .filter(ParkingRecord.exit_time.isnot(None))\
                .count()
            
            total_revenue = db_session.query(func.sum(ParkingRecord.parking_fee))\
                .filter(ParkingRecord.parking_fee.isnot(None))\
                .scalar() or 0
            
            stats = {
                'total_records': query.count(),
                'active_records': active_records_count,
                'completed_records': completed_records_count,
                'total_revenue': float(total_revenue),
                'average_parking_time': None  # 这里可以添加平均停车时间计算
            }
            
            return stats
        except Exception:
            return {
                'total_records': 0,
                'active_records': 0,
                'completed_records': 0,
                'total_revenue': 0,
                'average_parking_time': None
            }
        
    def to_dict(self):
        """将模型转换为字典"""
        return {
            'id': self.id,
            'plate_number': self.plate_number,
            'plate_color': self.plate_color,
            'entry_time': self.entry_time.isoformat() if self.entry_time else None,
            'exit_time': self.exit_time.isoformat() if self.exit_time else None,
            'parking_fee': self.parking_fee,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
    def save(self):
        """保存更改到数据库"""
        try:
            db_session.commit()
        except Exception:
            db_session.rollback()
            raise
