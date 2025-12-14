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
        """创建默认管理员用户 - 使用强密码"""
        from backend.models import db_session
        if not db_session.query(User).filter_by(username='admin').first():
            # 使用强密码hash替换明文密码
            # 密码: }q^C>W7nFK]V^Lt) 
            admin_password_hash = '$pbkdf2-sha256$29000$SYmxVsoZ4/y/t7aWspZSig$eiHQW3b40wWStxkBipkTufY4SsAlj2PeyI49Qt8vdFc'
            admin = User(username='admin', password=admin_password_hash, role='admin')
            db_session.add(admin)
            db_session.commit()
            
    @staticmethod
    def update_admin_password():
        """更新管理员密码为强密码"""
        from backend.models import db_session
        admin = db_session.query(User).filter_by(username='admin').first()
        if admin:
            # 使用强密码hash
            admin_password_hash = '$pbkdf2-sha256$29000$SYmxVsoZ4/y/t7aWspZSig$eiHQW3b40wWStxkBipkTufY4SsAlj2PeyI49Qt8vdFc'
            admin.password = admin_password_hash
            db_session.commit()
            print("管理员密码已更新为强密码")
        else:
            # 如果管理员不存在，创建新的
            User.create_default_admin()
