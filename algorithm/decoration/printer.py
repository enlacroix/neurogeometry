from utils import logger
from tskmanager import Task


def send(string):
    """
    Функция, которая будет выводить факт пользователю, в случае успешного применения.
    Именно атрибут to_print будет передаваться на сервер.
    """
    # print(string)
    Task.Instance().to_print.append(string)

# class SolutionPrinter:
#     # Todo использовать html разметку для списков, жирного шрифта и т.д.
#     def __init__(self):
#         pass


def f(nodeIndex: int):
    if Task.Instance().df.getPremises(nodeIndex)[0] is None: return
    for childIndex in Task.Instance().df.getPremises(nodeIndex):
        if Task.Instance().df.getPremises(childIndex) is None:
            send(Task.Instance().df.getDescriptionOfFact(childIndex))
            continue
        elif childIndex not in Task.Instance().printed:
            send(f'<b>Докажем</b>, что {Task.Instance().df.getFact(childIndex)}, используя <i>{Task.Instance().df.getTheorem(childIndex)}</i>.')
            Task.Instance().printed.append(childIndex)
            f(childIndex)
    send(Task.Instance().df.getDescriptionOfFact(nodeIndex))
    return 0


def getProofText():
    """
    Режим хаоса: когда нельзя восстановить взаимосвязь между утверждениями, но вопрос есть в множестве предикатов, то распечатай всё что есть.
    """
    logger(Task.Instance().df)
    start = Task.Instance().df.getFactIndex(Task.Instance().question)
    if start is None:
        send(f'Программе не удалось доказать, что {Task.Instance().question.humanize()}...')
        return
    send(f'<b>Докажем</b>, что {Task.Instance().question.humanize()}, используя {Task.Instance().df.getTheorem(start)}.')
    f(start)
    send('Что и требовалось доказать.')
