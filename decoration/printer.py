import varbank as stm
from random import choice
from extmethods import find_fact, send
import config as prm

funny_phrases = ['Очевидно. ', 'Нетрудно заметить, что ', 'Легко видеть: ', 'Каждый советский школьник знал, что ']


def get_premises(index):
    return stm.df['Указатели на предпосылки'][index]


def get_description(index):
    fin = stm.df['Факт'][index].humanize() + ', поскольку ' + stm.df['Описание'][index]
    if prm.fun:
        return choice(funny_phrases) + fin
    return fin


def get_rule(index):
    return stm.df['Правило'][index]


def get_fact(index):
    return stm.df['Факт'][index].humanize()




printed = []


def f(node):
    for child in get_premises(node):
        if get_premises(child) is None:
            send(get_description(child))
            continue
        elif child not in printed:
            send(f'  Докажем, что {get_fact(child)}, используя {get_rule(child)}:')
            printed.append(child)
            f(child)
    send(get_description(node))
    return 0


def generate_proof_text(question):
    start = find_fact(stm.df, question)
    send(f'1. Докажем, что {question.humanize()}, используя {get_rule(start)}.')
    f(start)
    send('Что и требовалось доказать.')
