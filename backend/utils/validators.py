"""
输入验证工具
提供各种数据验证功能
"""
import re
from typing import Any, Optional, List, Dict
from backend.utils.error_handler import ValidationError, ConflictError


class BaseValidator:
    """验证器基类"""
    
    @staticmethod
    def required(value: Any, field_name: str = "field") -> Any:
        """验证字段是否必填"""
        if value is None or value == "" or (isinstance(value, str) and value.strip() == ""):
            raise ValidationError(f"{field_name}不能为空", field=field_name)
        return value
    
    @staticmethod
    def min_length(value: str, min_len: int, field_name: str = "field") -> str:
        """验证字符串最小长度"""
        if len(str(value)) < min_len:
            raise ValidationError(f"{field_name}长度不能少于{min_len}个字符", field=field_name)
        return str(value)
    
    @staticmethod
    def max_length(value: str, max_len: int, field_name: str = "field") -> str:
        """验证字符串最大长度"""
        if len(str(value)) > max_len:
            raise ValidationError(f"{field_name}长度不能超过{max_len}个字符", field=field_name)
        return str(value)
    
    @staticmethod
    def length_range(value: str, min_len: int, max_len: int, field_name: str = "field") -> str:
        """验证字符串长度范围"""
        length = len(str(value))
        if length < min_len or length > max_len:
            raise ValidationError(f"{field_name}长度必须在{min_len}-{max_len}个字符之间", field=field_name)
        return str(value)


class ChinesePlateValidator:
    """中国车牌号验证器"""
    
    # 中国车牌号正则表达式
    PLATE_PATTERN = re.compile(r'^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领][A-Z][A-Z0-9]{4}[A-Z0-9挂学警港澳]$')
    
    @staticmethod
    def validate(plate_number: str, field_name: str = "车牌号") -> str:
        """验证中国车牌号格式"""
        if not plate_number:
            raise ValidationError(f"{field_name}不能为空", field=field_name)
        
        plate_number = plate_number.upper().strip()
        
        if not ChinesePlateValidator.PLATE_PATTERN.match(plate_number):
            raise ValidationError(f"{field_name}格式不正确，应为中国车牌号格式", field=field_name)
        
        return plate_number


class PhoneValidator:
    """手机号码验证器"""
    
    # 中国手机号正则表达式
    PHONE_PATTERN = re.compile(r'^1[3-9]\d{9}$')
    
    @staticmethod
    def validate(phone: str, field_name: str = "手机号") -> str:
        """验证中国手机号格式"""
        if not phone:
            # 手机号不是必填项，可以为空
            return ""
        
        phone = phone.strip()
        
        if not PhoneValidator.PHONE_PATTERN.match(phone):
            raise ValidationError(f"{field_name}格式不正确，应为11位中国手机号", field=field_name)
        
        return phone


class EmailValidator:
    """邮箱验证器"""
    
    @staticmethod
    def validate(email: str, field_name: str = "邮箱") -> str:
        """验证邮箱格式"""
        if not email:
            # 邮箱不是必填项，可以为空
            return ""
        
        email = email.strip()
        
        # 简单的邮箱格式验证
        pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not pattern.match(email):
            raise ValidationError(f"{field_name}格式不正确", field=field_name)
        
        return email


class MemberValidator:
    """会员信息验证器"""
    
    @staticmethod
    def validate_name(name: str) -> str:
        """验证会员姓名"""
        if not name:
            raise ValidationError("会员姓名不能为空", field="name")
        
        name = name.strip()
        BaseValidator.length_range(name, 1, 50, "会员姓名")
        
        # 检查是否包含非法字符
        if re.search(r'[<>"\']', name):
            raise ValidationError("会员姓名包含非法字符", field="name")
        
        return name
    
    @staticmethod
    def validate_plate_number(plate_number: str, existing_plate_numbers: Optional[List[str]] = None) -> str:
        """验证会员车牌号"""
        validated_plate = ChinesePlateValidator.validate(plate_number, "会员车牌号")
        
        # 检查车牌号是否已存在（如果提供了现有车牌号列表）
        if existing_plate_numbers and validated_plate.upper() in [p.upper() for p in existing_plate_numbers]:
            raise ConflictError(f"车牌号 {validated_plate} 已存在", resource="plate_number")
        
        return validated_plate
    
    @staticmethod
    def validate_phone(phone: str) -> str:
        """验证会员手机号"""
        return PhoneValidator.validate(phone, "会员手机号")
    
    @staticmethod
    def validate_status(status: str) -> str:
        """验证会员状态"""
        if not status:
            return "active"  # 默认状态
        
        valid_statuses = ["active", "inactive", "suspended"]
        if status not in valid_statuses:
            raise ValidationError(f"会员状态必须是以下值之一: {', '.join(valid_statuses)}", field="status")
        
        return status
    
    @staticmethod
    def validate_create_data(data: Dict[str, Any], existing_plate_numbers: Optional[List[str]] = None) -> Dict[str, Any]:
        """验证创建会员的完整数据"""
        validated_data = {}
        
        # 验证姓名
        if 'name' not in data:
            raise ValidationError("缺少必需字段: name", field="name")
        validated_data['name'] = MemberValidator.validate_name(data['name'])
        
        # 验证车牌号
        if 'plate_number' not in data:
            raise ValidationError("缺少必需字段: plate_number", field="plate_number")
        validated_data['plate_number'] = MemberValidator.validate_plate_number(
            data['plate_number'], existing_plate_numbers
        )
        
        # 验证手机号（可选）
        if 'phone' in data:
            validated_data['phone'] = MemberValidator.validate_phone(data['phone'])
        else:
            validated_data['phone'] = ""
        
        # 验证状态（可选）
        if 'status' in data:
            validated_data['status'] = MemberValidator.validate_status(data['status'])
        else:
            validated_data['status'] = "active"
        
        return validated_data


