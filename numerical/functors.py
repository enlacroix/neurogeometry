import sympy as sp
import varbank as vb


class SetValue:
    """
    Численное значение величины obj равно value. Базовый функтор этого модуля.
    """
    def __init__(self, obj, value, angles=True):
        x_row = [0] * vb.VAR_LIMIT
        x_row[obj.get_ind()] = 1
        x_row[-1] = value
        if angles:
            vb.task.AEM = vb.task.AEM.row_insert(1, sp.Matrix([x_row]))
            vb.task.angle_dict[obj] = value
        else:
            # То же самое для матрицы отрезков.
            pass


class Relation:
    """
    Отношение численного значения величины obj1 к obj2 равна k.
    """

    def __init__(self, obj1, obj2, k, angles=True):
        x_row = [0] * vb.VAR_LIMIT
        x_row[obj1.get_ind()] = 1
        x_row[obj2.get_ind()] = - k
        if angles:
            vb.task.AEM = vb.task.AEM.row_insert(1, sp.Matrix([x_row]))
        else:
            # То же самое для матрицы отрезков.
            pass


class Sum:
    """
    Функтор, который показывает, что сумма каких-то величин равна значению res. Типичный пример:
    Сумма углов в треугольнике равна 180 градусам.
    """

    def __init__(self, objects, res, angles=True):
        x_row = [0] * vb.VAR_LIMIT
        for elem in objects:
            x_row[elem.get_ind()] = 1
        x_row[-1] = res
        if angles:  # isinstance(objects[0], Angle)
            vb.task.AEM = vb.task.AEM.row_insert(1, sp.Matrix([x_row]))
        else:
            # То же самое для матрицы отрезков.
            pass


class Diff:  # Разность величин.
    pass
