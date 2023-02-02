from ng_solver.solver import run_solver
import numpy as np
from resources.problems import demo

np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

# N - номер задачи, которую вы хотите решить из подготовленного демонабора. С ним можно ознакомиться в файле demo.py.
N = 3
print(run_solver(demo(N)))
