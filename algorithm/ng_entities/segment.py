from ng_entities.entpoint import Point
from tskmanager import Task
from utils import logger, FindCommonFunction


class Segment:
    """
    Отрезок это часть прямой, ограниченная двумя точками. Нам требуется выделить сущность в отдельный класс, так как для вычислительного модуля
    не требуется все точки на прямой, а конкретные две - расстояние между которыми нас интересует.
    """
    def __init__(self, point1: Point, point2: Point):
        self.lst = [point1, point2]
        self.name = point1.n + point2.n
        assert point1 != point2, f'был проинициализирован отрезок {self.name} c совпадающими точками - проверьте источник!'
        if self not in Task.Instance().segments:
            # print(f'я из сегмента: {self}')
            Task.Instance().segments.append(self)

    def __eq__(self, other):
        return isinstance(other, type(self)) and set(self.lst) == set(other.lst)

    def __repr__(self): return f'{self.name}' # добавь отр, чтобы различать

    def humanize(self): return f'отрезок {self.name}'

    def __hash__(self):
        return hash(self.lst[0]) ^ hash(self.lst[1])

    def getIndex(self):
        if len(self.lst) != 2: return
        try:
            return Task.Instance().segments.index(self)
        except ValueError:
            Task.Instance().segments.append(self)
            return len(Task.Instance().segments) - 1

    def __contains__(self, item):
        return item in self.lst

    def getValue(self):
        if len(self.lst) != 2: return
        try:
            return Task.Instance().segment_dict[self]
        except KeyError:
            logger(f'Был проинициализирован отрезок {self} пустым значением!')
            Task.Instance().segment_dict[self] = None
            return
    def entry(self):
        """
        Точка доступа к "истинной" прямой, хранящейся в списке Task. Все методы должны вызываться от прямой, возвращаемой entry().
        Пример: Прямая АВ часть уже созданной прямой АВС, и мы хотим распечатать оригинальную прямую.
        Line(A, B).entry().humanize() -> Line(A, B, C).humanize() -> пр. АВС.
        """
        return next((line for line in Task.Instance().lines if FindCommonFunction(self.lst, line.lst).logic), self)

