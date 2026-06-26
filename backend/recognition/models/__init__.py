import os
import onnxruntime as ort
import logging
import time

logger = logging.getLogger(__name__)

from backend.config.config import Config

_sessions = None
_warmed = False


def load_models():
    """惰性加载 ONNX 模型，首次调用时初始化并缓存"""
    global _sessions
    if _sessions is not None:
        return _sessions

    if not os.path.exists(Config.PLATE_DETECT_MODEL):
        raise FileNotFoundError(
            f"车牌检测模型未找到: {Config.PLATE_DETECT_MODEL}"
        )
    if not os.path.exists(Config.PLATE_RECOG_MODEL):
        raise FileNotFoundError(
            f"车牌识别模型未找到: {Config.PLATE_RECOG_MODEL}"
        )

    logger.info("正在加载车牌识别模型...")
    t0 = time.time()
    detect = ort.InferenceSession(Config.PLATE_DETECT_MODEL)
    recog = ort.InferenceSession(Config.PLATE_RECOG_MODEL)
    _sessions = (detect, recog, Config.PLATE_DETECT_MODEL, Config.PLATE_RECOG_MODEL)
    logger.info(f"模型加载完成 ({time.time()-t0:.2f}s)")
    return _sessions


def warmup():
    """预热模型：执行一次空推理，避免首次调用延迟"""
    global _warmed
    if _warmed:
        return
    try:
        detect, recog, _, _ = load_models()
        dummy = __import__("numpy", fromlist=["zeros"]).zeros((1, 3, 640, 640), dtype="float32")
        detect.run([detect.get_outputs()[0].name], {detect.get_inputs()[0].name: dummy})
        logger.info("车牌检测模型预热完成")
        _warmed = True
    except Exception as e:
        logger.warning(f"模型预热失败（不影响后续使用）: {e}")


def get_detect_session():
    return load_models()[0] if _sessions else None


def get_recog_session():
    return load_models()[1] if _sessions else None


def is_ready() -> bool:
    """检查模型是否已成功加载"""
    return _sessions is not None
