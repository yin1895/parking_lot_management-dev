"""
验证器单元测试
"""
import pytest
from backend.utils.validators import ChinesePlateValidator, PhoneValidator, UserValidator
from backend.utils.error_handler import ValidationError


class TestChinesePlateValidator:
    """测试中国车牌号验证器"""
    
    def test_valid_plate_number(self):
        """测试有效车牌号"""
        assert ChinesePlateValidator.validate('京A12345') == '京A12345'
        assert ChinesePlateValidator.validate('沪B67890') == '沪B67890'
    
    def test_invalid_plate_number(self):
        """测试无效车牌号"""
        with pytest.raises(ValidationError):
            ChinesePlateValidator.validate('')
        
        with pytest.raises(ValidationError):
            ChinesePlateValidator.validate('ABC12345')
    
    def test_plate_number_case_insensitive(self):
        """测试车牌号大小写不敏感"""
        result = ChinesePlateValidator.validate('京a12345')
        assert result == '京A12345'


class TestPhoneValidator:
    """测试手机号验证器"""
    
    def test_valid_phone(self):
        """测试有效手机号"""
        assert PhoneValidator.validate('13812345678') == '13812345678'
        assert PhoneValidator.validate('15987654321') == '15987654321'
    
    def test_empty_phone(self):
        """测试空手机号"""
        assert PhoneValidator.validate('') == ''
    
    def test_invalid_phone(self):
        """测试无效手机号"""
        with pytest.raises(ValidationError):
            PhoneValidator.validate('12345678901')
        
        with pytest.raises(ValidationError):
            PhoneValidator.validate('abc12345678')


class TestUserValidator:
    """测试用户验证器"""
    
    def test_valid_username(self):
        """测试有效用户名"""
        assert UserValidator.validate_username('testuser') == 'testuser'
        assert UserValidator.validate_username('user_123') == 'user_123'
    
    def test_invalid_username(self):
        """测试无效用户名"""
        with pytest.raises(ValidationError):
            UserValidator.validate_username('')
        
        with pytest.raises(ValidationError):
            UserValidator.validate_username('ab')  # 太短
    
    def test_valid_password(self):
        """测试有效密码"""
        assert UserValidator.validate_password('TestPass123') == 'TestPass123'
        assert UserValidator.validate_password('Complex@Pass2023') == 'Complex@Pass2023'
    
    def test_invalid_password(self):
        """测试无效密码"""
        with pytest.raises(ValidationError):
            UserValidator.validate_password('weak')  # 太短且无数字
        
        with pytest.raises(ValidationError):
            UserValidator.validate_password('12345678')  # 无字母
