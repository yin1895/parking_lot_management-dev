from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from backend.models.base import Base

# 加载环境变量
load_dotenv()

# SQLAlchemy实例
db = SQLAlchemy()

# 创建数据库连接URL
db_url = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '3306') or os.getenv('MYSQL_PORT', '3306')}/{os.getenv('DB_NAME')}"

# 创建引擎
engine = create_engine(db_url)

# 创建会话工厂
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

def init_db(app):
    # 初始化Flask-SQLAlchemy
    db.init_app(app)
    
    # 创建所有表
    with app.app_context():
        db.create_all()

# 提供会话供各模型使用
Base.query = db_session.query_property()
