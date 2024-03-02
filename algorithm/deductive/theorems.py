from functools import lru_cache
from utils import getCommonElements, FindCommonFindUnique, toStrAllElems
from ng_entities.entangle import Angle
from ng_objects.triangles import Triangle, IsoTriangle
from numerical.functors import Relation
from predicates.freepred import col, cyl
from predicates.fixpred import mdp, cir, citer
from predicates.quadpred import eql, ort, prl
from predicates.entpred import eqa, eqr
from predicates.figpred import ctr
from tskmanager import Task

'''
Rules можно сделать словарём, где ключами будут типы предикатов, которые получаются на выходе. По аналогии
с предыдущим словарем, такой подход может пригодиться, когда будет нужда вернуться к комбинации 
"прямой ход + обратный". 
Rules = {'ort': [R1, R3, R5], # Разным ключам могут соотв. одни и те же правила, например, медиана в р/б треугольнике образует и биссектрису и высоту
         'eql': [R2],
         'prl': [R4, R7],
         'mdp': [R6, R9],
         'eqa': [R8],
         'col': [R0]}
'''


def T1(predicate: eqa):
    """
    1. Если бы это было классом, то у всех порождающих теорем был бы атрибут памяти, который записывал уже обработанные предикаты и не вызывал для них
    основной процесс.
    2. можно создать словарь, где ключи это названия порождающих теорем, а значения это списки обработанных этой теоремой предикатов. Будут делаться запросы к словарю,
    доступному для всех теорем.
    """
    if isinstance(predicate, eqa):
        return 1
    else:
        return 0


def T2(predicate: prl):
    if isinstance(predicate, prl):
        thName = 'свойство накрест лежащих углов при параллельных прямых'
        A, B, C, D = predicate.lst
        if col(B, C):
            eqa(B, C, D, A, B, C).totalConfirm(thName, f'Углы ∠{B.n + C.n + D.n} и ∠{A.n + B.n + C.n} равны, как накрест'
                                                       f' лежащие при ∥ прямых {A.n + B.n}, {C.n + D.n}.', [predicate])
        if col(A, D):
            eqa(A, D, C, D, A, B).totalConfirm(thName, f'Углы ∠{A.n + D.n + C.n} и ∠{D.n + A.n + B.n} равны, как накрест'
                                                       f' лежащие при ∥ прямых {A.n + B.n}, {C.n + D.n}.', [predicate])
        return 1
    return 0

def T3(predicate: ort):
    """
    ort(A, C, C, B), if mdp(M, A, B) => citer(M, A, B, C).
    """
    commonPoint, uniquePointList = FindCommonFindUnique(predicate.sgm[0].lst, predicate.sgm[1].lst)
    if commonPoint:
        C = commonPoint
        A, B = uniquePointList
    else: return 0
    for mP in Task.getPoints(C, A, B):
        if mdp(mP, A, B):
            citer(mP, A, B, C).totalConfirm('расположение центра описанной окружности в прямоугольном треугольнике',
                                           f'{mP.n}, середина гипотенузы {A.n + B.n}, является центром описанной окружности в прямоугольном треугольнике.',
                                           [predicate, mdp(mP, A, B)])
            return 1

def T4(predicate: eqa):
    """
    T4: если углы, опирающиеся на один отрезок, равны, и не лежат на одной прямой, то они лежат на одной окр.
    eqa(A, C, B, A, D, B) =>
    if !col(A, B, C, D): cyl(A, B, C, D).
    """
    if isinstance(predicate, eqa):
        firstAngle, secondAngle = predicate.sgm
        if firstAngle.arc == secondAngle.arc and not col(firstAngle.vertex, secondAngle.vertex, *firstAngle.arc.lst):
            cyl(firstAngle.vertex, secondAngle.vertex, *firstAngle.arc.lst).totalConfirm(thname='признак точек, лежащих на одной окружности',
                                                                                         descr=f'{firstAngle} = {secondAngle}, опирающиеся на один отрезок {firstAngle.arc.name}, следовательно '
                                                                                               f'вокруг точек можно описать окружность', premises=[predicate])
        return 1
    return 0


