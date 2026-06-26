from flask import Blueprint, request
from backend.services.member_service import MemberService
from backend.utils.response import api_success, api_error
from backend.utils.decorators import require_role

member_bp = Blueprint('members', __name__)

@member_bp.route('', methods=['GET'])
def get_members():
    """获取所有会员列表"""
    members = MemberService.list_all()
    return api_success({"members": members})


@member_bp.route('', methods=['POST'])
def create_member():
    """添加新会员"""
    try:
        member = MemberService.create(request.json or {})
        return api_success({"member": member}, "会员添加成功", 201)
    except Exception as e:
        return api_error(str(e), getattr(e, "status_code", 500))


@member_bp.route('/<int:member_id>', methods=['GET'])
def get_member(member_id):
    """获取特定会员"""
    try:
        member = MemberService.get_by_id(member_id)
        return api_success({"member": member})
    except Exception as e:
        return api_error(str(e), getattr(e, "status_code", 500))


@member_bp.route('/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    """更新会员信息"""
    try:
        member = MemberService.update(member_id, request.json or {})
        return api_success({"member": member}, "会员更新成功")
    except Exception as e:
        return api_error(str(e), getattr(e, "status_code", 500))


@member_bp.route('/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    """删除会员"""
    try:
        MemberService.delete(member_id)
        return api_success(None, "会员已删除")
    except Exception as e:
        return api_error(str(e), getattr(e, "status_code", 500))
