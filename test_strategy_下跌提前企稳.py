from unittest import TestCase

import datetime

from data import KlineData
from strategy import run_formula
from strategy_下跌提前企稳 import Strategy


class TestStrategy(TestCase):

    def test_603496_1d_230920(self):
        start = datetime.datetime(2023, 6, 29)
        end = datetime.datetime(2023, 9, 29)
        # 添加数据到cerebro
        data0 = KlineData(
            table="kline",
            exchange="asindex",
            symbol="sz399300",
            freq="1d",
            start_date=start,
            end_date=end,
        )
        datas = [data0, ]
        for symbol in ['603496', '002682','300042']:
            data1 = KlineData(
                table="kline",
                exchange="as",
                symbol=symbol,
                freq="1d",
                start_date=start,
                end_date=end,
            )
            datas.append(data1)
        result = run_formula(Strategy, datas)
        hit_list = list(result[0].orders.hit_dt.astype(str).values.tolist())
        self.assertIn("2023-09-20 09:30:00", hit_list, "hit")

    def test_硕贝德_2h_0928_1030(self):
        # 添加数据到cerebro
        data = KlineData(
            exchange="as",
            symbol="300322",
            freq="2h",
            start_date=datetime.datetime(2023, 9, 1),
            end_date=datetime.datetime(2023, 9, 28),
        )
        result = run_formula(Strategy, data)
        hit_list = list(result[0].orders.hit_dt.astype(str).values.tolist())
        self.assertIn("2023-09-28 10:30:00", hit_list, "hit")