def T5(predicate: eqa):
    """
    T5: если точки лежат на одной окружности и вписанные углы равны, то хорды (на которые опираются) равны.
    eqa(B, C, A, P, R, Q) =>
    if cyl(A, B, C, P, R, Q): eql(A, B, P, Q).
    """
    if isinstance(predicate, eqa):
        B, C, A, P, R, Q = predicate.lst
        if cyl(B, C, A, P, R, Q):
            eql(A, B, P, Q).totalConfirm(thname='равенство хорд по равенству вписанных углов, опирающихся на них',
                                         descr=f'{predicate.sgm[0]} = {predicate.sgm[1]} и точки принадлежат одной окружности, следовательно хорды {A.n + B.n} и'
                                               f'{P.n + Q.n} равны по равенству опирающихся на них вписанных углов.', premises=[predicate])
            return 1
    return 0


def T6(predicate: mdp):
    """
    Свойство средней линии.
    [mdp(E, A, B) <=> mdp(x*, A, x**)] => prl(E, x*, B, x**)
    Ищем совпадающую точку среди прямых AB и неизвестного Line. Если у них есть общая точка сР, то нам нужны остальные две точки, которы содержатся в предикате
    """
    if isinstance(predicate, mdp):
        E, A, B = predicate.lst
        for pred in Task.Instance().predicates['mdp']: # безопасно, потому что хотя бы один mdp уже есть
            if pred != predicate:
                cP = getCommonElements(predicate.sgm[1].lst, pred.sgm[1].lst)
                if not cP: return
                mX = pred.sgm[0] # x*
                mY = [p for p in pred.sgm[1].lst if p != cP[0]][0] # x**
                Z = [p for p in predicate.sgm[1].lst if p !=cP[0]][0]
                prl(E, mX, Z, mY).totalConfirm(thname='свойство средней линии', descr=f'средняя линия {E.n + mX.n} параллельна отрезку {Z.n + mY.n} согласно своему свойству.',
                                               premises=[predicate, mdp(mX, cP[0], mY)])
        return 1
    else:
        return 0


def T7(predicate: prl):
    """
    Т7: признак средней линии.
    prl(E, F, B, C) <=> mdp(E, x*, B) => найти такую маску mdp и проверь следующее:
    if col(F, x*, C): mdp(F, x*, C).
    """
    if isinstance(predicate, prl):
        E, F, B, C = predicate.lst
        for mP in Task.getPoints(E, F, B, C):
            if mdp(E, mP, B) and col(F, mP, C):
                mdp(F, mP, C).totalConfirm(thname='признак средней линии', descr=f'{predicate.sgm[0].name} ∥ {predicate.sgm[1].name}, {mdp(E, mP, B).humanize()}, следовательно '
                                                                                 f'сторону {F.n + C.n} прямая пересечёт в середине.', premises=[predicate, mdp(E, mP, B)])
                return 1
    return 0


def T8(predicate: eql):
    """
    T8: свойство равнобедренного треугольника - углы при основании равны.
    ВОЗМОЖНО вынесение в объект Равнобедренный треугольник, а это теорема замениться на его под-свойство.
    eql(O, A, O, B) and !col(O, A, B) and col(A, B) => eqa(O, A, B, A, B, O)
    """
    if isinstance(predicate, eql):
        O, uniquePoints = FindCommonFindUnique(predicate.sgm[0].lst, predicate.sgm[1].lst)
        if O:
            A, B = uniquePoints
        else:
            return 0
        if col(A, B) and not col(O, A, B):
            IsoTriangle.pointConstructor(B, A, vertex=O).totalConfirm(thname='свойство равнобедренного треугольника',
                                               descr=f'{eql(O, A, O, B).humanize()}, поэтому углы при основании {A.n + B.n} равны: {eqa(O, A, B, A, B, O).humanize()}.',
                                               premises=[eql(O, A, O, B)])
            return 1
    return 0


