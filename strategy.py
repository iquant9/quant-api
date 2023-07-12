from formula import *


# 我们使用的时候，直接用我们新的类读取数据就可以了。
class BaseStrategy(bt.Strategy):
    def __init__(self):
        self.orders = pd.DataFrame(columns=['hit_dt', 'executed_dt', 'ordtype', 'symbol', 'price', 'value'])

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        print('{}, {}'.format(dt.isoformat(), txt))

    def notify_order(self, order):
        if order.isbuy():
            if order.executed.dt:
                executed_dt = bt.num2date(order.executed.dt)
            else:
                executed_dt=None
            hit_dt = self.data.datetime.datetime(-1)
            self.buyprice = order.executed.price
            self.buycomm = order.executed.comm
            symbol = self.getdatanames()[0]
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
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
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


def run_formula(strategy, data):
    cerebro = bt.Cerebro()

    # 添加数据到cerebro
    cerebro.adddata(data, name=data.p.symbol + '.' + data.p.contract_type)

    # 添加手续费，按照万分之二收取
    cerebro.broker.setcommission(commission=0.0002, stocklike=True)
    # 设置初始资金为100万
    cerebro.broker.setcash(1_0000_0000)
    # 添加策略
    cerebro.addstrategy(strategy)
    tf = bt.TimeFrame.Minutes
    if data.p.interval.endswith('d') or data.p.interval.endswith('w'):
        tf = bt.TimeFrame.Days
    cerebro.addanalyzer(bt.analyzers.PyFolio, timeframe=tf, compression=None)
    # 运行回测
    backtest_result = cerebro.run()
    return backtest_result


def buys_time(result):
    for i in result._trades:
        print(i)
