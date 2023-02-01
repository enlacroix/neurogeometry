import numpy as np
import varbank as vb
#from numerical import Sum


class Point:
    def __init__(self, name):
        self.n = name
        # TODO может быть из этого сделать множество? чтобы не проверять на отсуствие элемента каждый раз
        if self not in vb.task.points:
            vb.task.points.append(self)

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
        if self not in vb.task.lines:
            vb.task.lines.append(self)

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

    # def length(self):
    #     # Length будет хранить всевозможные значения длины, выраженные через другие, а диагональный элемент хранит детерминированное значение длины.
    #     # Пока мы не убедимся, что, например, possible состоит из одного детерм. элемента, мы не добавим на диаг элемент с помощью ф-ции Measure.
    #     i = seg.index(str(self))
    #     if RLM[i][i] != 0:
    #         return RLM[i][i]
    #     else:
    #         possible = []
    #         for j, p in enumerate(RLM[i]):
    #             if p != 0 and RLM[j][j] != 0:  # целуемся с первым встречным и ретуреним. 1 может быть раньше 1/2
    #                 possible.append(RLM[i][j] * RLM[j][j])
    #         return possible

    def intersect(self, other):
        """
        Метод, обеспечивающий корректную работу предиката col(), который обобщает правило о:
        col(A, B, D) ^ col(C, B, D) = col(A, C) or col(A, C, B, D)
        :param other: другой объект класса Line.
        :return: None, если у прямых нет точек пересечения (о которых знает программа); точку пересечения, если прямые действ разные и пересеклись;
        Если точек пересечения больше двух, то эти прямые принадлежат одной единой прямой, которая и добавляется в массив lines.
        """
        eps = set(self.lst)
        phi = set(other.lst)
        if len(eps & phi) > 1 and Line(*list(eps | phi)) not in vb.task.lines:
            vb.task.lines.remove(self)
            vb.task.lines.remove(other)
            # TODO убрать self и other, поскольку они уже не несут полезной информации.
            # Это закомментировано, поскольку неизвестно, как lines будет применяться для вычислительного модуля.
            # Удаление может нарушить порядок индексов.
            vb.task.lines.append(Line(*list(eps | phi)))
            return 0
        elif len(eps & phi) == 1:
            return Point(str(*list(eps & phi)))  # Единственная точка пересечения двух прямых


class Segment(Line):
    '''
    класс, предназначенный для нумерикал модуля. У Segment уже есть понятие о длине.
    '''
    pass


class Curve(Line):

    def __init__(self, *lst):
        self.lst = lst
        if self not in vb.task.curves:
            vb.task.curves.append(self)

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
            vb.task.curves.append(Curve(*list(eps | phi)))
            return 0

            # Некоторые проблемы с хэшем, потому что родитель обрабатывает только первые две точки





class Angle:
    def __init__(self, *lst):
        self.lst = lst
        A, B, C, D = self.lst
        self.sgm = [Line(A, B), Line(C, D)]
        self.name = '∠[' + str(Line(A, B)) + ', ' + str(Line(C, D)) + ']'
        if self not in vb.task.angles:
            vb.task.angles.append(self)

    def __eq__(self, other):
        return isinstance(other, type(self)) and set(self.sgm) == set(other.sgm)

    def numerical(self):
        vb.task.angle_dict[self] = None

    def __str__(self):
        return self.name

    def get_ind(self):
        return vb.task.angles.index(self)

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        # hash(self.lst[0]) ^ hash(self.lst[1]) ^ hash(self.lst[2]) ^ hash(self.lst[3])
        return hash(self.sgm[0]) ^ hash(self.sgm[1])

    def set_value(self, value):

        vb.task.angle_dict[self] = value
        blank = [0] * vb.N_
        blank[self.get_ind()] = 1
        # vb.AEV[vb.AEM.shape[0]][0] = value
        vb.task.AEV = np.vstack([vb.task.AEV, np.array([value])])
        vb.task.AEM = np.vstack([vb.task.AEM, np.array(blank)])

    def get_value(self):
        try:
            return vb.task.angle_dict[self]
        except KeyError:
            print('Запрошенный угол не был создан.')


class Triangle:
    def __init__(self, *lst):
        self.lst = lst
        X, Y, Z = self.lst
        self.segments = [Line(X, Y), Line(X, Z), Line(Y, Z)]
        self.angles = [Angle(Y, Z, Y, X), Angle(X, Y, X, Z), Angle(X, Z, Y, Z)]
        #Sum(self.angles, 180)
        self.name = f'треугольник {X.n + Y.n + Z.n}'

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return set(self.lst) == set(other.lst)  # set(self.sgm) == set(other.sgm)
