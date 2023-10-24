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
        # Keep a reference to the "close" line in the data[0] dataseries
        self.bar_num = 0
        # 保存现有持仓的股票
        self.position_dict = {}
        # 当前有交易的股票
        self.stock_dict = {}

    def next(self):
        try:
            self.f()
        except:
            return

    def f(self):
        f0 = Formula(self.datas[0])
        current_date = f0.get_current_date()
        long_list = []
        short_list = []
        if current_date.day == 22:
            pass
        k = self.data
        ind = self.ind[self.data]
        # if ind.dif < 0:
        #     return False
        if ind.ma60 is not None and k.close < ind.ma60:
            pass
        else:
            return False

        # 找出最近40天的最高价
        n = 40
        if len(self.data) < n:
            n = len(self.data)
        high_t = HHVBARS(f0.C(), n)[-1]
        hit, start, end = self.formula.LAST_底部连阳上穿均线(self.data, self.ind[self.data])
        if not hit:
            return
        if end <= 3:
            return
        if ind.vol5:
            vol5_arr = self.formula.get_array(ind.vol5)
            if (vol5_arr < REF(vol5_arr, 1))[-1]:
                return False
        vol_arr = self.formula.get_array(self.data.volume)
        # 【筛选】上涨期间应该是放量的，随后的回调应该是缩量的，成交量至少缩1/2
        上涨期间max_vol = HHV(REF(vol_arr, end), start - end)[-1]
        if not COUNT(vol_arr < (上涨期间max_vol / 2), end)[-1]:
            return False
        # 陷阱1：回踩太多，比如dif已经到水下，说明股价已经失控，形态已经失效
        dif和macd在水下 = BARSLAST((self.formula.get_array(ind.dif) < 0) & (self.formula.get_array(ind.macd) < 0))
        if dif和macd在水下[-1] < end:
            return False
        # 临界条件
        close_arr = self.formula.get_array(self.data.close)
        ma5_arr = self.formula.get_array(self.ind[self.data].ma5.line)
        ma10_arr = self.formula.get_array(self.ind[self.data].ma10.line)

        high1 = HHVBARS(close_arr, start)
        # 如果今天不是最高价，要求上穿ma5和ma10
        if high1[-1] != 0:
            if k.volume < ind.vol5:
                return False
            if CROSS(close_arr, ma5_arr)[-1] and CROSS(close_arr, ma10_arr)[-1]:
                self.order = self.buy(data=self.data)
                return True
            return False
        # 只在第一次新高产生买点，避免连续的新高连续命中
        if REF(high1, 1)[-1] < 2:
            return False
