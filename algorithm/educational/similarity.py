"""
Метрики оценки схожести задач друг с другом.
"""
from collections import Counter


def taskTheta(mytask, construct):
    """
    Геометрическая задача задаётся четырьмя множествами - P, F, C, Q - предикаты, фигуры, вычислительные функторы и вопрос(-ы).
    Sim = Norm[alpha*p1(F1, F2) + beta*p2(P1, P2) + gamma*(типы вопросов совпадают?, p2-3(Q1, Q2)) + очень малый вклад вычислительных функторов еps*р3(C1, C2)]
    Альфа=0,6, бета=0,24, гамма=0,15, эпсилон=0,01 - настраиваемые параметры, однако наибольшее внимание нужно обратить на альфа, потом на бета и т.п.
    Их сумма равна 1. Совпадение фигур почти сразу сигнализирует о совпадении конструкций, тип вопроса тоже важен, если мы хотим найти идею для док-ва.
    """
    return 0.6 * figureTheta(mytask.figures, construct) + 0.45 * predicateTheta(mytask.statement, construct)

def figureTheta(f1, construct):
    """
    схожесть фигур. Проверяется совпадение имен. (не учитываем сущности и примитивы, i.e. Line и обычный Triangle)
    Counter(figures): Triangles: 3. Circles: 2. Если кол-ва совпали, то это значительно увеличивает баллы метрики.
    """
    score = 0
    cnt1 = Counter([pred.__class__.__name__ for pred in f1])
    cnt2 = Counter([pred for pred in construct.split('; ')])
    set1, set2 = set(cnt1.keys()), set(cnt2.keys())
    intersection = set1 & set2
    if len(intersection) == 0: return 0
    for simKey in intersection:
        if abs(cnt1[simKey] - cnt2[simKey]) <= 2:
            score += 1 / len(intersection) ** 2
        else:
            score -= 1 / len(intersection) ** 2
    return score

def predicateTheta(p1: list, construct: str):
    """
    Схожести предикатов. Ранее мы определяли свободный/несвободный предикат.
    (A, B, C, D, A, B) > (X, Y, Y, Z) < (A, B, C, D) < (A, B, C, D, E, F). -> легче всего построить биекцию: больше числитель, меньше знаменатель.
    Выбираем "несвободный" предикат и пытаемся построить биекцию, потом подставляем результаты в другие предикаты (проводим альфа-конверсию), смот
    если такого предиката такого же типа нет, то переходим к следующему по несвободности.
    1: mdp(M, B, C); eql(B, M, M, A); ort(B, C, C, A). в прямоугольном треугольнике провели медиану к гипотенузе
    2: ort(M, K, K, N); ort(K, H, M, N). в прямоугольном треугольнике провели высоту к гипотенузе.
    """
    score = 0
    cnt1 = Counter([pred.ttl for pred in p1])
    cnt2 = Counter([pred for pred in construct.split('; ')])
    set1, set2 = set(cnt1.keys()), set(cnt2.keys())
    intersection = set1 & set2
    if len(intersection) == 0: return 0
    for simKey in intersection:
        if abs(cnt1[simKey]-cnt2[simKey]) <= 2:
            score += 1 / len(intersection) ** 2
        else:
            score -= 1 / len(intersection) ** 3
    return score


# def functorsTheta(c1, c2):
#     """
#     Cхожесть вычислительных функторов. У них есть тип операндов (с чем они работают: углы, отрезки, отношения, площади).
#     Оценить схожесть типов (если в двух задачах сказано о сумме углов = 120 градусам, то они чем-то похожи).
#     """
#     pass

def questionsTheta(q1, q2):
    """
    Проверяется совпадение типов вопроса можно натолкнуть на верные мысли о доказательстве
    (доказательство перпендикулярности в обоих задачах делает их похоже друг на друга).
    """
    return 1 if q1.ttl == q2.ttl else 0