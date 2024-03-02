# # from sympy import Matrix
# #
# # first = Matrix(
# #     [
# #         [0, 1, 0, 0, 0],
# #         [-1, 0, 1, 0, 0],
# #         [0, -1, 0, 1, 0],
# #         [0, 0, -1, 0, 0],
# #         [0, 0, 0, 0, 0]
# #     ]
# # )
#
#
#
# # x = [0, 1, 2, 4] # А В С
# # y = [1, 3, 2] # А М В
# # z = [1, 7, 2, 4]
# # # x.coproduction(y) - А М В С
# # print([var in y for var in x]) # [1, 3, 2, 4]
# # print([var in y for var in z]) # Противоречие
# #
# # def coproduction(a: list, b: list):
# #     result = b[:]
# #     meetTrue = False
# #     boolList = [var in b for var in a]
# #     for val, cur in zip(a, boolList):
# #         if not meetTrue and not cur:
# #             result.insert(0, val)
# #         if cur:
# #             meetTrue = True
# #             continue
# #         if not cur and meetTrue:
# #             if any(boolList[a.index(val):]):
# #                 return False
# #             else:
# #                 result.append(val)
# #     return result
# #
# # print(coproduction(z, y))
# class PseudoPredicate:
#     def __init__(self, elem1, elem2):
#         self.info = elem1, elem2
#     def __bool__(self):
#         return self in P
#
#     def __repr__(self):
#         return f'{self.__class__.__name__}{self.info}'
#     def __eq__(self, other):
#         return isinstance(other, type(self)) and other.info == self.info
# class EQUAL(PseudoPredicate): pass
# class PARA(PseudoPredicate): pass
# class PERP(PseudoPredicate): pass
#
# class FA:
#     def __init__(self, line1, line2):
#         self.x, self.y = line1, line2
#
#     def __add__(self, other):
#         if isinstance(other, E): return self
#         if self.y == other.x: return FA(self.x, other.y)
#         return False
#
#
#     def __repr__(self):
#         return f'∠[{self.x}, {self.y}]'
#
#     def __eq__(self, other):
#         pass
#
# class E:
#     def __init__(self):
#         self.x, self.y = None, None
#     def __add__(self, other): # self + other
#         return other
#     def __radd__(self, other): # self + other
#         return other
#     def __repr__(self):
#         return 'нейтральный элемент'
#
# class R:
#     def __init__(self):
#         self.x, self.y = None, None
#     def __add__(self, other):
#         if isinstance(other, R): return E()
#     def __repr__(self):
#         return 'прямой угол'
#
# #
#
# L = ['u', 'm']
# P = [EQUAL('u', 'v'), PARA('v', 'm'), PARA('k', 'm'), PERP('u', 'k')]
#
# print(type(next((elem for elem in L if elem not in 'u'))))

l = [1, 2, 3, 4]
for i in l[:3]: print(i)