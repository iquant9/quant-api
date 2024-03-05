import backtrader as bt

from custom_mytt import HHV
from formula import Formula
from strategy.base import BaseStrategy, is_valid_number
import numpy as np


# ComparativeStrengthReboundStrategy 比较强度反弹策略
#
class ComparativeStrengthReboundStrategy(BaseStrategy):
    params = (
        ('lookback_period', 10),  # Lookback period for comparison
        ('threshold', 8),  # Threshold for 90% confidence
    )

    def __init__(self):
        super().__init__()
        self.ref_data = self.datas[0]
        self.other_datas = self.datas[1:]

    def prenext(self):
        # prenext()会从第一个交易日开始执行，知道所有的数据都存在交集的时候，切换到next()，当然可以在prenext()中主动调用next()
        self.next()

    def next(self):
        current_date = self.datas[0].datetime.datetime(0)
        if current_date.day == 22:
            pass
        if self.ref_data.close > self.ind[self.ref_data].ma20:
            return
            # Calculate the comparison result for each data
        # Loop through the other datas
        for data in self.other_datas:
            self.next_one(data)

    def next_one(self, data):
        current_date = self.datas[0].datetime.datetime(0)
        data_today = data.close[0]
        if data_today < data.ma5[0]:
            return
        # f1 = self.formula(data)
        pct_change_max = self.V(HHV(data.pct_change, 20))
        if not is_valid_number(pct_change_max):
            return
        # 过滤，命中的前提是当日涨幅相比近期最高涨幅，不能小于0.5
        if data.pct_change[0] / pct_change_max < 0.5:
            return
        data_yesterday = data.close[-1]
        # Compare the last 10 days of ref_data and data
        #  ago=-1是为了这10个价格里面不要包含今天的，是对过去10天的走势进行比较
        ref_closes = self.ref_data.get(size=self.params.lookback_period + 1, ago=-1)
        data_closes = data.get(size=self.params.lookback_period + 1, ago=-1)
        directions = []
        for i in range(len(ref_closes) - 1):
            same = ((ref_closes[i] <= ref_closes[i + 1]) == (data_closes[i] <= data_closes[i + 1]))
            directions.append(same)
        if len(list(directions)) == 0:
            return

        same_count = sum(directions)
        if same_count < self.params.threshold:
            return
        ref_today = self.ref_data.close[0]
        ref_yesterday = self.ref_data.close[-1]

        if ref_today < ref_yesterday and data_today > data_yesterday:
            self.log(f'BUY {data._name}, Ref Down and {data._name} Up')
            self.order = self.buy(data)
