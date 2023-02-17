"""
1. (ЕГЭ, 2018, Центр). В произвольном четырёхугольнике АВСD ~2.052 секунд
2. (5 класс, но суровой машине не в курсе, что это просто).
Время выполнения: ~4.276 секунд
Используются методы: Подсчёт углов
Дан треугольник АВС. Проведена прямая МВ. Угол ВАС - 20 градусов, <MBC = 60 градусов, угол АСВ в три раза больше чем угол А.
Доказать, что АС параллельно МВ.
3. ~0,029 сек
"""
# НЕ СТАВЬТЕ ТОЧКУ С ЗАПЯТОЙ В КОНЦЕ! Пожалуйста.
problems_dict = {
    1: [
        'Quadrangle(A, B, C, D); mdp(M, A, D); mdp(K, B, C); mdp(H, D, C); mdp(P, A, B); mdp(F, P, H); col(M, F, K)',
        'mdp(F, M, K)'
        ],
    2: [
        'Triangle(A, B, C); col(M, B); SetValue(Angle(B, A, A, C), 20); SetValue(Angle(M, B, B, C), 60); Relation(Angle(A, C, C, B), Angle(B, A, A, C), 3)',
        'prl(A, C, M, B)'
        ],
    3: [
        'Triangle(A, B, C); ort(A, C, C, B); mdp(M, A, B); col(C, M); col(E, C, B); col(M, E); mdp(E, C, B)',
        'ort(M, E, B, C)'
        ],
    4: [
        'Triangle(A, B, C); SetValue(Line(A, M), 4); Relation(Line(A, M), Line(A, B), 2); Sum((Line(A, B), Line(A, C), Line(B, C)), 12); mdp(M, A, C)',
        'ort(B, M, A, C)'
        ],

}


def demo(number: int):
    """
    :param number: Номер демонстрационной задачи из набора.
    :return:
    """
    try:
        return problems_dict[number]
    except KeyError:
        print('Введён неверный номер задачи!')
        return -1

