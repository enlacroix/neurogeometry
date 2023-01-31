import pandas as pd
import numpy as np
predicates = []
df = pd.DataFrame(columns=['Правило', 'Описание', 'Предпосылки', 'Указатели на предпосылки', 'Факт'])
df.index.name = 'Номера предикатов'
time = 0
to_print = []
# Блок 2. Хранение геометрических объектов.
points = []
lines = []  # Массив прямых (произвольное число точек)
angle_list = []
circ_lines = []  # Массив "кривых", но только точек, принадлежащих одной окружности.
angles = {}  # ключ: угол, значение: величина угла, дефолт None
segments = {}  # ключ: ОТРЕЗОК - ДВЕ ТОЧКИ, значение: его длина, дефолт None
# Блок 3. Хранение вычислительных матриц
N = 5  # Максимальное число допустимых переменных.
AEM = np.zeros((0, N))  # Angle Evaluation Matrix юыло 0 на первой позции
AEV = np.zeros((0, 1))
