import datetime

import pytz

from formula import *
from strategy.data import ArrowData

pd.set_option('display.max_rows', None)  # 显示所有行
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.width', None)  # 显示所有列宽


def get_data(exchange, bk, freq,
             start_date=datetime.datetime(2024, 1, 1),
             end_date=datetime.datetime(2024, 12, 12),
             tz=pytz.timezone('Asia/Shanghai')):
    return ArrowData(
        exchange=exchange,
        symbol=bk,
        freq=freq,
        start_date=start_date,
        end_date=end_date,
        tz=tz
    )


def init_cerebro():
    cerebro = bt.Cerebro()
    # 添加手续费，按照万分之二收取
    cerebro.broker.setcommission(commission=0.0002, stocklike=True)
    # 设置初始资金为100万
    cerebro.broker.setcash(1_0000_0000)
    # 添加自定义的分析指标
    cerebro.addanalyzer(bt.analyzers.PyFolio, timeframe=bt.TimeFrame.Minutes, compression=None)
    cerebro.addanalyzer(TradeList, _name='tradelist')

    return cerebro


class TradeList(bt.Analyzer):
    def __init__(self):

        self.trades = []
        self.cumprofit = 0.0

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        if len(trade.history) <= 0:
            return
        brokervalue = self.strategy.broker.getvalue()

        dir = 'short'
        if trade.history[0].event.size > 0: dir = 'long'

        pricein = trade.history[len(trade.history) - 1].status.price
        priceout = trade.history[len(trade.history) - 1].event.price
        datein = bt.num2date(trade.history[0].status.dt, tz=trade.data.p.tz, naive=False)
        dateout = bt.num2date(trade.history[len(trade.history) - 1].status.dt, tz=trade.data.p.tz, naive=False)
        # if trade.data._timeframe >= bt.TimeFrame.Days:
        #     datein = datein.date()
        #     dateout = dateout.date()

        pcntchange = 100 * priceout / pricein - 100
        pnl = trade.history[len(trade.history) - 1].status.pnlcomm
        pnlpcnt = 100 * pnl / brokervalue
        barlen = trade.history[len(trade.history) - 1].status.barlen
        pbar = pnl / barlen
        self.cumprofit += pnl

        size = value = 0.0
        for record in trade.history:
            if abs(size) < abs(record.status.size):
                size = record.status.size
                value = record.status.value

        highest_in_trade = max(trade.data.high.get(ago=0, size=barlen + 1))
        lowest_in_trade = min(trade.data.low.get(ago=0, size=barlen + 1))
        hp = 100 * (highest_in_trade - pricein) / pricein
        lp = 100 * (lowest_in_trade - pricein) / pricein
        if dir == 'long':
            mfe = hp
            mae = lp
        if dir == 'short':
            mfe = -lp
            mae = -hp

        self.trades.append({'ref': trade.ref,
                            'ticker': trade.data._name,
                            'dir': dir,
                            'datein': datein,
                            'pricein': pricein,
                            'dateout': dateout,
                            'priceout': priceout,
                            'chng%': round(pcntchange, 2),
                            'pnl': pnl, 'pnl%': round(pnlpcnt, 2),
                            'size': size,
                            'value': value,
                            'cumpnl': self.cumprofit,
                            'nbars': barlen, 'pnl/bar': round(pbar, 2),
                            'mfe%': round(mfe, 2), 'mae%': round(mae, 2)})

    def get_analysis(self):
        return self.trades


def print_result(cerebro):
    # 获取交易记录
    transactions = cerebro.broker.get_transactions()
    # 初始化总收益率
    total_return = 0.0
    # 打印所有交易记录及每笔交易的收益率
    for i, transaction in enumerate(transactions):
        # 买入或卖出的价格
        price = transaction.price
        # 买入或卖出的数量
        size = transaction.size
        # 交易成本（如果有）
        commission = transaction.comm
        # 交易类型（'buy' 或 'sell'）
        order = 'buy' if size > 0 else 'sell'
        # 计算单笔交易的价值
        value = price * size
        # 打印交易信息
        print(f'Transaction {i}: {order} {abs(size)} units at {price}')
        # 计算并打印单笔交易的收益率（此处简化处理，未考虑交易成本和时间价值）
        if order == 'buy':
            print(f'    Buy Value: {value}')
        else:
            # 卖出时计算收益率
            profit = (price - transactions[i - 1].price) * size - 2 * commission  # 假设买入和卖出都有佣金
            print(f'    Sell Profit/Loss: {profit}')
            total_return += profit
    # 打印总收益率
    print(f'Total Return: {total_return}')


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
        dt = dt or self.datas[0].datetime.datetime(0, naive=False)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        symbol = order.p.data.p.name
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

    def formula(self, data):
        return Formula(data, self.ind[data])

    def V(self, arr, ref=0):
        if len(arr) == 0:
            return None
        start = arr[len(arr) - 1 - ref]
        return start

    def get_idx(self):
        return self.data.close.idx


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
