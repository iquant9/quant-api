from formula import *
from strategy import BaseStrategy


# 我们使用的时候，直接用我们新的类读取数据就可以了。
class Strategy(BaseStrategy):
    params = (
        ('period', 30),
        ('hold_percent', 0.02)
    )

    def __init__(self):
        self.formula = Formula()
        # Keep a reference to the "close" line in the data[0] dataseries
        self.bar_num = 0
        # 保存现有持仓的股票
        self.position_dict = {}
        # 当前有交易的股票
        self.stock_dict = {}
        # 指标
        self.ind = {}
        # 均线
        for d in self.datas:
            self.ind[d] = Ind()
            self.ind[d].ma5 = bt.ind.SMA(d, period=5)
            self.ind[d].ma10 = bt.ind.SMA(d, period=10)
            self.ind[d].ma20 = bt.ind.SMA(d, period=20)
            # self.ind[d].ma60 = bt.ind.SMA(d, period=60)
            # self.ind[d].ma120 = bt.ind.SMA(d, period=120)

    def next(self):
        current_date = self.datas[0].datetime.datetime(0)
        long_list = []
        short_list = []
        n = self.formula.LAST_底部连阳上穿均线(self.data, self.ind[self.data])
        if n <= 3:
            return

        high1 = HHVBARS(self.formula.get_array(self.data.close), n)
        if high1 != 0:
            return False
        condition1 = self.formula.反弹至均线后下跌不创新低(self.data, self.ind[self.data])
        if condition1:
            self.order = self.buy(data=self.data)
