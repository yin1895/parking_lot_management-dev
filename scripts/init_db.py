from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os
import sys
import bcrypt  # 改回使用bcrypt

# 添加项目根目录到路径
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from backend.models.base import Base
from backend.models.user import User
from backend.models.member import Member
from backend.models.parking_record import ParkingRecord

def init_db():
    load_dotenv()
    
    # 创建数据库连接URL
    db_url = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    
    # 创建数据库引擎
    engine = create_engine(db_url)
    
    # 创建所有表
    Base.metadata.create_all(engine)
    
    print("数据库表创建成功!")
    
    # 创建会话
    SessionLocal = sessionmaker(bind=engine)
    
    # 返回SessionLocal对象
    return SessionLocal
    
def initialize_admin_user(session_maker):
    admin_username = "admin"
    admin_password = "admin"  # 默认密码
    # 使用bcrypt哈希密码
    hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # 创建会话
    session = session_maker()
    
    try:
        # 更新或插入管理员用户
        admin_user = session.query(User).filter_by(username=admin_username).first()
        if not admin_user:
            admin_user = User(username=admin_username, password=hashed_password)
            session.add(admin_user)
        else:
            admin_user.password = hashed_password  # 更新密码为正确的哈希格式
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"初始化管理员用户时出错: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    SessionLocal = init_db()
    initialize_admin_user(SessionLocal)
    print("管理员用户初始化完成")
