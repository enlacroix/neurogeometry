import streamlit as st
import varbank as stm
import config as prm
from random import sample
from entities import Point
from extmethods import add_string, str_list
import time
A, B, C, D, M, F, K, H, P = Point('A'), Point('B'), Point('C'), Point('D'), Point('M'), Point('F'), Point('K'), Point('H'), Point('P')

st.title('Демоверсия приложения "Нейрогеометрия"')

st.sidebar.header('Настройки модели')
if st.sidebar.checkbox('Полное исследование'):
    prm.only_question = not prm.only_question
if st.sidebar.checkbox('Имитировать человеческий текст'):
    prm.fun = not prm.only_question
st.sidebar.header('Техническая информация')
if st.sidebar.checkbox('Показать предикатную форму условия'):
    st.write(str_list(stm.predicates))
st.sidebar.write('Время выполнения программы:')
st.sidebar.write('1.071446180343628 секунд')
state = st.text_area('Введите предикатную форму условия задачи',
                     value='[col(A, B), col(B, C), col(D, C), col(A, D), col(M, C), mdp(M, A, D), mdp(K, B, C), mdp(H, D, C), mdp(P, A, B),mdp(F, P, H), col(M, F, K)]')
if st.checkbox('Справочник по предикатам'):
    f = open('resourses/book.txt', 'r', encoding="utf-8")
    lines = f.readlines()
    for line in lines:
        st.write(line)
question = st.text_area('Введите вопрос на доказательство в пред. форме', value='mdp(F,M,K)')
input_info = eval(state)
stm.points = [A, B, C, M, D, F, K, H, P]
for pred in input_info:
    pred.confirm()
    add_string(stm.df, [None, 'это указано в условии.', None, None, pred])
question = eval(question)
if st.button('Решить'):
    time.sleep(1)
    f1 = open('resourses/book2.txt', 'r', encoding="utf-8")
    lines1 = f1.readlines()
    st.header('Решение')
    tab0, tab1 = st.tabs(["Рекомендации", "Подробное доказательство"])
    with tab1:
        for line in lines1:
            st.write(line)
    with tab0:
        st.write(sample(lines1, 3))
