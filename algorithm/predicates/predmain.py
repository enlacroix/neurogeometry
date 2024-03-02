import config
from utils import toStrAllElems, logger, hum_list
import itertools as it
from tskmanager import Task

class GeneralizedPredicate: pass

class AbstractPredicate:
    @staticmethod
    def confirm(self):
        if self.ttl in Task.Instance().predicates:
            if self in Task.Instance().predicates[self.ttl]:
                return 0
            else:
                Task.Instance().predicates[self.ttl].append(self)
                self.numerize()
                return 1
        else:
            Task.Instance().predicates[self.ttl] = [self]
            return 1

    @staticmethod
    def bool(self):
        if self.ttl in Task.Instance().predicates:
            return self in Task.Instance().predicates[self.ttl]
        else:
            return False


def chaoticPrint(param):
     Task.Instance().to_print.append(param.capitalize())


class Predicate(GeneralizedPredicate):
    def __init__(self, *points):
        self.lst = tuple(points)
        self.ttl = self.__class__.__name__
        self.name = self.ttl + '(' + ', '.join(map(str, self.lst)) + ')'
        # self.bool = self in vb.task.predicates

    def __str__(self): return self.name

    def __hash__(self): return hash(self.name) # для lru_cache.

    def confirm(self): return AbstractPredicate.confirm(self)

    # def confirm(self):
    #     if self not in task.predicates:
    #         task.predicates.append(self)
    #         self.numerize()
    #         return 1
    #     return 0

    def totalConfirm(self, thname: str, descr: str, premises: list):
        if self.confirm():
            logger(f'{thname}: {", ".join(hum_list(premises))} => {self.humanize()}')
            if config.CHAOS_MOD: chaoticPrint(f'{thname}: {", ".join(hum_list(premises))} => {self.humanize()}')
            Task.DF().addString((thname, descr, premises, [Task.DF().getFactIndex(prem) for prem in premises], self))
            self.postConfirm()
            return 1
        return 0

    def __bool__(self):
        if self.ttl in Task.Instance().predicates: return self in Task.Instance().predicates[self.ttl]
        return False

    def transitive(self, other):
        """
        Абстрактный метод.
        :param other: other ТАКОГО же типа, что и self! В этом смысл именно операции транзитивности.
        :return:
        """
        pass

    def __getitem__(self, item):
        return self.lst[item]

    def __repr__(self): return self.name

    def numerize(self):
        """
        Абстрактный метод, который единожды добавляет в вычислительные матрицы уравнения, вытекающие из "алгебраического" смысла данного предиката.
        """
        pass

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

    def postConfirm(self):
        pass

    def humanize(self):
        pass