def T9(predicate: eqa):
    """
    T9: признак равнобедренного треугольника. (обратно к T8)
    eqa(O, A, B, A, B, O) => eql(O, A, O, B)
    """
    if not isinstance(predicate, eqa): return 0
    commonLine, uniqueLines = FindCommonFindUnique(predicate.sgm[0].sgm, predicate.sgm[1].sgm)
    if not commonLine: return 0
    cP = getCommonElements(uniqueLines[0].lst, uniqueLines[1].lst)
    if not cP: return 0
    A, B = commonLine.lst
    IsoTriangle.pointConstructor(B, A, vertex=cP[0]).totalConfirm(thname='признак равнобедренного треугольника',
                                   descr=f'{predicate.humanize()}, углы при основании треугольника равны => он равнобедренный, стороны {cP[0].n + A.n} и {cP[0].n + B.n} равны',
                                   premises=[predicate])
    return 1


def T10(predicate: cir):
    """
    T10: Угол между касательной и хордой равен вписанному углу, опир. на эту хорду.
    cir(O, A, B, C) <=> ort(O, A, A, *x) => eqa(*x, A, B, A, C, B)
    """
    if not isinstance(predicate, cir): return 0
    O, A, B, C = predicate.lst
    for mP in Task.Instance().getPoints(O, A, B, C):
        if ort(O, A, A, mP):
            eqa(mP, A, B, A, C, B).totalConfirm(thname='свойство угла между касательной и хордой',
                                                descr=f'{predicate.humanize()}, известно, что {ort(O, A, A, mP)}, т.е. {A.n + mP.n} является'
                                                      f'касательной к данной окружности. Угол между касательной и хордой {A.n + B.n}'
                                                      f' равен вписанному углу ∠{A.n + C.n + B.n}, опирающемуся на эту хорду.', premises=[predicate, ort(O, A, A, mP)])
    return 1


def T11(predicate: eqa):
    """
    T11: обратно к T10. если прямая образует равные углы с хордой, то это прямая - касательная (перпенд. радиусу)
    eqa(Х, A, B, A, C, B) && cir(mP, A, B, C): => ort(mP, A, A, X).
    TODO возможно стоит присвоить АХ статус касательной к окружности cir
    """
    if not isinstance(predicate, eqa): return 0
    fangle: Angle
    for fangle in predicate.sgm:
        if fangle.arc in predicate.another(fangle).sgm:
            A, B = fangle.arc.lst
            C = fangle.vertex
            X = [p for p in predicate.another(fangle).lst if p not in (A, B)][0]
            for mP in Task.Instance().points:
                if cir(mP, A, B, C):
                    ort(mP, A, A, X).totalConfirm(thname='признак касательной по хорде',
                                                  descr=f'{predicate.humanize()} и {cir(mP, A, B, C).humanize()}: прямая {X.n + A.n} образует угол с хордой {A.n + B.n},'
                                                        f'равный опирающемуся на неё вписанному углу. Тогда {X.n + A.n} - касательная и перпендикулярна {mP.n + A.n}.',
                                                  premises=[predicate, cir(mP, A, B, C)])
        return 1


def T12(predicate: ort):
    """
    T12: Медиана, проведенная к гипотенузе, равна ее половине.
    [ort(A, B, B, C) <=> mdp(*, A, C)] => eql(A, *, B, *).
    """
    if isinstance(predicate, ort):
        '''
        Могут ли аргументы соотв данному паттерну? A, B, B, C 
        Как решить это без перебора всех синонимов? 
        1. проверить, что у в sgm у двух Line есть общая точка. 
        2. По методу FindCommonFindUnique построить нужное соответствие между А, В, С и реальными аргументами ort().
        ФИЛОСОФИЯ: ИСПОЛЬЗОВАТЬ SGM И ЛОГИКУ ВМЕСТО ПЕРЕБОРА. 
        '''
        commonPointList, uniquePointList = FindCommonFindUnique(predicate.sgm[0].lst, predicate.sgm[1].lst)
        if commonPointList:
            B = commonPointList
            A, C = uniquePointList
        else:
            return 0
        for mP in Task.getPoints(C, A, B):
            if mdp(mP, A, C):
                eql(A, mP, B, mP).totalConfirm('свойство медианы в прямоугольном треугольнике',
                                               f'медиана {B.n + mP.n}, проведенная к гипотенузе {A.n + C.n} в прямоугольном треугольнике равна половине её длины.',
                                               [predicate, mdp(mP, A, C)])
                return 1
    else:
        return 0


