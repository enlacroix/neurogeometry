import varbank as vb
from external import stringify_list, str_list, logger


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
        self.name = ''.join(sorted([p.n for p in self.lst]))
        if self.lst[0] != self.lst[1] and self not in vb.task.lines:
            vb.task.lines.append(self)
            if len(self.lst) == 2 and self not in vb.task.segments:
                vb.task.segments.append(self)

    def get_ind(self):
        try:
            return vb.task.segments.index(self)
        except IndexError:
            logger(f'Попытка получить несуществующий индекс отрезка {self}!')
            return

    def get_value(self):
        try:
            return vb.task.segment_dict[self]
        except KeyError:
            logger(f'Был проинициализирован отрезок {self} пустым значением!')
            vb.task.segment_dict[self] = None
            return

    def __str__(self):
        return ''.join(self.name)

    def humanize(self):
        return 'пр. ' + str(self)

    def __eq__(self, other):
        return set(self.lst) == set(other.lst)

    def angle_between(self, other):
        """
        TODO перенести в отрезки.
        Метод принимает два отрезка (т.е. ровно две точки с ровно одним совпадающей точкой в названии), который возвращает объект
        угла между ними.
        """
        eps = set(self.lst)
        phi = set(other.lst)
        if len(list(eps & phi)) == 1:
            return Angle(list(eps - phi)[0], list(eps & phi)[0], list(eps & phi)[0], list(phi - eps)[0])
        else:
            return False

    def __contains__(self, item):
        return item in self.lst

    def is_reachable(self):
        """
        return: или True (RC = 0) или значение RC (RC > 0).
        """
        if self.get_value():
            return True
        else:
            pass

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


class Segment:
    """
    класс, предназначенный для нумерикал модуля. У Segment уже есть понятие о длине.
    """
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
        if len(list(eps & phi)) == 1:
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
            return

    def is_reachable(self):
        """
        Достижимо ли значение угла (как пример). Пояснение: если мы знаем его величину из словаря, то она очевидно достижима.
        Иначе, если мы знаем значение тригонометрической функции, то через 1 действие мы можем найти этот угол.
        Коэффициент достижимости (Reachable Coefficient, далее RC) равен 1.
        return: или True (RC = 0) или значение RC (RC > 0).
        """
        if self.get_value():
            return True
        else:
            pass


class Ratio:
    """
    Отношение между двумя величинами (отрезки/углы/площади). Применяются в теоремах про подобные треугольники.
    """
    pass
