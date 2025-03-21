from datetime import datetime

class FeeCalculator:
    def calculate(self, entry_time, exit_time, is_member=False):
        """计算停车费用"""
        duration = (exit_time - entry_time).total_seconds() / 60  # 分钟
        duration_hours = duration / 60
        rate = 8 if is_member else 10
        total_fee = round(duration_hours * rate, 2)
        return {
            'duration': duration,
            'duration_hours': duration_hours,
            'rate': rate,
            'is_member': is_member,
            'total_fee': total_fee
        }
