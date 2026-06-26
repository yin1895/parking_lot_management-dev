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
        from backend.models import db
        if not db.session.query(User).filter_by(username='admin').first():
            admin = User(username='admin', password=pbkdf2_sha256.hash('admin'), role='admin')
            db.session.add(admin)
            db.session.commit()
