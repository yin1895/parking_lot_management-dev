from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import sys

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
    
    # 创建默认管理员用户
    User.create_default_admin()
    print("默认管理员用户创建成功!")

if __name__ == "__main__":
    init_db()
