"""
1. (ЕГЭ, 2018, Центр). В произвольном четырёхугольнике АВСD
2. (5 класс, но суровой машине не в курсе, что это просто).
Время выполнения: ~4.276 секунд
Используются методы: Подсчёт углов
Дан треугольник АВС. Проведена прямая МВ. Угол ВАС - 20 градусов, <MBC = 60 градусов, угол АСВ в три раза больше чем угол А.
Доказать, что АС параллельно МВ.
"""
# НЕ СТАВЬТЕ ТОЧКУ С ЗАПЯТОЙ В КОНЦЕ! Пожалуйста.
problems_dict = {
    1: [
        'col(A, B); col(B, C); col(D, C); col(A, D); mdp(M, A, D); mdp(K, B, C); mdp(H, D, C); mdp(P, A, B); mdp(F, P, H); col(M, F, K)',
        'mdp(F, M, K)'
        ],
    2: [
        'Triangle(A, B, C); col(M, B); SetValue(Angle(B, A, A, C), 20); SetValue(Angle(M, B, B, C), 60); Relation(Angle(A, C, C, B), Angle(B, A, A, C), 3)',
        'prl(A, C, M, B)'
        ],
    3: [
        'col(A, B); col(B, C); col(A, C); ort(A, C, C, B); mdp(M, A, B); col(C, M); col(E, C, B); col(M, E); mdp(E, C, B)',
        'ort(M, E, B, C)'
        ],

}


def demo(number: int):
    """
    :param number: Номер демонстрационной задачи из набора.
    :return:
    """
    return problems_dict[number]
