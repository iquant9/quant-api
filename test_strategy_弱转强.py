from unittest import TestCase

from data import KlineData
from strategy import *
from strategy_弱转强 import Strategy


class TestStrategy(TestCase):
    def test_603598_20231130(self):
        # 引力传媒
        # 添加数据到cerebro
        data_a = KlineData(
            exchange="as",
            symbol="603598",
            freq="1h",
            start_date=datetime.datetime(2023, 8, 1),
            end_date=datetime.datetime(2023, 12, 12),
        )
        data_b= KlineData(
            exchange="emconcept",
            symbol="bk1151",
            freq="1h",
            start_date=datetime.datetime(2023, 8, 1),
            end_date=datetime.datetime(2023, 12, 12),
        )
        result = run_formula(Strategy, [data_a,data_b])
        hit_list = list(result[0].orders.hit_dt.astype(str).values.tolist())
        self.assertIn("2023-09-22 09:30:00", hit_list, "hit")
