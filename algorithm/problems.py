"""
Правила ввода:
- Команды вводится через точку с запятой с пробелом после. После последней команды точка с запятой не ставится.
-
"""

DEMO_PROBLEMS = {
    1: (
        'Quadrangle(A, B, C, D); mdp(M, A, D); mdp(K, B, C); mdp(H, D, C); mdp(P, A, B); mdp(F, P, H); Line(M, F, K)',
        'mdp(F, M, K)'
        ),
    2: (
        'Triangle(A, B, C); Line(M, B); SetValue(Angle(B, A, C), 20); SetValue(Angle(M, B, C), 60); Relation(Angle(A, C, B), Angle(B, A, C), 3)',
        'prl(A, C, M, B)'
        ),
    3: (
        'Triangle(A, B, C); ort(A, C, C, B); mdp(M, A, B); Line(C, M); Line(E, C, B); Line(M, E); mdp(E, C, B)',
        'ort(M, E, B, C)'
        ),
    4: (
        'Triangle(A, B, C); SetValue(Segment(A, M), 4); Relation(Segment(A, M), Segment(A, B), 2); Sum((Segment(A, B), Segment(A, C), Segment(B, C)), 12); mdp(M, A, C)',
        'ort(B, M, A, C)'
        ),
    5: (
        'Line(A, B, C); SetValue(Segment(A, M), 8); SetValue(Segment(A, B), 6); SetValue(Segment(B, C), 2)',
        'eqa(A, M, C, A, C, M)'
        ),

}



