import os
import logging
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from backend.recognition.plate_recognizer import PlateRecognizer

recognition_bp = Blueprint('recognition', __name__)
recognizer = PlateRecognizer()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'uploads'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_recognizer():
    return recognizer

@recognition_bp.route('/plate', methods=['POST'])
def recognize_plate():
    """车牌识别API端点"""
    if 'image' not in request.files:
        return jsonify({
            'success': False,
            'message': '没有上传文件'
        }), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({
            'success': False,
            'message': '未选择文件'
        }), 400
        
    if file and allowed_file(file.filename):
        # 确保上传目录存在
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
            
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        try:
            rec = get_recognizer()
            if rec is None:
                return jsonify({
                    'success': False,
                    'message': '车牌识别服务不可用'
                }), 500
                
            plate_text, plate_color, error = rec.process_image(filepath)
            
            # 清理临时文件
            os.remove(filepath)
            
            if error:
                return jsonify({
                    'success': False,
                    'message': f'识别失败: {error}'
                }), 400
                
            if not plate_text:
                return jsonify({
                    'success': False,
                    'message': '未能识别车牌'
                }), 400
                
            return jsonify({
                'success': True,
                'plate_number': plate_text,
                'plate_color': plate_color,
                'confidence': 0.95  # 示例置信度值
            })
        except Exception as e:
            # 确保临时文件被删除
            if os.path.exists(filepath):
                os.remove(filepath)
                
            logging.error(f"车牌识别异常: {str(e)}")
            return jsonify({
                'success': False,
                'message': f'识别失败: {str(e)}'
            }), 500
            
    return jsonify({
        'success': False,
        'message': '不支持的文件类型'
    }), 400
