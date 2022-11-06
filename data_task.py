import statement as stm
from entities import Point
from freepred import col, cyl
from fixpred import mdp, cir
from quadpred import eql, ort, prl
from objpred import eqa
from extmethods import add_string

'''
eval() - выполнить строку, интересная штука
1. Здесь мы имитируем "считывание условия". Определяем какие точки задействованы и какие предикаты в условии. Подтверждаем их истинность. Задаем утверждение для док-ва. 
'''
A, B, C, D, M, F, K, H, P = Point('A'), Point('B'), Point('C'), Point('D'), Point('M'), Point('F'), Point('K'), Point('H'), Point('P')
stm.points = [A, B, C, M, D, F, K, H, P]
input_info = [col(A, B), col(B, C), col(D, C), col(A, D), col(M, C), mdp(M, A, D), mdp(K, B, C), mdp(H, D, C), mdp(P, A, B),
              mdp(F, P, H), col(M, F, K)]
for pred in input_info:
    pred.confirm()
    add_string(stm.df, [None, 'это указано в условии.', None, None, pred])
question = mdp(F, M, K)