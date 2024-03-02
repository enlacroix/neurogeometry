from backwardLA.linangle import Linangle
from utils import logger
from ng_entities.entline import Line
from ng_entities.entpoint import Point
from tskmanager import Task

class Angle:
    """
    Обыкновенный* угол вида ∠АВС, как угол между отрезками АВ и ВС отражает вторую фундаментальную сущность геометрии.
    Сочетает в себе логические и вычислительные функции.
    """
    def __init__(self, A: Point, B: Point, C: Point):
        self.lst = A, B, C
        self.sgm = [Line(A, B), Line(B, C)]
        self.vertex = B
        self.arc = Line(A, C)
        self.name = f'∠{A.n + B.n + C.n}'
        if self not in Task.Instance().angles: Task.Instance().angles.append(self)

    def __eq__(self, other):
        return isinstance(other, type(self)) and set(self.sgm) == set(other.sgm)

    def convertToFullAngle(self):
        """
        ∠[u, v] - определение полного угла: который задаётся как угол между двумя прямыми.
        Данный метод переводит обычный угол в одну из версий полного ∠[AB, ВС] при помощи метода entry().
        Предупреждаю, что также верна запись ∠[BC, AС], но это нельзя установить точно в каком направлении идёт обход.
        """
        A, C = self.arc
        return Linangle(Line(A, self.vertex).entry(), Line(C, self.vertex).entry())

    def __repr__(self): return self.name

    def humanize(self): return f'{self.name}'

    def getIndex(self): return Task.Instance().angles.index(self)

    def __ne__(self, other): return not (self == other)

    def __hash__(self): return hash(self.sgm[0]) ^ hash(self.sgm[1])

    def getValue(self):
        try:
            return Task.Instance().angle_dict[self]
        except KeyError:
            logger(f'Величина угла {self} неизвестна!')
            Task.Instance().angle_dict[self] = None
            return

    def is_reachable(self):
        """
        Достижимо ли значение угла (как пример). Пояснение: если мы знаем его величину из словаря, то она очевидно достижима.
        Иначе, если мы знаем значение тригонометрической функции, то через 1 действие мы можем найти этот угол.
        Коэффициент достижимости (Reachable Coefficient, далее RC) равен 1.
        return: или True (RC = 0) или значение RC (RC > 0).
        """
        if self.getValue():
            return True
        else:
            pass


    # def numerical(self):
    #     vb.task.angle_dict[self] = None

    # def humanize(self):
    #     eps = set(self.sgm[0].lst)
    #     phi = set(self.sgm[1].lst)
    #     if len(list(eps & phi)) == 1:
    #         a = list(eps - phi)[0]
    #         b = list(eps & phi)[0]
    #         c = list(phi - eps)[0]
    #         return '∠' + a.n + b.n + c.n
    #     else:
    #         return self.name






