from datetime import datetime
from backend.models.parking_record import ParkingRecord
from backend.models.member import Member
from backend.services.fee_calculator import FeeCalculator
from backend.models import db_session

class ParkingService:
    def __init__(self):
        self.fee_calculator = FeeCalculator()
        
    def record_entry(self, plate_number, plate_color='蓝色'):
        """记录车辆入场"""
        try:
            # 检查车辆是否已在场内
            existing_record = ParkingRecord.get_active_by_plate(plate_number)
            if existing_record:
                return {
                    'success': False,
                    'message': f'车辆 {plate_number} 已在停车场内',
                    'record': existing_record.to_dict()
                }
            
            # 创建新记录
            entry_time = datetime.now()
            record = ParkingRecord(
                plate_number=plate_number,
                plate_color=plate_color,
                entry_time=entry_time
            )
            
            db_session.add(record)
            db_session.commit()
            
            return {
                'success': True,
                'message': f'车辆 {plate_number} 成功入场',
                'record': record.to_dict()
            }
        except Exception as e:
            db_session.rollback()
            return {
                'success': False,
                'message': f'记录入场失败: {str(e)}'
            }
    
    def record_exit(self, plate_number):
        """记录车辆出场并计算费用"""
        try:
            # 获取车辆入场记录
            record = ParkingRecord.get_active_by_plate(plate_number)
            if not record:
                return {
                    'success': False,
                    'message': f'未找到车辆 {plate_number} 的入场记录'
                }
            
            # 更新出场时间
            exit_time = datetime.now()
            record.exit_time = exit_time
            
            # 检查是否是会员
            member = Member.get_by_plate(plate_number)
            
            # 计算费用
            fee_details = self.fee_calculator.calculate(
                record.entry_time, 
                exit_time,
                is_member=(member is not None)
            )
            
            # 更新记录
            record.parking_fee = fee_details['total_fee']
            record.save()
            
            return {
                'success': True,
                'message': f'车辆 {plate_number} 成功出场',
                'record': record.to_dict(),
                'fee_details': fee_details
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'记录出场失败: {str(e)}'
            }
    
    def get_status(self):
        """获取停车场状态"""
        try:
            # 获取当前在场车辆数量
            active_vehicles = ParkingRecord.count_active()
            # 假设总车位为100
            total_spaces = 100
            available_spaces = total_spaces - active_vehicles
            
            return {
                'success': True,
                'total_spaces': total_spaces,
                'occupied_spaces': active_vehicles,
                'available_spaces': available_spaces,
                'occupancy_rate': (active_vehicles / total_spaces) * 100
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'获取停车场状态失败: {str(e)}'
            }
