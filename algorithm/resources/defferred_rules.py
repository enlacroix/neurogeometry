def R7(a):
    """
    Одно из проблемных теорем. Здесь четко выделяется три объекта: три прямые Line(A, B), Line(C, D), Line(P, Q)
    Нет смысла перебирать синонимы eqa, если нельзя выделить такие объекты. перефраз: нужно переставлять только линии,
    которые будут удовл требованиям ниже, переставлять по другому (синонимично) смысла нет.
    """
    if a.ttl == 'eqa':
        for x in a.synonyms():
            if x[2] == x[-2] and x[3] == x[-1]:
                A, B, P, Q, C, D = x[0], x[1], x[2], x[3], x[4], x[5]
                premises = [eqa(A, B, P, Q, C, D, P, Q)]
                if prl(A, B, C, D).confirm():
                    logger(f'R7 успешно применено на предикатах {str_list(premises)}!')
                    add_string(['признак параллельности по равным углам',
                                f'линии {A.n + B.n} и {C.n + D.n} образуют одинаковый угол с {P.n + Q.n}, поэтому они параллельны.',
                                premises, [find_fact(premises[0])],
                                prl(A, B, C, D)])
                    return 1
    else:
        return 0


def R8(a, b):
    if a.ttl == 'prl' and b.ttl == 'col':
        c, d = a, b
    elif a.ttl == 'col' and b.ttl == 'prl':
        c, d = b, a
    else:
        return 0
    if d[0] not in c.lst and d[1] not in c.lst:
        A, B, C, D, P, Q = c[0], c[1], c[2], c[3], d[0], d[1]
        premises = [prl(A, B, C, D)]
        if eqa(A, B, P, Q, C, D, P, Q).confirm():
            logger(f'R8 успешно применено на предикатах {str_list(premises)}!')
            add_string(['свойство параллельных прямых',
                        f'ввиду параллельности {A.n + B.n} и {C.n + D.n}, углы между {P.n + Q.n} и этими прямыми равны.',
                        premises, [find_fact(premises[0])],
                        eqa(A, B, P, Q, C, D, P, Q)])
         return 1

def R4(a, b):
    if a.ttl == 'mdp' and b.ttl == 'mdp':
        for x in a.synonyms():
            for y in b.synonyms():
                if x.lst[1] == y.lst[1]:
                    A, B, C, E, F = x.lst[1], x.lst[2], y.lst[2], x.lst[0], y.lst[0]
                    premises = [mdp(E, A, B), mdp(F, A, C)]

                    if prl(E, F, B, C).confirm():
                        logger(f'R4 успешно применено на предикатах {str_list(premises)}!')
                        add_string(['свойство средней линии',
                                    f'отрезок, соединяющий точки {E.n} и {F.n}, является средней линией и параллелен стороне {B.n + C.n}.',
                                    premises, [find_fact(premises[0]), find_fact(premises[1])], prl(E, F, B, C)])
                        return 1
    return 0


def R5(a, b):
    if a.ttl == 'mdp' and b.ttl == 'eql':
        c, d = a, b
    elif a.ttl == 'eql' and b.ttl == 'mdp':
        c, d = b, a
    else:
        return 0
    for x in c.synonyms():
        for y in d.synonyms():
            if x[2] == y[3] and x[1] == y[1] and x[0] != y[0]:
                M, A, B, O = x[0], x[1], x[2], y[0]
                premises = [mdp(M, A, B), eql(O, A, O, B)]

                if ort(O, M, A, B).confirm():
                    logger(f'R5 успешно применено на предикатах {str_list(premises)}!')
                    add_string(['свойство медианы, проведенной к основанию в р/б треугольнике',
                                f'медиана {O.n + M.n} в равнобедренном треугольнике {O.n + A.n + B.n}, проведенная к основанию, является и высотой.',
                                premises, [find_fact(premises[0]), find_fact(premises[1])],
                                ort(O, M, A, B)])
                    return 1


