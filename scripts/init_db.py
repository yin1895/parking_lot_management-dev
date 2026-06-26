import sys
import os

# 添加项目根目录到路径
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from flask import Flask
from backend.models import db
from backend.config.config import Config
from backend.models.user import User
from passlib.hash import pbkdf2_sha256


def initialize_admin():
    """初始化数据库表，创建或更新默认管理员用户"""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        print("数据库表创建成功!")

        admin = db.session.query(User).filter_by(username="admin").first()
        hashed = pbkdf2_sha256.hash("admin")
        if not admin:
            admin = User(username="admin", password=hashed, role="admin")
            db.session.add(admin)
        else:
            admin.password = hashed

        try:
            db.session.commit()
            print("管理员用户初始化完成")
        except Exception as e:
            db.session.rollback()
            print(f"初始化管理员用户时出错: {e}")


if __name__ == "__main__":
    initialize_admin()
