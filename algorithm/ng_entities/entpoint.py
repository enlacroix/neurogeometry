from tskmanager import Task


class Point:
    """
    Класс Точка - атомарная единица нейрогеометрии, аргумент для предикатов, фигур и конструкций.
    Имеет простую структуру и единственный атрибут: имя. Мы придерживаемся подхода, что точки обозначаются
    одной заглавной латинской буквой.
    """
    def __init__(self, name: str):
        self.n = name
        if self not in Task.Instance().points: Task.Instance().points.append(self)

    def __str__(self): return self.n

    def __hash__(self): return hash(self.n)

    def __eq__(self, other): return self.n == other.n

    def __ne__(self, other): return not self.n == other.n
