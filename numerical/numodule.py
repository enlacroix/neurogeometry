import varbank as vb
import sympy as sp
import itertools as it
from decoration.printer import add_string, send
from external import hum_dict, str_list, str_dict
from predicates.entpred import eqa
from numerical.lineq import LinearEquationsSystem
from predicates.quadpred import eql


def evaluate_angles():
    '''
    Сделать универсальным (?) - total_evaluation, просто подать другую матрицу/спиоок/другие названия - запарно, но я
    '''
    for k, elem in enumerate(LinearEquationsSystem(vb.task.AEM).solve(True)):
        try:
            vb.task.angle_dict[vb.task.angles[k]] = elem
        except IndexError:
            break
    # Не активируется, если не добавлена новая строчка с пред итерации.
    if vb.task.prev_row_num_ang == sp.shape(vb.task.AEM)[0]:
        return 0
    send('Модель вычислила на данной итерации следующие значения углов: ')
    send(str(hum_dict(vb.task.angle_dict)))
    vb.task.prev_row_num_ang = sp.shape(vb.task.AEM)[0]
    for comb in it.combinations(vb.task.angles, 2):
        a, b = comb
        if a.get_value() is not None and a.get_value() == b.get_value():
            print('Равные углы:', a.humanize(), a.get_value(), b.humanize(), b.get_value())
            pred = eqa.angle_init(a, b)
            if pred.confirm():
                add_string(['вычисления', 'величины углов получились одинаковыми в результате вычислений', None, None, pred])


def evaluate_segments():
    for k, elem in enumerate(LinearEquationsSystem(vb.task.SEM).solve(True)):
        try:
            vb.task.segment_dict[vb.task.segments[k]] = elem
        except IndexError:
            break
    # Не активируется, если не добавлена новая строчка с пред итерации.
    if vb.task.prev_row_num_seg == sp.shape(vb.task.SEM)[0]:
        return 0
    send('Модель вычислила на данной итерации следующие значения отрезков: ')
    send(str(hum_dict(vb.task.segment_dict)))
    vb.task.prev_row_num_seg = sp.shape(vb.task.SEM)[0]
    for comb in it.combinations(vb.task.segments, 2):
        a, b = comb
        if a.get_value() is not None and a.get_value() == b.get_value():
            print('Равные отрезки:', a.humanize(), a.get_value(), b.humanize(), b.get_value())
            pred = eql(a.lst[0], a.lst[1], b.lst[0], b.lst[1])
            if pred.confirm():
                add_string(['вычисления', 'величины отрезков получились одинаковыми в результате расчётов', None, None, pred])