
# 1. Функции, позволяющие увидеть содержимое контейнеров для геометрических объектов.
# Несут технический характер и нужны тестировщикам. В "релиз" не пойдут.
def str_list(lst):
    return [str(x) for x in lst]

def hum_list(lst):
    return [x.humanize() for x in lst]

def stringify(lst):
    return ''.join(str_list(lst))


def str_dict(my_dict):
    print({str(x): y for x, y in zip(my_dict.keys(), my_dict.values())})






