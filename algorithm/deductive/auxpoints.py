'''
Построение вспомогательных точек и других элементов чертежа.
'''
from ng_entities.entangle import Point, Angle
from numerical.functors import Relation
from objects import DescribedTriangle
from predicates.fixpred import cir
import varbank as vb


def A1(pred):
    """
    вписанный угол равен половине центрального угла, опирающегося на эту дугу.
    """
    if isinstance(pred, cir):
        aux = Point('H1')
        A, O, B = pred.lst[1], pred.lst[0], pred.lst[2]
        vb.task.points.append(aux)
        Relation(Angle(A, O, O, B), Angle(A, aux, aux, B), 2)
        cir(A, O, B, aux).confirm()
        DescribedTriangle(O, aux, A, B).confirm()
