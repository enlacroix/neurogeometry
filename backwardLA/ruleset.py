import itertools

import external
from backwardLA.linangle import LinAngle, NeutralLA, RightLA
from backwardLA.simplifier import Simplifier
from ng_entities.entline import Line
from predicates.quadpred import PRL, ORT
from tskmanager import Task


def R1(angle: LinAngle):
    """
    R1. ∠[u, v] -> ∠[u, m], если v ∥ m. ∀ u ∈ Task.lines.
    ∠[v, u] = ∠[m, u] (причем заменить можно в обе стороны). Таким образом, такое частное правило обеспечивает 4 замены.
    Цель: сформировать список углов, которым равен ∠[u, v] (и ∠[v, u] одновременно). добавить в substitution-словарь.
    """
    if PRL(angle.x, angle.y):
        Simplifier.addLink(keyAngle=angle, valAngle=NeutralLA(angle.x))
        return
    for m in Task.Instance().lines:
        if PRL(angle.y, m): Simplifier.addLink(keyAngle=angle, valAngle=LinAngle(angle.x, m))
        if PRL(angle.x, m): Simplifier.addLink(keyAngle=angle, valAngle=LinAngle(m, angle.y))

def R2(angle: LinAngle):
    """
    ORT(u, v) -> ∠[u, v] = [R]
    """
    if ORT(angle.x, angle.y): Simplifier.addLink(keyAngle=angle, valAngle=RightLA(angle.x, angle.y))

def R3():
    """
    C - вершина р/б треугольника.
    eql(A, C, B, C) => ∠[AB, BC] = ∠[AC, AB] - р/б треугольник.
    ∠[АВ, AC] = ∠[BC, АВ] - аналогично, если переменить местами точки А и В.
    """
    for eqlPredicate in Task.Instance().predicates.get('eql', []):
        commonPointList, uniquePoints = external.FindCommonFindUnique(eqlPredicate.sgm[0].lst, eqlPredicate.sgm[1].lst)
        if not commonPointList: continue
        C = commonPointList[0]
        A, B = uniquePoints
        Simplifier.addLink(keyAngle=LinAngle(Line(A, B), Line(B, C)), valAngle=LinAngle(Line(A, C), Line(A, B)))
        Simplifier.addLink(keyAngle=LinAngle(Line(A, C), Line(A, B)), valAngle=LinAngle(Line(A, B), Line(B, C)))

def R4():
    """
    cyl(O, A, M, K) => C^2_4 вариантов выбрать хорду
    <[OA, AM] = <[OK, MK] хорда OM, точки: A, K -> <[AM, OA] = <[MK, OK]
    <[OA, AK] = <[OM, KM] хорда OK, точки: A, M
    <[OM, MA] = <[OK, AK] хорда OA, точки: M, K
    <[AO, OM] = <[AK, MK] хорда AM, точки: O, K
    <[AO, OK] = <[AM, KM] хорда AK, точки: O, M
    <[MA, AK] = <[MO, KO] хорда MK, точки: A, O
    """
    for predicate in Task.Instance().predicates.get('cyl', []):
        if len(predicate.lst) < 4: continue
        for quadPoints in itertools.combinations(predicate.lst, 4):
            for chordePoints in itertools.combinations(quadPoints, 2):
                O, M = chordePoints
                A, K = external.getUniqueElements(quadPoints, chordePoints)
                Simplifier.addLink(keyAngle=LinAngle(Line(O, A), Line(A, M)), valAngle=LinAngle(Line(O, K), Line(M, K)))


