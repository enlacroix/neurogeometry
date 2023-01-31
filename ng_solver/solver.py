from extmethods import transitive_predicates, str_list
from ng_solver.rules import Rules
from inspect import signature
import config as prm
import varbank as stm
import itertools as it


def proof(question, prev_predicates, prev_size):
    i = 1
    while True:
        for r in Rules:
            #print(f'правило {i}')
            # хотя бы один предикат из связки ДОЛЖЕН БЫТЬ  свежим
            for predcomb in it.combinations(stm.predicates, len(signature(r).parameters)):
                if any([u not in prev_predicates for u in predcomb]):  # Этот пункт спасает полное исследование, снижая время в два раза.
                    r(*predcomb)
            transitive_predicates(stm.predicates)
            #i += 1
            #print(str_list(stm.lines))
        #print('перебор правил завершен')
        #print(f'{prev_size}, {len(stm.predicates)}')
        if prev_size == len(stm.predicates) or (prm.only_question and question):
            break
        else:
            prev_size = len(stm.predicates)
            prev_predicates = stm.predicates
    #print(str_list(stm.predicates))
    stm.df.to_csv('resources/geom.csv', encoding='utf-8')
    return 0


'''
Архив предыдущего подхода, который временно приоставил свою работу. Точечноориентированный подход с комбинацией прямого распространения + обратного поиска
уступил правилам-фукнциям от предикатов и базе данных. 
def R5(O, M, A, B, br=True):
    premises = [mdp(M, A, B), eql(O, A, O, B)]
    trivial = [True]
    if all(trivial) and all(premises):
        if ort(O, M, A, B).confirm():
            send(f'Медиана {O.n+M.n} в равнобедренном треугольнике {O.n+A.n+B.n}, проведенная к основанию, является и высотой.')
            return 1
    elif all(trivial) and br:
        children_search(premises)
    else:
        return 0
def R9(A, B, C, D, M, br=True):
    premises = [mdp(M, A, B), prl(A, C, B, D), prl(A, D, B, C)]
    if all(premises):
        if mdp(M, C, D).confirm():
            send(f'Если в 4-угольнике две пары противоположных сторон попарно параллельны,'
                 ' и одна из диагоналей точкой пересечения делятся пополам, то и вторая тоже. ')
            return 1
    elif br:
        children_search(premises)
    else:
        return 0
def R2(X, Y, Z, W, br=True):
    premises = [mdp(Z, X, Y), ort(X, W, W, Y)]
    trivial = [col(X, Y)]
    if all(trivial) and all(premises):
        if eql(W, Z, Z, X).confirm():
            send(f'Медиана {W.n + Z.n}, проведенная к гипотенузе {X.n + Y.n} в прямоугольном треугольнике равна половине её длины.')
        return 1
    else:
        return 0
def R4(A, B, C, E, F, br=True):

    premises = [mdp(E, A, B), mdp(F, A, C)]
     # РАНЬШЕ ЗДЕСЬ БЫЛИ УТВЕРЖДЕНИЯ, О ТОМ ЧТО ТОЧКИ НЕ РАВНЫ!
    if all(premises):
        if prl(E, F, B, C).confirm():
            send(f'Отрезок, соединяющий точки {E.n} и {F.n}, является средней линией и параллелен стороне {B.n + C.n}.')
            return 1
    elif br:
        children_search(premises)
    else:
        return 0
R = [R1, R2, R3, R4, R5, R6, R7, R8, R9]
def R1(X, Y, Z, W, br=True):
    premises = [mdp(Z, X, Y), eql(W, Z, Z, X)]
    trivial = [col(X, Y), col(W, Z)] # W != Z УВЕЛИЧИВАЕТ ДЛИТЕЛЬНО С 6 ДО 17 СЕКУНД КАК?
    # trivial = [col(X, Y), col(X, W), col(Y, W), col(W, Z)] - 2.7 секунд вместо 6! col сразу подсказывает нужные комбинации, а не перебирает "мусорные" точки
    if all(trivial) and all(premises):
        if ort(X, W, W, Y).confirm():
            send(f'Если медиана ({W.n + Z.n}), проведенная к стороне ({X.n + Y.n}) равна половине длины этой стороны,'
                 f' то треугольник {X.n + Y.n + W.n} - прямоугольный с прямым углом ∠[{X.n + W.n}, {Y.n + W.n}].')
        return 1
    elif all(trivial) and br:
        children_search(premises)
    else:
        return 0
Rules = {'ort': [R1, R3, R5], # Разным ключам могут соотв. одни и те же правила, например, медиана в р/б треугольнике образует и биссектриссу и высоту
         'eql': [R2],
         'prl': [R4, R7],
         'mdp': [R6, R9],
         'eqa': [R8],
         'col': [R0]} # А что писать в col? Будем надеяться, что его не потребуют.
def R6(A, B, C, E, F, br=True):
    premises = [mdp(E, A, B), prl(E, F, B, C), col(F, A, C)]
    #trivial = [True]
    if all(premises):
        if mdp(F, A, C).confirm():
            send(f'Линия {E.n+F.n} ∥ {B.n+C.n} и проходит через точку {E.n}, которая является серединой {A.n+B.n}, то точка {F.n} также является серединой {A.n+C.n}')
            return 1
    elif br:
        children_search(premises)
    else:
        return 0
def R3(A, B, C, D, E, F, br=True):
    premises = [prl(A, B, C, D), ort(C, D, E, F)]
    if all(trivial) and all(premises):
        if ort(A, B, E, F).confirm():
            send(f'Прямая {C.n + D.n} параллельна {A.n + B.n} и перпендикулярна {E.n + F.n}. Из этого следует, что {A.n + B.n} ортогональна {E.n + F.n}.')
        return 1
    elif all(trivial) and br:
        children_search(premises)
    else:
        return 0

def R7(A, B, C, D, P, Q, br=True):
    premises = [eqa(A, B, P, Q, C, D, P, Q)]
    if all(premises):
        if prl(A, B, C, D).confirm():
            send(f'Линии {A.n+B.n} и {C.n+D.n} образуют одинаковый угол с {P.n+Q.n}, поэтому они параллельны.')
            return 1
    elif br:
        children_search(premises)
    else:
        return 0

def R8(A, B, C, D, P, Q, br=True):
    premises = [prl(A, B, C, D)]
    trivial = [col(P, Q)]
    if all(trivial) and all(premises):
        if eqa(A, B, P, Q, C, D, P, Q).confirm() and br:
            send(f'Ввиду параллельности {A.n+B.n} и {C.n+D.n}, углы между {P.n+Q.n} и этими прямыми равны.')
            return 1
    elif br:
        children_search(premises)
    else:
        return 0
def children_search(premises):
    limit = max(1, len(premises) - 2)  # - кредит доверия. что делать с теми где они предикат-предпосылка?
    bool_premises = [bool(x) for x in premises]
    if bool_premises.count(True) >= limit or len(premises) == 1:
        for prem in premises:
            processed.append(prem)
            if not prem.bool and prem not in processed:
                print(prem)
                # print([str(x) for x in processed])
                point_search(prem)  # Если предикат попал в обработанные, то его нельзя вызывать в предикатах-предпосылках, чтобы не случился замкнутый круг.
            else:
                continue
    else:
        return 0


def point_search(thesis):  # в поиске не должны участвовать предикаты, которые уже были проанализированы
    # отработанные комбинации точек не должны вновь рассматриваться ???
    if thesis in stm.predicates:  #
        print('Цель достигнута: свернуть процесс. Лучше скрыть это сообщение, но return будет останавливать брутфорс')
        return 0
    for r in Rules[thesis.ttl]:
        for comb in gen_comb(len(signature(r).parameters) - 1, stm.points):  # каждый раз генерируется список из 2, 3, 4 точек. не проще ли заранее сгенерить, а потом обращаться?
            r(*comb)  # еще параметр, который управляет тем, активировать ли поиск потомков

def initial_explore(n):
    for _ in range(n):
        for r in R:
            for comb in gen_comb(len(signature(r).parameters) - 1, stm.points):  # каждый раз генерируется список из 2, 3, 4 точек. не проще ли заранее сгенерить, а потом обращаться?
                r(*comb, False)
        transitive_predicates(stm.predicates)
'''
