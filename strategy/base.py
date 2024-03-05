import pytz

from formula import *


# 我们使用的时候，直接用我们新的类读取数据就可以了。
class BaseStrategy(bt.Strategy):
    def __init__(self):
        self.orders = pd.DataFrame(columns=['hit_dt', 'executed_dt', 'ordtype', 'symbol', 'price', 'value'])
        # 指标
        self.ind = {}
        # 均线
        for d in self.datas:
            self.ind[d] = Ind()
            self.ind[d].ma5 = bt.ind.SMA(d, period=5)
            self.ind[d].ma10 = bt.ind.SMA(d, period=10)
            self.ind[d].ma20 = bt.ind.SMA(d, period=20)
        #     # 如果调用backtrader的SMA，但是k线条数不够会导致crash
        #     if len(d.array) > 60:
        #         self.ind[d].ma60 = bt.ind.SMA(d, period=60)
        #     if len(d.array) > 26:
        #         m = bt.indicators.MACD(self.data,
        #                                period_me1=12,
        #                                period_me2=26,
        #                                period_signal=9)
        #         self.ind[d].dif = m.macd
        #         self.ind[d].dea = m.signal
        #         self.ind[d].macd = (m.macd - m.signal) * 2
        #     self.ind[d].vol5 = bt.ind.SMA(d.volume, period=5)
        #     self.ind[d].vol10 = bt.ind.SMA(d.volume, period=10).
        self.formula = Formula()

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        dt = pytz.utc.localize(dt)
        # 定义东八区时区
        shanghai_timezone = pytz.timezone('Asia/Shanghai')
        # 将UTC datetime转换为东八区datetime
        shanghai_datetime = dt.astimezone(shanghai_timezone)
        print('{}, {}'.format(shanghai_datetime, txt))

    def notify_order(self, order):
        symbol = order.p.data.p.symbol
        if order.isbuy():
            if order.executed.dt:
                executed_dt = bt.num2date(order.executed.dt)
            else:
                executed_dt = None
            hit_dt = self.data.datetime.datetime(-1)
            self.buyprice = order.executed.price
            self.buycomm = order.executed.comm
            self.orders.loc[len(self.orders)] = [hit_dt, executed_dt, order.ordtype, symbol, order.executed.price,
                                                 order.executed.value]  # adding a row

        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    '%s BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (symbol, order.executed.price,
                     order.executed.value,
                     order.executed.comm))
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log(f'策略收益：\n毛收益 {trade.pnl:.2f}, 净收益 {trade.pnlcomm:.2f}')

    def formula(self, data):
        return Formula(data, self.ind[data])

    def V(self, arr, ref=0):
        if len(arr) == 0:
            return None
        start = arr[len(arr) - 1 - ref]
        return start

    def get_idx(self):
        return self.data.close.idx


def get_cerebro(data):
    cerebro = bt.Cerebro()
    tf = bt.TimeFrame.Minutes

    # 添加数据到cerebro
    if isinstance(data, list):
        if data[0].p.freq.endswith('d') or data[0].p.freq.endswith('w'):
            tf = bt.TimeFrame.Days
        for d in data:
            cerebro.adddata(d, name=d.p.symbol)
    else:
        cerebro.adddata(data, name=data.p.table)
        if data.p.freq.endswith('d') or data.p.freq.endswith('w'):
            tf = bt.TimeFrame.Days

    # 添加手续费，按照万分之二收取
    cerebro.broker.setcommission(commission=0.0002, stocklike=True)
    # 设置初始资金为100万
    cerebro.broker.setcash(1_0000_0000)

    cerebro.addanalyzer(bt.analyzers.PyFolio, timeframe=tf, compression=None)
    return cerebro


def buys_time(result):
    for i in result._trades:
        print(i)
def is_valid_number(value):
    # 检查变量是否是数字类型
    if isinstance(value, (int, float, complex)):
        # 检查是否不是NaN、正无穷或负无穷
        if not (isinstance(value, float) and (value != value or value == float('inf') or value == float('-inf'))):
            return True
    return False