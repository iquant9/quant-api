from unittest import TestCase

import datetime

from data import new_data
from strategy import run_formula
from strategy_极值对比 import Strategy


class TestStrategy(TestCase):
    def test_房地产_1h_20230614_1000(self):
        start_date = datetime.datetime(2023, 5, 1)
        end_date = datetime.datetime(2023, 8, 12)
        symbols = ["kline_asindex:index:sz399001:1h", "kline_asindex:em:创业板综:1h"]
        datas = []
        for section in symbols:
            datas.append(new_data(section, start_date, end_date))
        result = run_formula(Strategy, datas)
        hit_list = list(result[0].orders.hit_dt.astype(str).values.tolist())
        self.assertIn("2023-06-14 09:30:00", hit_list, "hit")

    # 华西股份
    def test_券商概念_1d_20230724(self):
        start_date = datetime.datetime(2023, 5, 1)
        end_date = datetime.datetime(2023, 8, 12)
        symbols = ["kline_asindex:index:sz399001:1h", "kline_asindex:em:券商概念:1h"]
        datas = []
        for section in symbols:
            datas.append(new_data(section, start_date, end_date))
        result = run_formula(Strategy, datas)
        hit_list = list(result[0].orders.hit_dt.astype(str).values.tolist())
        self.assertIn("2023-07-24 13:00:00", hit_list, "hit")
