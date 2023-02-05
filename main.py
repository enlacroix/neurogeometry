from ng_solver.solver import run_solver
import numpy as np
from resources.problems import demo

np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

# N - номер задачи, которую вы хотите решить из подготовленного демонабора. С ним можно ознакомиться в файле problems.py из папки resources.
N = 2
print(run_solver(demo(N)))


'''
Имитация непрерывного ввода данных с сайта. Задачи корректно обрабатываются в одном "запуске". 
while True:
    N = int(input())
    if demo(N) == -1:
        break
    print(run_solver(demo(N)))
'''