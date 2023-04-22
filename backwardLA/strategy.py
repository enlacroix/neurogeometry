import itertools
import networkx as nx
import external
from backwardLA.expression import Expression, SubstEdge
from backwardLA.linangle import LinAngle
from backwardLA.ruleset import R1, R2, R3, R4
from backwardLA.simplifier import Simplifier
from external import toStrDictKeys, stringifyDict
from ng_entities.entline import Line
from predicates.freepred import cyl
from predicates.quadpred import PRL, ORT, eql, prl
from statement import reading_points
from tskmanager import Task
import matplotlib.pyplot as plt

A, B, M, C, D = reading_points('A, B, M, C, D')
QUESTION = LinAngle(Line(A, M), Line(A, C)), LinAngle(Line(A, D), Line(A, C))
Line(A, B)
Line(A, C)
Line(B, D)
Line(B, M, C) # todo если его сместить ниже, чем confirm(), то они не поймут, что ВС = ВМС
PRL(Line(D, M), Line(A, C)).confirm()
PRL(Line(A, M), Line(B, C)).confirm()
ORT(Line(A, D), Line(B, C)).confirm()
eql(A, C, B, C).confirm()
cyl(A, B, C, D).confirm()

Simplifier.makeSubstitutionDict()
# print(stringifyDict(Task.Instance().predicates))

laList = [LinAngle(*comb) for comb in itertools.combinations(Task.Instance().lines, 2)]
RULESET = [R1, R2]
for r, angle in itertools.product(RULESET, laList): r(angle)
R3()
R4()
# каждый раз создаем Expression с новым списком аргументов и применяем редукцию/декомп

print(stringifyDict(Simplifier.substitutionDict))


'''
при запросе к словарю по ключу ∠[u, v], но есть ключ ∠[v, u], то верни список для имеющегося просто для каждого элемента списка примени операцию -. 
"применить одно правило в стеке" - это значить запомнить пару ключ-конкретное значение из списка (не сам список, он олицетворяет все теоремы,
применимые к углу). 
'''
'''
la1: [la2, la4], la2: [la3, la4]
В результате перебор сводится к декартовому произведению (перебору всевозможных комбинаций подстановок) и применению редукции.
Потом в игру вступает декомпозиция. 
'''