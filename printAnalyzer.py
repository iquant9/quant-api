from datetime import datetime
import backtrader as bt
import os.path  # 管理路径
import sys  # 发现脚本名字(in argv[0])


# ======================================================================================================================
# HELPERS：帮助函数，输出各种analyzer结果
# ======================================================================================================================
def pretty_print(format, *args):
    print(format.format(*args))


def exists(object, *properties):
    for property in properties:
        if not property in object: return False
        object = object.get(property)
    return True


def printTradeAnalysis(cerebro, analyzers):
    format = "  {:<24} : {:<24}"
    NA = '-'

    print('Backtesting Results')
    if hasattr(analyzers, 'ta'):
        ta = analyzers.ta.get_analysis()

        openTotal = ta.total.open if exists(ta, 'total', 'open') else None
        closedTotal = ta.total.closed if exists(ta, 'total', 'closed') else None
        wonTotal = ta.won.total if exists(ta, 'won', 'total') else None
        lostTotal = ta.lost.total if exists(ta, 'lost', 'total') else None

        streakWonLongest = ta.streak.won.longest if exists(ta, 'streak', 'won', 'longest') else None
        streakLostLongest = ta.streak.lost.longest if exists(ta, 'streak', 'lost', 'longest') else None

        pnlNetTotal = ta.pnl.net.total if exists(ta, 'pnl', 'net', 'total') else None
        pnlNetAverage = ta.pnl.net.average if exists(ta, 'pnl', 'net', 'average') else None

        pretty_print(format, 'Open Positions', openTotal or NA)
        pretty_print(format, 'Closed Trades', closedTotal or NA)
        pretty_print(format, 'Winning Trades', wonTotal or NA)
        pretty_print(format, 'Loosing Trades', lostTotal or NA)
        print('\n')

        pretty_print(format, 'Longest Winning Streak', streakWonLongest or NA)
        pretty_print(format, 'Longest Loosing Streak', streakLostLongest or NA)
        pretty_print(format, 'Strike Rate (Win/closed)',
                     (wonTotal / closedTotal) * 100 if wonTotal and closedTotal else NA)
        print('\n')

        pretty_print(format, 'Net P/L', '${}'.format(round(pnlNetTotal, 2)) if pnlNetTotal else NA)
        pretty_print(format, 'P/L Average per trade', '${}'.format(round(pnlNetAverage, 2)) if pnlNetAverage else NA)
        print('\n')

    if hasattr(analyzers, 'drawdown'):
        pretty_print(format, 'Drawdown', '${}'.format(analyzers.drawdown.get_analysis()['drawdown']))
    if hasattr(analyzers, 'sharpe'):
        pretty_print(format, 'Sharpe Ratio:', analyzers.sharpe.get_analysis()['sharperatio'])
    if hasattr(analyzers, 'vwr'):
        pretty_print(format, 'VRW', analyzers.vwr.get_analysis()['vwr'])
    if hasattr(analyzers, 'sqn'):
        pretty_print(format, 'SQN', analyzers.sqn.get_analysis()['sqn'])
    print('\n')

    print('Transactions')
    format = "  {:<24} {:<24} {:<16} {:<8} {:<8} {:<16}"
    pretty_print(format, 'Date', 'Amount', 'Price', 'SID', 'Symbol', 'Value')

