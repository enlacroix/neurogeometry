import itertools
from ng_entities.entangle import Angle, Line, Point
from ng_entities.segment import Segment
from ng_objects.circles import InscribedCircle
from ng_objects.figure import GeomFigure
from numerical.functors import Sum, LinearCombination
from predicates.entpred import eqa
from predicates.freepred import col
from predicates.quadpred import ort, eql
from tskmanager import Task
from utils import findIfObjWasDecorated, logger


class Triangle:
    def __init__(self, *lst):
        self.lst = lst
        X, Y, Z = self.lst
        self.wrapped = None
        self.segments = [Segment(X, Y), Segment(X, Z), Segment(Y, Z)]
        self.angles = [Angle(Y, X, Z), Angle(X, Z, Y), Angle(Z, Y, X)]
        self.name = f'Δ{X.n + Y.n + Z.n}'
        self.depthOfWrapping = 0
        self.collection = [] # col(X, Y), col(X, Z), col(Z, Y), писать это избыточно, поскольку уже проиниц Line.

    def __str__(self):
        return self.name

    def confirm(self):
        if self not in Task.Instance().figures:
            self.numerize()
            Task.Instance().figures.append(self)
            return 1
        else:
            return 0

    def numerize(self):
        Sum(self.angles, 180)

    # Подобен/равен один треугольник другому.
    def isSimilarTo(self, other):
        pass

    def isCongruentTo(self, other):
        pass

    def __hash__(self):
        return hash(self.segments[0]) ^ hash(self.segments[1]) ^ hash(self.segments[2])

    def __eq__(self, other):
        return isinstance(self, other) and set(self.lst) == set(other.lst)  # set(self.sgm) == set(other.sgm)


class OrtTriangle:
    def __init__(self, wrappedTriangle, vertex):
        """
        :vertex: вершина прямого угла
        """
        self.wrapped = wrappedTriangle
        self.depthOfWrapping = self.wrapped.depthOfWrapping + 1
        self.vertex = vertex
        self.segments = self.wrapped.segments
        self.angles = self.wrapped.angles
        X, Y = [pnt for pnt in wrappedTriangle.lst if pnt != vertex]
        self.X, self.Y = X, Y
        # self.collection = [ort(X, vertex, Y, vertex)]
        self.cathets = [Line(X, vertex), Line(Y, vertex)]
        self.hypotenuse = Line(X, Y)
        self.name = f'прямоугольный треугольник {X.n + vertex.n + Y.n} с вершиной {vertex}'
        self.ruleset = None

    def confirm(self):
        """
        Ruleset:
        - todo если центр описанной окружности лежит на стороне треугольника, то он прямоугольный. (необяз)
        """
        if self not in Task.Instance().figures:
            self.wrapped.confirm()
            ort(self.X, self.vertex, self.Y, self.vertex).totalConfirm('определение прямоугольного треугольника', f'задан {self.name}', premises=[self])
            Task.Instance().figures.append(self)

    def numerize(self):
        """
        Вычислительные свойства прямоугольного треугольника:
        - про значение прямого угла уже известно из ort.
        - TODO теорема Пифагора и обратная к ней.
        - сумма острых углов равна 90 - уже лежит такая информация в Numerical-модуле.
        - TODO радиус описанной окружности равен половине гипотенузы.
        - радиус вписанной окружности равен: (a + b - c)/2 - r = 0 - придётся изобретать новый функтор?
        """
        self.wrapped.numerize()

class DescribedTriangle:
    def __init__(self, wrappedTriangle, circle: InscribedCircle):
        """
        Декоратор описывающего треугольника (т.е., в которого вписана окружность).
        :circle: вписанная окружность. Обязательный параметр - center, остальные точки
        """
        self.wrapped = wrappedTriangle
        self.depthOfWrapping = self.wrapped.depthOfWrapping + 1
        self.circle = circle

    def __eq__(self, other):
        """
        1. Совпадение базового (корневого) типа
        2. Совпадение множества точек.
        3. Фигура с большей глубиной вложенности (depthOfWrapping) является приоритетнее и должен ЗАМЕНИТЬ собой старый.
        """
        basetr = findIfObjWasDecorated(other, Triangle)
        if basetr is None: return 0
        return set(findIfObjWasDecorated(self, Triangle).lst) == set(basetr.lst)



    def confirm(self):
        """
        - центр вписанной окружности лежит на биссектрисах всех трёх углов.
        - радиус к точке касания перпендикулярен стороне.
        """
        if self.circle.pointsOfTangency:
            currtr = findIfObjWasDecorated(self, Triangle)
            currtr: Triangle
            for pnt, seg in itertools.product(self.circle.pointsOfTangency, currtr.segments):
                if col(pnt, *seg.lst):
                    ort(self.circle.center, pnt, *seg.lst).totalConfirm(thname='радиус вписанной окружности перпендикулярен касательной',
                                                                        descr=f'Радиус {self.circle.center.n + pnt.n} проведённый к точке касания перпендикулярен стороне {seg}, так как она является '
                                                                              f'касательной. ', premises=[self])

    def numerize(self):
        currtr = findIfObjWasDecorated(self, OrtTriangle)
        currtr: OrtTriangle
        if currtr is not None and self.circle.radii:
            logger('Применена формула радиуса вписанной окружности в прямоугольном треугольнике.')
            LinearCombination({currtr.cathets[0]: 0.5, currtr.cathets[1]: 0.5, currtr.hypotenuse: -0.5, self.circle.radii[0]: -1})

class IsoTriangle(GeomFigure):
    def __init__(self, wrappedTriangle, vertex: Point):
        """
        :vertex: вершина равнобедренного треугольника
        """
        self.wrapped = wrappedTriangle
        self.depthOfWrapping = self.wrapped.depthOfWrapping + 1
        self.vertex = vertex
        self.baseOfTriangle = Line(*[pnt for pnt in wrappedTriangle.lst if pnt != vertex])
        self.segments = self.wrapped.segments
        self.angles = self.wrapped.angles

    def __eq__(self, other):
        return isinstance(self, type(other)) and self.vertex == other.vertex and self.baseOfTriangle == other.baseOfTriangle

    def humanize(self):
        return f'△{self.vertex.n + self.baseOfTriangle.lst[0].n + self.baseOfTriangle.lst[1].n} c основанием {self.baseOfTriangle}'

    def __str__(self): return f'р/б △{self.vertex.n + self.baseOfTriangle.lst[0].n + self.baseOfTriangle.lst[1].n}'

    @classmethod
    def pointConstructor(cls, A: Point, B: Point, vertex: Point): return cls(Triangle(A, B, vertex), vertex)

    def postConfirm(self):
        """
        △ ABC: BC - основание р/б.
        база: AB = AC; <ABC = <ACB
        mdp & ort -> Iso
        ort & eqa -> Iso
        mdp & eqa -> Iso
        ___ 2 блок теорем
        mdp (M, B, C) & Iso -> eqa, ort
        ort & Iso -> mdp, eqa
        eqa & Iso -> mdp, ort
        """
        A = self.vertex
        B, C = self.baseOfTriangle.lst
        for pred in (eql(A, B, A, C), eqa(A, B, C, A, C, B)):
            pred.totalConfirm(thname='свойства р/б треугольника', descr=f'{self.humanize()}', premises=[self])















