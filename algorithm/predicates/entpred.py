from ng_entities.entline import Line
from ng_entities.ratio import Ratio
from predicates.predmain import Predicate
from ng_entities.entangle import Angle
from numerical.functors import Relation
from predicates.quadpred import prl
from utils import FindCommonFindUnique


class eqa(Predicate):
    def __init__(self, A, B, C, D, E, F):
        super().__init__(A, B, C, D, E, F)
        self.sgm = [Angle(A, B, C), Angle(D, E, F)]

    def __eq__(self, other):
        return isinstance(other, eqa) and set(self.sgm) == set(other.sgm)

    def numerize(self):
        """
        Мостик между предикатом и функтором отношения.
        """
        Relation(self.sgm[0], self.sgm[1], 1)

    def another(self, angle: Angle) -> Angle:
        """
        извлечение второго элемента SGM, который не равен переданному аргументу.
        """
        return [xl for xl in self.sgm if xl != angle][0]

    def postConfirm(self):
        """
        признак параллельных прямых по равным накрест лежащим углам.: ['∠BAC = ∠BCA'] => prl(B, C, B, A)
        ∠BAC = BA; AC
        ∠BCA = BC; CA
        """
        premises = [self]
        theoremName = 'признак параллельных прямых по равным накрест лежащим углам.'
        angle1, angle2 = self.sgm
        listOfLines1, listOfLines2 = angle1.sgm, angle2.sgm
        commonLine = list(set(listOfLines1) & set(listOfLines2))
        if len(commonLine) == 0: return 0
        if len(set(listOfLines1) ^ set(listOfLines2)) == 0: return 0
        line1, line2 = list(set(listOfLines1) ^ set(listOfLines2))
        commonPointList = list(set(line1.lst) & set(line2.lst))
        if len(commonPointList) != 0: return 0
        description = f'{line1} параллельна {line2}, так как накрест лежащие углы при прямой {commonLine[0]} равны.'
        prl(*(line1.lst + line2.lst)).totalConfirm(theoremName, description, premises)

    def transitive(self, other):
        if not isinstance(other, type(self)): return 0
        commonElem, uniqueElems = FindCommonFindUnique(self.sgm, other.sgm)
        if not commonElem: return 0
        eqa.entityConstructor(*uniqueElems).totalConfirm(thname='равенство - отношение эквивалентности',
                                                         descr=f'{uniqueElems[0]} = {uniqueElems[1]}, так как оба равны {commonElem.name}.', premises=[self, other])
        return 1

    @classmethod
    def entityConstructor(cls, ang1: Angle, ang2: Angle):
        lst = ang1.lst + ang2.lst
        return cls(*lst)

    def humanize(self):
        return f'{self.sgm[0]} = {self.sgm[1]}'

    def __hash__(self):
        return hash(self.name)




class eqr(Predicate):
    """
    EqualRatio: x / y = a / с - исходное выражение. ОТНОШЕНИЕ ОТРЕЗКОВ. Именно для ПРЕДИКАТА. Не для Ratio.
    1. Перемена местами точек в х, у, а, с (согласно их правилам равенства) экивалентно исходному выражению.
    2. а / с = х / у - перемена мест аргументов eqr эквивалентно.
    3. у / х = с / а - первый алгебраический синоним
    4. х / а = у / с - второй алгебраический синоним
    5. свойство транзитивности: если есть общий ratio, то уникальные элементы равны друг другу.
    """
    def __init__(self, A, B, C, D, E, F, H, K):
        super().__init__(A, B, C, D, E, F, H, K)
        self.sgm = [Ratio(Line(A, B), Line(C, D)), Ratio(Line(E, F), Line(H, K))]

    @classmethod
    def entityConstructor(cls, arg1: Ratio, arg2: Ratio):
        return cls(*(arg1.lst + arg2.lst))


    def transitive(self, other):
        """
        x / y = a / b, a / b = c / d => x / y = c / d
        """
        if not isinstance(other, type(self)): return 0
        commonRatio, uniqueRatios = FindCommonFindUnique(self.sgm, other.sgm)
        if not commonRatio: return 0
        eqr.entityConstructor(*uniqueRatios).totalConfirm(thname='алгебраическое соображение',
                                                          descr=f'{self.humanize()}, {other.humanize()} => отношения {uniqueRatios[0]}, {uniqueRatios[1]} равны друг другу.',
                                                          premises=[self, other])
        return 1


    def __repr__(self):
        return self.name

    def humanize(self):
        return f'{self.sgm[0]} = {self.sgm[1]}'
    
    def numerize(self):
        # TODO новая матрица отношений
        pass

    def __eq__(self, other):
        """
        а) Реализация первых двух правил равенства.
        x / y = a / с == у / х = с / а
        Если множества sgm совпадают у other и у алгебраических синонимов, то other == self!
        #  or any(set(syn.sgm) == set(other.sgm) for syn in self.synonymConstructor())
        """
        return isinstance(other, eqr) and set(self.sgm) == set(other.sgm)

    def synonymConstructor(self) -> list:
        """
        x / y = a / с - исходное выражение.
        3. у / х = с / а - первый алгебраический синоним
        4. х / а = у / с - второй алгебраический синоним
        """
        eqr.entityConstructor(self.sgm[0].invert(), self.sgm[1].invert()).totalConfirm(thname='алгебраические преобразование', descr='отношение обратных величин', premises=[self])
        x, y = self.sgm[0].sgm
        a, c = self.sgm[1].sgm
        newRatio1 = Ratio(x, a)
        newRatio2 = Ratio(y, c)
        eqr.entityConstructor(newRatio1, newRatio2).totalConfirm(thname='алгебраические преобразование',
                                                                 descr=f'{newRatio1} = {newRatio2}, следует из {self.sgm[0]} = {self.sgm[1]}', premises=[self])
        return [eqr.entityConstructor(self.sgm[0].invert(), self.sgm[1].invert()), eqr.entityConstructor(newRatio1, newRatio2)]


