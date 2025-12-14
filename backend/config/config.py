import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # 基础配置
    SECRET_KEY = os.getenv('JWT_SECRET_KEY', '*$Qnx}xJQaa*j^P3-[i^>#82MOALIO-<|g8YI-JC6dw*Q&>Y)|2sORbQ!7P&N7mq')
    DEBUG = os.getenv('FLASK_DEBUG', '0') == '1'
    # 在Docker环境中固定使用5000端口（容器内部端口）
    IS_DOCKER = os.getenv('IS_DOCKER', '0') == '1'
    if IS_DOCKER:
        PORT = 5000
    else:
        # 非Docker环境使用环境变量
        PORT = int(os.getenv('BACKEND_PORT') or os.getenv('PORT', 5000))
    
    # 数据库配置 - 在Docker环境中使用服务名作为主机名
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    # 其他数据库配置参数
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_NAME = os.getenv('DB_NAME', 'parking_management')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG
    
    # JWT配置
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 86400))
    
    # 停车场配置
    PARKING_CAPACITY = int(os.getenv('PARKING_CAPACITY', 100))
    NORMAL_RATE = float(os.getenv('NORMAL_RATE', 10))
    MEMBER_RATE = float(os.getenv('MEMBER_RATE', 8))
    MEMBER_DISCOUNT = float(os.getenv('MEMBER_DISCOUNT', 0.8))
    
    # 添加权重文件配置
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    WEIGHTS_DIR = os.path.join(ROOT_DIR, 'weights')
    PLATE_DETECT_MODEL = os.path.join(WEIGHTS_DIR, 'plate_detect.onnx')
    PLATE_RECOG_MODEL = os.path.join(WEIGHTS_DIR, 'plate_rec_color.onnx')
    
    # 识别配置
    RECOGNITION_CONFIDENCE_THRESHOLD = 0.5
    RECOGNITION_MAX_RETRY = 3
    
    # CORS配置 - 安全加固
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:8080,http://127.0.0.1:8080').split(',')
    CORS_ALLOW_CREDENTIALS = True
    
    @property
    def JWT_SECRET_KEY(self):
        """获取JWT密钥，保持向后兼容"""
        return self.SECRET_KEY
    
    @classmethod
    def get_cors_config(cls):
        """获取CORS配置"""
        return {
            'origins': cls.CORS_ORIGINS,
            'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
            'allow_headers': ['Content-Type', 'Authorization', 'X-Requested-With'],
            'supports_credentials': cls.CORS_ALLOW_CREDENTIALS
        }
