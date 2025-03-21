const { isValidPlateNumber, isValidPlateColor } = require('../utils/validators');
// ...existing code...

router.post('/entry', (req, res) => {
    // 车辆入场接口
    const data = req.body;
    const plate_number = data.plate_number;
    const plate_color = data.plate_color || '蓝色';
    
    // 添加输入验证
    if (!plate_number) {
        return jsonify({'success': false, 'message': '车牌号不能为空'}), 400;
    }
    
    if (!isValidPlateNumber(plate_number)) {
        return jsonify({'success': false, 'message': '无效的车牌号格式'}), 400;
    }
    
    if (!isValidPlateColor(plate_color)) {
        plate_color = '蓝色'; // 默认使用蓝色
    }
    
    result = parking_service.record_entry(plate_number, plate_color);
    return jsonify(result);
});

// ...existing code...
