"""测试 停车记录服务 (record_service.py)"""
from datetime import datetime, timedelta
import pytest
from flask import Flask

from backend.services.record_service import RecordService
from backend.models import init_db, db
from backend.models.parking_record import ParkingRecord
from backend.utils.exceptions import NotFoundError


@pytest.fixture
def record_app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    init_db(app)

    with app.app_context():
        now = datetime.utcnow()
        for i in range(5):
            r = ParkingRecord(
                plate_number=f"京A{i:05d}",
                plate_color="蓝色",
                entry_time=now - timedelta(hours=i),
                exit_time=now - timedelta(hours=i - 1) if i % 2 == 0 else None,
                parking_fee=float(i * 5) if i % 2 == 0 else None,
            )
            db.session.add(r)
        db.session.commit()
    return app


class TestQuery:
    def test_no_filter(self, record_app):
        with record_app.app_context():
            result = RecordService.query()
        assert result["total"] == 5
        assert len(result["records"]) == 5

    def test_pagination(self, record_app):
        with record_app.app_context():
            result = RecordService.query(page=1, limit=2)
        assert result["total"] == 5
        assert len(result["records"]) == 2
        assert result["page"] == 1
        assert result["limit"] == 2

    def test_page_out_of_range(self, record_app):
        with record_app.app_context():
            result = RecordService.query(page=100, limit=10)
        assert len(result["records"]) == 0

    def test_filter_by_plate(self, record_app):
        with record_app.app_context():
            result = RecordService.query(plate_number="京A00000")
        assert result["total"] == 1
        assert result["records"][0]["plate_number"] == "京A00000"

    def test_filter_unknown_plate(self, record_app):
        with record_app.app_context():
            result = RecordService.query(plate_number="不存在")
        assert result["total"] == 0


class TestGetById:
    def test_found(self, record_app):
        with record_app.app_context():
            first = db.session.query(ParkingRecord).first()
        with record_app.app_context():
            r = RecordService.get_by_id(first.id)
        assert r["plate_number"] == first.plate_number

    def test_not_found(self, record_app):
        with record_app.app_context():
            with pytest.raises(NotFoundError):
                RecordService.get_by_id(99999)


class TestTodayStats:
    def test_returns_structure(self, record_app):
        with record_app.app_context():
            stats = RecordService.get_today_stats()
        assert "entries" in stats
        assert "exits" in stats
        assert "income" in stats
        assert "timestamp" in stats
