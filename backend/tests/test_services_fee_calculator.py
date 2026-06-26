"""测试 计费服务 (fee_calculator.py) — 纯逻辑，不需要 DB"""
from datetime import datetime, timedelta
from backend.services.fee_calculator import FeeCalculator


class TestFeeCalculator:
    def setup_method(self):
        self.calc = FeeCalculator()

    def test_basic_calculation(self):
        entry = datetime(2026, 6, 26, 8, 0)
        exit_ = datetime(2026, 6, 26, 10, 30)
        result = self.calc.calculate(entry, exit_)
        # 2.5 hours × 10 = 25.0
        assert result["total_fee"] == 25.0
        assert result["rate"] == 10
        assert result["is_member"] is False

    def test_member_discount(self):
        entry = datetime(2026, 6, 26, 8, 0)
        exit_ = datetime(2026, 6, 26, 10, 0)
        result = self.calc.calculate(entry, exit_, is_member=True)
        assert result["rate"] == 8  # member rate
        assert result["is_member"] is True
        assert result["total_fee"] == 16.0  # 2h × 8

    def test_short_stay(self):
        entry = datetime(2026, 6, 26, 12, 0)
        exit_ = datetime(2026, 6, 26, 12, 15)
        result = self.calc.calculate(entry, exit_)
        assert result["duration"] == 15  # 15 minutes
        assert result["total_fee"] == 2.5  # 0.25h × 10

    def test_zero_duration(self):
        entry = datetime(2026, 6, 26, 12, 0)
        exit_ = datetime(2026, 6, 26, 12, 0)
        result = self.calc.calculate(entry, exit_)
        assert result["duration"] == 0
        assert result["total_fee"] == 0

    def test_multiple_days(self):
        entry = datetime(2026, 6, 26, 8, 0)
        exit_ = datetime(2026, 6, 28, 8, 0)
        result = self.calc.calculate(entry, exit_)
        # 48 hours × 10
        assert result["total_fee"] == 480.0

    def test_duration_precision(self):
        entry = datetime(2026, 6, 26, 8, 0)
        exit_ = datetime(2026, 6, 26, 8, 1)
        result = self.calc.calculate(entry, exit_)
        assert result["duration"] == 1  # 1 minute
        # 1/60 hours × 10 ≈ 0.17
        assert abs(result["total_fee"] - 0.17) < 0.01
