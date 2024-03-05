import datetime
from unittest import TestCase

import pytz

from data import ArrowData
from strategy import *
from strategy.base import get_cerebro
from strategy.strategy_相对强势 import ComparativeStrengthReboundStrategy
import backtrader as bt


class TestStrategy(TestCase):
    def test_克来机电_1h(self):
        # 引力传媒
        # 添加数据到cerebro
        data_a = ArrowData(
            exchange="emconcept",
            symbol="BK1090",
            freq="1h",
            start_date=datetime.datetime(2024, 1, 2),
            end_date=datetime.datetime(2024, 12, 12),
        )
        data_b = ArrowData(
            exchange="as",
            symbol="603960",
            freq="1h",
            start_date=datetime.datetime(2024, 1, 2),
            end_date=datetime.datetime(2024, 12, 12),
        )

        cerebro = get_cerebro([data_a, data_b])
        cerebro = bt.Cerebro()
        cerebro.adddata(data_a)
        cerebro.adddata(data_b)

        cerebro.addstrategy(ComparativeStrengthReboundStrategy)  # 添加策略

        result = cerebro.run()
        hit_list = list(result[0].orders.hit_dt.astype(str).values.tolist())
        self.assertIn("2024-02-01 10:30:00", hit_list, "hit")
    def test_中视传媒_1h(self):
        # 引力传媒
        # 添加数据到cerebro
        data_a = ArrowData(
            exchange="emindustry",
            symbol="BK0486",
            freq="1h",
            start_date=datetime.datetime(2024, 1, 1),
            end_date=datetime.datetime(2024, 12, 12),
        )
        data_b = ArrowData(
            exchange="as",
            symbol="600088",
            freq="1h",
            start_date=datetime.datetime(2024, 1, 1),
            end_date=datetime.datetime(2024, 12, 12),
        )

        cerebro = get_cerebro([data_a, data_b])
        cerebro = bt.Cerebro()
        cerebro.adddata(data_a)
        cerebro.adddata(data_b)

        cerebro.addstrategy(ComparativeStrengthReboundStrategy)  # 添加策略

        result = cerebro.run()
        hit_list = list(result[0].orders.hit_dt.astype(str).values.tolist())
        self.assertIn("2024-01-23 09:30:00", hit_list, "hit")
