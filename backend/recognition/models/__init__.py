import os
import onnxruntime as ort

# 获取项目根目录
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 更新权重文件路径
WEIGHTS_DIR = os.path.join(ROOT_DIR, 'weights')
DETECT_MODEL = os.path.join(WEIGHTS_DIR, 'plate_detect.onnx')
RECOG_MODEL = os.path.join(WEIGHTS_DIR, 'plate_rec_color.onnx')

def load_models():
    """加载模型并返回会话"""
    if not os.path.exists(DETECT_MODEL) or not os.path.exists(RECOG_MODEL):
        raise FileNotFoundError(
            f"权重文件未找到。请确保以下文件存在：\n"
            f"1. {DETECT_MODEL}\n"
            f"2. {RECOG_MODEL}"
        )
    
    detect_session = ort.InferenceSession(DETECT_MODEL)
    recog_session = ort.InferenceSession(RECOG_MODEL)
    return detect_session, recog_session

# 初始化模型会话
detect_session, recog_session = load_models()
