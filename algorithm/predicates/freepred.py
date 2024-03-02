from predicates.predmain import Predicate
from tskmanager import Task
from utils import stringifyList


def chaosBool(lst, flg):
    """
    :param lst: аргументы предиката.
    :param flg: col/cyl - просто объединили две функции в одну.
    :return:
    """
    if flg == 'col':
        assert len(lst) == len(set(lst)), f'Не соблюдена уникальность для точек col {stringifyList(lst)}, {len(lst), len(set(lst))}'
        for line in Task.Instance().lines + Task.Instance().segments:
            if all([x in line for x in lst]):
                return True
        return False
    if flg == 'cyl':
        for line in Task.Instance().curves:
            if all([x in line for x in lst]):
                return True
        return False


class col(Predicate):
    def __init__(self, *lst):
        super().__init__(*lst)

    def __hash__(self): return hash(self.name)  # для lru_cache.

    def __bool__(self):
        """
        Логика col(). 1) если в предикатах существует такой
        """

        return self in Task.Instance().predicates.get(self.ttl, ()) or chaosBool(self.lst, self.ttl)

    def __eq__(self, other):
        return isinstance(other, col) and set(self.lst) == set(other.lst)

    def humanize(self):
        return f'Точки {self.name[4:-1]} лежат на одной прямой.'




class cyl(Predicate):
    def __init__(self, *lst):
        super().__init__(*lst)


    def __bool__(self): return chaosBool(self.lst, self.ttl)

    def __eq__(self, other):
        return isinstance(other, col) and set(self.lst) == set(other.lst)

    def humanize(self):
        return f'Точки {self.name[4:-1]} лежат на одной окружности.'

