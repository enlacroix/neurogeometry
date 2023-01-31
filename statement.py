import varbank as stm
from entities import Point
from predicates.freepred import col
from predicates.fixpred import mdp
from extmethods import add_string

'''
eval() - выполнить строку, интересная штука
1. Здесь мы имитируем "считывание условия". Определяем какие точки задействованы и какие предикаты в условии. Подтверждаем их истинность. Задаем утверждение для док-ва. 
'''

'''
Сделать так, чтобы можно было подключать разные условия демозадач. 
например, считывать различные предикаты из текстового файла, либо из поля, задаваемого пользователем. а лучше функция, которая может делать и то, и другое. 
'''

A, B, C, D, M, F, K, H, P = Point('A'), Point('B'), Point('C'), Point('D'), Point('M'), Point('F'), Point('K'), Point('H'), Point('P')
input_info = [col(A, B), col(B, C), col(D, C), col(A, D), col(M, C), mdp(M, A, D), mdp(K, B, C), mdp(H, D, C), mdp(P, A, B), mdp(F, P, H), col(M, F, K)]

# stm.points = [A, B, C, M, D, F, K, H, P] добавление в этот массив уже происходит на этапе инициализация
for pred in input_info:
    pred.confirm()
    add_string(stm.df, [None, 'это известно из условия.', None, None, pred])

question = mdp(F, M, K)

# 1. Инициализация точек.
# 2. Распознавание геометрических объектов (e.g. треугольник)
# 3а. Инициализация предикатов (свободных, e.g. col)
# 3б. Инициализация предикатов (логических - , e.g. mdp, ort, eql и т.п.)
# 4. Ввод численных значений.
# 5. Ввод численных отношений между значениями.