class ParkingValidator:
    """停车相关验证器"""
    
    @staticmethod
    def validate_entry_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """验证车辆入场数据"""
        validated_data = {}
        
        # 验证车牌号
        if 'plate_number' not in data:
            raise ValidationError("缺少必需字段: plate_number", field="plate_number")
        validated_data['plate_number'] = ChinesePlateValidator.validate(data['plate_number'])
        
        # 验证车牌颜色（可选）
        if 'plate_color' in data:
            plate_color = data['plate_color'].strip()
            valid_colors = ["蓝色", "黄色", "黑色", "白色", "其他"]
            if plate_color not in valid_colors:
                raise ValidationError(f"车牌颜色必须是以下值之一: {', '.join(valid_colors)}", field="plate_color")
            validated_data['plate_color'] = plate_color
        else:
            validated_data['plate_color'] = "蓝色"
        
        return validated_data
    
    @staticmethod
    def validate_exit_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """验证车辆出场数据"""
        validated_data = {}
        
        # 验证车牌号
        if 'plate_number' not in data:
            raise ValidationError("缺少必需字段: plate_number", field="plate_number")
        validated_data['plate_number'] = ChinesePlateValidator.validate(data['plate_number'])
        
        return validated_data


class UserValidator:
    """用户相关验证器"""
    
    @staticmethod
    def validate_username(username: str) -> str:
        """验证用户名"""
        if not username:
            raise ValidationError("用户名不能为空", field="username")
        
        username = username.strip()
        BaseValidator.length_range(username, 3, 50, "用户名")
        
        # 检查用户名格式（只能包含字母、数字、下划线）
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError("用户名只能包含字母、数字和下划线", field="username")
        
        return username
    
    @staticmethod
    def validate_password(password: str) -> str:
        """验证密码强度"""
        if not password:
            raise ValidationError("密码不能为空", field="password")
        
        # 密码长度至少8位
        BaseValidator.min_length(password, 8, "密码")
        
        # 检查密码复杂度
        if len(password) < 8:
            raise ValidationError("密码长度至少8位", field="password")
        
        # 检查是否包含字母和数字
        if not re.search(r'[a-zA-Z]', password):
            raise ValidationError("密码必须包含至少一个字母", field="password")
        
        if not re.search(r'\d', password):
            raise ValidationError("密码必须包含至少一个数字", field="password")
        
        return password
    
    @staticmethod
    def validate_email(email: str) -> str:
        """验证邮箱"""
        return EmailValidator.validate(email, "邮箱")
    
    @staticmethod
    def validate_login_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """验证登录数据"""
        validated_data = {}
        
        # 验证用户名
        if 'username' not in data:
            raise ValidationError("缺少必需字段: username", field="username")
        validated_data['username'] = UserValidator.validate_username(data['username'])
        
        # 验证密码
        if 'password' not in data:
            raise ValidationError("缺少必需字段: password", field="password")
        validated_data['password'] = data['password']  # 密码不进行清理，保留原始值
        
        return validated_data
    
    @staticmethod
    def validate_register_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """验证注册数据"""
        validated_data = {}
        
        # 验证用户名
        if 'username' not in data:
            raise ValidationError("缺少必需字段: username", field="username")
        validated_data['username'] = UserValidator.validate_username(data['username'])
        
        # 验证密码
        if 'password' not in data:
            raise ValidationError("缺少必需字段: password", field="password")
        validated_data['password'] = UserValidator.validate_password(data['password'])
        
        # 验证邮箱（可选）
        if 'email' in data:
            validated_data['email'] = UserValidator.validate_email(data['email'])
        else:
            validated_data['email'] = ""
        
        return validated_data
