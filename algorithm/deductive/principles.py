# from ng_objects.triangles import Triangle, DescribedTriangle
# import itertools as it
#
# from statement import reading_points
#
# A, B, C = reading_points('A, B, C')
# test = Triangle(A, B, C)
#
#
# def sine_theorem(dtr: DescribedTriangle):
#     for i in range(3):
#         # Отрезок и угол, который лежит Напротив него.
#         if [dtr.segments[i].is_reachable(), dtr.angles[(i + 1) % 3].is_reachable(), dtr.radius.is_reachable()].count(
#                 True) == 2:
#             pass
#             # Три реализации в зависимости от того, что неизвестно.
#
#
# def cosine_theorem(tr: Triangle):
#     for pair in it.combinations(tr.segments, 2):
#         a, b = pair
#         # Если известен а и b, то проверь угол.
#         # Cos() нас интересует именно косинус
#         a.angle_between(b)
import itertools

import config
from ng_entities.curve import Curve
from ng_entities.entangle import Angle
from ng_entities.entline import Line
from ng_entities.segment import Segment
from numerical.functors import Sum, LinearCombination, Relation
from predicates.entpred import eqa
from predicates.freepred import cyl
from tskmanager import Task

def principleApplying():
    for crv in Task.Instance().curves: P1(crv)
    for ln in Task.Instance().lines: P2(ln)
    P3()

def P1(entity: Curve):
    """
    Curve(A, B, C, D): Очень часто задача о вписанных углах возникает в описанном 4-х угольнике, поэтому можно определить эту теорему для фикс
    четырёх точек.
    хорды: [AB, AC, AD, BC, BD, CD] C^2_4 = 4! / 2!/2! = 6.
    """
    if not config.BETA: return
    thname = 'свойство вписанных углов'
    explanation = 'вписанные углы, опирающиеся на равные хорды равны.'
    if not isinstance(entity, Curve) or not len(entity.lst) == 4: return 0
    A, B, C, D = entity.lst
    for pred in [eqa(A, C, B, A, D, B), eqa(A, B, D, A, C, D), eqa(B, A, C, B, D, C), eqa(C, A, D, C, B, D)]:
        pred.totalConfirm(thname=thname, descr=explanation, premises=[cyl(A, B, C, D)])
    Sum([Angle(A, B, C), Angle(A, D, C)], 180)
    Sum([Angle(B, C, D), Angle(B, A, D)], 180)

def P2(entity: Line):
    """
    Реализация свойства аддитивности. Line(A, B, C, D) =>
    AD = AB + BC + CD
    - AC = AB + BC, AD = AC + CD, BD = BC + CD.
    остальные соотношения будут выведены матричным путем. LinearCombination(AC: 1, АВ: -1, ВС: -1)
    start = [0, N - 2)
    step in [1, N - 1)
    dist = step + 1: [2, N - 4)
    [0] - [2]: [0][1] [1][2]
    [1] - [3]: [1][2] [2][3]

    [0] - [3]: [0][2] [2][3]
    [2] - не имеет смысл рассматривать. до N - 2 не включительно.
    Line(A, B, C, D, E); N - 2 = 3
    step = 1
    [0] - [2]: [0][1] [1][2] - step здесь в первом аргументе. второй аргумент всегда +1.
    [1] - [3]: [1][2] [2][3]
    [2] - [4]: [2][3] [3][4]
    step = 2 N = 5
    [0] - [0 + dist = 3]: [0][2] [2][3]
    [1] - [1 + dist = 4]: [1][3] [3][4]
    step = 3 start + step + 1 < N
    [0] - [4] = [0][3] + [3][4]
    """
    if not config.BETA: return
    N = len(entity.lst)
    if N <= 2: return 0
    for step in range(1, N - 1): # N - 2 вариантов для шагов.
        for start in range(0, N - 1 - step): # N - 1 - step вариантов.
            # step = N - 2: N - 1 - (N - 2) = - 1 + 2 = 1, т.е [0. 1) - крайний случай, все верно.
            leftSegment = Segment(entity.lst[start], entity.lst[start + step + 1])
            rightSegment1 = Segment(entity.lst[start], entity.lst[start + step])
            rightSegment2 = Segment(entity.lst[start + step], entity.lst[start + step + 1]) # start + step + 1 < N
            print(f'{entity}: {leftSegment}, {rightSegment1}, {rightSegment2}')
            LinearCombination({leftSegment: -1, rightSegment1: 1, rightSegment2: 1})
    return 1

def P3():
    """
    commonSGM - cSGM(a, b) - сколько общих сторон у двух углов a и b. a.v - вершина угла а.
    ПРИЛЕГАЮЩИЕ. a.v != b.v, cSGM(a, b) = 1. - образуют треугольник
    СМЕЖНЫЕ. a.v = b.v, cSGM(a, b) = 1. - сумма равна 180
    ВЕРТИКАЛЬНЫЕ. a.v = b.v, cSGM(a, b) = 0. - равны друг другу
    На доработку. Вертикальные углы, например, образуются, когда прямые имеют единственную точку пересечения
    """
    pass
    # for entity, angle in itertools.combinations(Task.Instance().angles, 2):
    #     if entity.vertex == angle.vertex:
    #         if len(set(entity.arc.lst) & set(angle.arc.lst)) == 1:
    #             Sum([entity, angle], 180)
    #         # else:
    #         #     eqa.entityConstructor(entity, angle).totalConfirm(thname='равенство вертикальных углов', descr=f'{entity}={angle}, как вертикальные.', premises=[None])
    #         #     Relation(entity, angle, 1)
