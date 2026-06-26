"""测试 停车服务 (parking_service.py)"""
import pytest
from flask import Flask
from datetime import datetime

from backend.services.parking_service import ParkingService
from backend.models import init_db, db
from backend.models.parking_record import ParkingRecord
from backend.models.member import Member


@pytest.fixture
def parking_app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PARKING_CAPACITY"] = 100
    init_db(app)
    with app.app_context():
        m = Member(name="VIP用户", plate_number="京A00001", phone="13900000001", status="active")
        db.session.add(m)
        db.session.commit()
    return app


class TestParkingService:
    def test_entry_success(self, parking_app):
        with parking_app.app_context():
            svc = ParkingService()
            result = svc.record_entry("京B12345", "蓝色")
        assert result["success"] is True
        assert result["record"]["plate_number"] == "京B12345"

    def test_entry_duplicate(self, parking_app):
        with parking_app.app_context():
            svc = ParkingService()
            svc.record_entry("京B12345", "蓝色")
            result = svc.record_entry("京B12345", "蓝色")
        assert result["success"] is False  # already in park

    def test_exit_success(self, parking_app):
        with parking_app.app_context():
            svc = ParkingService()
            svc.record_entry("京C11111", "绿色")
            result = svc.record_exit("京C11111")
        assert result["success"] is True
        assert result["record"]["exit_time"] is not None
        assert "fee_details" in result

    def test_exit_no_record(self, parking_app):
        with parking_app.app_context():
            svc = ParkingService()
            result = svc.record_exit("京D99999")
        assert result["success"] is False

    def test_exit_member_discount(self, parking_app):
        with parking_app.app_context():
            svc = ParkingService()
            svc.record_entry("京A00001")  # member
            result = svc.record_exit("京A00001")
        assert result["success"] is True
        assert result["fee_details"]["is_member"] is True

    def test_get_status(self, parking_app):
        with parking_app.app_context():
            svc = ParkingService()
            svc.record_entry("京E11111")
            svc.record_entry("京E22222")
            status = svc.get_status()
        assert status["success"] is True
        assert status["occupied_spaces"] == 2
        assert status["available_spaces"] == 98
        assert status["total_spaces"] == 100
