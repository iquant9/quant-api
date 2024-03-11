from unittest import TestCase

import datetime

from data import KlineData
from strategy import run_formula
from strategy_底部连阳_回踩_突破 import Strategy


class TestStrategy(TestCase):
    def test_张江高科_1d_20230614_1000(self):
        # 添加数据到cerebro
        data = MySQLData(
            "kline_ashare",
            symbol="002896",
            contract_type="spot",
            start_date=datetime.datetime(2023, 1, 1),
            end_date=datetime.datetime(2023, 6, 20),
            interval="30m",
        )
        result = run_formula(Strategy, data)
        hit_list = list(result[0].orders.hit_dt.astype(str).values.tolist())
        self.assertIn("2023-06-14 09:30:00", hit_list, "hit")

    def test_002896_30min_20230614_1000(self):
        # 添加数据到cerebro
        data = MySQLData(
            "kline_ashare",
            symbol="002896",
            contract_type="spot",
            start_date=datetime.datetime(2023, 1, 1),
            end_date=datetime.datetime(2023, 6, 20),
            interval="30m",
        )
        result = run_formula(Strategy, data)
        hit_list = list(result[0].orders.hit_dt.astype(str).values.tolist())
        self.assertIn("2023-06-14 09:30:00", hit_list, "hit")

    # 华西股份
    def test_000936_1d_20230609(self):
        data = KlineData(
            "as_000933_1m",
            start_date=datetime.datetime(2023, 1, 1),
            end_date=datetime.datetime(2023, 6, 20),
            interval="1d",
        )
        result = run_formula(Strategy, data)
        hit_list = list(result[0].orders.hit_dt.astype(str).values.tolist())
        dates = result[0].orders.hit_dt.strftime('%Y-%m-%d')
        self.assertIn("2023-06-09", dates, "hit")
        self.assertEqual(len(dates), 1)

    def test_kline_em_index_减速器_1d(self):
        # hit 2023-06-12
        data = KlineData(
            table="em_减速器_1d",
            start_date=datetime.datetime(2023, 1, 1),
            end_date=datetime.datetime(2023, 6, 20),
            freq="1d",
        )
        result = run_formula(Strategy, data)
        hit_list = list(result[0].orders.hit_dt.astype(str).values.tolist())
        self.assertGreater(len(hit_list), 0)
        dates = result[0].orders.hit_dt.dt.strftime('%Y-%m-%d')
        # 对series去重
        dates = dates.drop_duplicates()
        self.assertIn("2023-06-12", list(dates), "hit")
        self.assertEqual(len(dates), 2)

    def test_kline_em_index_CPO概念_1d(self):
        data = KlineData(
            "kline_em",
            symbol="CPO概念",
            contract_type="index",
            start_date=datetime.datetime(2023, 1, 1),
            end_date=datetime.datetime(2023, 6, 20),
            interval="1d",
        )
        result = run_formula(Strategy, data)
        hit_list = list(result[0].orders.hit_dt.astype(str).values.tolist())
        self.assertGreater(len(hit_list), 0)
        dates = result[0].orders.hit_dt.dt.strftime('%Y-%m-%d')
        # 对series去重
        dates = dates.drop_duplicates()
        self.assertIn("2023-06-12", list(dates), "hit")
        self.assertEqual(len(dates), 2)

    def test_kline_em_index_AIGC概念_1d(self):
        data = KlineData(
            "kline_em",
            symbol="AIGC概念",
            contract_type="index",
            start_date=datetime.datetime(2022, 10, 1),
            end_date=datetime.datetime(2023, 1, 20),
            interval="1d",
        )
        result = run_formula(Strategy, data)
        hit_list = list(result[0].orders.hit_dt.astype(str).values.tolist())
        self.assertGreater(len(hit_list), 0)
        dates = result[0].orders.hit_dt.dt.strftime('%Y-%m-%d')
        # 对series去重
        dates = dates.drop_duplicates()
        self.assertIn("2023-06-12", list(dates), "hit")
        self.assertEqual(len(dates), 2)
