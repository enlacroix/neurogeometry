import varbank as stm


class Predicate:
    def __init__(self, *points):

        self.lst = list(points)
        self.name = '(' + ','.join([str(t) for t in self.lst]) + ')'

    def __mul__(self, other):
        pass

    def __str__(self):
        return self.name

    def confirm(self):
        if self not in stm.predicates:
            stm.predicates.append(self)
            return 1
        return 0

    def __getitem__(self, item):
        return self.lst[item]

    def __setitem__(self, key, value):
        self.lst[key] = value

    def __bool__(self):
        return self in stm.predicates

