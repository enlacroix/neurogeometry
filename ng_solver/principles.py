from objects import Triangle, DescribedTriangle
import itertools as it

from statement import reading_points

A, B, C = reading_points('A, B, C')
test = Triangle(A, B, C)


def sine_theorem(dtr: DescribedTriangle):
    for i in range(3):
        # Отрезок и угол, который лежит Напротив него.
        if [dtr.segments[i].is_reachable(), dtr.angles[(i + 1) % 3].is_reachable(), dtr.radius.is_reachable()].count(
                True) == 2:
            pass
            # Три реализации в зависимости от того, что неизвестно.


def cosine_theorem(tr: Triangle):
    for pair in it.combinations(tr.segments, 2):
        a, b = pair
        # Если известен а и b, то проверь угол.
        # Cos() нас интересует именно косинус
        a.angle_between(b)
