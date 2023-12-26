from formula import *
from strategy import BaseStrategy


# 我们使用的时候，直接用我们新的类读取数据就可以了。
class Strategy(BaseStrategy):
    params = (
        ('last_frame', 30),
    )

    def __init__(self):
        super().__init__()
        self.a_formula = Formula()
        self.b_formula = Formula()

        # Keep a reference to the "close" line in the data[0] dataseries
        self.bar_num = 0
        # 保存现有持仓的股票
        self.position_dict = {}
        # 当前有交易的股票
        self.stock_dict = {}

    def next(self):
        current_date = self.datas[0].datetime.datetime(0)
        if current_date.strftime("%Y-%m-%d %H:%M:%S")=='2023-11-30 13:00:00':
            pass
        for i in range(int(len(self.datas)/2)):
            try:
                if self.is_buy(i*2):
                    self.order = self.buy(data=self.datas[i])
            except:
                pass

        return

    def is_buy(self, i):
        # a是个股,b是指数
        data_a, data_b = self.datas[i], self.datas[i + 1]
        ind_a, ind_b = self.ind[data_a], self.ind[data_b]
        self.a_formula.data=data_a
        self.b_formula.data=data_b

        if data_a.close.get(0) <= data_a.close.get(-1):
            return False
        a_上次比今天高_t = self.a_formula.BARSLAST(self.a_formula.C() > data_a.close.get(0))
        if a_上次比今天高_t > 0 and a_上次比今天高_t < 5:
            return False
        b_上次比今天高_t = self.b_formula.BARSLAST(self.b_formula.C()> data_b.close.get(0))
        if b_上次比今天高_t < 0:
            return False
        if b_上次比今天高_t > a_上次比今天高_t:
            return False
        return True
