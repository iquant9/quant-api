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


# warnings.filterwarnings("ignore")
class 跌破中枢底背驰(Formula):
    def __init__(self):
        super().__init__(self)

    def hit(self):
        self.
