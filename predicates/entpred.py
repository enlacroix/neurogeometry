from predicates.predmain import Predicate
from entities import Angle
from objects import Triangle
import varbank as vb
from numerical.functors import Relation


class eqa(Predicate):
    def __init__(self, *lst):
        super().__init__(*lst)
        A, B, C, D, E, F, G, H = lst
        self.sgm = [Angle(A, B, C, D), Angle(E, F, G, H)]
        self.ttl = 'eqa'
        self.name = self.ttl + self.name
        self.bool = self in vb.task.predicates

    def __eq__(self, other):
        return isinstance(other, eqa) and set(self.sgm) == set(other.sgm)

    def numerize(self):
        """
        мускулистый мостик между предикатом и функтором отношения.
        """
        Relation(self.sgm[0], self.sgm[1], 1)

    def transitive(self, other):
        if isinstance(other, type(self)):
            eps = set(self.sgm)
            phi = set(other.sgm)
            pnt = []
            if len(list(eps & phi)) > 0 and self.bool and other.bool:  # Нужна ли проверка на истинность?
                for e in list(eps ^ phi):
                    pnt += e.lst
                eqa(*pnt).confirm()
                return 1
        else:
            return 0

    @classmethod
    def angle_init(cls, ang1: Angle, ang2: Angle):
        lst = ang1.lst + ang2.lst
        return cls(*lst)

    def humanize(self):
        return f'{self.sgm[0]} = {self.sgm[1]}'


class ctr(Predicate):
    """
    Congruent (подобные) треугольники.
    """

    def __init__(self, *lst):
        super().__init__(*lst)
        A, B, C, D, E, F = lst
        self.sgm = [Triangle(A, B, C), Triangle(D, E, F)]
        self.ttl = 'ctr'
        self.name = self.ttl + self.name
        self.bool = self in vb.task.predicates

    @classmethod
    def triangle_init(cls, tr1: Triangle, tr2: Triangle):
        lst = tr1.lst + tr2.lst
        return cls(*lst)

    def humanize(self):
        return f'Δ{self.sgm[0]} ~ Δ{self.sgm[1]}'

    def transitive(self, other):
        """
        Δ ABC ~ Δ DEF И Δ ABC ~ Δ HKM => Δ DEF ~ Δ HKM
        ctr(A, B, C, D, E, F).transitive(ctr(A, B, C, H, K, M))
        """
        if isinstance(other, type(self)):
            eps = set(self.sgm)
            phi = set(other.sgm)
            pnt = []
            if len(list(
                    eps & phi)) > 0 and self.bool and other.bool:  # проверка на истинность может помешать тестам, когда мы не confirm() предикаты.
                for e in list(eps ^ phi):
                    pnt += e.lst
                ctr(*pnt).confirm()
                return 1
        else:
            return 0

    def __eq__(self, other):
        return isinstance(other, self.__class__) and set(self.sgm) == set(other.sgm)


class etr(Predicate):
    """
    equal - равные треугольники.
    """

    def __init__(self, *lst):
        super().__init__(*lst)
        A, B, C, D, E, F = lst
        self.sgm = [Triangle(A, B, C), Triangle(D, E, F)]
        self.ttl = 'etr'
        self.name = self.ttl + self.name
        self.bool = self in vb.task.predicates

    @classmethod
    def triangle_init(cls, tr1: Triangle, tr2: Triangle):
        lst = tr1.lst + tr2.lst
        return cls(*lst)

    def humanize(self):
        return f'Δ {self.sgm[0]} = Δ {self.sgm[1]}'

    def transitive(self, other):
        """
        Δ ABC = Δ DEF И Δ ABC = Δ HKM => Δ DEF = Δ HKM
        """
        if isinstance(other, type(self)):
            eps = set(self.sgm)
            phi = set(other.sgm)
            pnt = []
            if len(list(
                    eps & phi)) > 0 and self.bool and other.bool:  # проверка на истинность может помешать тестам, когда мы не confirm() предикаты.
                for e in list(eps ^ phi):
                    pnt += e.lst
                ctr(*pnt).confirm()
                return 1
        else:
            return 0

    def __eq__(self, other):
        return isinstance(other, self.__class__) and set(self.sgm) == set(other.sgm)
