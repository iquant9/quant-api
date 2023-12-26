### sync requirements.txt
pipreqs . --force

公式使用
# 判断当天上涨:                
```
if data.close.get(0) > data.close.get(-1):
    pass
```
