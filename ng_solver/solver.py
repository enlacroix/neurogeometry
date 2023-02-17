from decoration.printer import get_proof_text
from external import str_list, hum_list, logger
from ng_solver.rules import Rules
from inspect import signature
import config as cf
import varbank as vb
import itertools as it


from numerical.numodule import evaluate_angles, evaluate_segments
from statement import read_task


def proof():
    """
    proof() проводит прямой перебор правил (теорем), в качестве аргументов у нас комбинации из массива предикатов,
    на которых наложено требование о том, чтобы комбинации с предыдущей итерации не повторились на текущей.
    Правила в случае успешного выполнения добавляют в дедуктивный дф и массив предикатов новые значения.

    """
    prev_predicates = []
    rnd = 1
    prev_size = len(vb.task.statement)
    while True:
        evaluate_angles()
        evaluate_segments()
        for i, R in enumerate(Rules):
            logger(f'Идёт обработка правила {i + 1}...')
            for predcomb in it.combinations(vb.task.predicates, len(signature(R).parameters)):
                # Хотя бы один предикат из комбинации должен быть получен на предыдущей итерации, иначе эта комбинация предикатов не рассматривается.
                # Этот пункт спасает полное исследование, снижая время в два раза.
                if any([u not in prev_predicates for u in predcomb]):
                    if R(*predcomb):  # если успешно сработало, то возвращается 1.
                        logger(f'Предикаты:\n {str_list(vb.task.predicates)}')
            vb.task.post_processing()
        logger(f'Итерация {rnd} завершена.')
        rnd += 1
        logger(
            f'Размер предикатного массива. Предыдущая итерация: {prev_size}, Текущая: {len(vb.task.predicates)}, Прирост: {len(vb.task.predicates) - prev_size}')
        if prev_size == len(vb.task.predicates) or (cf.only_question and vb.task.question) or rnd > cf.supremum:
            logger('Формирование датафрейма завершено.')
            break
        else:
            prev_size = len(vb.task.predicates)
            prev_predicates = vb.task.predicates
    if cf.dev_mode:
        vb.task.df.to_csv('resources/geom.csv', encoding='utf-8')
    return 0


def run_solver(text: list) -> str:
    """
    Верховная функция, королева бала, пик этого айсберга, которая всё и запускает.
    :param text: text подаётся как список из двух элементов, содержащих условие (первый) и вопрос (второй) в предикатной форме.
    :return: текст решения единой строкой.
    """
    # Создаем "пустой" новый объект класса Task, когда запускаем процесс решения.
    vb.task = vb.Task.getInstance() # TODO Сюда бы отдельный метод для создания и обнуления списков, поскольку у меня нервный тик от скрытой инициализации Task(), которая очищает
    # датафреймы и предикаты. Пусть в __init__ лежит что-то незначительное.
    # Переводим условие на предикатный язык.
    statement, question = text
    read_task(statement, question)
    # Функция, формирующая дедуктивный датафрейм.
    proof()
    # Генерируем текст доказательства, используем функцию из модуля decorator.
    get_proof_text()
    # Выводим на экран/консоль.
    # print(vb.task.full_exploration())
    sol_text = vb.task.get_solution()
    vb.Task.reload()
    return sol_text
