# import numpy as np
# import varbank as vb
#
#
#
#
#
# class Relation:  # Отношение величины obj1 к obj2 равна k.
#     def __init__(self, obj1, obj2, k):
#         blank = [0] * vb.N
#         blank[obj1.get_ind()] = 1
#         blank[obj2.get_ind()] = - k
#         vb.AEM = np.vstack([vb.AEM, np.array(blank)])
#         vb.AEV = np.vstack([vb.AEV, np.array([0])])
#
#
# class Sum:  # Сумма углов равна 180 градусам.
#     def __init__(self, objects, res):
#         blank = [0] * vb.N
#         for elem in objects:
#             blank[elem.get_ind()] = 1
#         # vb.AEV[vb.AEM.shape[0]][0] = res
#         vb.AEV = np.vstack([vb.AEV, np.array([res])])
#         vb.AEM = np.vstack([vb.AEM, np.array(blank)])
#
# class Diff:  # Разность величин.
#     pass
