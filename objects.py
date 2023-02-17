from entities import Angle, Line
from numerical.functors import Sum
from predicates.freepred import col


class Triangle:
    def __init__(self, *lst):
        self.lst = lst
        X, Y, Z = self.lst
        self.segments = [Line(X, Y), Line(X, Z), Line(Y, Z)]
        self.angles = [Angle(X, Y, X, Z), Angle(X, Z, Y, Z), Angle(Y, Z, Y, X)]
        Sum(self.angles, 180)  # TODO перенести в confirm()
        self.name = f'Треугольник {X.n + Y.n + Z.n}'
        col(X, Y).confirm()
        col(X, Z).confirm()
        col(Z, Y).confirm()

    def __str__(self):
        return self.name

    def confirm(self):
        # TODO добавить объект в vb.objects (triangles)
        pass

    def __hash__(self):
        return hash(self.segments[0]) ^ hash(self.segments[1]) ^ hash(self.segments[2])

    def __eq__(self, other):
        return set(self.lst) == set(other.lst)  # set(self.sgm) == set(other.sgm)


class DescribedTriangle(Triangle):
    """
    описанный треугольник.
    """

    def __init__(self, center, *lst):
        super().__init__(*lst)
        self.radius = Line(center, self.lst[0])


class Quadrangle:
    def __init__(self, *lst):
        self.lst = lst
        A, B, C, D = self.lst
        col(A, B).confirm()
        col(B, C).confirm()
        col(C, D).confirm()
        col(D, A).confirm()


class Parallelogram(Quadrangle):
    pass


class Circle:
    """
    Избыточность с предикатом cir (fixpred.py), тем не менее Circle будет выполнять свои функции.
    """
    pass


class InscribedCircle(Circle):
    pass
