from decoration.printer import add_string, find_fact
from predicates.predmain import Predicate
from entities import Line
import varbank as vb


class ort(Predicate):
    def __init__(self, *points):
        super().__init__(*points)
        X, Y, Z, W = self.lst
        self.sgm = [Line(X, Y), Line(Z, W)]
        self.ttl = 'ort'
        self.name = self.ttl + self.name
        self.bool = self in vb.task.predicates  # TODO ?не перемещай его в родительский класс, он не знает, что такое sgm на этапе вызова родительского конструктора.

    # он котролирует будет ли добавляться в чистые предикаты, т.е. влияет на in
    def __eq__(self, other):
        return isinstance(other, ort) and set(self.sgm) == set(other.sgm)  # type(self) вместо ort

    # TODO ort должен добавлять в вычисл матрицу информацию о том, что угол между прямыми равен 90 градусам.

    # def count(self):  # Метод count работает с матрицами отношений, которые не нужны для доказательств.
    #     X, Y, Z, W = self.lst
    #     a = seg_index(X, Y)
    #     b = seg_index(Z, W)
    #     if a is not None and b is not None and self.bool:
    #         alpha = 90
    #         RAM[a][b] = alpha  # Это симметричная матрица с нулями на главной диагонали (хотя? по поводу нулей).
    #         RAM[b][
    #             a] = 180 - alpha  # Отрицательный угол означает, что мы замерили его в другом направлении. На самом деле эти углы смежные, т.е. RAM[a][b] + RAM[b][a] = 180

    def transitive(self, other):
        if isinstance(other, type(self)):
            eps = set(self.sgm)
            phi = set(other.sgm)
            pnt = []
            if len(list(eps & phi)) > 0:
                for e in list(eps ^ phi):
                    pnt += e.lst
                if prl(*pnt).confirm():
                    add_string(['правило трёх прямых',
                                            f'две прямые {list(eps ^ phi)[0]}, {list(eps ^ phi)[1]} ортогональные {list(eps & phi)[0]} - параллельны между собой.',
                                            None, None, prl(*pnt)])
                return 1
        else:
            return 0

    def humanize(self):
        return f'{self.sgm[0]}⟂{self.sgm[1]}'


class prl(Predicate):  # Четыре точки, первые две и последние две из них обозначают прямые, которые параллельны.
    def __init__(self, *points):
        super().__init__(*points)
        self.ttl = 'prl'
        X, Y, Z, W = self.lst
        self.sgm = [Line(X, Y), Line(Z, W)]
        self.name = self.ttl + self.name
        self.bool = self in vb.task.predicates

    def __eq__(self, other):
        return isinstance(other, prl) and set(self.sgm) == set(other.sgm)

    def transitive(self, other):
        """
        а) a || b, c || b => a || c
        """
        if isinstance(other, type(self)):
            eps = set(self.sgm)
            phi = set(other.sgm)
            pnt = []
            if len(list(eps & phi)) > 0:
                for e in list(eps ^ phi):
                    pnt += e.lst
                if prl(*pnt).confirm():
                    add_string(['правило транзитивности',
                                f'две прямые {list(eps ^ phi)[0]}, {list(eps ^ phi)[1]} параллельные {list(eps & phi)[0]} - параллельны между собой.',
                                [self, other], [find_fact(self), find_fact(other)],
                                prl(*pnt)])
                return 1
        else:
            return 0

    def humanize(self):
        return f'{self.sgm[0]}∥{self.sgm[1]}'


class eql(Predicate):  # Или отедльным предикатом-класс для равных уже отрезков?
    def __init__(self, *points):
        super().__init__(*points)
        X, Y, Z, W = self.lst
        self.ttl = 'eql'
        self.sgm = [Line(X, Y), Line(Z, W)]
        self.name = self.ttl + self.name
        self.bool = self in vb.task.predicates

    def __eq__(self, other):
        return isinstance(other, eql) and set(self.sgm) == set(other.sgm)

    # TODO eql должен добавлять уравнения о равенстве отрезков между собой.

    def transitive(self, other):
        if isinstance(other, type(self)):
            eps = set(self.sgm)
            phi = set(other.sgm)
            pnt = []
            if len(list(eps & phi)) > 0:  # Нужна ли проверка на истинность? (см. eqa)
                for e in list(eps ^ phi):
                    pnt += e.lst
                if eql(*pnt).confirm():
                    # 'Правило', 'Описание', 'Предпосылки', 'Указатели на предпосылки', 'Факт'
                    add_string(['Транзитивность для отрезков', f'два отрезка {list(eps ^ phi)[0]}, {list(eps ^ phi)[1]} равные с {list(eps & phi)[0]} - равны между собой.',
                                [self, other], [find_fact(self), find_fact(other)],
                                eql(*pnt)])
                return 1
        else:
            return 0

    def humanize(self):
        return f'{self.sgm[0]}={self.sgm[1]}'
