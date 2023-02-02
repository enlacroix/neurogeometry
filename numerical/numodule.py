import varbank as vb
import sympy as sp
import itertools as it
from decoration.printer import add_string, send
from external import hum_dict
from predicates.entpred import eqa


def evaluate_angles():
    X = vb.task.AEM.rref()[0]
    for i in vb.task.AEM.rref()[1]:
        vb.task.angle_dict[vb.task.angles[i]] = X.col(-1)[i]
    # Не активируется, если не добавлена новая строчка с пред итерации.
    if vb.task.prev_row_num == sp.shape(vb.task.AEM)[0]:
        return 0
    send('Модель вычислила на данной итерации следующие значения углов: ')
    send(str(hum_dict(vb.task.angle_dict)))
    vb.task.prev_row_num = sp.shape(vb.task.AEM)[0]
    for comb in it.combinations(vb.task.angles, 2):
        a, b = comb
        if a.get_value() == b.get_value():
            pred = eqa.angle_init(a, b)
            pred.confirm()
            add_string(['вычисления', 'величины углов получились одинаковыми в результате вычислений', None, None, pred])
    return X.col(-1)