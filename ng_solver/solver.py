from external import str_list, hum_list
from ng_solver.rules import Rules
from inspect import signature
import config as cf
import varbank as vb
import itertools as it

# TODO print() заменить на log(), функция, отмечающая технические моменты, которые можно запросить с веб-приложения. Но это не точно.



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
        for i, R in enumerate(Rules):
            print(f'Идёт обработка правила {i}...')
            for predcomb in it.combinations(vb.task.predicates, len(signature(R).parameters)):
                # Хотя бы один предикат из комбинации должен быть получен на предыдущей итерации, иначе эта комбинация предикатов не рассматривается.
                # Этот пункт спасает полное исследование, снижая время в два раза.
                if any([u not in prev_predicates for u in predcomb]):
                    R(*predcomb)
            vb.task.post_processing()
            # print(str_list(task.lines)) str_list(task.angles) потом
            #print('Предикаты:\n', str_list(vb.task.predicates))
        print(f'Итерация {rnd} завершена.')
        rnd += 1
        print(f'Размер предикатного массива. Предыдущая итерация: {prev_size}, Текущая: {len(vb.task.predicates)}, Прирост: {len(vb.task.predicates) - prev_size}')
        if prev_size == len(vb.task.predicates) or (cf.only_question and vb.task.question) or rnd > cf.supremum:
            print('Формирование датафрейма завершено.')
            break
        else:
            prev_size = len(vb.task.predicates)
            prev_predicates = vb.task.predicates
    vb.task.df.to_csv('resources/geom.csv', encoding='utf-8')
    return 0



