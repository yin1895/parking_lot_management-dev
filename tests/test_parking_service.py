import pytest
from datetime import datetime
from backend.services.parking_service import ParkingService
from backend.models.parking_record import ParkingRecord
from backend.models.member import Member

class TestParkingService:
    @pytest.fixture
    def service(self):
        return ParkingService()
    
    def test_record_entry(self, service):
        result = service.record_entry("京A12345", "蓝色")
        assert result['success'] is True
        assert "京A12345" in result['message']
        
    def test_record_exit(self, service):
        # 先入场
        service.record_entry("京A12345", "蓝色")
        # 后出场
        result = service.record_exit("京A12345")
        assert result['success'] is True
        assert 'fee_details' in result
