from unittest import TestCase
import backtrader as bt

import datetime
import pandas as pd
import numpy as np
import os, sys
import copy

import math
import warnings

from MyTT import *
from formula import *
from mysql import MySQLData
from printAnalyzer import printTradeAnalysis
from strategy import run_formula, buys_time
from strategy_底部连阳_回踩_突破 import Strategy


class TestStrategy(TestCase):
    def test(self):
        # 添加数据到cerebro
        data = MySQLData(
            "kline_ashare",
            symbol="300081",
            contract_type="spot",
            fromdate=datetime.datetime(2023, 1, 1),
            todate=datetime.datetime(2023, 6, 12),
            interval="1h",
        )
        result = self.run_formula(Strategy, data)
        self.assertIn("2020-01-01 19:00:00", result, "hit")

    def test_002896_30min_20230614_1000(self):
        # 添加数据到cerebro
        data = MySQLData(
            "kline_ashare",
            symbol="002896",
            contract_type="spot",
            fromdate=datetime.datetime(2023, 1, 1),
            todate=datetime.datetime(2023, 6, 20),
            interval="30m",
        )
        result = run_formula(Strategy, data)
        hit_list = list(result[0].orders.hit_dt.astype(str).values.tolist())
        self.assertIn("2023-06-14 09:30:00", hit_list, "hit")

    # 华西股份
    def test_000936_1d_20230609(self):
        data = MySQLData(
            "kline_ashare",
            symbol="000936",
            contract_type="spot",
            fromdate=datetime.datetime(2023, 1, 1),
            todate=datetime.datetime(2023, 6, 20),
            interval="1d",
        )
        result = run_formula(Strategy, data)
        hit_list = list(result[0].orders.hit_dt.astype(str).values.tolist())
        dates = result[0].orders.hit_dt.strftime('%Y-%m-%d')
        self.assertIn("2023-06-09", dates, "hit")
        self.assertEqual(len(dates), 1)

    def test_kline_em_index_减速器_1d(self):
        data = MySQLData(
            "kline_em",
            symbol="减速器",
            contract_type="index",
            fromdate=datetime.datetime(2023, 1, 1),
            todate=datetime.datetime(2023, 6, 20),
            interval="1d",
        )
        result = run_formula(Strategy, data)
        hit_list = list(result[0].orders.hit_dt.astype(str).values.tolist())
        self.assertGreater(len(hit_list), 0)
        dates = result[0].orders.hit_dt.dt.strftime('%Y-%m-%d')
        # 对series去重
        dates=dates.drop_duplicates()
        self.assertIn("2023-06-12", list(dates), "hit")
        self.assertEqual(len(dates), 2)
    def test_kline_em_index_CPO概念_1d(self):
        data = MySQLData(
            "kline_em",
            symbol="CPO概念",
            contract_type="index",
            fromdate=datetime.datetime(2023, 1, 1),
            todate=datetime.datetime(2023, 6, 20),
            interval="1d",
        )
        result = run_formula(Strategy, data)
        hit_list = list(result[0].orders.hit_dt.astype(str).values.tolist())
        self.assertGreater(len(hit_list), 0)
        dates = result[0].orders.hit_dt.dt.strftime('%Y-%m-%d')
        # 对series去重
        dates=dates.drop_duplicates()
        self.assertIn("2023-06-12", list(dates), "hit")
        self.assertEqual(len(dates), 2)
