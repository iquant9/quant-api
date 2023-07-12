from formula import *
from strategy import BaseStrategy


# 我们使用的时候，直接用我们新的类读取数据就可以了。
class Strategy(BaseStrategy):
    params = (
        ('period', 30),
        ('hold_percent', 0.02)
    )

    def __init__(self):
        super().__init__()
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
            m = bt.indicators.MACD(self.data,
                                   period_me1=12,
                                   period_me2=26,
                                   period_signal=9)
            self.ind[d].dif = m.macd
            self.ind[d].dea = m.signal
            self.ind[d].macd = m.macd - m.signal

    def next(self):
        current_date = self.datas[0].datetime.datetime(0)
        long_list = []
        short_list = []
        if current_date.day == 14:
            pass
        if current_date.day == 12:
            pass
        k = self.data
        ind = self.ind[self.data]
        if ind.dif < 0:
            return False
        hit, start, end = self.formula.LAST_底部连阳上穿均线(self.data, self.ind[self.data])
        if not hit:
            return
        if end <= 3:
            return
        # 陷阱1：回踩太多，比如dif已经到水下，说明股价已经失控，形态已经失效
        dif和macd在水下 = BARSLAST((self.formula.get_array(ind.dif) < 0) &(self.formula.get_array(ind.macd)<0))
        if dif和macd在水下[-1]<end:
            return False
        # 临界条件
        close_arr = self.formula.get_array(self.data.close)
        ma5_arr = self.formula.get_array(self.ind[self.data].ma5.line)
        ma10_arr = self.formula.get_array(self.ind[self.data].ma10.line)

        high1 = HHVBARS(close_arr, start)
        if high1[-1] != 0:
            if CROSS(close_arr, ma5_arr)[-1] and CROSS(close_arr, ma10_arr)[-1]:
                self.order = self.buy(data=self.data)
                return True
            return False
        # 只在第一次新高产生买点，避免连续的新高连续命中
        if REF(high1, 1)[-1] < 2:
            return False
        self.order = self.buy(data=self.data)
