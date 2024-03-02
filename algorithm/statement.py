from utils import logger
from ng_entities.entangle import Point
from tskmanager import Task
from predicates.predmain import GeneralizedPredicate

'''
Мы импортируем все модули предикатов, чтобы eval их корректно распознал.
'''
from predicates.freepred import col, cyl
from numerical.functors import SetValue, Relation, Sum, LinearCombination
from ng_objects.triangles import Triangle, IsoTriangle, OrtTriangle
from predicates.fixpred import mdp, cir, inter, citer
from predicates.quadpred import prl, ort, eql, PRL, ORT
from ng_entities.entangle import Angle
from ng_entities.entline import Line
from ng_entities.segment import Segment
from predicates.entpred import eqa, eqr
from predicates.figpred import ctr, etr
from ng_objects.quadrangular import Quadrangle


def reading_points(string: str):
    """
    :param string: строка, состоящая из всех точек, задействованных в условии задачи. Пример: А, B, C. Разделены запятой и пробелом.
    Как и в геометрии, точка обозначается лишь одним символом.
    :return: список объектов класса Point.
    """
    res = []
    for name in string.split(', '):
        res.append(Point(name))
    return res

# 1. Инициализация точек.
# 2. Распознавание геометрических объектов (e.g. треугольник, Triangle)
# 3. Инициализация предикатов
# 4. Ввод численных значений.
# 5. Ввод численных отношений между значениями.

def read_task(predicates_listing, question_str):
    """
    Для инициализации условия нужно три вещи: первая это список точек.
    :param predicates_listing: предикаты условия, записанные в одной строке, разделённые точкой с запятой с пробелом
    :param question_str: вопрос в строковой форме.
    :return:
    """
    # TODO Ручной ввод точек.
    A, B, C, D, E, M, F, K, H, P, O, Q, N = reading_points('A, B, C, D, E, M, F, K, H, P, O, Q, N')
    for pred_name in predicates_listing.split('; '):
        try:
            pred = eval(pred_name)
        except NameError:
            logger(f'Внимание! Имя {pred_name} некорректно и не было обработано! Импортируйте соответствующий модуль.')
            continue
        if isinstance(pred, GeneralizedPredicate):
            Task.Instance().statement.append(pred)
            Task.DF().addString((None, 'это известно из условия.', [None], None, pred))
            pred.confirm()
    Task.Instance().question = eval(question_str)





# input_info = [col(A, B), col(B, C), col(D, C), col(A, D), col(M, C), mdp(M, A, D), mdp(K, B, C), mdp(H, D, C),
#               mdp(P, A, B), mdp(F, P, H), col(M, F, K)]
# question = mdp(F, M, K)
# for pred in input_info:
#     pred.confirm()
#     add_string([None, 'это известно из условия.', None, None, pred])
