By Traders, For Traders.
quant-api is a Python-based open source quantitative strategy system development framework.
# goal
make it easier to run a strategy, pass input params and return which stocks statisfied the requirentments

# how to develop it
### sync requirements.txt
pipreqs . --force

# how to use formula in your strategy
# 判断当天上涨:                
```
if data.close.get(0) > data.close.get(-1):
    pass
```
