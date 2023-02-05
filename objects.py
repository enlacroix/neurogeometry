from predicates.freepred import col


class Quadrangle:
    def __init__(self, *lst):
        self.lst = lst
        A, B, C, D = self.lst
        col(A, B).confirm()
        col(B, C).confirm()
        col(C, D).confirm()
        col(D, A).confirm()



class Parallelogram(Quadrangle):
    pass


class Circle:
    """
    Избыточность с предикатом cir (fixpred.py), тем не менее Circle будет выполнять свои функции.
    """
    pass


class InscribedCircle(Circle):
    pass
