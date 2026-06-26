from flask_sqlalchemy import SQLAlchemy
import logging

logger = logging.getLogger(__name__)

db = SQLAlchemy()

def init_db(app):
    """初始化数据库：连接 Flask 应用并创建所有表"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
    logger.info("数据库表创建成功")
