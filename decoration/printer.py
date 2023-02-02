import varbank as vb
from random import choice, randint
import config as cf

funny_phrases = ['Очевидно. ', 'Нетрудно заметить, что ', 'Легко видеть: ', 'Каждый советский школьник знал, что ']


def get_premises(index):
    try:
        return vb.task.df['Указатели на предпосылки'][index]
    except KeyError:
        return 'Ошибка! Указатели не удалось получить'


def send(string):
    """
    Функция, которая будет выводить факт пользователю, в случае успешного применения.
    :param string:
    :return:
    """
    vb.task.to_print.append(string)


def get_description(index):
    """
    40% - шанс выпадения "смешной" фразы.
    :param index:
    :return:
    """
    fin = vb.task.df['Факт'][index].humanize() + ', поскольку ' + vb.task.df['Описание'][index]
    if cf.fun and randint(1, 100) <= 40:
        return choice(funny_phrases) + fin
    return fin


def get_rule(index):
    try:
        return vb.task.df['Правило'][index]
    except KeyError:
        print('Правило не найдено!')


def get_fact(index):
    try:
        return vb.task.df['Факт'][index].humanize()
    except KeyError:
        return 'Ошибка! Имя теоремы не удалось получить. '


def add_string(lst):
    # 'Правило', 'Описание', 'Предпосылки', 'Указатели на предпосылки', 'Факт'
    vb.task.df.loc[len(vb.task.df.index)] = lst


def find_fact(fact_name):
    try:
        return vb.task.df['Факт'][vb.task.df['Факт'] == fact_name].index[0]
    except IndexError:
        print(f'{fact_name.humanize()} не найден!')


printed = []


def f(node):
    for child in get_premises(node):
        if get_premises(child) is None:
            send(get_description(child))
            continue
        elif child not in printed:
            send(f'~Докажем, что {get_fact(child)}, используя {get_rule(child)}:')
            printed.append(child)
            f(child)
    send(get_description(node))
    return 0


def get_proof_text():
    print(vb.task.df)
    start = find_fact(vb.task.question)
    send(f'Докажем, что {vb.task.question.humanize()}, используя {get_rule(start)}.')
    f(start)
    send('Что и требовалось доказать.')
