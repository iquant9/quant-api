from datetime import datetime
import traceback
import pymysql

from backtrader.feed import DataBase
from backtrader import date2num


class MySQLData(DataBase):
    params = (
        ('fromdate', datetime.min),
        ('todate', datetime.max),
        ('symbol', ''),
        ('contract_type', ''),
        ('interval', '1m'),
    )
    # 默认是这些列：datetime'、 'open'、'high'、'low'、'close'、'volume'、'openinterest'
    # 如果需要增加，在这里声明
    lines = (
        "turnover",
        "turnover_rate",
        "change_pct"
    )

    def load_data_from_db(self, symbol, contract_type,interval, start_time, end_time):
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
        db = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            db="feeds_dev",
            port=4000
        )

        cur = db.cursor()

        sql = cur.execute(
            f"SELECT * FROM {self.table} WHERE vol>0 and timestamp_in_micro >= %s"
            "and timestamp_in_micro < %s and symbol = %s and contract_type = %s and `interval` = %s order by timestamp_in_micro asc",
            (start_time.timestamp()*1e6, end_time.timestamp()*1e6, symbol,contract_type, interval,)
        )
        data = cur.fetchall()
        db.close()
        return iter(list(data))

    def __init__(self, table, **kwargs):
        self.result = []
        self.table = table

    def start(self):
        self.result = self.load_data_from_db(
            self.p.symbol, self.p.contract_type,self.p.interval, self.p.fromdate, self.p.todate
        )

    def _load(self):
        try:
            one_row = next(self.result)
        except StopIteration:
            return False
        dt=datetime.fromtimestamp(one_row[3]/1e6)
        self.lines.datetime[0] = date2num(dt)
        self.lines.open[0] = float(one_row[6])
        self.lines.close[0] = float(one_row[7])
        self.lines.high[0] = float(one_row[9])
        self.lines.low[0] = float(one_row[8])
        self.lines.volume[0] = float(one_row[10])
        self.lines.turnover[0] = float(one_row[11])
        self.lines.change_pct[0] = self.lines.close[0]/self.lines.close[-1]-1

        return True
