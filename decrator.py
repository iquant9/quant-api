def to_array(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        isinstance(args[0],)
        return func(*args, **kw)

    return wrapper
