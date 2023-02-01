import varbank as vb
from ng_solver.solver import proof
from decoration.printer import get_proof_text
import numpy as np
from statement import read_task
from resources.problems import demo
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)


def run_solver(text):
    # Создаем "пустой" новый объект класса Task, когда запускаем процесс решения.
    vb.task = vb.Task() # TODO Сюда бы отдельный метод для создания и обнуления списков, поскольку у меня нервный тик от скрытой инициализации Task(), которая очищает
    # TODO датафреймы и предикаты. Пусть в __init__ лежит какая-то хрень
    # Переводим условие на предикатный язык.
    statement, question = text
    read_task(statement, question)
    # Функция, формирующая дедуктивный датафрейм.
    proof()
    # Генерируем текст доказательства, используем функцию из модуля decorator.
    get_proof_text()
    # Выводим на экран/консоль.
    return vb.task.get_solution()


print(run_solver(demo(1)))
