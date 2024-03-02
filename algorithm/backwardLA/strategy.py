import itertools
from typing import Union

from backwardLA.expression import Expression
from backwardLA.linangle import Linangle, RightLA, NeutralLA
from backwardLA.ruleset import R1, R2, R3, R4
from backwardLA.simplifier import Simplifier
from ng_entities.entpoint import Point
from tskmanager import Task

def LAReductor(info: str):
    """
    Перед вводом линейных углов убедитесь, что вы ввели предикатное условие.
    Входные данные: одна строчка, разделенная точкой с запятой с пробелом. Элементами строки являются объекты, заключённые в квадратные
    скобки. В них через запятую с пробелом перечисленны прямые, записанные в виде двух(!) заглавных букв латиницы.
    Валидно:
    - [AD, AM]; [CD, MN]
    - [R]; [E]; [CD, MN]
    Невалидно:
    - [ADC, AM];
    - f[DC, MK], {KJ, 4L}
    Метод, выводящий на экран решение линейных углов, называется Task.Instance().getLAProof() -> str.
    Примеры:
    LAReductor('[AD, AM]; [R]')
    LAReductor('[CD, BC]; [AB, AD]; [AM, BD]; [BD, BC]; [E]')
    """
    LAlist = []
    for LAName in info.split('; '):
        try:
           LAlist.append(toLA(LAName))
        except TypeError:
            Task.writeLA(f'Внимание! Имя {LAName} некорректно и не было обработано! ')
            break
    applyingLARules()
    Expression.NReduction(*LAlist)

def toLA(info: str) -> Union[Linangle, NeutralLA, RightLA]:
    """
    Ввод данных должен быть в формате [AB, AD], обе прямые должны представлять только две точки.
    """
    if info == '[R]': return RightLA()
    if info == '[E]': return NeutralLA()
    pointList = []
    for pname in info[1:-1].replace(', ', ''):
        pointList.append(Point(pname))
    return Linangle.q(*pointList)

def printingEquiv(lst):
    res = ''
    for i, subset in enumerate(lst):
        res += ' = '.join(map(str, subset))
        res += '; '
        if i % 4 == 3: res += '<br> \n'
    return res

def applyingLARules():
    laList = [Linangle(*comb) for comb in itertools.combinations(Task.Instance().lines, 2)]
    for r, angle in itertools.product([R1, R2], laList): r(angle)
    R3()
    R4()
    Task.writeLA(printingEquiv(Simplifier.equivLists))

