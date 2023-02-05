from predicates.predmain import Predicate
import varbank as vb
from entities import Line, Curve, Point


def chaos_bool(lst, flg):
    """
    :param lst: аргументы предиката.
    :param flg: col/cyl - просто объединили две функции в одну.
    :return:
    """
    if flg == 'col':
        if lst[0] == lst[1]:  # col (X, X) будет считаться False
            return False
        for line in vb.task.lines:
            if all([x in line for x in lst]):
                return True
        return False
    if flg == 'cyl':
        for line in vb.task.curves:
            if all([x in line for x in lst]):
                return True
        return False


class col(Predicate):
    def __init__(self, *lst):
        super().__init__(*lst)
        self.ttl = 'col'
        self.name = self.ttl + '(' + ','.join(sorted([str(t) for t in self.lst])) + ')'
        self.bool = chaos_bool(self.lst, self.ttl)
        self.ln = Line(*lst)
        if self.ln not in vb.task.lines:
            vb.task.lines.append(self.ln)

    def __bool__(self):
        return chaos_bool(self.lst, self.ttl)

    def __eq__(self, other):
        return isinstance(other, col) and set(self.lst) == set(other.lst)

    def humanize(self):
        return f'Точки {self.name[4:-1]} лежат на одной прямой.'

    # def transitive(self, other):
    #     """
    #     Метод, обеспечивающий корректную работу предиката col(), который обобщает правило о:
    #     col(A, B, D) ^ col(C, B, D) = col(A, C) or col(A, C, B, D)
    #     :param other: другой объект класса col.
    #     :return: None, если у прямых нет точек пересечения (о которых знает программа); точку пересечения, если прямые действ разные и пересеклись;
    #     Если точек пересечения больше двух, то эти прямые принадлежат одной единой прямой, которая и добавляется в массив lines.
    #     """
    #     eps = set(self.lst)
    #     phi = set(other.lst)
    #     if len(eps & phi) > 1:
    #         try:
    #             vb.task.lines.remove(self.ln)
    #         except ValueError:
    #             pass
    #         try:
    #             vb.task.lines.remove(other.ln)
    #         except ValueError:
    #             pass
    #         # TODO Откровенная чушь. Пусть пока повисит. Это опасно, поскольку неизвестно, как lines будет применяться для вычислительного модуля.
    #         # Удаление может нарушить порядок индексов, если проявить халатность с segments/lines.
    #         Line(*list(eps | phi))  # Всякий раз, когда мы инициализируем линию, то она УЖЕ добавляется в список.
    #         return 0
    #     elif len(eps & phi) == 1:
    #         return Point(str(*list(eps & phi)))  # Единственная точка пересечения двух прямых


class cyl(Predicate):
    def __init__(self, *lst):
        super().__init__(*lst)
        self.ttl = 'cyl'
        self.name = self.ttl + '(' + ','.join(sorted([str(t) for t in self.lst])) + ')'
        self.bool = chaos_bool(self.lst, self.ttl)
        self.ln = Curve(*lst)
        if self.ln not in vb.task.curves:
            vb.task.curves.append(self.ln)

    def __bool__(self):
        return chaos_bool(self.lst, self.ttl)

    def __eq__(self, other):
        return isinstance(other, col) and set(self.lst) == set(other.lst)

    def humanize(self):
        return f'Точки {self.name[4:-1]} лежат на одной окружности.'

    # def transitive(self, other):
    #     """
    #     см. col
    #     """
    #     eps = set(self.lst)
    #     phi = set(other.lst)
    #     if len(eps & phi) > 1:
    #         vb.task.lines.remove(self.ln)
    #         vb.task.lines.remove(other.ln)
    #         Curve(*list(eps | phi))  # Всякий раз, когда мы инициализируем линию, то она УЖЕ добавляется в список.
    #         return 0
    #     elif len(eps & phi) == 1:
    #         return Point(str(*list(eps & phi)))