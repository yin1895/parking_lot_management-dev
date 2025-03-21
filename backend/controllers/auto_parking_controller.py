import logging
from flask import Blueprint, request, jsonify
from backend.recognition.plate_recognizer import PlateRecognizer
from backend.services.parking_service import ParkingService
from backend.models.parking_record import ParkingRecord

auto_parking_bp = Blueprint('auto_parking', __name__)
recognizer = PlateRecognizer()
parking_service = ParkingService()

# 缓存上次识别结果，防止短时间内重复处理
recognition_cache = {
    'plate_number': None,
    'timestamp': 0,
    'cooldown': 5  # 秒
}

@auto_parking_bp.route('/process-frame', methods=['POST'])
def process_video_frame():
    """处理视频帧识别车牌并自动处理车辆进出"""
    try:
        if not request.json or 'frame_data' not in request.json:
            return jsonify({
                'success': False,
                'message': '没有提供帧数据'
            }), 400
        
        frame_data = request.json.get('frame_data')
        plate_text, plate_color, error = recognizer.process_frame(frame_data)
        
        if error and error != "未检测到车牌":
            logging.error(f"处理视频帧时出错: {error}")
            return jsonify({
                'success': False,
                'message': f'处理失败: {error}'
            }), 400
        
        if not plate_text:
            return jsonify({
                'success': False,
                'message': '未检测到车牌'
            }), 200
        
        # 检查是否在冷却期
        import time
        current_time = time.time()
        if (recognition_cache['plate_number'] == plate_text and 
            current_time - recognition_cache['timestamp'] < recognition_cache['cooldown']):
            return jsonify({
                'success': True,
                'message': '车牌已识别，等待冷却期结束',
                'plate_number': plate_text,
                'plate_color': plate_color,
                'action': 'none'
            })
        
        # 更新缓存
        recognition_cache['plate_number'] = plate_text
        recognition_cache['timestamp'] = current_time
        
        # 判断该车是入场还是出场
        active_record = ParkingRecord.get_active_by_plate(plate_text)
        
        if active_record:
            # 车辆已在停车场，执行出场操作
            result = parking_service.record_exit(plate_text)
            action = 'exit'
        else:
            # 车辆不在停车场，执行入场操作
            result = parking_service.record_entry(plate_text, plate_color)
            action = 'entry'
        
        return jsonify({
            'success': True,
            'plate_number': plate_text,
            'plate_color': plate_color,
            'action': action,
            'action_result': result
        })
        
    except Exception as e:
        logging.exception("自动识别处理异常")
        return jsonify({
            'success': False,
            'message': f'处理异常: {str(e)}'
        }), 500
