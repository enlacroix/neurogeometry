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
    return {x.humanize(): y for x, y in zip(my_dict.keys(), my_dict.values())}