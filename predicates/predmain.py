import varbank as vb
import itertools as it


class Predicate:
    def __init__(self, *points):
        self.lst = list(points)
        self.name = '(' + ','.join([str(t) for t in self.lst]) + ')'
        #self.bool = self in vb.task.predicates

    def __str__(self):
        return self.name

    def confirm(self):
        if self not in vb.task.predicates:
            vb.task.predicates.append(self)
            self.numerize()
            return 1
        return 0

    def transitive(self, other):
        """
        Абстрактный метод.
        :param other: other ТАКОГО же типа, что и self! В этом смысл именно операции транзитивности.
        :return:
        """
        pass

    def __getitem__(self, item):
        return self.lst[item]

    def __setitem__(self, key, value):
        self.lst[key] = value

    def numerize(self):
        """
        Абстрактный метод, который единожды добавляет в вычислительные матрицы уравнения, которые вытекают из "алгебраического" смысла данного предиката.
        :return:
        """
        pass

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
