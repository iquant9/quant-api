from formula import *
from formula_三段底背驰 import 三段底背驰
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
        ind = self.ind[self.datas[0]]
        self.f1 = 三段底背驰(self.datas[0], ind)

    def next(self):
        try:
            self.f()
        except:
            return

    def f(self):
        f1 = self.f1

        res = f1.hit()
        if res.hit == True:
            self.buy()
        return
