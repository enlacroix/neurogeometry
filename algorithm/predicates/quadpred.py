import itertools as it

from ng_entities.segment import Segment
from numerical.functors import Relation, SetValue, LinearCombination
from predicates.predmain import Predicate, AbstractPredicate, GeneralizedPredicate
from ng_entities.entangle import Line, Angle
from tskmanager import Task
from utils import FindCommonFindUnique


class ort(Predicate):
    """
    Здесь была обнаружена проблема с self.bool:
    не перемещай его в родительский класс, он не знает, что такое sgm на этапе вызова родительского конструктора.
    """
    def __init__(self, X, Y, Z, W):
        super().__init__(X, Y, Z, W)
        self.sgm = [Line(X, Y), Line(Z, W)]

    def __bool__(self):
        if ORT(*self.sgm): return True
        if self.ttl in Task.Instance().predicates: return self in Task.Instance().predicates[self.ttl]
        return False

    def __eq__(self, other): return isinstance(other, type(self)) and set(self.sgm) == set(other.sgm)

    def transitive(self, other):
        """
        "Транзитивность" или операция возведения предиката в квадрат определяет результат логической формулы ort() & ort() = x * y.
        Если FC(x.sgm, y.sgm) == 1, то результатом будет теорема о двух прямых а и b ортогональных третьей, из чего следует, что а \\ b.
        Иначе ort() & ort() -> None.
        """
        if isinstance(other, type(self)):
            commonLine, uniqueLines = FindCommonFindUnique(self.sgm, other.sgm)
            if not commonLine: return 0
            prl.entityConstructor(*uniqueLines).totalConfirm(thname='правило трёх прямых',
                                                             descr=f'прямые {uniqueLines[0]}, {uniqueLines[1]} перпендикулярные {commonLine.name} параллельны друг другу.',
                                                             premises=[self, other])
            return 1
        return 0

    def humanize(self):
        return f'{self.sgm[0]}⟂{self.sgm[1]}'

    def another(self, line):
        return [xl for xl in self.sgm if xl != line][0]

    def numerize(self):
        """
        ort: угол между компонующими линиями равен 90 градусов.
        """
        commonPoint, uniquePoints = FindCommonFindUnique(self.sgm[0].lst, self.sgm[1].lst)
        if not commonPoint: return
        SetValue(Angle(uniquePoints[0], commonPoint, uniquePoints[1]), 90)


class prl(Predicate):  # Четыре точки, первые две и последние две из них обозначают прямые, которые параллельны.
    def __init__(self, X, Y, Z, W):
        super().__init__(X, Y, Z, W)
        self.sgm = [Line(X, Y), Line(Z, W)]

    def __eq__(self, other):
        return isinstance(other, prl) and set(self.sgm) == set(other.sgm)

    def another(self, line: Line) -> Line:
        """
        извлечение у квадропредикатов второго элемента SGM, который не равен переданному аргументу.
        """
        return [xl for xl in self.sgm if xl != line][0]

    def __bool__(self):
        if PRL(*self.sgm): return True
        if self.ttl in Task.Instance().predicates: return self in Task.Instance().predicates[self.ttl] #  or bool(PRL(*self.sgm))
        return False

    @classmethod
    def entityConstructor(cls, line1: Line, line2: Line):
        return cls(*(line1.lst + line2.lst))

    def transitive(self, other):
        """
        Реализация интуитивного геометрического свойства (отношение эквивалентности): a || b, c || b => a || c.
        prl(...) & prl(...) -> prl(...) if FC(a, b) == 1 else None.
        FC(a, b) - FindCommon функция, которая вычисляет количество совпавших элементов.
        """
        if isinstance(other, type(self)):
            commonLine, uniqueLines = FindCommonFindUnique(self.sgm, other.sgm)
            if not commonLine: return 0
            prl.entityConstructor(*uniqueLines).totalConfirm(thname='аксиома о транзитивности параллельности',
                                                             descr=f'прямые {uniqueLines[0]}, {uniqueLines[1]} параллельные {commonLine.name} параллельны друг другу.',
                                                             premises=[self, other])
            return 1
        return 0

    def humanize(self): return f'{self.sgm[0]} ∥ {self.sgm[1]}'



