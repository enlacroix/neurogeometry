import itertools
from backwardLA.linangle import Linangle, NeutralLA, RightLA
from backwardLA.simplifier import Simplifier
from tskmanager import Task

class Expression:

    def __init__(self, *args):
        self.first, self.second = args[0], args[1]
        self.allElements = args
    @classmethod
    def getMethodsDict(cls, numOfArgs):
     return {2: cls.pairFullReduction, 3: cls.trioFullReduction, 4: cls.quadFullReduction, 5: cls.quintetFullReduction, 6: cls.sixtetFullReduction}.get(numOfArgs, None)

    # def simplifying(self):
    #     """
    #     Упрощенный алгоритм редуцирования.
    #     - Формируем словарь подстановок, анализируя входные данные из предикатов.
    #     - функция упрощения принимает question - пара углов, нужно доказать, что их сумма равна 0.
    #     - берём первый аргумент Х из пары. getLAList() - начинаем итерироваться по выведенному списку l1, l2...
    #     - запоминаем пару (Х, l1) в список edges. пары считаются равными, если совпадают их множества, т.е. (Х, l1) = (l1, X) -
    #     это считается применением правила.
    #     - Формируем новый Expression(l1, Y) - пытаемся провести Reduction.
    #     - если упрощение удалось, то мы победили.
    #     - если нет, то смотрим чему равна l1 в словаре подстановок. начинаем итерацию по getLAList(l1). запоминая пары.
    #     - условие остановки:
    #     """
    #     pass

    # def step(self, leadAngle, depth):
    #     for ind, equivAngle in enumerate(Simplifier.getLAList(leadAngle)):
    #         if SubstEdge.addEdge(leadAngle, equivAngle):  # Если такой пары нет в записанных
    #             result = Expression.reduction(self.second, equivAngle)
    #             if result:
    #                 print(f'выражение успешно редуцировано к {result} выражениями {equivAngle}, {self.second}')
    #                 return True
    #             if not self.step(equivAngle, depth+1): # напоролись на лист.
    #                 if ind < len(Simplifier.getLAList(leadAngle)) - 1: self.step(Simplifier.getLAList(leadAngle)[ind + 1], depth)
    #                 else: return False
    #         else: continue
    #     return False # Мы перебрали все углы в списке смежности с ведущим углом.

    @staticmethod
    def pairFullReduction(alpha: Linangle, beta, aim=NeutralLA()):
        if Simplifier.getConnectComponent(alpha) == Simplifier.getConnectComponent(beta):
            if isinstance(aim, NeutralLA):
                Task.writeLA(f'Углы {alpha} = {beta}, поэтому они принадлежат одному классу эквивалентности.')
                if alpha.checkDegeneration():
                    Task.writeLA('Оба элемента равными нейтральному, поэтому их сумма очевидно нейтральна.')
                    return True
                elif RightLA() in Simplifier.getConnectComponent(alpha):
                    '''
                    a + b = aim, a = b -> 2<[u, v] = aim. Это может быть только КОГДА а = b = R.
                    док-во: <[u, v] + <[u, v] = Е -> <[u, v] = -<[u, v] -> <[u, v] = <[v, u] = [R], чтд
                    '''
                    Task.writeLA(f'Так как {alpha} равняется прямому углу, и {alpha} = {beta}, то их сумма равна нейтральному элементу.')
                    return True
                else:
                    Task.writeLA(f'Элемент {alpha} не является нейтральным, утверждение ложно')
                    return False
        for reductedPair in itertools.product(Simplifier.getConnectComponent(alpha), Simplifier.getConnectComponent(beta)):
            result = Expression.reduction(*reductedPair)
            if not result: continue
            # Task.writeLA(f'Удалось редуцировать аргументы {reductedPair[0]}, {reductedPair[1]} к {result}!')
            result: Linangle
            if isinstance(aim, NeutralLA) and result.checkDegeneration():
                Task.writeLA(f'{Expression(alpha, beta)} ввиду того, что {alpha} = {reductedPair[0]}, {beta} = {reductedPair[1]}')
                return True
            if aim == result: # Заготовка под тройку
                Task.writeLA(f'{alpha}+{beta}={aim} ввиду того, что {alpha} = {reductedPair[0]}, {beta} = {reductedPair[1]}')
                return True
        # todo старт декомпозиции - разложить сначала альфа, потом бета? (или достаточно только альфа?) применить редукцию для троек
        Task.writeLA(f'Пару {alpha}, {beta} невозможно редуцировать к {aim} на данном множестве прямых и предикатов.')
        return False

    @staticmethod
    def trioFullReduction(a, b, c):
        if Expression.pairFullReduction(a, b, aim=-c): # с заменой на -с in pairReductionSet(a, b).
            Task.writeLA(f'Что доказывает утверждение {Expression(a, b, c)}.')
            return True
        return False

    @staticmethod
    def quadFullReduction(a, b, c, d):
        for elem in Expression.pairReductionSet(c, d):
            if Expression.pairFullReduction(a, b, aim=-elem):
                Task.writeLA(f'Утверждение {Expression(a, b, c, d)} было успешно доказано. Так как {c}, {d} могут быть '
                      f'редуцированы к {elem}, а {a}, {b} к {-elem}, то их сумма равна нейтральному элементу. ')
                return True
        return False

    @staticmethod
    def quintetFullReduction(a, b, c, d, e):
        for elem in Expression.trioReductionSet(a, b, c):
            if Expression.pairFullReduction(d, e, aim=-elem):
                Task.writeLA(f'Утверждение {Expression(a, b, c, d, e)} было успешно доказано. Так как {d} и {e} могут быть '
                             f'редуцированы к {-elem}, а {a} + {b} + {c} = {elem}, то их сумма равна нейтральному элементу. ')
                return True
        return False

    @staticmethod
    def sixtetFullReduction(a, b, c, d, e, f):
        for elem in Expression.trioReductionSet(a, b, c):
            if -elem in Expression.trioReductionSet(d, e, f):
                Task.writeLA(f'Утверждение {Expression(a, b, c, d, e, f)} было успешно доказано. Так как {d} + {e} + {f} могут быть '
                             f'редуцированы к {-elem}, а {a} + {b} + {c} = {elem}, то их сумма равна нейтральному элементу. ')
                return True
        return False

    @classmethod
    def NReduction(cls, *args):
        """
        Обобщенное редуцирование полинома, в правой части которого стоит Нейтральный элемент.
        """
        method = cls.getMethodsDict(len(args))
        if method is None:
            Task.writeLA(f'Не имеет смысла редуцировать выражение, состоящее из {len(args)} аргумента(-ов) .')
            return False
        return method(*args)



    @staticmethod
    def pairReductionSet(alpha, beta):
        summary = []
        for reductedPair in itertools.product(Simplifier.getConnectComponent(alpha), Simplifier.getConnectComponent(beta)):
            result = Expression.reduction(*reductedPair)
            if not result: continue
            summary.append(result)
        return summary

    @staticmethod
    def trioReductionSet(*args):
        summary = []
        for pair in itertools.combinations(args, 2): # 3
            another = next(elem for elem in args if elem not in pair)
            for reductedPair in itertools.product(Expression.pairReductionSet(*pair), Simplifier.getConnectComponent(another)):
                result = Expression.reduction(*reductedPair)
                if not result: continue
                summary.append(result)
        return summary

    def __repr__(self): return ' + '.join(map(str, self.allElements)) + ' = [E]'
    
    @staticmethod
    def reduction(alpha: Linangle, beta: Linangle):
        resultA = alpha + beta
        resultB = beta + alpha
        if resultA: return resultA
        if resultB: return resultB
        return False

    def decomposition(self):
        # R2 ∠[u, v] = ∠[u, m] + ∠[m, v] = ∠[u, m] + [r], если v ⊥ m для любого u. - это частный случай декомпозиции.
        # для угла ∠[m, v] и ∠[v, m] должно стоять значение [r] в словаре подстановок. if ORT[m, v]
        pass


'''class SubstEdge:
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
'''