import logging
from backend.models.member import Member
from backend.models import db
from backend.utils.exceptions import NotFoundError, ConflictError, ValidationError

logger = logging.getLogger(__name__)


class MemberService:
    """会员管理服务"""

    @staticmethod
    def list_all() -> list:
        return [m.to_dict() for m in db.session.query(Member).all()]

    @staticmethod
    def get_by_id(member_id: int) -> dict:
        member = db.session.query(Member).get(member_id)
        if not member:
            raise NotFoundError("会员不存在")
        return member.to_dict()

    @staticmethod
    def create(data: dict) -> dict:
        name = data.get("name")
        plate_number = data.get("plate_number")
        if not name or not plate_number:
            raise ValidationError("名称和车牌号不能为空")

        if db.session.query(Member).filter_by(plate_number=plate_number).first():
            raise ConflictError(f"车牌号 {plate_number} 已存在")

        member = Member(
            name=name,
            plate_number=plate_number,
            phone=data.get("phone"),
            status=data.get("status", "active"),
        )
        db.session.add(member)
        db.session.commit()
        logger.info(f"创建会员: {name} ({plate_number})")
        return member.to_dict()

    @staticmethod
    def update(member_id: int, data: dict) -> dict:
        member = db.session.query(Member).get(member_id)
        if not member:
            raise NotFoundError("会员不存在")

        if "name" in data:
            member.name = data["name"]
        if "phone" in data:
            member.phone = data["phone"]
        if "status" in data:
            member.status = data["status"]

        db.session.commit()
        logger.info(f"更新会员: id={member_id}")
        return member.to_dict()

    @staticmethod
    def delete(member_id: int) -> None:
        member = db.session.query(Member).get(member_id)
        if not member:
            raise NotFoundError("会员不存在")
        db.session.delete(member)
        db.session.commit()
        logger.info(f"删除会员: id={member_id}")
