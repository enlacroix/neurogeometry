from __future__ import annotations
from ng_entities.entpoint import Point
from ng_entities.segment import Segment
from tskmanager import Task
from utils import FindCommonFunction, coproduction, logger


class Line:
    """
    Класс Прямая - фундаментальная сущность для всей программы. Прямая является объединением точек, но в отличие от col(), является
    упорядоченной структурой и пытается отразить реальную структуру точек на чертеже.
    Данный класс реализует главную аксиому планиметрии: через две точки проходит прямая и притом только одна.
    FC(l1, l2) - функция, находящая общие точки у двух прямых. Если её значение > 1, то в список прямых Task() новая прямая не попадёт, а если в ней
    есть новые точки, то добавь их в уже существующую прямую согласно правилам непротиворечивости и копродукции.
    """
    def __init__(self, *lst):
        """
        Будет только одна прямая в списке Task(), для которой FC > 1, поскольку иную ситуацию построенный мной конструктор не допустит.
        """
        self.lst = list(lst)
        self.name = ''.join((p.n for p in self.lst))
        assert len(self.lst) == len(set(self.lst)), f'Внимание, нарушено правило - все точки прямой должны быть уникальны для {self.name}!'
        # if len(self.lst) != len(set(self.lst)): print(f'Внимание, нарушено правило - все точки прямой должны быть уникальны для {self.name}!')

        flagNotFoundSimilarLine = True
        for line in Task.Instance().lines:
            if FindCommonFunction(self.lst, line.lst).logic:
                flagNotFoundSimilarLine = False
                line.coproduction(self)
                break
        if flagNotFoundSimilarLine:
            Task.Instance().lines.append(self)
            # if len(self.lst) == 2 and self not in Task.Instance().segments:
            #     print(f'я из лайна: {self}')
            #     Task.Instance().segments.append(self)

    def entry(self) -> Line:
        """
        Точка доступа к "истинной" прямой, хранящейся в списке Task. Все методы должны вызываться от прямой, возвращаемой entry().
        Пример: Прямая АВ часть уже созданной прямой АВС, и мы хотим распечатать оригинальную прямую.
        Line(A, B).entry().humanize() -> Line(A, B, C).humanize() -> пр. АВС.
        """
        return next((line for line in Task.Instance().lines if FindCommonFunction(self.lst, line.lst).logic), self)

    def coproduction(self, other: Line):
        """
        как ключи временного словаря (неизменяемый тип, и т.д.).
        Операция некоммунитативная.
        соседи А? - В и пустое.
        соседи В? - А и С
        соседи С? - В.
        ANBF & ABC = ABCNF (по сформулированной логике). Однако тот факт, что не указали точку N между А и В навевает на мысль, что это копроизведение
        должно завершиться выводом None. МЫ НЕ ДОПОЛНЯЕМ ИНФОРМАЦИЮ, А ВНОСИМ ПРОТИВОРЕЧИЕ, КОТОРОЕ ВОЗМОЖНО БЫЛО ИЗБЕЖАТЬ.
        H_АВ_TС & KANBTF = HKANBTFC. всё, что является соседями во втором аргументе останется ими в результате. Мы ищем, как дополнить точками из первого аргумента,
        (пример - С), чтобы а) сохранить форму второго, б) точки не должны "перепрыгивать" через своего соседа. они не могут оказаться левее, чем раньше.
        Это не ошибка(только тест)! ('BMC', 'BC') нарушают правило согласования точек - пример нарушения правила.
        """
        if self == other: return # копродукция одинаковых по множеству прямых бесполезна
        newLineLst = coproduction(self.lst, other.lst)
        if not newLineLst:
            # external.logger(f'Это не ошибка(только тест)! {self.name, other.name} нарушают правило согласования точек.')
            return
        Task.Instance().lines.remove(self)
        if other in Task.Instance().lines: Task.Instance().lines.remove(other)
        Line(*newLineLst)

    def __repr__(self): return self.name

    def humanize(self):
        """ если метод __str__ представляет отладочную информацию, то humanize() формирует запись, понятную человеку. """
        return 'отр. ' + str(self)

    def __eq__(self, other):
        """
        АВС != АСВ, т.к. важен порядок точек.
        АВ = ВА, если речь идёт об отрезках
        """
        return set(self.lst) == set(other.lst)

    def strictEq(self, other): return self.lst == other.lst

    def __contains__(self, item):
        return item in self.lst


    def getIndex(self):
        assert len(self.lst) == 2, f'Был вызван метод отрезка getIndex для прямой {self}, состоящей не из двух точек! '
        return Segment(*self.lst).getIndex()

    def getValue(self):
        assert len(self.lst) == 2, f'Был вызван метод отрезка getValue для прямой {self}, состоящей не из двух точек! '
        return Segment(*self.lst).getValue()

    def __hash__(self):
        return hash(self.lst[0]) ^ hash(self.lst[1])
        # todo Line теперь не только из двух точек, но она применяется только при двухточечных Line при сравнении предикатов. Так что все нормально?

    # def intersect(self, other):
    #     """
    #     Метод, обеспечивающий корректную работу предиката col(), который обобщает правило о:
    #     col(A, B, D) ^ col(C, B, D) = col(A, C) or col(A, C, B, D)
    #     :param other: другой объект класса Line.
    #     :return: None, если у прямых нет точек пересечения (о которых знает программа); точку пересечения, если прямые действ разные и пересеклись;
    #     Если точек пересечения больше двух, то эти прямые принадлежат одной единой прямой, которая и добавляется в массив lines.
    #     """
    #     eps = set(self.lst)
    #     phi = set(other.lst)
    #     if len(eps & phi) > 1:
    #         # vb.task.lines.remove(self)
    #         # vb.task.lines.remove(other)
    #         # TODO опасное удаление self и other, поскольку они уже не несут полезной информации.
    #         # Это закомментировано, поскольку неизвестно, как lines будет применяться для вычислительного модуля.
    #         # Удаление может нарушить порядок индексов.
    #         Line(*list(eps | phi))
    #         # Всякий раз, когда мы инициализируем линию, то она УЖЕ добавляется в список.
    #         return 0
    #     elif len(eps & phi) == 1:
    #         return Point(str(*list(eps & phi)))  # Единственная точка пересечения двух прямых