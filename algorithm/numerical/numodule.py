import sympy as sp
import itertools as it
from config import evalMode
from decoration.printer import send
from utils import humanizeDictForEvals
from predicates.entpred import eqa
from numerical.lineq import LinearEquationsSystem
from predicates.quadpred import eql
from tskmanager import Task


def totalEvaluation(settings: evalMode):
    if settings.angle: evaluateAngles()
    if settings.segment: evaluateSegments()
    if settings.ratio: evaluateRatios()


def evaluateAngles():
    """
    Расчёт углов.
    """
    currentSystem = LinearEquationsSystem(Task.Instance().AEM)
    send(currentSystem.printSystemOfEquations(namesOfVars=Task.Instance().angles[:currentSystem.matrix.cols-1]))
    for k, elem in enumerate(currentSystem.solve(geom_mode=True)):
        try:
            Task.Instance().angle_dict[Task.Instance().angles[k]] = elem
        except IndexError:
            break
    # Не активируется, если не добавлена новая строчка с предыдущей итерации.
    if Task.Instance().prev_row_num_ang == sp.shape(Task.Instance().AEM)[0]:
        return 0
    send('Модель вычислила на данной итерации следующие значения углов: ')
    send(str(humanizeDictForEvals(Task.Instance().angle_dict)))
    # todo добавить визуализацию систем уравнений (просто их напечатать, вместо переменных - хуманизированные отрезки
    Task.Instance().prev_row_num_ang = sp.shape(Task.Instance().AEM)[0]

    for comb in it.combinations(Task.Instance().angles, 2):
        a, b = comb
        if a.getValue() is not None and a.getValue() == b.getValue():
            send(f'Равные углы: {a.humanize()} = {a.getValue()}°; {b.humanize()} = {b.getValue()}°')
            eqa.entityConstructor(a, b).totalConfirm(thname='результаты вычислений', descr='величины углов получились одинаковыми в результате вычислений', premises=[None])


def evaluateSegments():
    currentSystem = LinearEquationsSystem(Task.Instance().SEM)
    send(currentSystem.printSystemOfEquations(namesOfVars=Task.Instance().segments[:currentSystem.matrix.cols - 1]))
    for k, elem in enumerate(currentSystem.solve(geom_mode=True)):
        try:
            Task.Instance().segment_dict[Task.Instance().segments[k]] = elem
        except IndexError:
            break
    # Не активируется, если не добавлена новая строчка с предыдущей итерации.
    if Task.Instance().prev_row_num_seg == sp.shape(Task.Instance().SEM)[0]:
        return 0
    send('Модель вычислила на данной итерации следующие значения отрезков: ')
    send(str(humanizeDictForEvals(Task.Instance().segment_dict)))
    Task.Instance().prev_row_num_seg = sp.shape(Task.Instance().SEM)[0]
    for comb in it.combinations(Task.Instance().segments, 2):
        a, b = comb
        if a.getValue() is not None and a.getValue() == b.getValue():
            send(f'Равные отрезки: {a.humanize()}, {a.getValue()}, {b.humanize()}, {b.getValue()}')
            eql(a.lst[0], a.lst[1], b.lst[0], b.lst[1]).totalConfirm(thname='результаты вычислений', descr='величины отрезков получились одинаковыми в результате вычислений', premises=[None])

def evaluateRatios(): pass