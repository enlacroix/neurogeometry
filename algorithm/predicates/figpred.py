"""
orthocenter ORTER - ортоцентр, точка пересечения высот.
"""
from predicates.quadpred import eql
from utils import FindCommonFindUnique
from ng_objects.triangles import Triangle
from predicates.entpred import eqa, eqr
from predicates.predmain import Predicate


class ctr(Predicate):
    """
    Congruent (подобные, на самом деле нет) треугольники.
    Потому что по Колмогорову конгруэнтные треугольники, значит равные. Но similar (подобный) приводит к схожести с str(), поэтому было сделано такое
    допущение.
    ВНИМАНИЕ! ctr() является полу фиксированным предикатом, т.к. от первых трёх точек А В С зависит расположение точек P Q R,
    они должны быть расставлены в соответствии с подобием. Т.е. <B_A_C = <Q_P_R, если верно ctr(A, B, C, P, Q, R).
    """

    def __init__(self, A, B, C, P, Q, R):
        super().__init__(A, B, C, P, Q, R)
        self.sgm = [Triangle(A, B, C), Triangle(P, Q, R)]

    @classmethod
    def entityConstructor(cls, tr1: Triangle, tr2: Triangle):
        lst = tr1.lst + tr2.lst
        return cls(*lst)

    def confirm(self):
        """
        Из подобия треугольников следует АВС ~ PQR: (A->P, B->Q, C->R).
        - равенство углов (соотв) <ABC = <PQR, <BAC = <QPR, <ACB = <QRP.
        - равенство отношений; BC / QR = AB / PQ = AC / PR
        Необходимо все это подтвердить и добавить в Р, поэтому если родительский метод confirm() вернул 1, то работаем.
        """
        res = super().confirm()
        if res:
            A, B, C, P, Q, R = self.lst
            collection = [eqa(A, B, C, P, Q, R), eqa(B, A, C, Q, P, R), eqa(A, C, B, Q, P, R), eqr(B, C, Q, R, A, B, P, Q),
                          eqr(A, B, P, Q, A, C, P, R), eqr(B, C, Q, R, A, C, P, R)]
            # Последний предикат лишний, но оставим его из соображений единообразия. (и оптимизации, чтобы сразу на итерации был нужный пред)
            for pred in collection:
                pred.totalConfirm(thname='свойство подобных треугольников', descr=self.humanize(), premises=[self])
        return res

    def humanize(self):
        return f'{self.sgm[0]} ~ {self.sgm[1]}'

    def transitive(self, other):
        """
        Δ ABC ~ Δ DEF И Δ ABC ~ Δ HKM => Δ DEF ~ Δ HKM
        ctr(A, B, C, D, E, F).transitive(ctr(A, B, C, H, K, M))
        """
        if not isinstance(other, type(self)): return 0
        commonElem, uniqueElems = FindCommonFindUnique(self.sgm, other.sgm)
        if not commonElem: return 0
        ctr.entityConstructor(*uniqueElems).totalConfirm(thname='подобие - отношение эквивалентности',
                                                         descr=f'{uniqueElems[0]} ~ {uniqueElems[1]}, так как оба подобны {commonElem.name}.', premises=[self, other])
        return 1

    def __eq__(self, other):
        return isinstance(other, self.__class__) and set(self.sgm) == set(other.sgm)


class etr(Predicate):
    """
    equal - равные треугольники.
    """

    def __init__(self, A, B, C, D, E, F):
        super().__init__(A, B, C, D, E, F)
        self.sgm = [Triangle(A, B, C), Triangle(D, E, F)]

    @classmethod
    def entityConstructor(cls, tr1: Triangle, tr2: Triangle):
        lst = tr1.lst + tr2.lst
        return cls(*lst)

    def humanize(self):
        return f'Δ {self.sgm[0]} = Δ {self.sgm[1]}'

    def transitive(self, other):
        """
        Δ ABC = Δ DEF И Δ ABC = Δ HKM => Δ DEF = Δ HKM
        """
        if not isinstance(other, type(self)): return 0
        commonElem, uniqueElems = FindCommonFindUnique(self.sgm, other.sgm)
        if not commonElem: return 0
        etr.entityConstructor(*uniqueElems).totalConfirm(thname='равенство треугольников - отношение эквивалентности',
                                                         descr=f'{uniqueElems[0]} = {uniqueElems[1]}, так как оба равны {commonElem.name}.', premises=[self, other])
        return 1

    def __eq__(self, other):
        return isinstance(other, self.__class__) and set(self.sgm) == set(other.sgm)

    def confirm(self):
        """
        Из подобия треугольников следует АВС ~ PQR: (A->P, B->Q, C->R).
        - равенство углов (соотв) <ABC = <PQR, <BAC = <QPR, <ACB = <QRP.
        - равенство отношений; BC / QR = AB / PQ = AC / PR
        Необходимо все это подтвердить и добавить в Р, поэтому если родительский метод confirm() вернул 1, то работаем.
        """
        res = super().confirm()
        if res:
            A, B, C, P, Q, R = self.lst
            collection = [eqa(A, B, C, P, Q, R), eqa(B, A, C, Q, P, R), eqa(A, C, B, Q, P, R), eql(B, C, Q, R),
                          eql(A, B, P, Q), eql(A, C, P, R)]
            # Последний предикат лишний, но оставим его из соображений единообразия. (и оптимизации, чтобы сразу на итерации был нужный пред)
            for pred in collection:
                pred.totalConfirm(thname='свойство равных треугольников', descr=self.humanize(), premises=[self])
        return res


        
