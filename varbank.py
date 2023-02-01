import pandas as pd
import sympy as sp
import time
import itertools as it

# predicates = []
# df = pd.DataFrame(columns=['Правило', 'Описание', 'Предпосылки', 'Указатели на предпосылки', 'Факт'])
# df.index.name = 'Номера предикатов'
# time = 0
# to_print = []
# # Блок 2. Хранение геометрических объектов.
# points = []
# lines = []  # Массив прямых (произвольное число точек)
# angle_list = []
# circ_lines = []  # Массив "кривых", но только точек, принадлежащих одной окружности.
# angles = {}  # ключ: угол, значение: величина угла, дефолт None
# segments = {}  # ключ: ОТРЕЗОК - ДВЕ ТОЧКИ, значение: его длина, дефолт None
# # Блок 3. Хранение вычислительных матриц и векторов
# N = 5  # Максимальное число допустимых переменных.
# AEM = np.zeros((0, N))  # Angle Evaluation Matrix юыло 0 на первой позции
# AEV = np.zeros((0, 1))


class Task:
    def __init__(self):
        """
        Каждый раз, когда мы вызовем инициализацию объекта класса Task, то
        """
        self.df = pd.DataFrame(columns=['Правило', 'Описание', 'Предпосылки', 'Указатели на предпосылки', 'Факт'])
        self.df.index.name = 'Номера предикатов'
        self.to_print = []
        self.predicates = []
        # Может быть множество. метод add() на добавление.
        self.start_time = time.time()
        self.statement = []  # Условие задачи в предикатной форме.
        self.question = None
        # Блок 2а. Хранение геометрических объектов.
        self.points = []  # Сделал ранее массив точек множеством.
        self.lines = []
        self.curves = []  # Массив "кривых", но только точек, принадлежащих одной окружности.
        self.angles = []
        # Блок 2б. Хранение словарей, в которых по значению хранится величина угла/отрезка.
        self.angle_dict = {}
        self.segment_dict = {}  # ключ: ОТРЕЗОК - ДВЕ ТОЧКИ, значение: его длина, дефолт None
        # Блок 3. Хранение вычислительных матриц и векторов
        self.AEM = None  # Angle Evaluation Matrix
        self.AEV = None

    def reload(self):
        return self

    def show_time(self):
        return round(time.time() - self.start_time, 3)

    def get_solution(self) -> str:
        """
        :return: решение задачи единой строкой с переносами строки в нужных местах.
        """
        return '\n'.join(self.to_print) + f'\nЗадача была решена за {self.show_time()} секунд. Нейрогеометрия - качество и точка.'

    def load_statement(self):
        pass

    def post_processing(self):  # словарь сделан, но ты от него отказался
        """
        Метод вызывается после итерации применения правил к условию задачи.
        1) сталкивает между собой квадропредикаты, которые при взаимодействии друг с другом могут дать новую информацию.
        Пример: две прямые параллельны третьей. Значит и исходные прямые параллельны между собой. Здесь зашиты аксиомы, которые не выносятся в правила Rules.
        2) аксиоматика для предикатов, которые утверждают о том, что точки принадлежат одной линии. Подробнее об этом можно прочитать в методе intersect()
        """
        for p in it.combinations(self.predicates, 2):
            if p[0].ttl in ['eql', 'prl', 'ort'] and p[1].ttl in ['eql', 'prl', 'ort']:  # isinstance
                p[0].transitive(p[1])
        # Для правильной работы col и cyl.
        # TODO Воможный источник гадостей по типу бесконечной или очень долгого выполнения. На данный момент починено, но пусть пока будет "на карандаше"
        for ln in it.combinations(self.lines, 2):
            ln[0].intersect(ln[1])
        for ln in it.combinations(self.curves, 2):
            ln[0].intersect(ln[1])
        return 0

    def predicates_to_dict(self) -> dict:
        """
        на основе self.predicates делает следующий словарь: ключи - тип предиката, значения: все предикаты, которые имеют данный класс.
        Для тестирований (и возможно для функции transitive_predicates).
        :return: словарь предикатов.
        """
        titles = [x.ttl for x in self.predicates]
        d = dict.fromkeys(titles)
        for k in d.keys():
            d[k] = []
        for t in d.keys():
            for p in self.predicates:
                if p.ttl == t:
                    d[t] += [p]
                else:
                    continue
        return d


task = Task()
# Количество допустимых переменных.
N_ = 5