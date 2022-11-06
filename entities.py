import numpy as np

circ_lines = []  # Массив "прямых", но только точек, принадлежащих одной окружности.
lines = []  # Массив прямых (произвольное число точек)
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

    def __str__(self):
        name = ''
        for p in self.lst:
            if p is not None:
                name += p.n
        return ''.join(sorted(name))

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
        if len(eps & phi) > 1 and Line(*list(eps | phi)) not in lines:
            # lines.remove()
            lines.append(Line(*list(eps | phi)))
            return 0
        elif len(eps & phi) == 1:
            return Point(str(*list(eps & phi)))  # Единственная точка пересечения двух прямых


class CircleLine(Line):
    global circ_lines

    def __init__(self, *lst):
        super().__init__(*lst)

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
            circ_lines.append(CircleLine(*list(eps | phi)))
            return 0

            # Некоторые проблемы с хэшем, потому что родитель обрабатывает только первые две точки


class Angle:
    def __init__(self, *lst):
        self.lst = lst
        A, B, C, D = self.lst
        self.sgm = [Line(A, B), Line(C, D)]
        self.name = '∠[' + str(Line(A, B)) + ', ' + str(Line(C, D)) + ']'

    def __eq__(self, other):
        return isinstance(other, type(self)) and set(self.sgm) == set(other.sgm)

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.sgm[0]) ^ hash(self.sgm[1])

    # hash(self.lst[0]) ^ hash(self.lst[1]) ^ hash(self.lst[2]) ^ hash(self.lst[3])

    def value(self):
        pass
        # return 180 -


class Triangle:
    def __init__(self, *lst):
        self.lst = lst
        X, Y, Z = self.lst
        self.sgm = [Line(X, Y), Line(X, Z), Line(Y, Z)]
        self.name = f'Треугольник {X.n + Y.n + Z.n}'

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return set(self.lst) == set(other.lst)  # set(self.sgm) == set(other.sgm)
