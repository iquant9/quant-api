import backtrader as bt

from strategy.MyTT import *


class Result:
    def __init__(self):
        self.hit = False
        self.data = {}


class Ind:
    def __init__(self):
        self.ma5 = None
        self.ma10 = None
        self.ma20 = None
        self.ma60 = None
        self.ma120 = None
        self.dif = None
        self.dea = None
        self.macd = None
        self.vol5 = None
        self.vol10 = None

    def get_macd_arr(self):
        return self.macd


# warnings.filterwarnings("ignore")
class Formula():
    def __init__(self,):
        self.data = None
        self.ind = None
    # def __init__(self, data, ind):
    #     self.data = data
    #     self.ind = ind

    def get_date(self, ref=0):
        return self.data.datetime.datetime(-ref)

    def f_底部连阳上穿均线(self, k):
        ma5, ma10 = np.array(self.ma5[k]), np.array(self.ma10[k])
        n = BARSLAST(np.array(k.close.array) < np.array(k.open.array))
        n = BARSLAST(ma5 < ma10)
        if n[0] == 1:
            self.log("n=" + str(n[0]))
        return n

    def 反弹至均线后下跌不创新低(self, k, ind: Ind):
        if k.close < k.close[-1]:
            return False
        ind.ma5.get()
        ma5, ma10 = self.get_array(ind.ma5.line), self.get_array(ind.ma10.line)
        close = self.get_array(k.close)
        cond1 = LAST((close < ma5) & (ma5 < ma10), 20, 0)
        if not (cond1[0] == True and ma10[-1] > 0):
            return False

        return True

    def LAST_底部连阳上穿均线(self, k, ind: Ind):
        ma5, ma10 = self.get_array(ind.ma5.line), self.get_array(ind.ma10.line)
        ma20 = self.get_array(ind.ma20.line)
        # ma60 = self.get_array(ind.ma60.line)
        close = self.get_array(k.close)
        dif = self.get_array(ind.dif)
        dea = self.get_array(ind.dea)

        lows = BARSLAST((close < REF(close, 1)) & (close < ma5) & (ma5 < ma10) & (ma10 < ma20) & (dif < 0))
        start = lows[-1]
        if start > self.get_idx(k):
            return False, 0, 0
        if start < 5:
            return False, 0, 0
        cond1 = BARSSINCEN((close > REF(close, 1)) & (close > ma5) & (ma5 > ma10) & (ma10 > ma20), start)
        end = cond1[-1]
        if end <= 1:
            return False, 0, 0
        # k.datetime.datetime(-start)
        # k.datetime.datetime(-end)
        连阳 = LAST((close / REF(close, 1)) > 0.995, self.get_idx(k) - start, self.get_idx(k) - end)
        if 连阳[-1]:
            pass
        else:
            return False, 0, 0
        有回调 = BARSLAST((ma5 < REF(ma5, 1)))
        有回调_t = 有回调[-1]
        if 有回调_t > end:
            return False, 0, 0
        return True, start, end

    def T(self, arr, ref=0):
        start = arr[len(arr) - 1 - ref]
        start = start + ref
        if start > self.get_idx():
            return None
        return start

    def V(self, arr, ref=0):
        start = arr[len(arr) - 1 - ref]
        return start

    def BARSLAST(self, ss, ref=0):
        v = self.T(BARSLAST(ss), ref=ref)
        return v

    def HHV(self, ss, from_ref, to_ref):
        v = self.Value(HHV(ss, from_ref - to_ref), ref=to_ref)
        return v

    def LLV(self, ss, from_ref, to_ref):
        v = self.V(LLV(ss, from_ref - to_ref), ref=to_ref)
        return v

    def SUM(self, ss, from_ref, to_ref):
        v = self.V(SUM(ss, from_ref - to_ref), ref=to_ref)
        return v

    def COUNT(self, ss, from_ref, to_ref):
        v = COUNT(ss, from_ref - to_ref, )
        v = self.V(v, ref=to_ref)
        return v

    def BARSSINCEN(self, ss, n):
        v = BARSSINCEN(ss, n)
        if v[-1] == 0:
            return None
        return v[-1]

    def get_idx(self):
        return self.data.close.idx

    def get_array(self, line):
        try:
            # kline path
            return np.array(line.get(0, size=line.idx + 1))
        except:
            # ind path
            return np.array(line.get(0, size=line.line.idx + 1))

    def C(self):
        return self.get_array(self.data.close)

    def DIF(self):
        return self.get_array(self.ind.dif)

    def DEA(self):
        return self.get_array(self.ind.dea)

    def MACD(self):
        return self.get_array(self.ind.macd)

    def REF(self, ss, ref):
        return self.V(ss, ref=ref)

    def get_past_array(self, line):
        return np.array(line.get(ago=-1, size=line.idx))


# 我们使用的时候，直接用我们新的类读取数据就可以了。
class FormulaStrategy(bt.Strategy):
    params = (('period', 30),
              ('hold_percent', 0.02),
              ('macd1', 12),
              ('macd2', 26),
              ('macdsig', 9),
              )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        print('{}, {}'.format(dt.isoformat(), txt))

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

    def prenext(self):

        self.next()

    def next(self):
        current_date = self.datas[0].datetime.datetime(0)
        long_list = []
        short_list = []
        n = self.formula.LAST_底部连阳上穿均线(self.data, self.ind[self.data])
        if n < 0:
            return

        condition1 = self.formula.反弹至均线后下跌不创新低(self.data, self.ind[self.data])
        if condition1:
            self.order = self.buy(data=self.data)

    def notify_order(self, order):

        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status == order.Rejected:
            self.log(f"Rejected : order_ref:{order.ref}  data_name:{order.p.data._name}")

        if order.status == order.Margin:
            self.log(f"Margin : order_ref:{order.ref}  data_name:{order.p.data._name}")

        if order.status == order.Cancelled:
            self.log(f"Concelled : order_ref:{order.ref}  data_name:{order.p.data._name}")

        if order.status == order.Partial:
            self.log(f"Partial : order_ref:{order.ref}  data_name:{order.p.data._name}")

        if order.status == order.Completed:
            if order.isbuy():
                self.log(
                    f" BUY : data_name:{order.p.data._name} price : {order.executed.price} , cost : {order.executed.value} , commission : {order.executed.comm}")

            else:  # Sell
                self.log(
                    f" SELL : data_name:{order.p.data._name} price : {order.executed.price} , cost : {order.executed.value} , commission : {order.executed.comm}")

    def notify_trade(self, trade):
        # 一个trade结束的时候输出信息
        if trade.isclosed:
            self.log('closed symbol is : {} , total_profit : {} , net_profit : {}'.format(
                trade.getdataname(), trade.pnl, trade.pnlcomm))
            # self.trade_list.append([self.datas[0].datetime.date(0),trade.getdataname(),trade.pnl,trade.pnlcomm])

        if trade.isopen:
            self.log('open symbol is : {} , price : {} '.format(
                trade.getdataname(), trade.price))

    def stop(self):

        pass

    # 初始化cerebro,获得一个实例
