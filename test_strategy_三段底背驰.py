from unittest import TestCase

import datetime

from data import KlineData
from strategy import run_formula
from strategy_三段底背驰 import Strategy


class TestStrategy(TestCase):

    def test_399300_1d_220426(self):
        # 添加数据到cerebro
        data = KlineData(
            table="kline",
            exchange="asindex",
            symbol="sz399300",
            freq="1d",
            start_date=datetime.datetime(2021, 5, 1),
            end_date=datetime.datetime(2022, 4, 27),
        )
        result = run_formula(Strategy, data)
        hit_list = list(result[0].orders.hit_dt.astype(str).values.tolist())
        self.assertIn("2022-04-26 09:30:00", hit_list, "hit")
        self.assertNotIn("2023-10-19 09:30:00", hit_list, "hit")

    def test_硕贝德_2h_0928_1030(self):
        # 添加数据到cerebro
        data = KlineData(
            exchange="as",
            symbol="300322",
            freq="2h",
            start_date=datetime.datetime(2023, 9, 1),
            end_date=datetime.datetime(2023, 9, 28),
        )
        result = run_formula(Strategy, data)
        hit_list = list(result[0].orders.hit_dt.astype(str).values.tolist())
        self.assertIn("2023-09-28 10:30:00", hit_list, "hit")
