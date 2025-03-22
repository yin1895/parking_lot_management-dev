import cv2
import numpy as np
import os
import time
import copy
from .models import detect_session, recog_session

class PlateRecognizer:
    def __init__(self):
        # 添加防抖动参数
        self.last_recognition_time = 0
        self.recognition_cooldown = 2  # 两次识别间的冷却时间(秒)
        self.last_recognized_plate = None
        self.confidence_threshold = 0.5
        
        # 移植的参数
        self.plate_color_list = ['黑色', '蓝色', '绿色', '白色', '黄色']
        self.plateName = r"#京沪津渝冀晋蒙辽吉黑苏浙皖闽赣鲁豫鄂湘粤桂琼川贵云藏陕甘青宁新学警港澳挂使领民航危0123456789ABCDEFGHJKLMNPQRSTUVWXYZ险品"
        self.mean_value, self.std_value = (0.588, 0.193)  # 识别模型均值标准差

    def _load_char_dict(self):
        # 完整的字符字典
        return {i: char for i, char in enumerate(self.plateName)}

    def my_letter_box(self, img, size=(640, 640)):
        """图像预处理方法"""
        h, w, c = img.shape
        r = min(size[0] / h, size[1] / w)
        new_h, new_w = int(h * r), int(w * r)
        top = int((size[0] - new_h) / 2)
        left = int((size[1] - new_w) / 2)
        bottom = size[0] - new_h - top
        right = size[1] - new_w - left
        img_resize = cv2.resize(img, (new_w, new_h))
        img = cv2.copyMakeBorder(img_resize, top, bottom, left, right, borderType=cv2.BORDER_CONSTANT, value=(114, 114, 114))
        return img, r, left, top

    def preprocess_image(self, image):
        """图像预处理方法"""
        img, r, left, top = self.my_letter_box(image, (640, 640))
        img = img[:, :, ::-1].transpose(2, 0, 1).copy().astype(np.float32)
        img = img / 255
        img = img.reshape(1, *img.shape)
        return img, r, left, top

    def detect_plate(self, image):
        """使用检测模型找到车牌"""
        img, r, left, top = self.preprocess_image(image)
        y_onnx = detect_session.run([detect_session.get_outputs()[0].name], {detect_session.get_inputs()[0].name: img})[0]
        outputs = self.post_processing(y_onnx, r, left, top)
        return outputs

    def post_processing(self, dets, r, left, top, conf_thresh=0.3, iou_thresh=0.5):
        """后处理方法"""
        choice = dets[:, :, 4] > conf_thresh
        dets = dets[choice]
        dets[:, 13:15] *= dets[:, 4:5]
        box = dets[:, :4]
        boxes = self.xywh2xyxy(box)
        score = np.max(dets[:, 13:15], axis=-1, keepdims=True)
        index = np.argmax(dets[:, 13:15], axis=-1).reshape(-1, 1)
        output = np.concatenate((boxes, score, dets[:, 5:13], index), axis=1)
        reserve_ = self.my_nms(output, iou_thresh)
        output = output[reserve_]
        output = self.restore_box(output, r, left, top)
        return output

    def xywh2xyxy(self, boxes):
        """坐标转换方法"""
        xywh = copy.deepcopy(boxes)
        xywh[:, 0] = boxes[:, 0] - boxes[:, 2] / 2
        xywh[:, 1] = boxes[:, 1] - boxes[:, 3] / 2
        xywh[:, 2] = boxes[:, 0] + boxes[:, 2] / 2
        xywh[:, 3] = boxes[:, 1] + boxes[:, 3] / 2
        return xywh

    def my_nms(self, boxes, iou_thresh):
        """非极大值抑制方法"""
        index = np.argsort(boxes[:, 4])[::-1]
        keep = []
        while index.size > 0:
            i = index[0]
            keep.append(i)
            x1 = np.maximum(boxes[i, 0], boxes[index[1:], 0])
            y1 = np.maximum(boxes[i, 1], boxes[index[1:], 1])
            x2 = np.minimum(boxes[i, 2], boxes[index[1:], 2])
            y2 = np.minimum(boxes[i, 3], boxes[index[1:], 3])
            w = np.maximum(0, x2 - x1)
            h = np.maximum(0, y2 - y1)
            inter_area = w * h
            union_area = (boxes[i, 2] - boxes[i, 0]) * (boxes[i, 3] - boxes[i, 1]) + (boxes[index[1:], 2] - boxes[index[1:], 0]) * (boxes[index[1:], 3] - boxes[index[1:], 1])
            iou = inter_area / (union_area - inter_area)
            idx = np.where(iou <= iou_thresh)[0]
            index = index[idx + 1]
        return keep

    def restore_box(self, boxes, r, left, top):
        """盒子坐标恢复方法"""
        boxes[:, [0, 2, 5, 7, 9, 11]] -= left
        boxes[:, [1, 3, 6, 8, 10, 12]] -= top
        boxes[:, [0, 2, 5, 7, 9, 11]] /= r
        boxes[:, [1, 3, 6, 8, 10, 12]] /= r
        return boxes

    def rec_pre_processing(self, img, size=(48, 168)):
        """车牌识别预处理方法"""
        img = cv2.resize(img, (168, 48))
        img = img.astype(np.float32)
        img = (img / 255 - self.mean_value) / self.std_value
        img = img.transpose(2, 0, 1)
        img = img.reshape(1, *img.shape)
        return img

    def decode_plate(self, preds):
        """车牌解码方法"""
        pre = 0
        new_preds = []
        for i in range(len(preds)):
            if preds[i] != 0 and preds[i] != pre:
                new_preds.append(preds[i])
            pre = preds[i]
        plate = ""
        for i in new_preds:
            plate += self.plateName[int(i)]
        return plate

    def recognize_text(self, plate_img):
        """识别车牌文字和颜色 """
        img = self.rec_pre_processing(plate_img)
        y_onnx_plate, y_onnx_color = recog_session.run(
            [recog_session.get_outputs()[0].name, recog_session.get_outputs()[1].name], 
            {recog_session.get_inputs()[0].name: img}
        )
        
        # 解码车牌号
        index = np.argmax(y_onnx_plate, axis=-1)
        plate_no = self.decode_plate(index[0])
        
        # 解码车牌颜色
        index_color = np.argmax(y_onnx_color)
        if index_color < len(self.plate_color_list):
            plate_color = self.plate_color_list[index_color]
        else:
            plate_color = '蓝色'  # 默认颜色
            
        return plate_no, plate_color

    def process_image(self, img_path):
        """处理图像文件并识别车牌"""
        image = cv2.imread(img_path)
        if image is None:
            return None, None, "无法读取图片"
        
        try:
            outputs = self.detect_plate(image)
            if len(outputs) == 0:
                return None, None, "未检测到车牌"
            
            # 获取最大的车牌区域
            box = outputs[0][:4].astype(int)
            plate_img = image[box[1]:box[3], box[0]:box[2]]
            plate_text, plate_color = self.recognize_text(plate_img)
            
            return plate_text, plate_color, None
        except Exception as e:
            return None, None, str(e)

    def process_frame(self, frame_data):
        """处理前端发送的视频帧并识别车牌"""
        try:
            # 检查冷却时间，防止过于频繁的识别请求
            current_time = time.time()
            if current_time - self.last_recognition_time < self.recognition_cooldown:
                return None, None, "识别冷却中，请稍后"
            
            # 将Base64数据转换为图像
            import base64
            jpg_as_np = np.frombuffer(base64.b64decode(frame_data.split(',')[1]), dtype=np.uint8)
            image = cv2.imdecode(jpg_as_np, cv2.IMREAD_COLOR)
            
            if image is None:
                return None, None, "无法解析图像数据"
            
            # 使用移植的方法检测车牌
            outputs = self.detect_plate(image)
            if len(outputs) == 0:
                return None, None, "未检测到车牌"
            
            # 获取最大的车牌区域
            box = outputs[0][:4].astype(int)
            plate_img = image[box[1]:box[3], box[0]:box[2]]
            plate_text, plate_color = self.recognize_text(plate_img)
            
            # 更新最后识别时间
            self.last_recognition_time = current_time
            self.last_recognized_plate = plate_text
            
            return plate_text, plate_color, None
        except Exception as e:
            return None, None, str(e)
