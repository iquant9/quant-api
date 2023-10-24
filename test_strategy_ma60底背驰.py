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
from data import KlineData
from printAnalyzer import printTradeAnalysis
from strategy import run_formula, buys_time
from strategy_ma60底背驰 import Strategy


class TestStrategy(TestCase):

    def test_张江高科_1h_0922_0930(self):
        # 添加数据到cerebro
        data = KlineData(
            exchange="as",
            symbol="600895",
            freq="1h",
            fromdate=datetime.datetime(2023, 9, 1),
            todate=datetime.datetime(2023, 11, 12),
        )
        result = run_formula(Strategy, data)
        hit_list = list(result[0].orders.hit_dt.astype(str).values.tolist())
        self.assertIn("2023-09-22 09:30:00", hit_list, "hit")

    def test_硕贝德_2h_0928_1030(self):
        # 添加数据到cerebro
        data = KlineData(
            exchange="as",
            symbol="300322",
            freq="2h",
            fromdate=datetime.datetime(2023, 9, 1),
            todate=datetime.datetime(2023, 9, 28),
        )
        result = run_formula(Strategy, data)
        hit_list = list(result[0].orders.hit_dt.astype(str).values.tolist())
        self.assertIn("2023-09-28 10:30:00", hit_list, "hit")
