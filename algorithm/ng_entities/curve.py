from utils import FindCommonFunction
from tskmanager import Task


class Curve:
    """
    Кривая (дословный перевод), правильнее назвать её дуга, предназначена для того, чтобы обрабатывать факты о том, что точки
    принадлежат одной окружности.
    Принцип 1 из дедуктивного модуля (реализация теоремы о вписанном угле в обыкновенной форме) требует от Curve строго соблюдения порядка
    точек
    """
    def __init__(self, *lst):
        self.lst = lst
        if self not in Task.Instance().curves: Task.Instance().curves.append(self)

    def __hash__(self):
        """
        Хеширование реализовано для произвольного количества точек.
        """
        res = hash(self.lst[0])
        for i in range(2, len(self.lst)):
            res = res ^ hash(self.lst[i])
        return res


    def __eq__(self, other):
        """
        Если у дуг окружностей больше двух общих точек, то они одинаковы.
        Заметьте отличие от прямых: там достаточно двух общих точек, чтобы заявить об одинаковости.
        Тут возможен случай, что две окружности пересекаются по двум точкам.
        """
        return FindCommonFunction(self.lst, other.lst).length > 2

    def intersect(self, other):
        if len(set(self.lst) & set(other.lst)) > 2:
            Task.Instance().curves.remove(self)
            Task.Instance().curves.remove(other)
            Curve(*list(set(self.lst) | set(other.lst)))
            return 0

    def __contains__(self, item):
        return item in self.lst