from flask import Blueprint, request, jsonify
from backend.models.member import Member
from backend.models import db_session

member_bp = Blueprint('members', __name__)

@member_bp.route('', methods=['GET'])
def get_members():
    """获取所有会员"""
    try:
        members = db_session.query(Member).all()
        result = {
            'success': True,
            'members': [member.to_dict() for member in members]
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取会员列表失败: {str(e)}'
        }), 500

@member_bp.route('', methods=['POST'])
def create_member():
    """添加新会员"""
    try:
        data = request.json
        # 验证必要字段
        if not data.get('name') or not data.get('plate_number'):
            return jsonify({
                'success': False,
                'message': '名称和车牌号不能为空'
            }), 400
            
        # 检查车牌号是否已存在
        existing = db_session.query(Member).filter_by(plate_number=data.get('plate_number')).first()
        if existing:
            return jsonify({
                'success': False,
                'message': f'车牌号 {data.get("plate_number")} 已存在'
            }), 400
        
        # 创建新会员
        member = Member(
            name=data.get('name'),
            plate_number=data.get('plate_number'),
            phone=data.get('phone'),
            status=data.get('status', 'active')
        )
        
        db_session.add(member)
        db_session.commit()
        
        return jsonify({
            'success': True,
            'message': '会员添加成功',
            'member': member.to_dict()
        }), 201
    except Exception as e:
        db_session.rollback()
        return jsonify({
            'success': False,
            'message': f'添加会员失败: {str(e)}'
        }), 500

@member_bp.route('/<int:member_id>', methods=['GET'])
def get_member(member_id):
    """获取特定会员"""
    try:
        member = db_session.query(Member).get(member_id)
        if not member:
            return jsonify({
                'success': False,
                'message': '会员不存在'
            }), 404
            
        return jsonify({
            'success': True,
            'member': member.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取会员失败: {str(e)}'
        }), 500

@member_bp.route('/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    """更新会员信息"""
    try:
        data = request.json
        member = db_session.query(Member).get(member_id)
        
        if not member:
            return jsonify({
                'success': False,
                'message': '会员不存在'
            }), 404
            
        # 更新字段
        if 'name' in data:
            member.name = data['name']
        if 'phone' in data:
            member.phone = data['phone']
        if 'status' in data:
            member.status = data['status']
            
        db_session.commit()
        
        return jsonify({
            'success': True,
            'message': '会员更新成功',
            'member': member.to_dict()
        })
    except Exception as e:
        db_session.rollback()
        return jsonify({
            'success': False,
            'message': f'更新会员失败: {str(e)}'
        }), 500

@member_bp.route('/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    """删除会员"""
    try:
        member = db_session.query(Member).get(member_id)
        
        if not member:
            return jsonify({
                'success': False,
                'message': '会员不存在'
            }), 404
            
        db_session.delete(member)
        db_session.commit()
        
        return jsonify({
            'success': True,
            'message': '会员已删除'
        })
    except Exception as e:
        db_session.rollback()
        return jsonify({
            'success': False,
            'message': f'删除会员失败: {str(e)}'
        }), 500
