import os
from dotenv import load_dotenv

load_dotenv()

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config:
    """停车场管理系统配置（Flask app.config.from_object 兼容）"""
    # ─── 应用 ─────────────────────────────────
    SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-key")
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"

    # ─── 端口 ─────────────────────────────────
    IS_DOCKER = os.getenv("IS_DOCKER", "0") == "1"
    if IS_DOCKER:
        PORT = 5000
    else:
        PORT = int(os.getenv("BACKEND_PORT") or os.getenv("PORT", "5000"))

    # ─── 数据库 ───────────────────────────────
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "parking_management")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER', 'root')}:{os.getenv('DB_PASSWORD', '')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'parking_management')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG

    # ─── JWT ──────────────────────────────────
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-key")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "86400"))
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", "2592000"))

    # ─── 停车场 ───────────────────────────────
    PARKING_CAPACITY = int(os.getenv("PARKING_CAPACITY", "100"))
    NORMAL_RATE = float(os.getenv("NORMAL_RATE", "10"))
    MEMBER_RATE = float(os.getenv("MEMBER_RATE", "8"))
    MEMBER_DISCOUNT = float(os.getenv("MEMBER_DISCOUNT", "0.8"))

    # ─── 车牌识别 ─────────────────────────────
    ROOT_DIR = _root
    WEIGHTS_DIR = os.path.join(_root, "weights")
    PLATE_DETECT_MODEL = os.path.join(WEIGHTS_DIR, "plate_detect.onnx")
    PLATE_RECOG_MODEL = os.path.join(WEIGHTS_DIR, "plate_rec_color.onnx")
    RECOGNITION_CONFIDENCE_THRESHOLD = float(os.getenv("RECOGNITION_CONFIDENCE_THRESHOLD", "0.5"))
    RECOGNITION_COOLDOWN = int(os.getenv("RECOGNITION_COOLDOWN", "2"))

    # ─── 环境选择 ─────────────────────────────
    ENV = os.getenv("FLASK_ENV", "development")
    if ENV == "production":
        DEBUG = False
        SQLALCHEMY_ECHO = False
