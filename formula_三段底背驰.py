import logging

import backtrader as bt
import datetime
import pandas as pd
import numpy as np
import os, sys
import copy

import math
import warnings

from MyTT import *
from formula import Formula, Result
from printAnalyzer import printTradeAnalysis


# 沪深300 1d 20220426
class 三段底背驰(Formula):
    # 1. dif最低点不能在第一波
    # 2. 有面积递减的三个波
    def hit(self):
        res = Result()
        # 提升效率：dif or dea不能>=0
        if self.ind.dif >= 0 or self.ind.dea >= 0:
            return res
        # macd在水上
        高点t = self.T(BARSLAST(np.logical_and(self.DIF() > 0, self.MACD() < 0)))
        if 高点t <= 30:
            return res
        t1, t2 = self.get_date(ref=高点t), self.get_date()
        if t2.date() == datetime.date(2023, 10, 19):
            pass
        elif t2.date() == datetime.date(2022, 4, 26):
            pass
        else:
            return res
        wave1_start, wave1_end = self.get_第1次绿波(高点t)
        t1, t2 = self.get_date(ref=wave1_start), self.get_date(ref=wave1_end)
        low1 = self.LLV(self.C(), wave1_start, wave1_end)
        tmp = wave1_end - 2
        while True:
            wave2_start, wave2_end = self.get_第1次绿波(tmp)
            count = self.COUNT(self.C() < low1 * 0.99, wave2_start, wave2_end)
            if count <= 2:
                tmp = wave2_end
            else:
                break

        t1, t2 = self.get_date(ref=wave2_start), self.get_date(ref=wave2_end)

        高点后第2次金叉t = self.BARSSINCEN(CROSS(self.DIF(), self.DEA()), 高点后第1次金叉t)
        if 高点后第2次金叉t < 10:
            return res
        最近一次死叉t = self.BARSLAST(CROSS(self.DEA(), self.DIF()))
        if 最近一次死叉t > 高点后第2次金叉t:
            return res
        logging.info(self.get_date(ref=高点t), self.get_date())
        wave1_end = self.BARSSINCEN(self.MACD() > 0, 高点t)
        if wave1_end > 高点t:
            return res
        wave1 = []
        t1, t2 = self.get_date(ref=高点t), self.get_date()
        if t2.date() == datetime.date(2023, 10, 19):
            pass
        res.hit = True
        return res

    def get_第1次绿波(self, 高点t):
        高点后第1次金叉t = self.BARSSINCEN(CROSS(self.DIF(), self.DEA()), 高点t)
        第1次死叉t = self.BARSLAST(CROSS(self.DEA(), self.DIF()), ref=高点后第1次金叉t)
        return 第1次死叉t, 高点后第1次金叉t

    def get_第2次绿波(self, 高点t):
        高点后第1次金叉t = self.BARSSINCEN(CROSS(self.DIF(), self.DEA()), 高点t)
        第1次死叉t = self.BARSLAST(CROSS(self.DIF(), self.DEA()), ref=高点后第1次金叉t)
        return 第1次死叉t, 高点后第1次金叉t
