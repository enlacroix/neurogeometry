import streamlit as st
from random import sample
import config as cf
from deductive.solver import run_solver
from tskmanager import Task


st.title('Приложение "Нейрогеометрия"')

st.sidebar.header('Настройки модели')
if st.sidebar.checkbox('Полное исследование'): cf.FULL_EXPLORATION = True
if st.sidebar.checkbox('Имитация текста'): cf.FUN = False
if st.sidebar.checkbox('Ручной ввод точек'): PNTS = st.text_input('Введите точки, которые будут использованы в задаче: ', value='A, B, C, D, E, M, F, K, O')

age = st.sidebar.slider('Лимит переменных', 10, 200, 51)
iters_ = st.sidebar.slider('Максимальное количество итераций', 5, 15, 10)
option = st.sidebar.selectbox(
    'Метод решения',
    ('Прямой: дедуктивная последовательная обработка', 'Обратный: метод линейных углов', 'Хаотичный: печатай всё, что верно'))

st.sidebar.header('Техническая информация')
if st.sidebar.button('Предикатная форма условия'): st.write(Task.Instance().predicates)
if st.sidebar.button('Геометрические фигуры'): st.sidebar.write(Task.Instance().figures)
if st.sidebar.button('Прямые'): st.sidebar.write(Task.Instance().lines)

col1, col2 = st.columns(2)
with col1:
    STATE = st.text_area('Введите предикатную форму условия задачи', value='')
    options = st.multiselect(
        'Какие вычислительные матрицы вы хотите подключить?',
        ['Углы', 'Отрезки', 'Отношения', 'Площади'],
        ['Углы', 'Отрезки'])

if st.checkbox('Справка пользователя'):
    f = open('resources/book.txt', 'r', encoding="utf-8")
    lines = f.readlines()
    for line in lines:
        st.markdown(line)

with col2:
    QUEST = st.text_input('Введите вопрос на доказательство в пред. форме', value='')
    number = st.number_input('Оценка решения:', step=1, min_value=0, max_value=10)
    SOL = ''
    if len(STATE) != 0 and len(QUEST) != 0: SOL = run_solver([STATE, QUEST])
    resultOfSolution = st.button('Решить')


# streamlit run C:\Users\User\PycharmProjects\neurogeometry\algorithm\demo.py
if resultOfSolution:
    st.header('Решение')
    tab0, tab1, tab2 = st.tabs(["Подробное решение", "Рекомендации", "Метрики схожести"])
    with tab0:
        for elem in Task.Instance().to_print: st.write(elem)
        st.download_button('Скачать решение', SOL)
    with tab1:
        try:
            st.write(sample(Task.Instance().to_print, 3))
        except ValueError:
            st.write('Недостаточно образцов для формирования рекомендаций.')
    with tab2:
        st.write('схожесть с задачей - 20%')
