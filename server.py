import datetime

from sanic import Sanic, json, SanicException
from sanic.log import logger

import strategy_底部连阳_回踩_突破
from mysql import MySQLData
from strategy import run_formula
from dateutil.parser import parse
import qstock
import akshare

import Ashare

strategyMap = {
    "底部连阳_回踩_突破": strategy_底部连阳_回踩_突破.Strategy,
}

app = Sanic(name='your_application_name')

date_format = '%Y-%m-%d %H:%M:%S'


@app.post("run_strategy")
async def handler(request):
    d = request.json
    f = strategyMap[d['strategy']]
    df = None
    start = parse(d['start'])
    end = parse(d['end'])
    for section in d["symbol_group"]:
        table, contract_type, symbol, interval = section.split(".")
        data = MySQLData(
            table,
            symbol=symbol,
            contract_type=contract_type,
            fromdate=start,
            todate=end,
            interval=interval,
        )
        try:
            result = run_formula(f, data)
        except Exception as e:
            logger.error('run_formula error:%s', e)
            continue
        if df is None:
            df = result[0].orders
        else:
            df = df.append(result[0].orders)
    if df is None:
        return json([])
    df['hit_dt'] = df['hit_dt'].astype(str)
    df['executed_dt'] = df['executed_dt'].astype(str)
    return json(df.to_dict('records'))


@app.get("rest")
def rest(request):
    cmd = request.args.get("cmd")
    logger.info('cmd is %s' % cmd)
    # import Ashare
    try:
        df = eval(str(cmd))
    except Exception as e:
        logger.error("eval is running at error:%s" % e)
        raise SanicException("Something went wrong.%s" % (e), status_code=501)
    logger.info('df len is %d' % len(df))

    # df = qstock.realtime_data()
    # response = df.to_json(orient='records', force_ascii=False)
    # 查看前几行
    return json(df.to_dict('records'))

    # return JsonResponse(json.loads(response), json_dumps_params={'ensure_ascii': False}, safe=False)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8020)
