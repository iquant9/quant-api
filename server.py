from sanic import Sanic, json, SanicException, text
from sanic.log import logger

import strategy_底部连阳_回踩_突破
from mysql import MySQLData
from dateutil.parser import parse
import akshare
import Ashare

strategyMap = {
    "底部连阳_回踩_突破": strategy_底部连阳_回踩_突破.Strategy,
}

app = Sanic(name='your_application_name')

date_format = '%Y-%m-%d %H:%M:%S'


@app.get("/")
async def hello_world(request):
    return text("Hello, world.")


@app.post("run_strategy")
async def handler(request):
    from strategy import run_formula
    d = request.json
    f = strategyMap[d['strategy']]
    df = None
    start = parse(d['start'])
    end = parse(d['end'])
    for section in d["symbol_group"]:
        table, contract_type, symbol, interval = section.split(":")
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
            logger.error('run_formula error:%s %s', e, d)
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

    # default is a function applied to objects that aren't serializable.
    # In this case it's str, so it just converts everything it doesn't know to strings.
    return json(df.dropna().to_dict('records'), headers={"charset": "utf-8"},
                default=str,
                ensure_ascii=False)

    # return JsonResponse(json.loads(response), json_dumps_params={'ensure_ascii': False}, safe=False)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8020)
