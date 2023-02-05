import varbank as vb
import sympy as sp
import itertools as it
from decoration.printer import add_string, send
from external import hum_dict, str_list, str_dict
from predicates.entpred import eqa
from numerical.lineq import LinearEquationsSystem


def evaluate_angles():
    '''
    Сделать универсальным - total_evaluation, просто подать другую матрицу.
    '''
    print(str_list(vb.task.angles))
    for k, elem in enumerate(LinearEquationsSystem(vb.task.AEM).solve(True, True)):
        print(k)
        vb.task.angle_dict[vb.task.angles[k]] = elem
    # Не активируется, если не добавлена новая строчка с пред итерации.
    if vb.task.prev_row_num == sp.shape(vb.task.AEM)[0]:
        return 0
    send('Модель вычислила на данной итерации следующие значения углов: ')
    send(str(hum_dict(vb.task.angle_dict)))
    vb.task.prev_row_num = sp.shape(vb.task.AEM)[0]
    for comb in it.combinations(vb.task.angles, 2):
        a, b = comb
        if a.get_value() is not None and a.get_value() == b.get_value():
            print('Равные углы:', a.humanize(), a.get_value(), b.humanize(), b.get_value())
            pred = eqa.angle_init(a, b)
            pred.confirm()
            add_string(['вычисления', 'величины углов получились одинаковыми в результате вычислений', None, None, pred])