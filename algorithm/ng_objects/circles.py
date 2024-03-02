from __future__ import annotations
from ng_entities.curve import Curve
from ng_entities.entline import Line
from ng_entities.entpoint import Point


class Circle:
    """
    Истинность предиката cir проверяется ссылкой на поиск Circle, но он остаётся 4-точечным.
    """
    def __init__(self, center: Point, *points):
        self.center = center
        self.sgm = [self.center, Curve(*points)]
        self.radii = [Line(center, pnt) for pnt in points]
        self.diameters = [] # Диаметр это прямая состоящая из центра и двух точек на окружности А и В, про которых известно, что col(A, B, O) = True.

    def numerize(self):
        """
        все радиусы равны между собой. (см. реализацию в предикате cir).
        """
        pass

    def __eq__(self, other):
        return isinstance(other, Circle) and self.sgm == other.sgm



class InscribedCircle(Circle):
    def __init__(self, center: Point, pointsOfTangency: list[Point] = None, restPoints: list[Point] = None):
        self.pointsOfTangency = [] if pointsOfTangency is None else pointsOfTangency
        self.restPoints = [] if restPoints is None else restPoints
        super().__init__(center, *(pointsOfTangency + restPoints))

