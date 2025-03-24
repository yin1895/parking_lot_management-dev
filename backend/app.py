import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.config.config import Config
from backend.models import init_db, db
from backend.controllers.parking_controller import parking_bp
from backend.controllers.recognition_controller import recognition_bp
from backend.utils.error_handler import register_error_handlers
from backend.controllers.member_controller import member_bp
from backend.controllers.record_controller import record_bp
from backend.controllers.auth_controller import auth_bp
from backend.controllers.auto_parking_controller import auto_parking_bp
import logging

app = Flask(__name__)
# 为Docker环境配置更宽松的CORS策略
CORS(app, resources={r"/api/*": {"origins": "*", "supports_credentials": True}})
app.config.from_object(Config)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 记录环境和连接信息
logger.info(f"环境变量: FLASK_ENV={os.getenv('FLASK_ENV', '未设置')}")
logger.info(f"环境变量: BACKEND_PORT={os.getenv('BACKEND_PORT', '未设置')}")
logger.info(f"环境变量: PORT={os.getenv('PORT', '未设置')}")
logger.info(f"使用端口: {Config.PORT}")
logger.info(f"数据库主机: {Config.DB_HOST}")
logger.info(f"数据库名称: {Config.DB_NAME}")

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
    # 测试数据库连接
    with app.app_context():
        db.engine.connect()
    logger.info("数据库连接成功")
except Exception as e:
    logger.error(f"数据库连接失败: {str(e)}")
    # 应用继续运行，但数据库功能可能不可用

@app.route('/api/status', methods=['GET'])
def status():
    # 检查数据库连接状态
    db_status = "connected"
    try:
        with app.app_context():
            db.engine.connect()
    except Exception as e:
        db_status = f"disconnected: {str(e)}"
    
    # 增强状态响应，包含更多环境信息
    return jsonify({
        'status': 'running',
        'database': db_status,
        'version': '1.0.0',
        'env': os.getenv('FLASK_ENV', 'production'),
        'api_url': request.host_url + 'api',
        'db_host': Config.DB_HOST,
        'port': Config.PORT
    })

if __name__ == '__main__':
    logger.info(f"服务器启动在 http://0.0.0.0:{Config.PORT}")
    app.run(host='0.0.0.0', port=Config.PORT)
