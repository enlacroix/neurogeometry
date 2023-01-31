import time

import extmethods
import varbank as stm
from ng_solver.solver import proof
import numpy as np
from decoration.printer import generate_proof_text
from statement import question, input_info
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

start_time = time.time()

# Функция, формирующая дедуктивный датафрейм.
proof(question, [], len(input_info))

# Распечатываем доказательство, используем функцию из модуля decorator.
generate_proof_text(question)
print(extmethods.show_all())
stm.time = time.time() - start_time
print(f'{stm.time} секунд')