def T13(predicate: eql):
    """
    T13: обратно к T12.
    eql(A, M, B, M) => if mdp(M, A, *x): ort(A, B, B, *x).
    """
    if not isinstance(predicate, eql): return 0
    M, uniquePoints = FindCommonFindUnique(predicate.sgm[0].lst, predicate.sgm[1].lst)
    if not M: return 0
    A, B = uniquePoints
    for mP in Task.getPoints(M, A, B):
        if mdp(M, A, mP):
            ort(A, B, B, mP).totalConfirm(thname='признак прямоугольного треугольника по свойству медианы',
                                          descr=f'{predicate.humanize()} и {mdp(M, A, mP).humanize()}, если медиана {B.n + M.n} равна половине стороны'
                                                f'{A.n + mP.n}, то треугольник {A.n + B.n + mP.n} - прямоугольный с прямым углом в {B.n}.', premises=[predicate, mdp(M, A, mP)])
            return 1

def T14(predicate: cir):
    """
    T14: Вписанный угол, опирающийся на диаметр, равен 90. (отражено в виде перпенд сторон).
    cir(O, A, B, C) => if col(O, A, C): ort(A, B, B, C)
    """
    if not isinstance(predicate, cir): return 0
    O, A, B, C = predicate.lst
    if col(O, A, C):
        conclusion = ort(A, B, B, C)
    elif col(O, A, B):
        conclusion = ort(A, C, C, B)
    elif col(O, C, B):
        conclusion = ort(B, A, A, C)
    else:
        return 0
    commonPoint, uniquePoints = FindCommonFindUnique(conclusion.sgm[0].lst, conclusion.sgm[1].lst)
    X, Y = uniquePoints
    conclusion.totalConfirm(thname='вписанный угол, опирающийся на диаметр',
                            descr=f'есть окружность с диаметром {X.n + Y.n}, на неё опирается угол с вершиной {commonPoint.n}, тогда он равен 90 градусам.', premises=[predicate])
    return 1

def T15(predicate: prl):
    """
    TODO обратная теорема к Т15 насколько актуальна?
    T15: Параллельные прямые высекают одинаковые дуги на окружности.
    prl(A, B, C, D), if cyl(A, B, C, D): eqa(A, D, C, D, C, B).
    """
    if not isinstance(predicate, prl): return 0
    A, B, C, D = predicate.lst
    if cyl(A, B, C, D):
        eqa(A, D, C, D, C, B).totalConfirm(thname='параллельные прямые высекают одинаковые дуги на окружности. ',
                                           descr=f'{predicate.humanize()}, {cyl(A, B, C, D).humanize()}, параллельные прямые высекают одинаковые дуги на окружности, '
                                                 f'поэтому углы равны.', premises=[predicate, cyl(A, B, C, D)])
        return 1

def T16(predicate: eqa):
    """
    Первый признак подобия треугольника по двум углам.
    eqa(A, B, C, P, Q, R) if eqa(A, C, B, P, R, Q) and !col(A, B, C) => ctr(A, B, C, P, Q, R).
    """
    if not isinstance(predicate, eqa): return 0
    A, B, C, P, Q, R = predicate.lst
    if eqa(A, C, B, P, R, Q) and not col(A, B, C) and not col(P, Q, R):
        ctr(A, B, C, P, Q, R).totalConfirm(thname='первый признак подобия треугольника по двум углам',
                                           descr=f'{predicate.humanize()}, {eqa(A, C, B, P, R, Q).humanize()} => {ctr(A, B, C, P, Q, R).humanize()} по двум углам.',
                                           premises=[predicate, eqa(A, C, B, P, R, Q)])
        return 1

