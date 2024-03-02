import itertools
from backwardLA.linangle import Linangle, NeutralLA, RightLA
from backwardLA.simplifier import Simplifier
from ng_entities.entline import Line
from predicates.quadpred import PRL, ORT
from tskmanager import Task
from utils import getUniqueElements, FindCommonFindUnique


def R1(angle: Linangle):
    """
    R1. ∠[u, v] -> ∠[u, m], если v ∥ m. ∀ u ∈ Task.lines.
    ∠[v, u] = ∠[m, u] (причем заменить можно в обе стороны). Таким образом, такое частное правило обеспечивает 4 замены.
    Цель: сформировать список углов, которым равен ∠[u, v] (и ∠[v, u] одновременно). добавить в substitution-словарь.
    """
    if PRL(angle.x, angle.y):
        Simplifier.addValue(angle, NeutralLA(angle.x))
        return
    for m in Task.Instance().lines:
        if PRL(angle.y, m): Simplifier.addValue(angle, Linangle(angle.x, m))
        if PRL(angle.x, m): Simplifier.addValue(angle, Linangle(m, angle.y))

def R2(angle: Linangle):
    """
    ORT(u, v) -> ∠[u, v] = [R]
    """
    if ORT(angle.x, angle.y): Simplifier.addValue(angle, RightLA(angle.x, angle.y))

def R3():
    """
    C - вершина р/б треугольника.
    eql(A, C, B, C) => ∠[AB, BC] = ∠[AC, AB] - р/б треугольник.
    ∠[АВ, AC] = ∠[BC, АВ] - аналогично, если переменить местами точки А и В.
    """
    for eqlPredicate in Task.Instance().predicates.get('eql', []):
        commonPoint, uniquePoints = FindCommonFindUnique(eqlPredicate.sgm[0].lst, eqlPredicate.sgm[1].lst)
        if not commonPoint: continue
        C = commonPoint
        A, B = uniquePoints
        Simplifier.addValue(Linangle(Line(A, B), Line(B, C)), Linangle(Line(A, C), Line(A, B)))
        Simplifier.addValue(Linangle(Line(A, C), Line(A, B)), Linangle(Line(A, B), Line(B, C)))

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
                A, K = getUniqueElements(quadPoints, chordePoints)
                Simplifier.addValue(Linangle(Line(O, A), Line(A, M)), Linangle(Line(O, K), Line(M, K)))


