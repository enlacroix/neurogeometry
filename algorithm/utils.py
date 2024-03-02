from typing import Union
import config as cf
from collections import namedtuple


# 1. Функции, позволяющие увидеть содержимое контейнеров для геометрических объектов.
def toStrAllElems(lst) -> list: return list(map(str, lst))


def hum_list(lst):
    return [x.humanize() for x in lst if x is not None]


def stringifyList(lst):
    # не добавляй в качестве разделителя /n
    return ' '.join(toStrAllElems(lst))

def newStringifyList(lst):
    # не добавляй в качестве разделителя /n
    return '\n'.join(toStrAllElems(lst))

def toStrDictKeys(my_dict): return {str(x): y for x, y in my_dict.items()}

def convertDictPairToString(myDict: dict) -> list:
    """
    Возвращает список из пар ключ - значение (превращенное в строку)
    """
    return [f'{x}: {stringifyList(y)}; ' for x, y in myDict.items()]

def stringifyDict(myDict: dict): return '\n'.join(convertDictPairToString(myDict))

def humanizeDictForEvals(my_dict):
    if all((v is None for v in my_dict.values())):
        return ' '
    return {x.humanize(): 'Неизв' if y is None else y for x, y in zip(my_dict.keys(), my_dict.values())}



def logger(input_string: str):
    if cf.DEVMODE: print(input_string)


def getCommonElements(containerA: Union[list, tuple], containerB: Union[list, tuple]) -> Union[list, bool]:
    comp = list(set(containerA) & set(containerB))
    if len(comp) == 0: return False
    return comp

def FindCommonFunction(containerA, containerB):
    """
    Функция FC(x, y) - подсчитывает количество совпадающих элементов и возвращает количество общих элементов.
    FC > 1 - True/False.
    """
    resFunc = namedtuple("resFunc", "length logic")
    res = len(set(containerA) & set(containerB))
    return resFunc(length=res, logic=res>1)

def getUniqueElements(containerA, containerB): return list(set(containerA) ^ set(containerB))


def FindCommonFindUnique(containerA, containerB) -> tuple:
    """
    ИЗМЕНЯЙ АККУРАТНО. ЧАСТО ИСПОЛЬЗУЕТСЯ.
    ВОЗВРАЩАЕТ ПЕРВЫЙ СОВПАШИЙ ЭЛЕМЕНТ!
    """
    commonElementsList = list(set(containerA) & set(containerB))
    if len(commonElementsList) == 0:
        return False, None
    return commonElementsList[0], list(set(containerA) ^ set(containerB))

def findIfObjWasDecorated(figure, xcls):
    """
    :return: возвращает объект типа f(...(t(x)) c нужными нами полями.
    Проверяет существует ли обёртка типа f (xcls) в конструкции figure = g(h(...t(x))).
    объект х должен иметь атрибут wrapped, но быть равным None.
    """
    wrappedFigure = figure.wrapped
    while wrappedFigure is not None:
        if isinstance(wrappedFigure, xcls):
            return wrappedFigure
        else:
            wrappedFigure = wrappedFigure.wrapped
    return


def neighbours(elem, lst) -> tuple:
    if elem in lst:
        ind = lst.index(elem)
    else:
        return None, None
    if ind in range(1, len(lst) - 2): return lst[ind - 1], lst[ind + 1]
    if ind == 0: return None, lst[1]
    if ind==len(lst)-1: return lst[ind-1], None

def newNeighbours(elem, lst) -> tuple:
    ind = lst.index(elem)
    if ind in range(1, len(lst) - 2): return lst[ind - 1], lst[ind + 1]
    else: return None, None

def isConcreteClass(obj, className): return type(obj).__name__ == className # очевидно, что наследников он не поддержит, но не нужно импортировать имя для проверки

def coproduction(a: list, b: list) -> Union[bool, list]:
    """
    Копроизведение формирует наиболее общий объект, который перенимает свойства аргументов.
    Причём сделано допущение о том, что новая информация имеет приоритет над старой (второй аргумент главнее первого).
    Копроизведение некоммуникативное, и выдаёт ложный результат для несовместимых прямых, нарушающих логику точек.
    Оно позволяет получить наиболее точные прямые и реализовать таким образом свойство аддитивности.
    """
    result = b[:] # Результат полностью включает в себя второй аргумент
    meetTrue = False
    boolList = [var in b for var in a] # Содержатся ли элементы первого аргумента во втором.
    if set(a) == set(b) and a != b: return False
    for val, cur in zip(a, boolList):
        if not meetTrue and not cur:
            result.insert(0, val)
        if cur:
            meetTrue = True
            continue
        if not cur and meetTrue:
            if any(boolList[a.index(val):]):
                return False
            else:
                result.append(val)
    return result