def T17(predicate: ort):
    """
    T17: Если в треугольнике медиана совпадает с высотой, то треугольник - равнобедренный. и ОМ явл биссектрисой.
    ort(O, M, A, B), if mdp(M, A, B): [eql(O, A, O, B), eqa(A, O, M, B, O, M)]
    ВОТ БЫ АНАЛОГИЧНО для БИССЕКТРИСЫ и вообще развернуть тему с р/б треугольником. ОПЯТЬ ТАКИ ПРО ОБЪЕКТ-декоратор ISOTRIANGLE.
    """
    if not isinstance(predicate, ort): return 0
    O, M, A, B = predicate.lst
    if mdp(M, A, B): pass

def T18(predicate: prl):
    """
    T18: свойство диагоналей пр-грамма.
    [prl(A, B, C, D) if prl(B, C, A, D) <=> mdp(х*, A, C)] => mdp(x*, B, D)
    """
    if isinstance(predicate, prl):
        A, B, C, D = predicate.lst
        if prl(B, C, A, D):
            for mP in Task.Instance().points:
                if mdp(mP, A, C):  # Примечательно, что здесь уже можно остановиться, поскольку середина уже найдена!
                    mdp(mP, B, D).totalConfirm(thname='свойство диагоналей параллелограмма',
                                               descr=f'две пары противоположных сторон попарно параллельны {A.n + B.n} ∥ {C.n + D.n}, {B.n + C.n} ∥ {A.n + D.n}, и одна из диагоналей'
                                                     f' точкой пересечения {mP.n} делятся пополам, то {mP.n} также является серединой второй диагонали {B.n + D.n}.',
                                               premises=[predicate, prl(B, C, A, D), mdp(mP, A, C)])
                    return 1
    return 0

def T19(predicate: prl):
    """
    временная сложность: ~О(2*P[ort])
    prl(fline, sline) * ort(fline | sline, xline) => ort(xline, sline | fline).
    я применяю двойной цикл, поскольку я не знаю, на какой позиции может быть общий элемент.
    """
    if isinstance(predicate, prl):
        thname = 'свойство перпендикулярных и параллельных прямых'
        for fline in predicate.sgm:
            for pred in [pred for pred in Task.Instance().predicates.get('ort', ()) if fline in pred.sgm]:
                xline = pred.another(fline)
                description = f'{fline} ∥ {predicate.another(fline).name} и ⊥ {xline.name}, тогда {predicate.another(fline).name} ⊥ {xline.name}'
                ort(*(xline.lst + predicate.another(fline).lst)).totalConfirm(thname, description, [predicate, pred])
        return 1
    return 0

def T20(predicate: eqr):
    """
    T20: второй признак подобия треугольников.
    [eqr(A, B, P, Q, A, C, P, R), if eqa(B, A, C, Q, P, R)] => ctr(A, B, C, P, Q, R) - треугольники подобны.
    Будем использовать алгебраический синоним eqr(A, B, P, Q, A, C, P, R): eqr(A, B, A, C, P, Q, P, R)
    """
    pass
    # if not isinstance(predicate, eqr): return 0
    # ratio1, ratio2 = predicate.sgm
    # results = []
    # # for ratio in predicate.sgm:
    # #     commonPoint = FindCommonFindUnique(ratio.sgm[0].lst, ratio.sgm[1].lst)
    # #     if not commonPoint: return 0
    # #     results.append(commonPoint)
    # A, P = results
    # B = [p for p in ratio1.sgm[0].lst if p != A][0]
    # C = [p for p in ratio1.sgm[1].lst if p != A][0]
    # Q = [p for p in ratio2.sgm[0].lst if p != P][0]
    # R = [p for p in ratio2.sgm[1].lst if p != P][0]
    # if not len((B, C, Q, R)) == len({B, C, Q, R}): return 0 # Все точки должны иметь разные имена
    # if eqa(B, A, C, Q, P, R):
    #     ctr(A, B, C, P, Q, R).totalConfirm(thname='второй признак подобия треугольников',
    #                                        descr=f'{predicate.humanize()}, {eqa(B, A, C, Q, P, R).humanize()} => {ctr(A, B, C, P, Q, R).humanize()}',
    #                                        premises=[predicate, eqa(B, A, C, Q, P, R)])
    #     return 1

