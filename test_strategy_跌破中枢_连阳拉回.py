from unittest import TestCase
from strategy import *
from strategy_跌破中枢_连阳拉回 import Strategy


class TestStrategy(TestCase):
    def test_002896_1h_202300613_0930(self):
        # 添加数据到cerebro
        data = MySQLData(
            "kline_ashare",
            symbol="002896",
            contract_type="spot",
            start_date=datetime.datetime(2023, 1, 1),
            end_date=datetime.datetime(2023, 6, 12),
            interval="1h",
        )
        result = run_formula(Strategy, data)
        self.assertIn("2020-01-01 19:00:00", result, "hit")
