from backwardLA.strategy import LAReductor
from deductive.solver import run_solver
import numpy as np
from problems import DEMO_PROBLEMS
from tskmanager import Task

np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

'''
N - номер задачи, которую вы хотите решить из подготовленного демонабора.
С ним можно ознакомиться в файле problems.py из папки resources.
# DEMO_PROBLEMS.get(N, None)
'''
N = 4
# print(run_solver(('Line(A, B); Line(B, D); Line(B, M, C); ORT(Line(A, D), Line(B, C)); cyl(A, B, C, D)', 'mdp(M, B, C)')))
# LAReductor('[AD, BC]; [R]')
print(run_solver(DEMO_PROBLEMS.get(N, None)))