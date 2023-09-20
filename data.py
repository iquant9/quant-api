from datetime import datetime
import traceback
import pymysql

from backtrader.feed import DataBase
from backtrader import date2num
from taosrest import RestClient
import taosrest


def new_data(section, start, end):
    table, contract_type, symbol, interval = section.split(":")
    data = KlineData(
        table,
        symbol=symbol,
        contract_type=contract_type,
        fromdate=start,
        todate=end,
        interval=interval,
    )
    return data


class KlineData(DataBase):
    params = (
        ('fromdate', datetime.min),
        ('todate', datetime.max),
        ('table', ''),
        ('freq', ''),
    )
    # 默认是这些列：datetime'、 'open'、'high'、'low'、'close'、'volume'、'openinterest'
    # 如果需要增加，在这里声明
    lines = (
        "turnover",
        "turnover_rate",
        "change_pct"
    )

    def load_data_from_db(self, table, start_time, end_time):
        """
        从MySQL加载指定数据
        Args:
            table (str): 表名
            ts_code (str): 股票代码
            start_time (str): 起始时间
            end_time (str): 终止时间
        return:
            data (List): 数据集
        """

        cur = self.conn.cursor()
        try:
            sql = cur.execute(
                f"SELECT * FROM '{table}' WHERE vol>0 and ts >= ? "
                "and ts < ?  order by ts asc",
                (start_time.timestamp() * 1e3, end_time.timestamp() * 1e3,)
            )
            data = cur.fetchall()
            return iter(list(data))
        except BaseException as e:
            print("exception occur")
            print(e)
            raise e

    def __init__(self, **kwargs):
        self.result = []
        self.conn = taosrest.connect(url="http://localhost:6041", user="root", password="taosdata", database="feeds")

    def start(self):
        self.result = self.load_data_from_db(
            self.p.table, self.p.fromdate, self.p.todate
        )

    def _load(self):
        try:
            one_row = next(self.result)
        except StopIteration:
            return False
        dt = datetime.fromtimestamp(one_row[3] / 1e6)
        self.lines.datetime[0] = date2num(dt)
        self.lines.open[0] = float(one_row[6])
        self.lines.close[0] = float(one_row[7])
        self.lines.high[0] = float(one_row[9])
        self.lines.low[0] = float(one_row[8])
        self.lines.volume[0] = float(one_row[10])
        self.lines.turnover[0] = float(one_row[11])
        self.lines.change_pct[0] = self.lines.close[0] / self.lines.close[-1] - 1

        return True
