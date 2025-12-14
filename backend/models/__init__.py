from flask_sqlalchemy import SQLAlchemy
from .base import Base

# SQLAlchemy实例
db = SQLAlchemy()

# 创建会话工厂 - 将在init_db中配置
db_session = None

def init_db(app):
    global db_session
    # 初始化Flask-SQLAlchemy
    db.init_app(app)
    
    # 创建所有表
    with app.app_context():
        db.create_all()
    
    # 创建会话工厂
    from sqlalchemy.orm import sessionmaker, scoped_session
    db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=db.engine)
    )
    
    # 提供会话供各模型使用
    Base.query = db_session.query_property()
