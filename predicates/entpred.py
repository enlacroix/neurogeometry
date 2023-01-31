from predicates.predmain import Predicate
from entities import Angle
import varbank as stm
import numerical as nm


class eqa(Predicate):
    def __init__(self, *lst):
        super().__init__(*lst)
        A, B, C, D, E, F, G, H = lst
        self.sgm = [Angle(A, B, C, D), Angle(E, F, G, H)]
        self.ttl = 'eqa'
        self.name = self.ttl + self.name
        self.bool = self in stm.predicates
        # nm.Relation(self.sgm[0], self.sgm[1], 1)

    def __eq__(self, other):
        return isinstance(other, eqa) and set(self.sgm) == set(other.sgm)

    def __mul__(self, other):
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