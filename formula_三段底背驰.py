import backtrader as bt
import datetime
import pandas as pd
import numpy as np
import os, sys
import copy

import math
import warnings

from MyTT import *
from formula import Formula
from printAnalyzer import printTradeAnalysis


# 沪深300 1d 20220426
class 三段底背驰(Formula):
    def __init__(self):
        super().__init__(self)

    def hit(self):
        k = self.data
        高点t = BARSLAST(self.DIF() > 0)
        高点后第一次金叉t = REF(BARSSINCEN(CROSS(self.DIF(), self.DEA()), 高点t))
        高点后第二次金叉t = REF(BARSSINCEN(CROSS(self.DIF(), self.DEA()), 高点后第一次金叉t))