def R6(a, b):
    if a.ttl == 'mdp' and b.ttl == 'prl':
        c, d = a, b
    elif a.ttl == 'prl' and b.ttl == 'mdp':
        c, d = b, a
    else:
        return 0
    for x in c.synonyms():
        for y in d.synonyms():
            if x[0] == y[0] and x[2] == y[2]:
                E, A, B, F, C = x[0], x[1], x[2], y[1], y[3]
                if not col(F, A, C):
                    continue
                premises = [mdp(E, A, B), prl(E, F, B, C), col(F, A, C)]
                if mdp(F, A, C).confirm():
                    logger(f'R6 успешно применено на предикатах {str_list(premises)}!')
                    add_string(['обратное свойство средней линии',
                                f'линия {E.n + F.n} ∥ {B.n + C.n} и проходит через точку {E.n}, которая является серединой {A.n + B.n}, то точка {F.n} также является серединой {A.n + C.n}',
                                premises, [find_fact(premises[0]), find_fact(premises[1])],
                                mdp(F, A, C)])
                    return 1

def R3(a, b):
    if a.ttl == 'prl' and b.ttl == 'ort':
        c, d = a, b
    elif a.ttl == 'ort' and b.ttl == 'prl':
        c, d = b, a
    else:
        return 0
    for x in c.synonyms():
        for y in d.synonyms():
            if x[2] == y[0] and x[3] == y[1]:
                A, B, C, D, E, F = x[0], x[1], x[2], x[3], y[2], y[3]
                premises = [prl(A, B, C, D), ort(C, D, E, F)]

                if ort(A, B, E, F).confirm():
                    logger(f'R3 успешно применено на предикатах {str_list(premises)}!')
                    add_string(['аксиома перепендикулярности',
                                f'прямая {C.n + D.n} параллельна {A.n + B.n} и перпендикулярна {E.n + F.n}. Из этого следует, что {A.n + B.n} ортогональна {E.n + F.n}.',
                                premises, [find_fact(premises[0]), find_fact(premises[1])],
                                ort(A, B, E, F)])
                    return 1

def R2(a, b):
    if a.ttl == 'mdp' and b.ttl == 'ort':
        c, d = a, b
    elif a.ttl == 'ort' and b.ttl == 'mdp':
        c, d = b, a
    else:
        return 0
    for x in c.synonyms():
        for y in d.synonyms():
            if x[1] == y[0] and x[2] == y[3] and y[2] == y[1]:
                Z, X, Y, W = x[0], x[1], x[2], y[1]
                premises = [mdp(Z, X, Y), ort(X, W, W, Y)]

                if eql(W, Z, Z, X).confirm():
                    logger(f'R2 успешно применено на предикатах {str_list(premises)}!')
                    add_string(['свойство медианы, проведенной к гипотенузе',
                                f'медиана {W.n + Z.n}, проведенная к гипотенузе {X.n + Y.n} в прямоугольном треугольнике равна половине её длины.',
                                premises, [find_fact(premises[0]), find_fact(premises[1])],
                                eql(W, Z, Z, X)])
                    return 1

def R1(a, b):
    # 1. Удостоверимся в том, что мы приняли предикаты нужного типа и выставим их в необходимом порядке.
    if a.ttl == 'mdp' and b.ttl == 'eql':
        c, d = a, b
    elif a.ttl == 'eql' and b.ttl == 'mdp':
        c, d = b, a
    else:
        return 0

    for x in c.synonyms():
        for y in d.synonyms():
            if x[0] == y[1] == y[2] and x[1] == y[3] and y[0] != x[2]:
                Z, X, Y, W = x[0], x[1], x[2], y[0]
                premises = [mdp(Z, X, Y), eql(W, Z, Z, X)]
                print(str_list(premises))
                print(ort(X, W, W, Y), Z.n)
                if ort(X, W, W, Y).confirm():
                    logger(f'R1 успешно применено на предикатах {str_list(premises)}!')
                    add_string(['признак прямоугольного треугольнике по медиане',
                                f'если медиана ({W.n + Z.n}), проведенная к стороне ({X.n + Y.n}) равна половине длины этой стороны,'
                                f' то треугольник {X.n + Y.n + W.n} - прямоугольный с прямым углом ∠[{X.n + W.n}, {Y.n + W.n}].',
                                premises, [find_fact(premises[0]), find_fact(premises[1])],
                                ort(X, W, W, Y)])
                    return 1