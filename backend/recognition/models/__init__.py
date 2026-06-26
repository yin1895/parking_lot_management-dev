import os
import onnxruntime as ort
import logging

logger = logging.getLogger(__name__)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WEIGHTS_DIR = os.path.join(ROOT_DIR, 'weights')
DETECT_MODEL = os.path.join(WEIGHTS_DIR, 'plate_detect.onnx')
RECOG_MODEL = os.path.join(WEIGHTS_DIR, 'plate_rec_color.onnx')

_sessions = None

def load_models():
    """惰性加载 ONNX 模型，首次调用时初始化并缓存"""
    global _sessions
    if _sessions is not None:
        return _sessions

    if not os.path.exists(DETECT_MODEL):
        raise FileNotFoundError(
            f"车牌检测模型未找到: {DETECT_MODEL}"
        )
    if not os.path.exists(RECOG_MODEL):
        raise FileNotFoundError(
            f"车牌识别模型未找到: {RECOG_MODEL}"
        )

    detect = ort.InferenceSession(DETECT_MODEL)
    recog = ort.InferenceSession(RECOG_MODEL)
    _sessions = (detect, recog)
    logger.info("车牌识别模型加载完成")
    return _sessions

def get_detect_session():
    return load_models()[0]

def get_recog_session():
    return load_models()[1]
