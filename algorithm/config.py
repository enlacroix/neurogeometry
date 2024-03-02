from collections import namedtuple
evalMode = namedtuple('EvalMode', ['angle', 'segment', 'ratio', 'square'])

# Полное исследование задачи - убери question, если ответ найден исследование прекращается.
FULL_EXPLORATION = False
# Нужно ли добавлять фразочки в начале каждого предложения.
FUN = True
# Через сколько итераций алгоритм будет прекращен.
MAX_ITERS = 10
# Режим разработчика - будут ли печататься технические сообщения
DEVMODE = True
# Количество переменных в одной задаче равно VAR_LIMIT - 1. IndexError: list assignment index out of range - если такая штука, то поднимай VAR_LIMIT
VARIABLE_LIMIT = 51
# Записать дедуктивный датафрейм в csv файл или нет.
WRITE_DOWN_DF_TO_CSV = False
# Подключить вычислительный модуль к задаче (увеличивает время решения). Можно настроить каждый компонент отдельно.
EVALUATION_MODE = evalMode(angle=True, segment=True, ratio=False, square=False)
# Распечатать все факты, что есть в бд. (печатать логи о применении теорем в основной поток или нет).
CHAOS_MOD = False
# Подключать ли спорные модули, которые могут привести к багам.
BETA = False
# Сколько великолепных рекомендаций может получить пользователь
HOWMANYHINTS = 2