import sympy as sp
import config
from utils import isConcreteClass
from tskmanager import Task


class SetValue:
    """
    Численное значение величины obj равно value. Базовый функтор этого модуля.
    """
    def __init__(self, obj, value):
        x_row = [0] * config.VARIABLE_LIMIT
        x_row[obj.getIndex()] = 1
        x_row[-1] = value
        if isConcreteClass(obj, 'Angle'):
            Task.Instance().AEM = Task.Instance().AEM.row_insert(1, sp.Matrix([x_row]))
            Task.Instance().angle_dict[obj] = value
        if isConcreteClass(obj, 'Segment'):
            Task.Instance().SEM = Task.Instance().SEM.row_insert(1, sp.Matrix([x_row]))
            Task.Instance().segment_dict[obj] = value


class Relation:
    """
    Отношение численного значения величины obj1 к obj2 равна k.
    """

    def __init__(self, obj1, obj2, k):
        x_row = [0] * config.VARIABLE_LIMIT
        x_row[obj1.getIndex()] = 1
        x_row[obj2.getIndex()] = - k
        if isConcreteClass(obj1, 'Angle'): Task.Instance().AEM = Task.Instance().AEM.row_insert(1, sp.Matrix([x_row]))
        if isConcreteClass(obj1, 'Segment'): Task.Instance().SEM = Task.Instance().SEM.row_insert(1, sp.Matrix([x_row]))


class Sum:
    """
    Функтор, который показывает, что сумма элементов списка равна значению res. Типичный пример:
    Сумма углов в треугольнике равна 180 градусам.
    """

    def __init__(self, objects: list, res: int):
        x_row = [0] * config.VARIABLE_LIMIT
        for elem in objects:
            x_row[elem.getIndex()] = 1
        x_row[-1] = res
        # эх сюда бы match-case, но мы на 3.8(
        if isConcreteClass(objects[0], 'Angle'): Task.Instance().AEM = Task.Instance().AEM.row_insert(1, sp.Matrix([x_row]))
        if isConcreteClass(objects[0], 'Segment'): Task.Instance().SEM = Task.Instance().SEM.row_insert(1, sp.Matrix([x_row]))

class LinearCombination:
    """
    LinearCombination({x: 1, y: -2}, 0) => x - 2y = 0 - сущности обязаны быть однородными!
    """
    def __init__(self, varsWithCoeffs: dict, res=0):
        x_row = [0] * config.VARIABLE_LIMIT
        for elem in varsWithCoeffs:
            x_row[elem.getIndex()] = varsWithCoeffs[elem]
        x_row[-1] = res
        if isConcreteClass(list(varsWithCoeffs.keys())[0], 'Angle'):
            Task.Instance().AEM = Task.Instance().AEM.row_insert(1, sp.Matrix([x_row]))
        if isConcreteClass(list(varsWithCoeffs.keys())[0], 'Segment'):
            Task.Instance().SEM = Task.Instance().SEM.row_insert(1, sp.Matrix([x_row]))

