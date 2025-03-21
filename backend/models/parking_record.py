from sqlalchemy import Column, String, Float, DateTime
from backend.models.base import BaseModel
from backend.models import db_session

class ParkingRecord(BaseModel):
    __tablename__ = 'parking_records'

    plate_number = Column(String(20), nullable=False)
    plate_color = Column(String(10), default='蓝色')
    entry_time = Column(DateTime, nullable=False)
    exit_time = Column(DateTime, nullable=True)
    parking_fee = Column(Float, nullable=True)

    @staticmethod
    def get_active_by_plate(plate_number):
        """获取当前在场的车辆记录"""
        return db_session.query(ParkingRecord).filter_by(plate_number=plate_number, exit_time=None).first()

    @staticmethod
    def count_active():
        """统计当前在场车辆数量"""
        return db_session.query(ParkingRecord).filter_by(exit_time=None).count()
        
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
        db_session.commit()
