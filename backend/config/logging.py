import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    # 创建logs目录
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # 配置文件处理器
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=1024 * 1024,  # 1MB
        backupCount=10
    )
    
    # 配置格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    # 设置日志级别
    file_handler.setLevel(logging.INFO)
    
    # 添加处理器到应用
    app.logger.addHandler(file_handler)
