from sqlalchemy import Column, String, Integer
from backend.models.base import BaseModel
from backend.models import db_session

class Member(BaseModel):
    __tablename__ = 'members'

    name = Column(String(50), nullable=False)
    plate_number = Column(String(20), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    status = Column(String(20), default='active')
    
    @staticmethod
    def get_by_plate(plate_number):
        """通过车牌号获取会员"""
        return db_session.query(Member).filter_by(plate_number=plate_number).first()
        
    def to_dict(self):
        """将模型转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'plate_number': self.plate_number,
            'phone': self.phone,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