def T21(predicate: cir):
    """
    cir(O, A, B, C) => <BCA = 1/2 <BOA (дуга ВА)
    <ABC = 1/2 <AOC; <BAC = 1/2 <BOC.
    Вписанный угол равен половине центрального угла, опирающегося на ту же хорду.
    """
    O, A, B, C = predicate.lst
    Relation(Angle(B, O, A), Angle(B, C, A), 2)
    Relation(Angle(A, O, C), Angle(A, B, C), 2)
    Relation(Angle(B, O, C), Angle(B, A, C), 2)
    return 1
'''
ABC, M, АВ = АС. 
mdp & Iso -> eqa, ort
ort & Iso -> mdp, eqa
eqa & Iso -> mdp, ort
'''
def T22(predicate: ort):
    # mdp(M, B, C) & ort(A, M, B, C) -> Iso
    A, M, B, C = predicate.lst
    if mdp(M, B, C): IsoTriangle.pointConstructor(B, C, vertex=A).totalConfirm(thname='признак р/б треугольника',
                                                  descr=f'Медиана {A.n+M.n} является и высотой, поэтому {A.n+B.n+C.n} - р/б треугольник.',
                                                  premises=[predicate, mdp(M, B, C)])

def T24(predicate: ort):
    # ort(A, M, B, C) & eqa -> Iso
    A, M, B, C = predicate.lst
    if not len(predicate.lst) == len(set(predicate.lst)): return
    if eqa(B, A, M, M, A, C): IsoTriangle.pointConstructor(B, C, vertex=A).totalConfirm(thname='признак р/б треугольника',
                                          descr=f'Высота {A.n+M.n} является и биссектрисой, поэтому {A.n+B.n+C.n} - р/б треугольник.',
                                          premises=[predicate, eqa(B, A, M, M, A, C)])
def T25(predicate: mdp):
    # mdp & eqa -> Iso
    M, B, C = predicate
    for mP in Task.getPoints(M, B, C):
        if eqa(B, mP, M, M, mP, C): IsoTriangle.pointConstructor(B, C, vertex=mP).totalConfirm(thname='признак р/б треугольника',
                                          descr=f'Медиана {mP.n+M.n} является и биссектрисой, поэтому {mP.n+B.n+C.n} - р/б треугольник.',
                                          premises=[predicate, eqa(B, mP, M, M, mP, C)])
        return 1


def TF1(figure: IsoTriangle):
    if not isinstance(figure, IsoTriangle): return 0
    A = figure.vertex
    B, C = figure.baseOfTriangle.lst
    for M in Task.getPoints(A, B, C):
        if mdp(M, B, C):
            for pred in (eqa(B, A, M, M, A, C), ort(A, M, B, C)):
                pred.totalConfirm(thname='медиана, проведенная к основанию является биссектрисой и высотой одновременно',
                                  descr=f'{figure.humanize()}',
                                  premises=[figure, mdp(M, B, C)])
            break
        if ort(A, M, B, C):
            for pred in (eqa(B, A, M, M, A, C), mdp(M, B, C)):
                pred.totalConfirm(thname='высота, проведенная к основанию является биссектрисой и медианой одновременно', descr=f'{figure.humanize()}',
                                  premises=[figure, ort(A, M, B, C)])
            break
        if eqa(B, A, M, M, A, C):
            for pred in (ort(A, M, B, C), mdp(M, B, C)):
                pred.totalConfirm(thname='биссектриса, проведенная к основанию является высотой и медианой одновременно', descr=f'{figure.humanize()}',
                                  premises=[figure, eqa(B, A, M, M, A, C)])
            break
    return 1