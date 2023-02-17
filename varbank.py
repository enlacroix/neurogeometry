import pandas as pd
import sympy as sp
import time
import itertools as it
from external import str_dict, hum_list

# Количество переменных в одной задаче равно VAR_LIMIT - 1.
VAR_LIMIT = 50


# IndexError: list assignment index out of range - если такая штука, то поднимай VAR_LIMIT


class Task:
    _instance = None

    def __init__(self):
        """
        Каждый раз, когда мы вызовем инициализацию объекта класса Task, то
        """
        if not Task._instance:
            self.df = pd.DataFrame(columns=['Правило', 'Описание', 'Предпосылки', 'Указатели на предпосылки', 'Факт'])
            self.df.index.name = 'Номера предикатов'
            self.to_print = []
            self.predicates = []
            # Может быть множество. метод add() на добавление.
            self.start_time = time.time()
            self.statement = []  # Условие задачи в предикатной форме.
            self.question = None
            # Блок 2а. Хранение геометрических объектов.
            self.points = []  # Сделать ранее массив точек множеством.
            self.lines = []
            self.curves = []  # Массив "кривых", но только точек, принадлежащих одной окружности.
            # Блок 2б. Хранение словарей, в которых по значению хранится величина угла/отрезка.
            self.angles = []
            self.segments = []
            # Из списков выше НИКОГДА нельзя удалять элементы и сбивать порядок индексов.
            self.angle_dict = {}
            self.segment_dict = {}  # ключ: ОТРЕЗОК - только ДВЕ ТОЧКИ, значение: его длина, дефолт None
            # Блок 3. Хранение вычислительных матриц и векторов
            self.AEM = sp.Matrix()  # Angle Evaluation Matrix - хранение коэффицентов СЛУ для углов
            self.prev_row_num_ang = 0  # Параметр, который используется, для остановки избыточных расчётов.
            self.SEM = sp.Matrix()
            self.prev_row_num_seg = 0
        else:
            print('Объект Task уже был создан.')

    @classmethod
    def getInstance(cls):
        if not cls._instance:
            cls._instance = Task()
        return cls._instance

    @classmethod
    def reload(cls):
        cls._instance = None

    def show_time(self):
        return round(time.time() - self.start_time, 3)

    def get_solution(self) -> str:
        """
        :return: решение задачи единой строкой с переносами строки в нужных местах.
        """
        return '\n'.join(
            self.to_print) + f'\nЗадача была решена за {self.show_time()} секунд.'

    def load_statement(self):
        """
        альтернативная возможность загрузки условия в Task.
        """
        pass

    def post_processing(self):  # словарь сделан, но ты от него отказался
        """
        Метод вызывается после итерации применения правил к условию задачи.
        1) сталкивает между собой квадропредикаты, которые при взаимодействии друг с другом могут дать новую информацию.
        Пример: две прямые параллельны третьей. Значит и исходные прямые параллельны между собой. Здесь зашиты аксиомы, которые не выносятся в правила Rules.
        2) аксиоматика для предикатов, которые утверждают о том, что точки принадлежат одной линии. Подробнее об этом можно прочитать в методе intersect()
        ВНИМАНИЕ: TRANSITIVE работает с предикатами, которые имеют ОДИНАКОВЫЙ тип. Т.е. prl ^ ort не обрабатываются!
        """
        '''
        Эта реализация даёт лишних 0.6 секунд выполнения программы из-за громоздкости. 
        boss = self.predicates_to_dict()
        for ttl in boss.keys():
            if ttl in ['eql', 'prl', 'ort']:
                for pair in it.combinations(boss[ttl], 2):
                    pair[0].transitive(pair[1])
        '''
        for p in it.combinations(self.predicates, 2):
            white_list = ['eql', 'prl', 'ort', 'eqa']
            if p[0].ttl in white_list and p[1].ttl in white_list:  # isinstance, но придётся импортировать
                p[0].transitive(p[1])
        # Для правильной работы col и cyl.
        # TODO Воможный источник гадостей по типу бесконечной или очень долгого выполнения. На данный момент починено, но пусть пока будет "на карандаше"
        for ln in it.combinations(self.lines, 2):
            ln[0].intersect(ln[1])
        for ln in it.combinations(self.curves, 2):
            ln[0].intersect(ln[1])
        return 0

    def full_exploration(self) -> str:
        """
        Пользователь можно отдельно запросить "Полное исследование", для этого в config нужно поставить only_question = False.
        :return: строка, в которой отражены Все найденные соотношения между геометрическими объектами (не только нужные для построения решения).
        """
        boss = self.predicates_to_dict()
        report = 'Обнаруженные закономерности: \n'
        for key in boss.keys():
            if key in ['col',
                       'cyl']:  # Слишком нудно выводить это. Уж слишком мал запрос в обществе на подобный контент.
                continue
            report += ', '.join(hum_list(boss[key])) + ';\n'
        return report

    def predicates_to_dict(self) -> dict:
        """
        на основе self.predicates делает следующий словарь: ключи - тип предиката, значения: все предикаты, которые имеют данный класс.
        Для тестирований (и возможно для функции transitive_predicates).
        :return: словарь предикатов.
        """
        titles = [x.ttl for x in self.predicates]
        d = dict.fromkeys(titles)
        for k in d.keys():
            d[k] = []  # Каждому ключу нужно поставить УНИКАЛЬНЫЙ список со своим id.
        for t in d.keys():
            for p in self.predicates:
                if p.ttl == t:
                    d[t] += [p]
                else:
                    continue
        return d


task = Task()
