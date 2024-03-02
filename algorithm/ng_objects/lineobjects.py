from typing import TYPE_CHECKING

from predicates.entpred import eqa

if TYPE_CHECKING:
    from ng_entities.entangle import Angle, Point, Line


class Bisect:
    """
    Угол АВС и точка О. ОВ - биссектриса угла АВС.
    <OBC = <OBA
    если Е - принадлежит прямой ОВ, то ОЕ - биссектриса угла АВС.
    общее свойство: если выяснилось, что Line - биссектриса, то это относится ко всей прямой, т.е. является ее свойством.
    isBisect(), isMedian(), isHeight().
    """
    def __init__(self, angle: Angle, point: Point):
        self.angle = angle
        self.line = Line(angle.vertex, point)
        A, B, C = angle.lst
        self.collection = [eqa(A, B, point, point, B, C)]
        # Find(self.line) в общем списке. присвоить ему тот факт, что это биссектриса и все новые точки, которые к нему
        # прибавятся - это тоже бис.

    def confirm(self):
        # определение биссектрисы - равные углы
        # биссектриса разбивает треугольник на два подобных.
        pass

    def numerical(self):
        # Relation = 1, Sum(частей) равно углу
        pass



