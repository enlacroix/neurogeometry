import sympy as sp


class LinearEquationsSystem:
    """
    Работает ТОЛЬКО с матрицами Sympy! Вызываем методы, которые определены только для них.
    """

    def __init__(self, matrix: sp.Matrix):
        self.matrix = matrix
        self.var_num = max(0, sp.shape(matrix)[1] - 1)

    def printSystemOfEquations(self, namesOfVars):
        res = ''
        for i in range(self.matrix.rows):
            for j in range(len(namesOfVars)):
                if self.matrix.row(i)[j] != 0:
                    if self.matrix.row(i)[j] != 1: res += str(self.matrix.row(i)[j])
                    res += f'{namesOfVars[j]} + '
            res = res[:-2] + f'= {self.matrix.row(i)[-1]} \n'
        return res

    def solve(self, geom_mode=False, print_answer=False):
        """
        Решает неоднородную систему уравнений.
        На вход подается дополненная матрица (А|b), т.е. содержащая в себе столбец значений b.
        Возвращает list.
        """
        if self.var_num == 0:
            return []
        # Nullspace у нас это ядро пространства столбцов матрицы коэффициентов (без последнего столбца)
        space = self.matrix[:, :-1].nullspace()
        # Приводим матрицу к главному ступенчатому виду, pivot содержат номера тех столбцов, которые содержат базисные переменные.
        X, pivot = self.matrix.rref()
        # Здесь мы позорно находим столбец, содержащий частное решение неоднородной системы.
        n = sp.zeros(self.var_num, 1)
        h = 0
        for elem in X.col(-1):
            try:
                i = pivot[h]
            except IndexError:
                break
            n[i, 0] = elem
            h += 1
        # Добавляем в ядро однородной системы.
        space.append(n)
        vrs = [0] * self.var_num
        glb_rem = ''
        for i in range(self.var_num):
            rem = f'x_{i + 1} = '
            for j, mtr in enumerate(space):
                if j < len(space) - 1:
                    if mtr[i] != 0 and geom_mode:
                        vrs[i] = None
                        break
                    rem += f'{mtr[i]} C_{j + 1} + '
                else:
                    rem += f'{mtr[i]}.'
                    vrs[i] = mtr[i]
            glb_rem += rem + '\n'
        if print_answer:
            print(glb_rem)
        return vrs

'''
# Ничем не примечательная система. Здесь будут выведены все None при активированном geom_mode.
test0 = sp.Matrix([[1, 2, 1, 1, 7],
                   [1, 2, 2, -1, 12],
                   [2, 4, 0, 6, 4]])


# (не забудьте активировать geom_mode)
# Матрица из демозадачи 2. Она вычислит первые три угла, но она ничего не знает достоверно о четвёртом угле, поэтому ему присвоен None.

test1 = sp.Matrix([[1, 1, 1, 0, 180],
                   [1, -3, 0, 0, 0],
                   [0, 0, 1, 0, 20]])

# Она знает только про четвёртый угол, остальные ей неведомы.
test2 = sp.Matrix([[1, 1, 1, 0, 180],
                   [0, 0, 0, 1, 20]])

l = LinearEquationsSystem(test1)
print(l.printSystemOfEquations(['a', 'b', 'c', 'd']))
l.solve(geom_mode=True, print_answer=True)
'''

