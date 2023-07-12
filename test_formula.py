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


class TestFormula(TestCase):
    def test_f_底部连阳上穿均线_1(self):
        # 添加数据到cerebro
        data = MySQLData(
            "kline_ashare",
            symbol="002995",
            contract_type="spot",
            fromdate=datetime.datetime(2023, 1, 1),
            todate=datetime.datetime(2023, 6, 12),
            interval="30m",
        )
        result=self.run_formula("反弹至均线后下跌不创新低", data)
        self.assertIn("2020-01-01 19:00:00",result,"hit")
    def test_f_底部连阳上穿均线_300081(self):
        # 添加数据到cerebro
        data = MySQLData(
            "kline_ashare",
            symbol="300081",
            contract_type="spot",
            fromdate=datetime.datetime(2023, 1, 1),
            todate=datetime.datetime(2023, 6, 12),
            interval="1h",
        )
        result=self.run_formula("反弹至均线后下跌不创新低", data)
        self.assertIn("2020-01-01 19:00:00",result,"hit")

    def run_formula(self, func_name, data):
        cerebro = bt.Cerebro()

        # 添加数据到cerebro
        cerebro.adddata(data)

        print("加载数据完毕")
        # 添加手续费，按照万分之二收取
        cerebro.broker.setcommission(commission=0.0002, stocklike=True)
        # 设置初始资金为100万
        cerebro.broker.setcash(1_0000_0000)
        # 添加策略
        cerebro.addstrategy(FormulaStrategy)

        cerebro.addanalyzer(bt.analyzers.PyFolio, timeframe=bt.TimeFrame.Minutes, compression=None)
        # 运行回测
        backtest_result = cerebro.run()
        return backtest_result
