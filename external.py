import config as cf
import time


# 1. Функции, позволяющие увидеть содержимое контейнеров для геометрических объектов.
def str_list(lst):
    return [str(x) for x in lst]


def hum_list(lst):
    return [x.humanize() for x in lst]


def stringify_list(lst):
    return ''.join(str_list(lst))


def str_dict(my_dict):
    return {str(x): y for x, y in zip(my_dict.keys(), my_dict.values())}


def hum_dict(my_dict):
    if all((v is None for v in my_dict.values())):
        return ' '
    return {x.humanize(): 'Неизв' if y is None else y for x, y in zip(my_dict.keys(), my_dict.values())}


def clock(func):
    def clocked(*args):
        t0 = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        logger(f'[{elapsed:0.8f}s] {name}({arg_str}) -> {result!r}')
        return result

    return clocked


def logger(input_string: str):
    if cf.dev_mode:
        print(input_string)
