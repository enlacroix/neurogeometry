# import numpy as np
# np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
from collections import Counter

from educational.similarity import taskTheta
from ng_entities.segment import Segment
from predicates.fixpred import mdp
from predicates.freepred import col
from predicates.quadpred import *
from utils import stringifyDict, toStrAllElems
from statement import reading_points

O, A, B, C, M, D = reading_points('O, A, B, C, M, D')
# Line(D, M, O)
# ORT.q(A, C, D, M).confirm()
# print(bool(ort(O, M, C, A)))
#
# Line(D, M, O)
# ort(O, M, C, A).confirm()
# print(bool(ORT.q(A, C, D, M)))
#
# Line(O, A, B)
# Line(A, B, O)
# print(toStrAllElems(Task.Instance().lines))

predicateList = [mdp(M, A, B), mdp(D, A, C), ort(M, D, O, C)]


