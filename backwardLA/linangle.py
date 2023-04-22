from ng_entities.entline import Line


class LinAngle:
    """
    Линейный угол - абстрактное представление угла между двумя прямыми(!) (не отрезками) (будем обозначать их u и v). Сам угол обозначается так: ∠[u, v].
    Два линейных угла ∠[u, v], ∠[m, k] считаются равными, если существует такой поворот R, что R(u) ∥ m && R(v) ∥ k.
    Линейный угол с заданной бинарной операцией сложения образует группу.
    Операция сложения (дальше будем называть её редукцией) задается следующим образом:
    ∠[u, w] + ∠[w, v] = ∠[u, v]
    Нейтральный элемент в данном случае это угол ∠[v, v], т.е. 0 или 180 градусов в зависимости от направления обхода.
    Дальнейшую информацию по линейным углам можно прочитать в руководстве.
    _______________________________________
    если зафиксировать поворот против чс, по ч.с.?
    второй признак подобия трп?
    LA().value = MIN(value, 180 - value). Выбирать такое напр обхода?
    Но это неправильно по отношению к тупым углам, мб давать им метку, что они - тупые?
    """
    def __init__(self, line1: Line, line2: Line):
        self.x, self.y = line1.entry(), line2.entry()
        self.components = (self.x, self.y)

    def __repr__(self): return f'∠[{self.x}, {self.y}]'

    def __hash__(self):
        """
        Хеширование необходимо, чтобы использовать линейные углы, как ключи в словаре подстановок.
        Для хеширования критичен порядок аргументов, поэтому мы передаем в хэш-функцию кортеж, а не побитовое пр-ние аргументов.
        """
        return hash((self.x, self.y))

    def __add__(self, other):
        if isinstance(other, NeutralLA): return self
        if self.y == other.x: return LinAngle(self.x, other.y)
        return False

    def __neg__(self): return LinAngle(self.y, self.x)

    def __sub__(self, other):
        return self + (-other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        """
        оператор != вернёт правду, если ∠[u, v] = ∠[v, u]
        """
        return self.x, self.y == other.y, other.x

    def checkDegeneration(self) -> bool:
        """
        Проверка вырождения линейного угла. Если в результате преобразований его компоненты равны, то такой угол равен 0 (нейтральному)
        """
        return self.x == self.y


class NeutralLA:
    def __init__(self, oneline=None):
        self.x, self.y = oneline, oneline
    def __add__(self, other): # self + other
        return other
    def __radd__(self, other): # self + other
        return other

    def __neg__(self): return self

    def __repr__(self):
        return 'E'

class RightLA:
    def __init__(self, line1=None, line2=None):
        self.x, self.y = line1, line2
    def __add__(self, other):
        if isinstance(other, RightLA): return NeutralLA()

    def __neg__(self): return self

    def __repr__(self):
        return 'R'




