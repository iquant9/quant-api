import backtrader as bt
class VolMa(bt.Indicator):

    lines = ('mid','top','bot',)
    params = (('maperiod',20),
              ('period',3),
              ('highRate',1.2),
              ('lowRate',0.85),)
    #与价格在同一张图
    plotinfo = dict(subplot=False)

    def __init__(self):
        ema = bt.ind.SMA(self.data, period=self.p.maperiod)
        #计算上中下轨线
        self.l.mid=bt.ind.EMA(ema,period=self.p.period)
        self.l.top=bt.ind.EMA(self.mid*self.p.highRate,\
                              period=self.p.period)
        self.l.bot=bt.ind.EMA(self.mid*self.p.lowRate,\
                              period=self.p.period)
        super(TrendBand, self).__init__()