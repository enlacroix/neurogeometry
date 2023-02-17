from ng_solver.solver import run_solver
import numpy as np
from resources.problems import demo, problems_dict

np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)


def go_tests():
    """
    Функция для быстрого тестирования всех задач.
    """
    for value in problems_dict.values():
        print(run_solver(value))


'''
N - номер задачи, которую вы хотите решить из подготовленного демонабора.
С ним можно ознакомиться в файле problems.py из папки resources.
'''
N = 1
print(run_solver(demo(N)))
