import numpy as np
import sympy as sp
from entities import Angle, Triangle
from external import str_dict, str_list
from numerical.functors import Relation, SetValue
from predicates.freepred import col, cyl
from predicates.entpred import eqa, ctr, etr
from predicates.quadpred import prl, ort, eql
import varbank as vb
from statement import reading_points
import itertools as it
# np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
'''
Задача: Дан треугольник АВС. Проведена прямая МВ. Угол ВАС - 20 градусов, <MBC = 60 градусов, угол АСВ в три раза больше чем угол А. 
Доказать, что АС параллельно МВ.
# '''

# 1. Инициализация точек.
A, B, C, M = reading_points('A, B, C, M')
# 2. Распознавание геометрических объектов (e.g. треугольник)

# 3. Инициализация предикатов

# 4. Ввод численных значений.

# 5. Ввод численных отношений между значениями.

# 6. Инициализация вопроса.




