import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # 基础配置
    SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-key')
    DEBUG = os.getenv('FLASK_DEBUG', '0') == '1'
    PORT = int(os.getenv('PORT', 5000))
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG
    
    # JWT配置
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-key')
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
