from formula import *
from strategy import BaseStrategy


# 我们使用的时候，直接用我们新的类读取数据就可以了。
class Strategy(BaseStrategy):
    params = (
        ('last_frame', 30),
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

    def next(self):
        current_date = self.datas[0].datetime.datetime(0)
        long_list = []
        short_list = []
        if current_date.day == 24:
            pass
        if current_date.day == 12:
            pass
        k = self.data
        ind = self.ind[self.data]
        if ind.dif < 0:
            return False
        base = self.datas[0]
        close_arr = self.formula.get_array(base.close)

        min_closes = LLVBARS(close_arr, 30)
        if min_closes[-1] == 0:
            for data in self.datas[1:]:
                # base创新低，但是指数没有跌，也不要
                if data.close.get(0) > data.close.get(-1):
                    continue
                b_close_arr = self.formula.get_array(data.close)
                # a创新低，b创新低
                b_min_closes = LLVBARS(b_close_arr, 30)
                if not b_min_closes[-1] > 0:
                    continue
                ind_tmp = self.ind[self.data]
                if ind_tmp.dif > 0:
                    self.order = self.buy(data=data)
        return
