from ng_entities.curve import Curve
from ng_entities.entline import Line
from ng_entities.segment import Segment
from ng_objects.circles import Circle
from ng_objects.triangles import Triangle
from numerical.functors import Relation
from predicates.entpred import eqa
from predicates.predmain import Predicate
from predicates.quadpred import eql
from tskmanager import Task


class mdp(Predicate):
    def __init__(self, Z, X, Y):
        super().__init__(Z, X, Y)
        self.sgm = [Z, Line(X, Y)]

    def __eq__(self, other):
        return isinstance(other, mdp) and set(self.sgm) == set(other.sgm)

    def __hash__(self): return hash(self.sgm[0]) ^ hash(self.sgm[1])

    def confirm(self):
        res = Predicate.confirm(self)
        if res:
            Z, X, Y = self.lst
            eql(X, Z, Y, Z).totalConfirm(thname='свойство середины', descr='точка делит отрезок пополам', premises=[self])
            Line(X, Z, Y)
        return res

    def humanize(self):
        return f'{self.sgm[0]} - середина отрезка {self.sgm[1]}'

    def numerize(self):
        """
        Z - середина ХУ. ХУ / ZX = 2
        """
        Relation(Segment(self.lst[1], self.lst[2]), Segment(self.lst[0], self.lst[1]), 2)




class cir(Predicate):
    def __init__(self, center, fp, sp, tp):
        super().__init__(center, fp, sp, tp)
        self.sgm = [center, Curve(fp, sp, tp)]

    def __eq__(self, other):
        return isinstance(other, type(self)) and set(self.sgm) == set(other.sgm)

    # def __bool__(self): return Circle(*self.lst) in Task.Instance().figures

    def confirm(self):
        res = Predicate.confirm(self)
        if res:
            points_on_the_circle = self.lst[1:]
            center = self.lst[0]
            for i in range(len(points_on_the_circle) - 1):
                eql(center, points_on_the_circle[i], center, points_on_the_circle[i + 1]).totalConfirm(thname='радиусы одной окружности равны',
                                                                                                       descr=f'радиусы окружности с центром в {center} равны.', premises=[self])
        return res

    def humanize(self):
        return f'Окружность с центром в точке {self.sgm[0]}, содержащая точки {self.sgm[1]}'

class citer(Predicate):
    """
    circumcenter CITER - центр описанной окружности (точка пересечения серединных перпендикуляров).
    ort(A, C, C, B), if mpd(M, A, B) => citer(M, A, B, C).
    """
    def __init__(self, O, A, B, C):
        super().__init__(O, A, B, C)
        self.sgm = [O, Triangle(A, B, C)]

    def humanize(self): return f'{self.sgm[0]} - центр описанной окружности {self.sgm[1]}'

    def confirm(self):
        res = Predicate.confirm(self)
        if res:
            O, A, B, C = self.lst
            cir(O, A, B, C).totalConfirm(thname='свойство окружности', descr=f'окружность с центром в точке {O}', premises=[self])
        return res

    def __eq__(self, other): return isinstance(other, self.__class__) and set(self.sgm) == set(other.sgm)

class inter(Predicate):
    """
    incenter INTER - центр вписанной окружности (точка пересечения биссектрис)
    """
    def __init__(self, O, A, B, C):
        super().__init__(O, A, B, C)
        self.sgm = [O, Triangle(A, B, C)]

    def humanize(self): return f'{self.sgm[0]} - центр вписанной окружности {self.sgm[1]}'

    def confirm(self):
        res = Predicate.confirm(self)
        if res:
            O, A, B, C = self.lst
            t_name = 'свойство центра вписанной окружности'
            eqa(A, B, O, C, B, O).totalConfirm(thname=t_name, descr=f'{O.n + B.n} - биссектриса угла ∠{A.n + B.n + C.n}', premises=[self])
            eqa(B, A, O, O, A, C).totalConfirm(thname=t_name, descr=f'{O.n + A.n} - биссектриса угла ∠{B.n + A.n + C.n}', premises=[self])
            eqa(A, C, O, B, C, O).totalConfirm(thname=t_name, descr=f'{O.n + C.n} - биссектриса угла ∠{A.n + C.n + B.n}', premises=[self])
        return res

    def __eq__(self, other): return isinstance(other, self.__class__) and set(self.sgm) == set(other.sgm)