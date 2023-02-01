"""
1. (ЕГЭ, 2018, Центр). В четырёхугольнике АВСD
"""

problems_dict = {
    1: ['col(A, B); col(B, C); col(D, C); col(A, D); col(M, C); mdp(M, A, D); mdp(K, B, C); mdp(H, D, C); mdp(P, A, B); mdp(F, P, H); col(M, F, K)',
        'mdp(F, M, K)'
        ],

}

def demo(number):
    return problems_dict[number]