from typing import Union
import pandas as pd

from utils import logger


class DeductiveDF:
    def __init__(self):
        self.table = pd.DataFrame(columns=['Правило', 'Описание', 'Предпосылки', 'Указатели на предпосылки', 'Факт'])
        self.table.index.name = 'Номера предикатов'

    def getPremises(self, index: int):
        try:
            return self.table['Указатели на предпосылки'][index]
        except KeyError:
            print(f'Ошибка! Указатели по индексу {index} для факта {self.getFact(index)} не удалось получить')
            return

    def __repr__(self): return str(self.table)

    def getDescriptionOfFact(self, index: int) -> str:
        """
        возвращает строку вида "предикат в понятной форме" + описание, которое ему соответствует.
        """
        return f'{self.getFact(index)}, поскольку ' + self.table['Описание'][index]

    def getTheorem(self, index: int) -> str:
        try:
            return self.table['Правило'][index]
        except KeyError:
            print(f'Правило c индексом {index} не найдено!')

    def getFact(self, index: int):
        try:
            return self.table['Факт'][index].humanize()
        except KeyError:
            print(f'Ошибка! Имя факта по индексу {index} не удалось получить. ')
            return

    def getFactIndex(self, fact_name) -> Union[int, None]:
        if fact_name is None: return None
        try:
            return self.table['Факт'][self.table['Факт'] == fact_name].index[0]
        except IndexError:
            logger(f'{fact_name.humanize()} не найден!')
            return

    def addString(self, lst):
        # 'Правило', 'Описание', 'Предпосылки', 'Указатели на предпосылки', 'Факт'
        self.table.loc[len(self.table.index)] = lst