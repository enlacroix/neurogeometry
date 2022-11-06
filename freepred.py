from predmain import Predicate
from entities import lines, circ_lines, Line, CircleLine
import statement as stm

def chaos_bool(lst, flg):
    if flg == 'col':
        if lst[0] == lst[1]:  # col (X, X) будет считаться False
            return False
        for line in lines:
            if all([x in line for x in lst]):
                return True
        return False
    if flg == 'cyl':
        for line in circ_lines:
            if all([x in line for x in lst]):
                return True
        return False


class col(Predicate):
    def __init__(self, *lst):
        super().__init__(*lst)
        self.ttl = 'col'
        self.name = self.ttl + '(' + ','.join(sorted([str(t) for t in self.lst])) + ')'
        self.bool = chaos_bool(self.lst, self.ttl)

    def __bool__(self):
        return chaos_bool(self.lst, self.ttl)

    def confirm(self):
        if self not in stm.predicates:
            stm.predicates.append(self)
            lines.append(Line(*self.lst))
            return 1
        return 0

    def __eq__(self, other):
        return isinstance(other, col) and set(self.lst) == set(other.lst)

    def humanize(self):
        return f'Точки {self.name[4:]} лежат на одной прямой.'


class cyl(col):
    def __init__(self, *lst):
        super().__init__(*lst)
        self.ttl = 'cyl'
        self.bool = chaos_bool(self.lst, self.ttl)

    def __bool__(self):
        return chaos_bool(self.lst, self.ttl)

    def confirm(self):
        if self not in stm.predicates:
            stm.predicates.append(self)
            circ_lines.append(CircleLine(*self.lst))
            return 1
        return 0

    def humanize(self):
        return f'Точки {self.name[4:]} лежат на одной прямой.'