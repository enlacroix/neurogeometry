from decoration.printer import add_string, find_fact
from predicates.predmain import Predicate
from predicates.quadpred import eql
from predicates.freepred import col
from entities import Line, Curve
import varbank as vb


class mdp(Predicate):
    def __init__(self, *points):
        super().__init__(*points)
        self.lst = points
        Z, X, Y = points
        self.ttl = 'mdp'
        self.sgm = [Z, Line(X, Y)]
        self.name = self.ttl + self.name
        self.bool = self in vb.task.predicates
        if self.bool:
            pred = eql(X, Z, Y, Z)
            if pred.confirm():
                # 'Правило', 'Описание', 'Предпосылки', 'Указатели на предпосылки', 'Факт'
                add_string(['Свойство середины', 'точка делит отрезок пополам', [self], [find_fact(self)], pred])
            col(Z, X, Y).confirm()

    def __eq__(self, other):
        return isinstance(other, mdp) and set(self.sgm) == set(other.sgm)

    def __hash__(self):
        return hash(self.name)

    def humanize(self):
        return f'{self.sgm[0]} - середина отрезка {self.sgm[1]}'

    def __mul__(self, other):
        return 0


class cir(Predicate):  # Это предикат Вот в чем вопрос.
    def __init__(self, *lst):
        super().__init__(*lst)
        self.ttl = 'cir'
        self.name = self.ttl + self.name
        self.sgm = [lst[0], Curve(*lst[1:])]
        self.bool = self in vb.task.predicates
        if self.bool: # можно сделать и через вызов метода confirm
            points_on_the_circle = self.lst[1:]
            center = self.lst[0]
            for i in range(len(points_on_the_circle) - 1):
                pred = eql(center, points_on_the_circle[i], center, points_on_the_circle[i + 1])
                if pred.confirm():
                    # 'Правило', 'Описание', 'Предпосылки', 'Указатели на предпосылки', 'Факт'
                    add_string(['свойство радиусов одной окружности', 'это радиусы одной окружности', [self], [find_fact(self)], pred])



    def __eq__(self, other):
        return isinstance(other, type(self)) and set(self.sgm) == set(other.sgm)

    def humanize(self):
        return f'Окружность с центром в точке {self.sgm[0]}, содержащая точки {self.sgm[1]}'
