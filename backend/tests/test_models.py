"""测试 数据模型序列化 (models/)"""
from datetime import datetime
import pytest
from flask import Flask

from backend.models import init_db, db
from backend.models.user import User
from backend.models.member import Member
from backend.models.parking_record import ParkingRecord


@pytest.fixture
def model_app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    init_db(app)
    return app


class TestUserModel:
    def test_to_dict(self, model_app):
        with model_app.app_context():
            u = User(username="tester", password="hash", email="t@t.com", role="admin")
            db.session.add(u)
            db.session.commit()
            # BaseModel has id, created_at, updated_at
            assert u.id is not None
            assert u.username == "tester"
            assert u.role == "admin"

    def test_create_default_admin(self, model_app):
        with model_app.app_context():
            User.create_default_admin()
            admin = db.session.query(User).filter_by(username="admin").first()
            assert admin is not None
            assert admin.role == "admin"
            # Idempotent — second call should not crash
            User.create_default_admin()
            count = db.session.query(User).filter_by(username="admin").count()
            assert count == 1


class TestMemberModel:
    def test_to_dict(self, model_app):
        with model_app.app_context():
            m = Member(name="张三", plate_number="京A88888", phone="13800000000", status="active")
            db.session.add(m)
            db.session.commit()
            d = m.to_dict()
            assert d["name"] == "张三"
            assert d["plate_number"] == "京A88888"
            assert d["phone"] == "13800000000"
            assert d["status"] == "active"
            assert "id" in d
            assert "created_at" in d

    def test_to_dict_none_dates(self, model_app):
        with model_app.app_context():
            m = Member(name="李四", plate_number="沪B12345")
            # to_dict should handle None created_at
            d = m.to_dict()
            assert d["created_at"] is None

    def test_get_by_plate(self, model_app):
        with model_app.app_context():
            m = Member(name="王五", plate_number="粤C54321")
            db.session.add(m)
            db.session.commit()
            found = Member.get_by_plate("粤C54321")
            assert found is not None
            assert found.name == "王五"
            assert Member.get_by_plate("nonexistent") is None


class TestParkingRecordModel:
    def test_to_dict(self, model_app):
        with model_app.app_context():
            now = datetime.utcnow()
            r = ParkingRecord(
                plate_number="京A12345",
                plate_color="蓝色",
                entry_time=now,
                parking_fee=25.0,
            )
            db.session.add(r)
            db.session.commit()
            d = r.to_dict()
            assert d["plate_number"] == "京A12345"
            assert d["parking_fee"] == 25.0
            assert d["exit_time"] is None

    def test_get_active_by_plate(self, model_app):
        with model_app.app_context():
            now = datetime.utcnow()
            r1 = ParkingRecord(plate_number="京A11111", entry_time=now)
            r2 = ParkingRecord(plate_number="京A11111", entry_time=now, exit_time=now)
            db.session.add_all([r1, r2])
            db.session.commit()
            # active = no exit_time
            active = ParkingRecord.get_active_by_plate("京A11111")
            assert active is not None
            assert active.exit_time is None

    def test_get_active_not_found(self, model_app):
        with model_app.app_context():
            assert ParkingRecord.get_active_by_plate("京X00000") is None

    def test_count_active(self, model_app):
        with model_app.app_context():
            now = datetime.utcnow()
            r1 = ParkingRecord(plate_number="京A00001", entry_time=now)
            r2 = ParkingRecord(plate_number="京A00002", entry_time=now)
            r3 = ParkingRecord(plate_number="京A00003", entry_time=now, exit_time=now)
            db.session.add_all([r1, r2, r3])
            db.session.commit()
            assert ParkingRecord.count_active() == 2

    def test_save(self, model_app):
        with model_app.app_context():
            r = ParkingRecord(plate_number="京A99999", entry_time=datetime.utcnow())
            db.session.add(r)
            db.session.commit()
            r.parking_fee = 100.0
            r.save()
            reloaded = db.session.query(ParkingRecord).get(r.id)
            assert reloaded.parking_fee == 100.0

    def test_base_model_timestamps(self, model_app):
        with model_app.app_context():
            now = datetime.utcnow()
            r = ParkingRecord(plate_number="京A00000", entry_time=now)
            db.session.add(r)
            db.session.commit()
            assert r.created_at is not None
            assert r.updated_at is not None
