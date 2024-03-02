from ng_entities.entline import Line


class Quadrangle:
    def __init__(self, A, B, C, D ):
        self.sgm = [Line(A, B), Line(B, C), Line(C, D), Line(D, A)]


class Parallelogram(Quadrangle):
    pass



