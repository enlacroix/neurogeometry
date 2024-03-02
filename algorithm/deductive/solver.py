import itertools
from decoration.printer import getProofText
from deductive.principles import principleApplying
from ng_entities.segment import Segment
from utils import logger, stringifyDict, stringifyList
from deductive.thdict import THEOREMS, FIGURE_THEOREMS
import config as cf
from numerical.numodule import totalEvaluation
from statement import read_task
from tskmanager import Task


def makeSegments():
    """
    Формирует всевозможные сочетания отрезков, обеспечивая коррекретность работы вычислительного модуля.
    """
    for line in Task.Instance().lines:
        for pointPair in itertools.combinations(line.lst, 2):
            Segment(*pointPair)


def proof():
    """
    proof() проводит прямой перебор правил (теорем), в качестве аргументов у нас комбинации из массива предикатов,
    на которых наложено требование о том, чтобы комбинации с предыдущей итерации не повторились на текущей.
    Правила в случае успешного выполнения добавляют в дедуктивный дф и массив предикатов новые значения.

    """
    solverIteration = 1
    previousSize = len(Task.Instance().statement)
    while solverIteration < cf.MAX_ITERS:
        makeSegments()
        principleApplying()
        totalEvaluation(cf.EVALUATION_MODE)
        for predTitle, predicateList in Task.Instance().predicates.items():
            for theorem, predicate in itertools.product(THEOREMS.get(predTitle, ()), predicateList):
                theorem(predicate)
        for figureTheorem, figure in itertools.product(FIGURE_THEOREMS, Task.Instance().figures): figureTheorem(figure)
        Task.Instance().post_processing()
        logger(f'Прирост предикатов на итерации {solverIteration}: {Task.Instance().deltaDict()}')
        logger(stringifyDict(Task.Instance().predicates))
        logger(stringifyList(Task.Instance().figures))
        solverIteration += 1
        Task.Instance().previousPredicates = Task.Instance().predicates.copy()
        if previousSize == Task.Instance().numOfPredicates or (not cf.FULL_EXPLORATION and Task.Instance().question):
            logger('Формирование датафрейма завершено.')
            break
        else:
            previousSize = Task.Instance().numOfPredicates
    if cf.WRITE_DOWN_DF_TO_CSV:
        logger('Датафрейм был записан в файл!')
        Task.Instance().df.to_csv('resources/geom.csv', encoding='utf-8')
    return 0


def run_solver(text: tuple) -> str:
    """
    Верховная функция, королева бала.
    TODO запрос к полным углам
    todo сравнение с конструкциями
    todo допточки?
    :return: текст решения единой строкой.
    """
    if text is None: return 'Условие и вопрос задачи не загружены.'
    # Создаем "пустой" новый объект класса Task, когда запускаем процесс решения.
    Task.reload()  # Обнуление статической переменной
    # Переводим условие на предикатный язык.
    statement, question = text
    read_task(statement, question)
    # Функция, формирующая дедуктивный датафрейм.
    proof()
    # Генерируем текст доказательства, используем функцию из модуля decorator.
    getProofText()
    # Выводим на экран/консоль.
    if cf.FULL_EXPLORATION: Task.Instance().full_exploration()
    return Task.Instance().get_solution()
