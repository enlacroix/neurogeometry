import pandas as pd
points = []
predicates = []
df = pd.DataFrame(columns=['Правило', 'Описание', 'Предпосылки', 'Указатели на предпосылки', 'Факт'])
df.index.name = 'Номера предикатов'
time = 0