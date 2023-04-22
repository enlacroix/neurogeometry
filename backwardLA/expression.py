from backwardLA.linangle import LinAngle
from backwardLA.simplifier import Simplifier


class SubstEdge:
    edgeList = []
    def __init__(self, firstAngle: LinAngle, secondAngle: LinAngle):
        self.firstAngle, self.secondAngle = firstAngle, secondAngle

    def __repr__(self):
        return f'Равенство {self.firstAngle} = {self.secondAngle}'

    @classmethod
    def addEdge(cls, first, second):
        if cls(first, second) in cls.edgeList: return False
        else:
            cls.edgeList.append(cls(first, second))
            return True

    def __hash__(self): return hash(self.firstAngle) ^ hash(self.secondAngle)

    def __eq__(self, other):
        """
        вынести знак - из other. если не по
        """
        return {self.firstAngle, self.secondAngle} == {other.firstAngle, other.secondAngle} or {self.firstAngle, self.secondAngle} == {-other.firstAngle, -other.secondAngle}

class Expression:
    def __init__(self, first, second):
        self.first, self.second = first, second

    def simplifying(self):
        """
        Упрощенный алгоритм редуцирования.
        - Формируем словарь подстановок, анализируя входные данные из предикатов.
        - функция упрощения принимает question - пара углов, нужно доказать, что их сумма равна 0.
        - берём первый аргумент Х из пары. getLAList() - начинаем итерироваться по выведенному списку l1, l2...
        - запоминаем пару (Х, l1) в список edges. пары считаются равными, если совпадают их множества, т.е. (Х, l1) = (l1, X) -
        это считается применением правила.
        - Формируем новый Expression(l1, Y) - пытаемся провести Reduction.
        - если упрощение удалось, то мы победили.
        - если нет, то смотрим чему равна l1 в словаре подстановок. начинаем итерацию по getLAList(l1). запоминая пары.
        - условие остановки:
        """
        self.step(self.first, 0)

    def step(self, leadAngle, depth):
        for ind, equivAngle in enumerate(Simplifier.getLAList(leadAngle)):
            if SubstEdge.addEdge(leadAngle, equivAngle):  # Если такой пары нет в записанных
                result = Expression.reduction(self.second, equivAngle)
                if result:
                    print(f'выражение успешно редуцировано к {result} выражениями {equivAngle}, {self.second}')
                    return True
                if not self.step(equivAngle, depth+1): # напоролись на лист.
                    if ind < len(Simplifier.getLAList(leadAngle)) - 1: self.step(Simplifier.getLAList(leadAngle)[ind + 1], depth)
                    else: return False
            else: continue
        return False # Мы перебрали все углы в списке смежности с ведущим углом.



    def __repr__(self): return ' + '.join(map(str, (self.first, self.second))) + ' = [E]'
    
    @staticmethod
    def reduction(alpha: LinAngle, beta: LinAngle):
        resultA = alpha + beta
        resultB = beta + alpha
        if resultA: return resultA
        if resultB: return resultB
        return False

    def decomposition(self):
        # R2 ∠[u, v] = ∠[u, m] + ∠[m, v] = ∠[u, m] + [r], если v ⊥ m для любого u. - это частный случай декомпозиции.
        # для угла ∠[m, v] и ∠[v, m] должно стоять значение [r] в словаре подстановок. if ORT[m, v]
        pass
