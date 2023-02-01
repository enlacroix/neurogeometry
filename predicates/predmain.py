import varbank as vb
import itertools as it


class Predicate:
    def __init__(self, *points):
        self.lst = list(points)
        self.name = '(' + ','.join([str(t) for t in self.lst]) + ')'
        #self.bool = self in vb.task.predicates

    def __mul__(self, other):
        pass

    def __str__(self):
        return self.name

    def confirm(self):
        if self not in vb.task.predicates:
            vb.task.predicates.append(self)
            return 1
        return 0

    def __getitem__(self, item):
        return self.lst[item]

    def __setitem__(self, key, value):
        self.lst[key] = value

    def __bool__(self):
        return self in vb.task.predicates

    def synonyms(self):
        # Добавить set() к функции synonyms?
        """
        Переставляет аргументы предиката (точки) так, чтобы результат был равен исходному предикату.
        Они называются синонимичными друг другу.
        :param self: предикат.
        :return: список предикатов, удовлетворяющих данному условию.
        Пример: mdp(M, A, B) == mdp(M, B, A) != mdp(A, M, B)
        """
        return [self.__class__(*y) for y in it.permutations(self.lst) if self.__class__(*y) == self]
