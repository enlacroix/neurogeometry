import statement as stm
from random import choice
from extmethods import find_fact
import parameters as prm
import streamlit as st

funny_phrases = ['Очевидно. ', 'Нетрудно заметить, что ', 'Легко видеть: ', 'Каждый советский школьник знал, что ',
                 'Из ясельного курса планиметрии, ', '']


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


def send(string):
    print(string)


printed = []


def f(node):
    for child in get_premises(node):
        if get_premises(child) is None:
            send(get_description(child))
            continue
        elif child not in printed:
            send(f'Докажем, что {get_fact(child)}, используя {get_rule(child)}:')
            printed.append(child)
            f(child)
    send(get_description(node))
    return 0


def print_proof(question):
    start = find_fact(stm.df, question)
    send(f'Докажем, что {question.humanize()}, используя {get_rule(start)}.')
    f(start)
    send('Что и требовалось доказать.')
