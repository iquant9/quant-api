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
    def test_ban_kline_em_index_LED_1d(self):
        data = MySQLData(
            "kline_em",
            symbol="LED",
            contract_type="index",
            fromdate=datetime.datetime(2023, 3, 1),
            todate=datetime.datetime(2023, 6, 20),
            interval="1d",
        )
        result = run_formula(Strategy, data)
        hit_list = list(result[0].orders.hit_dt.astype(str).values.tolist())
        self.assertEqual( 0,len(hit_list))

    def test_ban_kline_em_index_eSIM_1d(self):
        data = MySQLData(
            "kline_em",
            symbol="eSIM",
            contract_type="index",
            fromdate=datetime.datetime(2023, 3, 1),
            todate=datetime.datetime(2023, 7, 20),
            interval="1d",
        )
        result = run_formula(Strategy, data)
        hit_list = list(result[0].orders.hit_dt.astype(str).values.tolist())
        self.assertEqual( 0,len(hit_list))

    def test_ban_kline_em_index_Chiplet概念_1d(self):
        data = MySQLData(
            "kline_em",
            symbol="Chiplet概念",
            contract_type="index",
            fromdate=datetime.datetime(2023, 3, 1),
            todate=datetime.datetime(2023, 7, 20),
            interval="1d",
        )
        result = run_formula(Strategy, data)
        hit_list = list(result[0].orders.hit_dt.astype(str).values.tolist())
        self.assertEqual( 0,len(hit_list))
