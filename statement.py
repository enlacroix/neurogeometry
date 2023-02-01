from decoration.printer import add_string
from entities import Point, Triangle
from external import str_list
import varbank as vb
'''
Мы импортируем все модули предикатов, чтобы eval их корректно распознал.
'''
from predicates.freepred import col
from predicates.fixpred import mdp
from predicates.quadpred import eql, ort, prl
from predicates.entpred import eqa





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


# TODO Жуткий кошмарный костыль.
# Пользователю нужный каждый раз залезать в файл, чтобы добавить/убрать точки. Либо иниц весь английский алфавит (у нас же нет перебора точек больше)
# может ли и здесь помочь eval?
A, B, C, D, M, F, K, H, P = reading_points('A, B, C, D, M, F, K, H, P')


def read_task(predicates_listing, question_str):
    """
    Для инициализации условия нужно три вещи: первая это список точек.
    :param predicates_listing: предикаты условия, записанные в одной строке, разделённые точкой с запятой с пробелом
    :param question_str: вопрос в строковой форме.
    :return:
    """
    # Не подходит для считывания объектов типа Triangle и Relation
    for pred_name in predicates_listing.split('; '):
        try:
            vb.task.statement.append(eval(pred_name))
        except NameError:
            print(f'Внимание! Имя {pred_name} некорректно и не было обработано!')
            continue
        pred = vb.task.statement[-1]
        pred.confirm()
        add_string([None, 'это известно из условия.', None, None, pred])
    vb.task.question = eval(question_str)




'''
Сделать так, чтобы можно было подключать разные условия демозадач. 
например, считывать различные предикаты из текстового файла, либо из поля, задаваемого пользователем. а лучше функция, которая может делать и то, и другое. 
'''

# 1. Инициализация точек.
# 2. TODO Распознавание геометрических объектов (e.g. треугольник, ent.Triangle)
# 3. Инициализация предикатов
# 4. TODO Ввод численных значений.
# 5. TODO Ввод численных отношений между значениями.

# input_info = [col(A, B), col(B, C), col(D, C), col(A, D), col(M, C), mdp(M, A, D), mdp(K, B, C), mdp(H, D, C),
#               mdp(P, A, B), mdp(F, P, H), col(M, F, K)]
# question = mdp(F, M, K)
# for pred in input_info:
#     pred.confirm()
#     add_string([None, 'это известно из условия.', None, None, pred])
