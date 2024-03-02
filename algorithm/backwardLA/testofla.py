from backwardLA.expression import Expression
from backwardLA.linangle import Linangle
from backwardLA.simplifier import Simplifier
from backwardLA.strategy import toLA, applyingLARules, LAReductor
from tskmanager import Task
from utils import newStringifyList
from ng_entities.entline import Line
from predicates.freepred import cyl
from predicates.quadpred import PRL, ORT, eql
from statement import reading_points

'''
R1(): u = v. Тогда найди список, в котором есть u и добавь туда v. Если такого списка нет, то создай [u, v]. 
здесь u и -u будут разными вершинами.
спорный случай 1: угол равняется некому коэффициенту умноженному на другой угол
ReductionWithCoefficients? 
спорный случай 2: угол равняется сумме нескольких углов. (причем эту сумму нельзя получить из декомпозиции)
'''

A, B, M, C, D = reading_points('A, B, M, C, D')
QUESTION = Linangle(Line(A, M), Line(A, C)), Linangle(Line(A, D), Line(A, C))
Line(A, B)
Line(B, D)
Line(B, M, C) # todo если его сместить ниже, чем confirm(), то они не поймут, что ВС = ВМС
PRL(Line(D, M), Line(A, C)).confirm()
PRL(Line(A, M), Line(B, C)).confirm()
ORT(Line(A, D), Line(B, C)).confirm()
eql(A, C, B, C).confirm()
cyl(A, B, C, D).confirm()


# applyingLARules()
# Expression.NReduction(toLA('[AB, AD]'), toLA('[R]'))
# Expression.trioFullReduction(toLA('[AM, DM]'), toLA('[AC, AM]'), toLA('[AC, DM]')),
# Expression.pairFullReduction(toLA('[AD, AM]'), toLA('[R]'))
# Expression.quadFullReduction(toLA('[AB, AD]'), toLA('[CD, BC]'), toLA('[AM, BD]'), toLA('[BD, BC]'))
LAReductor('[CD, BC]; [AB, AD]; [AM, BD]; [BD, BC]; [E]')
print(Task.Instance().getLAProof())