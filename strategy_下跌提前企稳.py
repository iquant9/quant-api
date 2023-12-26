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
        for i in range(1, len(self.datas)):
            try:
                if self.f(i).hit is True:
                    self.buy(data=self.datas[i])
                    return
            except Exception as e:
                continue

    def f(self, b_index):
        res = Result()
        a = self.datas[0]  # 指数
        a_ind = self.ind[a]
        af = Formula(a, a_ind)
        b = self.datas[b_index]  # 个股
        b_ind = self.ind[b]
        bf = Formula(b, b_ind)
        a_closes = af.C()
        b_closes = bf.C()
        t1 = af.get_date(ref=0)
        if t1.date() == datetime.date(2023, 9, 20):
            pass
        # 大指数连续下跌两天
        if af.REF(a_closes, 0) / af.REF(a_closes, 1) < 1 and af.REF(a_closes, 1) / af.REF(a_closes, 2) < 1:
            pass
        else:
            return False
        # 股票连续上涨两天
        if bf.REF(b_closes, 0) / bf.REF(b_closes, 1) > 1 and bf.REF(b_closes, 1) / bf.REF(b_closes, 2) > 1:
            pass
        else:
            return False
        # 已经连续n天出现同步下跌
        a_zd = a_closes > REF(a_closes, 1)
        b_zd = b_closes > REF(b_closes, 1)
        同步 = 0
        for i in range(2, 10):
            if a_zd[-i] == b_zd[-i]:
                同步 += 1
        if 同步 < 3:
            return False
        res.hit = True
        return res
