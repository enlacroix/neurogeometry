import numpy as np
import predicates.freepred
import varbank as vb
from numerical import Sum

seg = []  # Массив отрезков (только две точки)
RLM = np.zeros((len(seg), len(seg)))
# relation_length_matrix. Возможно стоит поставить 100 на 100, чтобы не париться с IndexError.
RAM = np.zeros((len(seg), len(seg)))
pure_points = []
processed = []

class Point:
    def __init__(self, name):
        self.n = name

    def __str__(self):
        return self.n

    def __hash__(self):
        return hash(self.n)

    def __eq__(self, other):
        return self.n == other.n  # hash для опти?

    def __ne__(self, other):
        return not self.n == other.n

class Line:
    def __init__(self, *lst):
        self.lst = lst
        self.value = None
        vb.lines.append(self)
        predicates.freepred.col(*lst).confirm()
        if len(lst) == 2:
            vb.segments[self] = None

    def __str__(self):
        name = ''
        for p in self.lst:
            if p is not None:
                name += p.n
        return ''.join(sorted(name))

    def set_value(self, value):
        for key in vb.segments.keys():
            if key == self:
                vb.segments[key] = value

    def __eq__(self, other):
        return set(self.lst) == set(other.lst)

    def __contains__(self, item):
        return item in self.lst

    def __hash__(self):
        return hash(self.lst[0]) ^ hash(self.lst[1])
        # Line теперь не только из двух точек, но она применяется только при двухточечных Line при сравнении предикатов. Так что все нормально?

    def length(self):
        # Length будет хранить всевозможные значения длины, выраженные через другие, а диагональный элемент хранит детерминированное значение длины.
        # Пока мы не убедимся, что, например, possible состоит из одного детерм. элемента, мы не добавим на диаг элемент с помощью ф-ции Measure.
        i = seg.index(str(self))
        if RLM[i][i] != 0:
            return RLM[i][i]
        else:
            possible = []
            for j, p in enumerate(RLM[i]):
                if p != 0 and RLM[j][j] != 0:  # сосемся с первым встречным и ретуреним. 1 может быть раньше 1/2
                    possible.append(RLM[i][j] * RLM[j][j])
            return possible

    def intersect(self, other):
        eps = set(self.lst)
        phi = set(other.lst)
        if len(eps & phi) > 1 and Line(*list(eps | phi)) not in vb.lines:
            # lines.remove()
            vb.lines.append(Line(*list(eps | phi)))
            return 0
        elif len(eps & phi) == 1:
            return Point(str(*list(eps & phi)))  # Единственная точка пересечения двух прямых


class CircleLine(Line):

    def __init__(self, *lst):
        vb.circ_lines.append(CircleLine(*lst))

    def __hash__(self):
        res = hash(self.lst[0])
        for i in range(2, len(self.lst)):
            res = res ^ hash(self.lst[i])
        return res

    def intersect(self, other):
        eps = set(self.lst)
        phi = set(other.lst)
        if len(eps & phi) > 2:
            # lines.remove()
            vb.circ_lines.append(CircleLine(*list(eps | phi)))
            return 0

            # Некоторые проблемы с хэшем, потому что родитель обрабатывает только первые две точки


class Angle:
    def __init__(self, *lst):
        self.lst = lst
        A, B, C, D = self.lst
        self.sgm = [Line(A, B), Line(C, D)]
        self.name = '∠[' + str(Line(A, B)) + ', ' + str(Line(C, D)) + ']'
        if self not in vb.angle_list:
            vb.angle_list.append(self)

    def __eq__(self, other):
        return isinstance(other, type(self)) and set(self.sgm) == set(other.sgm)

    def numerical(self):
        vb.angles[self] = None

    def __str__(self):
        return self.name

    def get_ind(self):
        return vb.angle_list.index(self)

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        # hash(self.lst[0]) ^ hash(self.lst[1]) ^ hash(self.lst[2]) ^ hash(self.lst[3])
        return hash(self.sgm[0]) ^ hash(self.sgm[1])

    def set_value(self, value):
        vb.angles[self] = value
        blank = [0] * vb.N
        blank[self.get_ind()] = 1
        # vb.AEV[vb.AEM.shape[0]][0] = value
        vb.AEV = np.vstack([vb.AEV, np.array([value])])
        vb.AEM = np.vstack([vb.AEM, np.array(blank)])

    def get_value(self):
        try:
            return vb.angles[self]
        except KeyError:
            print('Запрошенный угол не был создан.')





class Triangle:
    def __init__(self, *lst):
        self.lst = lst
        X, Y, Z = self.lst
        self.segments = [Line(X, Y), Line(X, Z), Line(Y, Z)]
        self.angles = [Angle(Y, Z, Y, X), Angle(X, Y, X, Z), Angle(X, Z, Y, Z)]
        Sum(self.angles, 180)
        self.name = f'треугольник {X.n + Y.n + Z.n}'

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return set(self.lst) == set(other.lst)  # set(self.sgm) == set(other.sgm)