class eql(Predicate):
    def __init__(self, X, Y, Z, W):
        super().__init__(X, Y, Z, W)
        self.sgm = [Line(X, Y), Line(Z, W)]

    def __eq__(self, other): return isinstance(other, eql) and set(self.sgm) == set(other.sgm)


    def transitive(self, other):
        """
        Равенство также является отношением эквивалентности, и данный метод реализует следующее свойство:
        [АВ = ВС, ВС = MN] => AB = MN.
        В переводе на наш язык: eql(A, B, B, C) & eql(B, C, M, N) -> eql(UniqueLines: A, B, M, N).
        """
        if not isinstance(other, type(self)): return 0
        commonLine, uniqueLines = FindCommonFindUnique(self.sgm, other.sgm)
        if not commonLine: return 0
        eql.entityConstructor(*uniqueLines).totalConfirm(thname='аксиома о транзитивности равенства отрезков',
                                                         descr=f'{self.humanize()}, {other.humanize()} => отрезки {uniqueLines[0]}, {uniqueLines[1]} равны друг другу.',
                                                         premises=[self, other])
        return 1

    def humanize(self):
        return f'{self.sgm[0]}={self.sgm[1]}'

    def another(self, line):
        return [xl for xl in self.sgm if xl != line][0]

    @classmethod
    def entityConstructor(cls, line1: Line, line2: Line):
        return cls(*(line1.lst + line2.lst))

    def numerize(self):
        """
        eql уведомляет вычислительный модуль о том, что длины отрезков одинаковы.
        """
        X, Y, Z, W = self.lst
        Relation(Segment(X, Y), Segment(Z, W), 1)

class PRL(GeneralizedPredicate):
    def __init__(self, line1: Line, line2: Line):
        self.ttl = 'PRL'
        self.name = self.ttl + f'[{line1.name}, {line2.name}]'
        self.sgm = [line1.entry(), line2.entry()]

    def __eq__(self, other):
        return isinstance(other, PRL) and set(self.sgm) == set(other.sgm)

    def __repr__(self):
        return self.name

    def confirm(self): return AbstractPredicate.confirm(self)

    def numerize(self): pass

    @classmethod
    def q(cls, A, B, C, D):
        return cls(Line(A, B), Line(C, D))


    def __bool__(self):
        """
        Полная проверка истинности сущностных предикатов состоит в том, чтобы перебрать всевозможные сочетания точек по два с прямых-аргументов,
        и проверить существует ли в множестве Р соотв. точечные предикаты prl/ort.
        С^2_l * C^2_m * O(prl) вместо О(prl).
        for firstPair, secondPair in it.product(it.combination(self.sgm[0].lst, 2), it.combination(self.sgm[1].lst, 2):
        if prl(*(firstPair+secondPair)): return True
        return False
        """
        presence = self in Task.Instance().predicates[self.ttl]
        if presence: return True
        for firstPair, secondPair in it.product(it.combinations(self.sgm[0].lst, 2), it.combinations(self.sgm[1].lst, 2)):
            # print(tuple(map(str, firstPair + secondPair)))
            if prl(*(firstPair + secondPair)) in Task.Instance().predicates.get('prl', ()): return True
        return False

    def transitive(self, other):
        pass


class ORT(GeneralizedPredicate):
    def __init__(self, line1: Line, line2: Line):
        self.ttl = self.__class__.__name__
        self.name = self.ttl + f'[{line1.name}, {line2.name}]'
        self.sgm = [line1.entry(), line2.entry()]

    def __eq__(self, other):
        return isinstance(other, self.__class__) and set(self.sgm) == set([ln.entry() for ln in other.sgm])

    def confirm(self): return AbstractPredicate.confirm(self)

    def __bool__(self):
        presence = self in Task.Instance().predicates[self.ttl]
        if presence: return True
        for firstPair, secondPair in it.product(it.combinations(self.sgm[0].lst, 2), it.combinations(self.sgm[1].lst, 2)):
            # print(tuple(map(str, firstPair + secondPair)))
            if ort(*(firstPair + secondPair)) in Task.Instance().predicates.get('ort', ()):
                return True
        return False
    @classmethod
    def q(cls, A, B, C, D):
        return cls(Line(A, B), Line(C, D))

    def numerize(self): pass

    def transitive(self, other):
        pass

    def __repr__(self):
        return self.name