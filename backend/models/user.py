from sqlalchemy import Column, String, Integer
from backend.models.base import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    role = Column(String(20), default='user')

    @staticmethod
    def create_default_admin():
        """创建默认管理员用户"""
        from backend.models import db_session
        if not db_session.query(User).filter_by(username='admin').first():
            admin = User(username='admin', password='admin', role='admin')
            db_session.add(admin)
            db_session.commit()
