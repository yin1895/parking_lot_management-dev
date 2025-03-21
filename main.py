import os
from backend.app import app
from backend.config.config import Config

def init_project():
    """项目初始化"""
    # 确保必要目录存在
    os.makedirs('weights', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # 检查权重文件
    if not os.path.exists(Config.PLATE_DETECT_MODEL):
        print(f"警告: 缺少检测模型文件: {Config.PLATE_DETECT_MODEL}")
        print("请下载模型文件并放入正确位置")
    if not os.path.exists(Config.PLATE_RECOG_MODEL):
        print(f"警告: 缺少识别模型文件: {Config.PLATE_RECOG_MODEL}")
        print("请下载模型文件并放入正确位置")

if __name__ == '__main__':
    init_project()
    print(f"启动Web服务，地址: http://0.0.0.0:{Config.PORT}")
    # 直接使用Flask后端
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
