import varbank as vb
from external import stringify_list, str_list
from numerical.functors import Sum


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
        if len(eps & phi) > 1:
            vb.task.lines.remove(self)
            vb.task.lines.remove(other)
            # TODO опасное удаление self и other, поскольку они уже не несут полезной информации.
            # Это закомментировано, поскольку неизвестно, как lines будет применяться для вычислительного модуля.
            # Удаление может нарушить порядок индексов.
            Line(*list(eps | phi))  # Всякий раз, когда мы инициализируем линию, то она УЖЕ добавляется в список.
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

    # def numerical(self):
    #     vb.task.angle_dict[self] = None

    def humanize(self):
        eps = set(self.sgm[0].lst)
        phi = set(self.sgm[1].lst)
        if len(list(eps & phi)) > 0:
            a = list(eps - phi)[0]
            b = list(eps & phi)[0]
            c = list(phi - eps)[0]
            return '∠' + a.n + b.n + c.n
        else:
            return self.name

    def __str__(self):
        return self.name

    def get_ind(self):
        return vb.task.angles.index(self)

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        # hash(self.lst[0]) ^ hash(self.lst[1]) ^ hash(self.lst[2]) ^ hash(self.lst[3])
        return hash(self.sgm[0]) ^ hash(self.sgm[1])

    def get_value(self):
        try:
            return vb.task.angle_dict[self]
        except KeyError:
            print(f'Величина угла {self.humanize()} неизвестна!')
            vb.task.angle_dict[self] = None
            return None


class Triangle:
    def __init__(self, *lst):
        self.lst = lst
        X, Y, Z = self.lst
        self.segments = [Line(X, Y), Line(X, Z), Line(Y, Z)]
        self.angles = [Angle(X, Y, X, Z), Angle(X, Z, Y, Z), Angle(Y, Z, Y, X)]
        Sum(self.angles, 180)
        self.name = f'Треугольник {X.n + Y.n + Z.n}'
        # TODO Инициализация col от Line. Вызывает циркулярный импорт. Поправить, иначе смысла в Triangle немного
        # col(X, Y).confirm()
        # col(X, Z).confirm()
        # col(Z, Y).confirm()

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.segments[0]) ^ hash(self.segments[1]) ^ hash(self.segments[2])

    def __eq__(self, other):
        return set(self.lst) == set(other.lst)  # set(self.sgm) == set(other.sgm)


class Ratio:
    pass
