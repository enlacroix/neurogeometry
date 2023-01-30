import varbank as stm
from entities import Point
from predicates.freepred import col
from predicates.fixpred import mdp
from extmethods import add_string

'''
eval() - выполнить строку, интересная штука
1. Здесь мы имитируем "считывание условия". Определяем какие точки задействованы и какие предикаты в условии. Подтверждаем их истинность. Задаем утверждение для док-ва. 
'''


A, B, C, D, M, F, K, H, P = Point('A'), Point('B'), Point('C'), Point('D'), Point('M'), Point('F'), Point('K'), Point('H'), Point('P')
input_info = [col(A, B), col(B, C), col(D, C), col(A, D), col(M, C), mdp(M, A, D), mdp(K, B, C), mdp(H, D, C), mdp(P, A, B), mdp(F, P, H), col(M, F, K)]
stm.points = [A, B, C, M, D, F, K, H, P]
for pred in input_info:
    pred.confirm()
    add_string(stm.df, [None, 'по условию.', None, None, pred])

question = mdp(F, M, K)