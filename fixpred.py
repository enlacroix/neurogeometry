from predmain import Predicate
from extmethods import seg_index
from quadpred import eql
from freepred import col
from entities import Line, RLM, CircleLine
import statement as stm

class mdp(Predicate):  # должен добавлять предикат eql о равенстве отрезков
    def __init__(self, *points):
        super().__init__(*points)
        self.lst = points
        Z, X, Y = points
        self.ttl = 'mdp'
        self.sgm = [Z, Line(X, Y)]
        self.name = self.ttl + self.name
        self.bool = self in stm.predicates
        if self.bool:
            eql(X, Z, Y, Z).confirm()
            col(Z, X, Y).confirm()

    def __eq__(self, other):
        return isinstance(other, mdp) and set(self.sgm) == set(other.sgm)

    def count(self):
        Z, X, Y = self.lst
        a = seg_index(X, Y)
        b = seg_index(Y, Z)
        c = seg_index(X, Z)
        if a is not None and b is not None and c is not None and self.bool:
            RLM[a][b] = 2
            RLM[a][c] = 2
            RLM[b][a] = 1 / 2  # RLM[i][j] = 1 / RLM [j][i], where i != j.
            RLM[c][a] = 1 / 2

    def __hash__(self):
        return hash(self.name)

    def humanize(self):
        return f'{self.sgm[0]} - середина отрезка {self.sgm[1]}'

    def __mul__(self, other):
        return 0



class cir(Predicate):  # Это предикат или элемент чертежа? Вот в чем вопрос.
    def __init__(self, *lst):
        super().__init__(*lst)
        self.ttl = 'cir'
        self.name = self.ttl + self.name
        self.sgm = [lst[0], CircleLine(*lst[1:])]
        self.bool = self in stm.predicates

    def __eq__(self, other):
        return isinstance(other, type(self)) and set(self.sgm) == set(other.sgm)

    def humanize(self):
        return f'Окружность с центром в точке {self.sgm[0]}, содержащая точки {self.sgm[1]}'