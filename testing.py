import numpy as np
import sympy as sp
from entities import Angle, Line
from external import str_dict, str_list, hum_dict
from numerical.functors import Relation, SetValue
from predicates.fixpred import cir, mdp
from predicates.freepred import col, cyl
from predicates.entpred import eqa, ctr, etr
from predicates.quadpred import prl, ort, eql
import varbank as vb
from statement import reading_points
import itertools as it

np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

O, A, B, C = reading_points('O, A, B, C')


