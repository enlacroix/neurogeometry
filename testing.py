from fixpred import mdp
from entities import Point
from quadpred import eql, ort, prl
from freepred import col
from extmethods import str_list, gen_only_right_perm, add_string, find_fact
import statement as stm

'''
Тестировочный полигон, здесь комната несбывшихся надежд и амбициозных экспериментов. 
'''
A, B, C, D, M = Point('A'), Point('B'), Point('C'), Point('D'), Point('M')

# x = eval('prl(A, D, B, C)') - интересная опция.






def normalize_form(pred):
    '''
    :param pred: предикат
    :return: вернуть нормальную форму
    '''


def find_uncertain_predicate(target):
    '''
    :param target: предикат с пропущенными точками
    :return: все кандидаты, которые подошли по ориентировке розыска
    участвуют: глобальные переменные stm.predicates и stm.points
    Если первый аргумент функции-правила совпал с предикатом, то запускается поиск остальных аргументов правила в списке предикатов.
    find_uncertain_predicate(prl(A, *, B, *)) - мы передаем строковое описание или сам класс?
    '''







