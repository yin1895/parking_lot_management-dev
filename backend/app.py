import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.config.config import Config
from backend.config.logging import setup_logging
from backend.models import init_db, db
from backend.controllers.parking_controller import parking_bp
from backend.controllers.recognition_controller import recognition_bp
from backend.utils.error_handler import register_error_handlers
from backend.utils.limiter import limiter
from backend.controllers.member_controller import member_bp
from backend.controllers.record_controller import record_bp
from backend.controllers.auth_controller import auth_bp
from backend.controllers.auto_parking_controller import auto_parking_bp
from backend.recognition.models import warmup as warmup_models
import logging

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*", "supports_credentials": True}})

app.config.from_object(Config)
limiter.init_app(app)

# 日志
setup_logging(app)
logger = logging.getLogger(__name__)

# 记录环境和连接信息
logger.info(f"环境变量: FLASK_ENV={os.getenv('FLASK_ENV', '未设置')}")
logger.info(f"环境变量: BACKEND_PORT={os.getenv('BACKEND_PORT', '未设置')}")
logger.info(f"环境变量: PORT={os.getenv('PORT', '未设置')}")
logger.info(f"使用端口: {Config.PORT}")
logger.info(f"数据库主机: {Config.DB_HOST}")
logger.info(f"数据库名称: {Config.DB_NAME}")
logger.info(f"运行环境: {os.getenv('FLASK_ENV', 'development')}")

# 注册蓝图
app.register_blueprint(parking_bp, url_prefix='/api/parking')
app.register_blueprint(recognition_bp, url_prefix='/api/recognition')
app.register_blueprint(member_bp, url_prefix='/api/members')
app.register_blueprint(record_bp, url_prefix='/api/records')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
# 注册自动停车控制器蓝图
app.register_blueprint(auto_parking_bp, url_prefix='/api/auto-parking')

# 注册错误处理器
register_error_handlers(app)

# 尝试初始化数据库
try:
    init_db(app)
    with app.app_context():
        db.engine.connect()
    logger.info("数据库连接成功")
except Exception as e:
    logger.error(f"数据库连接失败: {str(e)}", exc_info=True)

# 预热车牌识别模型（异步加载，不影响启动）
with app.app_context():
    try:
        warmup_models()
    except Exception as e:
        logger.warning(f"车牌模型预热跳过: {e}")

@app.route('/api/status', methods=['GET'])
def status():
    db_status = "connected"
    try:
        with app.app_context():
            db.engine.connect()
    except Exception as e:
        db_status = f"disconnected: {str(e)}"

    return jsonify({
        "success": True,
        "data": {
            "status": "running",
            "database": db_status,
            "version": "1.0.0",
            "env": os.getenv("FLASK_ENV", "production"),
            "api_url": request.host_url + "api",
            "db_host": Config.DB_HOST,
            "port": Config.PORT,
        },
    })

if __name__ == "__main__":
    logger.info(f"服务器启动在 http://0.0.0.0:{Config.PORT}")
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)
