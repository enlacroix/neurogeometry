from predicates.predmain import Predicate
import varbank as vb
from entities import Line, Curve


def chaos_bool(lst, flg):
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
        ln = Line(*lst)
        if ln not in vb.task.lines:
            vb.task.lines.append(ln)

    def __bool__(self):
        return chaos_bool(self.lst, self.ttl)

    def __eq__(self, other):
        return isinstance(other, col) and set(self.lst) == set(other.lst)

    def humanize(self):
        return f'Точки {self.name[4:-1]} лежат на одной прямой.'


class cyl(Predicate):
    def __init__(self, *lst):
        super().__init__(*lst)
        self.ttl = 'cyl'
        self.name = self.ttl + '(' + ','.join(sorted([str(t) for t in self.lst])) + ')'
        self.bool = chaos_bool(self.lst, self.ttl)
        ln = Curve(*lst)
        if ln not in vb.task.curves:
            vb.task.curves.append(ln)

    def __bool__(self):
        return chaos_bool(self.lst, self.ttl)

    def __eq__(self, other):
        return isinstance(other, col) and set(self.lst) == set(other.lst)

    def humanize(self):
        return f'Точки {self.name[4:-1]} лежат на одной окружности.'