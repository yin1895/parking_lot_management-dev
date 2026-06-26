"""测试 会员服务 (member_service.py)"""
import pytest
from backend.services.member_service import MemberService
from backend.utils.exceptions import NotFoundError, ConflictError, ValidationError


class TestMemberService:
    def test_list_empty(self, db_session, app):
        with app.app_context():
            members = MemberService.list_all()
        assert members == []

    def test_create_and_list(self, db_session, app):
        with app.app_context():
            m = MemberService.create({"name": "李四", "plate_number": "沪B99999"})
            assert m["name"] == "李四"
            assert m["plate_number"] == "沪B99999"

            all_m = MemberService.list_all()
            assert len(all_m) == 1

    def test_create_missing_fields(self, db_session, app):
        with app.app_context():
            with pytest.raises(ValidationError):
                MemberService.create({"name": ""})
            with pytest.raises(ValidationError):
                MemberService.create({})

    def test_create_duplicate_plate(self, db_session, app):
        with app.app_context():
            MemberService.create({"name": "王五", "plate_number": "京A88888"})
            with pytest.raises(ConflictError):
                MemberService.create({"name": "赵六", "plate_number": "京A88888"})

    def test_get_by_id(self, db_session, app):
        with app.app_context():
            m = MemberService.create({"name": "X", "plate_number": "粤C12345"})
            fetched = MemberService.get_by_id(m["id"])
            assert fetched["plate_number"] == "粤C12345"

    def test_get_by_id_not_found(self, db_session, app):
        with app.app_context():
            with pytest.raises(NotFoundError):
                MemberService.get_by_id(9999)

    def test_update(self, db_session, app):
        with app.app_context():
            m = MemberService.create({"name": "旧名", "plate_number": "苏D11111"})
            updated = MemberService.update(m["id"], {"name": "新名", "phone": "123"})
            assert updated["name"] == "新名"
            assert updated["phone"] == "123"
            # plate_number unchanged
            assert updated["plate_number"] == "苏D11111"

    def test_update_not_found(self, db_session, app):
        with app.app_context():
            with pytest.raises(NotFoundError):
                MemberService.update(9999, {"name": "x"})

    def test_delete(self, db_session, app):
        with app.app_context():
            m = MemberService.create({"name": "Del", "plate_number": "冀E22222"})
            MemberService.delete(m["id"])
            with pytest.raises(NotFoundError):
                MemberService.get_by_id(m["id"])

    def test_delete_not_found(self, db_session, app):
        with app.app_context():
            with pytest.raises(NotFoundError):
                MemberService.delete(9999)

    def test_create_with_extra_fields(self, db_session, app):
        with app.app_context():
            m = MemberService.create({
                "name": "钱七", "plate_number": "鲁F33333",
                "phone": "13900000000", "status": "active",
            })
            assert m["phone"] == "13900000000"
            assert m["status"] == "active"
