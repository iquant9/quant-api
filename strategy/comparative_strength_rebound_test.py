import datetime
from pprint import pprint
from unittest import TestCase

import akshare
import pytz

from data import ArrowData
from strategy import *
from strategy import comparative_strength_rebound
from strategy.base import init_cerebro, print_result, TradeList, get_data
import backtrader as bt
import pandas as pd

from strategy.comparative_strength_rebound import Strategy


class TestStrategy(TestCase):
    def setUp(self):
        self.strategy = comparative_strength_rebound.Strategy

    def test_backtest_沪深300(self):
        cerebro = init_cerebro()
        freq = "1h"
        data_ref = get_data("asindex", "sh000300", freq,
                            start_date=datetime.datetime(2024, 1, 2),
                            end_date=datetime.datetime(2024, 12, 12), )

        cerebro.adddata(data_ref)
        df = akshare.stock_zh_a_spot_em()
        for symbol in df['代码'][:100]:
            try:
                data = get_data("as", symbol, freq,
                         start_date=datetime.datetime(2024, 1, 2),
                         end_date=datetime.datetime(2024, 12, 12), )
                cerebro.adddata(data)
            except:
                pass
        cerebro.addstrategy(self.strategy)  # 添加策略

        # 启动回测
        result = cerebro.run(tradehistory=True)
        # 返回结果
        ret = pd.DataFrame(result[0].analyzers.tradelist.get_analysis())
        pprint(ret)

    def test_backtest_算力(self):
        cerebro = init_cerebro()
        bk = "BK1134"
        data_ref = self.get_data(bk)
        cerebro.adddata(data_ref)
        df = akshare.stock_board_concept_cons_em(symbol="算力概念")
        for symbol in df['代码']:
            try:
                data = ArrowData(
                    exchange="as",
                    symbol=symbol,
                    freq="1h",
                    start_date=datetime.datetime(2024, 1, 2),
                    end_date=datetime.datetime(2024, 12, 12),
                    tz=pytz.timezone('Asia/Shanghai')
                )
                cerebro.adddata(data)
            except:
                pass
        cerebro.addstrategy(self.strategy)  # 添加策略

        # 启动回测
        result = cerebro.run(tradehistory=True)
        # 返回结果
        ret = pd.DataFrame(result[0].analyzers.tradelist.get_analysis())
        pprint(ret)

    def test_克来机电_1h(self):
        # 引力传媒
        # 添加数据到cerebro
        data_a = self.get_data("BK1090")
        data_b = ArrowData(
            exchange="as",
            symbol="603960",
            freq="1h",
            start_date=datetime.datetime(2024, 1, 2),
            end_date=datetime.datetime(2024, 12, 12),
            tz=pytz.timezone('Asia/Shanghai')
        )

        cerebro = get_cerebro([data_a, data_b])
        cerebro = bt.Cerebro()
        cerebro.adddata(data_a)
        cerebro.adddata(data_b)

        cerebro.addstrategy(self.strategy)  # 添加策略

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

    def test_华映科技_5m(self):
        # 华映科技
        # 添加数据到cerebro
        freq = "5m"
        data_a = get_data("emindustry", "BK1038", freq, )
        data_b = get_data("as", "000536", freq, )

        cerebro = init_cerebro()
        cerebro.adddata(data_a)
        cerebro.adddata(data_b)

        cerebro.addstrategy(self.strategy)  # 添加策略

        result = cerebro.run(tradehistory=True)
        hit_list = list(result[0].orders.hit_dt.astype(str).values.tolist())
        self.assertIn("2024-02-22 13:30:00", hit_list, "hit")
        self.assertNotIn("2024-03-05 09:50:00", hit_list, "hit")
        # 返回结果
        ret = pd.DataFrame(result[0].analyzers.tradelist.get_analysis())
        pprint(ret)
