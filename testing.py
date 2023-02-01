"""
Тестировочный полигон, здесь комната несбывшихся надежд и амбициозных экспериментов.
"""
import numpy as np
from sympy import Matrix

import entities as ent
import external
from external import pprint_dict
from numerical import Relation
from predicates.freepred import col

# x = eval('prl(A, D, B, C)') - интересная опция.


# def normalize_form(pred):
#     '''
#     :param pred: предикат
#     :return: вернуть нормальную форму
#     '''
#
#
# def find_uncertain_predicate(target):
#     '''
#     :param target: предикат с пропущенными точками
#     :return: все кандидаты, которые подошли по ориентировке розыска
#     участвуют: глобальные переменные stm.predicates и stm.points
#     Если первый аргумент функции-правила совпал с предикатом, то запускается поиск остальных аргументов правила в списке предикатов.
#     find_uncertain_predicate(prl(A, *, B, *)) - мы передаем строковое описание или сам класс?
#     '''
from predicates.entpred import eqa
from predicates.quadpred import prl
from varbank import task

'''
Задача: Дан треугольник АВС. Проведена прямая МВ. Угол ВАС - 20 градусов, <MBC = 60 градусов, угол АСВ в три раза больше чем угол А. 
Доказать, что АС параллельно МВ.
'''
# 1. Инициализация точек.
A, B, C, M = ent.Point('A'), ent.Point('B'), ent.Point('C'), ent.Point('M')
# 2. Распознавание геометрических объектов (e.g. треугольник)
ent.Triangle(A, B, C)
# 3а. Инициализация предикатов (свободных, e.g. col)
col(M, B)
# 3б. Инициализация предикатов (логических - , e.g. mdp, ort, eql и т.п.)

# 4. Ввод численных значений.
ent.Angle(B, A, A, C).set_value(20)
ent.Angle(M, B, B, C).set_value(60)

# 5. Ввод численных отношений между значениями.
Relation(ent.Angle(A, C, C, B), ent.Angle(B, A, A, C), 3)

# print(extmethods.str_list(vb.angle_list))
# print(vb.AEM)
# print(vb.AEV)
pprint_dict(task.angles)
T = Matrix([[1, 1, 1, 0, 0, 180],
            [0, 1, 0, 0, 0, 20],
            [0, 0, 0, 1, 0, 60],
            [0, -3, 1, 0, 0, 0]]
           )
X = T.rref()[0]
res = []
for i in T.rref()[1]:
    task.angle_dict[task.angle_dict[i]] = X.col(-1)[i]
pprint_dict(task.angle_dict)
# A = Matrix([[1, 1, 1, 0, 0],
#             [0, 1, 0, 0, 0],
#             [0, 0, 0, 1, 0],
#             [0, -3, 1, 0, 0]]
#            )
# b = Matrix([[180],
#             [20],
#             [60],
#             [0]]
#            )
# 6. Инициализация вопроса.
question = prl(A, C, M, B)

# ScanEvaluationMatrix - считать вычисленные данные в предикатную форму.
