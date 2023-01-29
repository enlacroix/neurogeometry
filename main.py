import time
import varbank as stm
from ng_solver.solver import proof
import numpy as np
from decoration.printer import print_proof
from statement import question, input_info
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

start_time = time.time()

# Функция, формирующая дедуктивный датафрейм.
proof(question, [], len(input_info))

# Распечатываем доказательство, используем функцию из модуля decorator.
print_proof(question)

stm.time = time.time() - start_time
print(f'{stm.time} секунд')