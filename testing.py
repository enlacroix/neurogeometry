"""
Тестировочный полигон, здесь комната несбывшихся надежд и амбициозных экспериментов.
"""
import numpy as np

import entities as ent
import extmethods
from extmethods import pprint_dict
from numerical import Relation
from predicates.freepred import col
from scipy.linalg import solve
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
from predicates.objpred import eqa
from predicates.quadpred import prl
import varbank as vb
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
eqa(M, B, B, C, A, C, C, B)
# 4. Ввод численных значений.
ent.Angle(B, A, A, C).set_value(20)
ent.Angle(M, B, B, C).set_value(60)


# 5. Ввод численных отношений между значениями.
Relation(ent.Angle(A, C, C, B), ent.Angle(B, A, A, C), 3)

print(extmethods.str_list(vb.angle_list))
print(vb.AEM)
print(vb.AEV)
# print(solve(vb.AEM, vb.AEV))

# 5. Инициализация вопроса.
question = prl(A, C, M, B)

# ScanEvaluationMatrix - считать вычисленные данные в предикатную форму.
