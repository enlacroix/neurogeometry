import itertools
from typing import Union
from backwardLA.linangle import Linangle, NeutralLA, RightLA
from tskmanager import Task


class Simplifier:
    substitutionDict = {}
    equivLists = []

    def __init__(self):
        pass

    @classmethod
    def makeSubstitutionDict(cls):
        cls.substitutionDict = dict.fromkeys((Linangle(*comb) for comb in itertools.combinations(Task.Instance().lines, 2)))
        for subkey in cls.substitutionDict: cls.substitutionDict[subkey] = [] # todo set()?

    @classmethod
    def getConnectComponent(cls, angle):
        firstcomp = next((subset for subset in cls.equivLists if angle in subset), None)
        if firstcomp is None:
            return next(({-elem for elem in subset} for subset in cls.equivLists if -angle in subset), None)
        else:
            return firstcomp

    @classmethod
    def getLAList(cls, keyAngle: Linangle):
        if keyAngle in cls.substitutionDict: return cls.substitutionDict[keyAngle]
        if -keyAngle in cls.substitutionDict: return [-la for la in cls.substitutionDict[keyAngle]]
        return False

    @classmethod
    def addValue(cls, first: Linangle, second: Union[Linangle, NeutralLA, RightLA]):
        for subset in cls.equivLists:
            if first in subset:
                subset.add(second)
                return
        cls.equivLists.append({first, second})

    @classmethod
    def addLink(cls, keyAngle: Linangle, valAngle: Union[Linangle, NeutralLA, RightLA]):
        '''
            if keyAngle in cls.substitutionDict:
        if valAngle not in cls.substitutionDict[keyAngle]: cls.substitutionDict[keyAngle].append(valAngle)
    if -keyAngle in cls.substitutionDict:
        if valAngle not in cls.substitutionDict[keyAngle]: cls.substitutionDict[keyAngle].append(-valAngle)
        '''
        if keyAngle in cls.substitutionDict:
            if valAngle not in cls.substitutionDict[keyAngle]: cls.substitutionDict[keyAngle].append(valAngle)
        if -keyAngle in cls.substitutionDict:
            if valAngle not in cls.substitutionDict[-keyAngle]: cls.substitutionDict[-keyAngle].append(-valAngle)


