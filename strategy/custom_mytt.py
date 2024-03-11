import numpy as np

from strategy import MyTT


def to_array(func):
    def wrapper(*args, **kwargs):
        # 检查传入的参数是否是集合类型
        if not isinstance(args[0], (set, list, tuple)):
            line = args[0]
            size = args[1]
            # 比如第一天，可取长度为1，如果size>1，line.get将返回空
            if size > len(line):
                size = len(line)
            # 如果不是，转换为集合类型
            try:
                # kline path
                S = np.array(line.get(0, size=size))
            except:
                # ind path
                S = np.array(line.get(0, size=size))
            return func(S, size)
        else:
            # 如果已经是集合类型，直接调用原始方法
            return func(*args, **kwargs)

    return wrapper


@to_array
def HHV(S, N):  # HHV(C, 5) 最近5天收盘最高价
    return MyTT.HHV(S, N)
@to_array
def LLV(S, N):  # HHV(C, 5) 最近5天收盘最高价
    return MyTT.LLV(S, N)