import json

import pyarrow
import pyarrow.parquet as pq
import pandas as pd
import backtrader as bt
import pytz
from pyarrow import flight

client = pyarrow.flight.FlightClient(f"grpc://localhost:11001", )


def get_flight(params):
    b = json.dumps(params)
    ticket = flight.Ticket(b)
    reader = client.do_get(ticket)
    df = reader.read_pandas()
    return df


# 创建自定义DataFeed类
class ArrowData(bt.feeds.PandasData):
    lines=('pct_change','ma5')
    params = (
        # 根据你的数据列设置参数
        ('datetime', 'datetime'),  # 日期时间列
        ('open', 'Open'),  # 开盘价列
        ('high', 'High'),  # 最高价列
        ('low', 'Low'),  # 最低价列
        ('close', 'Close'),  # 收盘价列
        ('volume', 'Vol'),  # 成交量列
        ('ma5', 'ma5'),
        ('pct_change', 'pct_change'),
        # ('exchange', ''),
        # ('symbol', ''),
        # ('freq', ''),
        # 可以根据需要添加其他参数
    )

    def __init__(self, exchange, symbol, freq, start_date, end_date):
        req = {
            "name": f"kline_{exchange}_{symbol}_{freq}",
            "timestampStart": start_date.timestamp() * 1000,
            "timestampEnd": end_date.timestamp() * 1000,
        }
        df = get_flight(req)
        df['datetime'] = pd.to_datetime(df['Timestamp'], unit='ms', utc=True).dt.tz_convert(
            pytz.timezone('Asia/Shanghai'))
        # 计算MA5
        df['ma5'] = df['Close'].rolling(window=5).mean()
        df['pct_change'] = df['Close'].pct_change() * 100
        # 确保时间列是datetime类型
        self.p.dataname = df
        self.p.freq = freq
        self.p.symbol = symbol
        self.p.timeframe = bt.TimeFrame.Days
        # 调用父类的__init__方法，传递处理后的DataFrame
        super(ArrowData, self).__init__()
