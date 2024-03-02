from functools import cached_property, reduce
import sympy as sp
import time
import itertools as it
from decoration.database import DeductiveDF
from utils import hum_list


class Task:
    _instance = None

    def __init__(self):
        """
        Каждый раз, когда мы вызовем инициализацию объекта класса Task, то
        """
        if not Task._instance:
            self.df = DeductiveDF()
            self.to_print = []
            self.previousPredicates = {}
            self.predicates = {'col': [], 'cyl': [], 'mdp': [], 'prl': [], 'ort': [], 'eqa': [], 'cir': [], 'ELA': [],
                               'eql': [], 'eqr': [], 'PRL': [], 'ORT': [], 'ctr': [], 'etr': [], 'citer': [], 'inter': []}
            self.start_time = time.time()
            self.statement = []  # Условие задачи в предикатной форме.
            self.question = None
            self.printed = []
            self.linangle_print = []
            # Блок 2а. Хранение геометрических объектов.
            self.points = []
            self.lines = []
            self.curves = []  # Массив "кривых", но только точек, принадлежащих одной окружности.
            self.figures = []
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
            self.REM = sp.Matrix() # Вычислительная матрица отношений (Ratio)
            self.prev_row_num_ratio = 0


    @classmethod
    def Instance(cls):
        if not cls._instance:
            cls._instance = Task()
        return cls._instance

    @classmethod
    def writeLA(cls, string):
        cls.Instance().linangle_print.append(string)



    @classmethod
    def DF(cls) -> DeductiveDF: return cls.Instance().df

    @classmethod
    def reload(cls): cls._instance = None

    @classmethod
    def getPoints(cls, *forbidden):
        return filter(lambda p: p not in forbidden, cls.Instance().points)

    def show_time(self): return round(time.time() - self.start_time, 3)

    def get_solution(self) -> str:
        """
        :return: решение задачи единой строкой с переносами строки в нужных местах.
        """
        return '\n<br>'.join(self.to_print) + f'\nЗадача была решена за {self.show_time()} секунд.'

    def getLAProof(self) -> str:
        return '\n<br>'.join(self.linangle_print) + f'\n Что и требовалось доказать.'

    def load_statement(self, pointList, problemCondition, question):
        """
        Альтернативная возможность загрузки условия в Task.
        """
        self.statement = problemCondition
        self.question = question
        self.points = pointList
        # add_string([None, 'это известно из условия.', None, None, pred])
        for pred in self.statement:
            pred.confirm()

    def post_processing(self):
        """
        Метод вызывается после итерации применения правил к условию задачи.
        1) возводит в квадрат предикат, которые при взаимодействии друг с другом могут дать новую информацию.
        Пример: две прямые параллельны третьей. Значит и исходные прямые параллельны между собой. Здесь зашиты аксиомы, которые не выносятся в правила Rules.
        2) аксиоматика для предикатов, которые утверждают о том, что точки принадлежат одной линии.
        Подробнее об этом можно прочитать в методе intersect()
        ВНИМАНИЕ: TRANSITIVE работает с предикатами, которые имеют ОДИНАКОВЫЙ тип. Т.е. prl ^ ort не обрабатываются!
        """
        self.predicates: dict
        for key in self.predicates:
            for predicatePair in it.combinations(self.predicates[key], 2):
                    predicatePair[0].transitive(predicatePair[1]) # Обратите внимание, что тип предикатов в паре - одинаковый.
        for curvePair in it.combinations(self.curves, 2): curvePair[0].intersect(curvePair[1])
        return 0

    def full_exploration(self) -> str:
        """
        Пользователь можно отдельно запросить "Полное исследование", для этого в config нужно поставить only_question = False.
        :return: строка, в которой отражены Все найденные соотношения между геометрическими объектами (не только нужные для построения решения).
        """
        report = 'Обнаруженные закономерности: <br> \n'
        for key, valList in self.predicates.items():
            if key != 'col':  # Слишком нудно выводить это. Уж слишком мал запрос в обществе на подобный контент.
                continue
            report += ', '.join(hum_list(valList)) + ';\n'
        return report

    @cached_property
    def numOfPredicates(self):
        return reduce(lambda prv, nxt: prv + nxt, (len(val) for val in self.predicates.values()))


    def deltaDict(self):
        """
        Вернуть словарь delta, который покажет как изменились длины контейнеров значений.
        """
        return {key: len(self.predicates[key]) - len(self.previousPredicates.get(key, ())) for key in self.predicates}

    # def predicates_to_dict(self) -> dict:
    #     """
    #     на основе self.predicates делает следующий словарь: ключи - тип предиката, значения: все предикаты, которые имеют данный класс.
    #     Для тестирований (и возможно для функции transitive_predicates).
    #     :return: словарь предикатов.
    #     """
    #     titles = [x.ttl for x in self.predicates]
    #     d = dict.fromkeys(titles)
    #     for k in d.keys():
    #         d[k] = []  # Каждому ключу нужно поставить УНИКАЛЬНЫЙ список со своим id.
    #     for t in d.keys():
    #         for p in self.predicates:
    #             if p.ttl == t:
    #                 d[t] += [p]
    #             else:
    #                 continue
    #     return d
