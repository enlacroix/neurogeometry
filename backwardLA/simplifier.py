import itertools
from typing import Union
from backwardLA.linangle import LinAngle, NeutralLA, RightLA
from tskmanager import Task


class Simplifier:
    substitutionDict = {}

    def __init__(self):
        pass

    @classmethod
    def makeSubstitutionDict(cls):
        cls.substitutionDict = dict.fromkeys((LinAngle(*comb) for comb in itertools.combinations(Task.Instance().lines, 2)))
        for subkey in cls.substitutionDict: cls.substitutionDict[subkey] = [] # todo set()?

    @classmethod
    def getLAList(cls, keyAngle: LinAngle):
        if keyAngle in cls.substitutionDict: return cls.substitutionDict[keyAngle]
        if -keyAngle in cls.substitutionDict: return [-la for la in cls.substitutionDict[keyAngle]]
        return False

    @classmethod
    def addLink(cls, keyAngle: LinAngle, valAngle: Union[LinAngle, NeutralLA, RightLA]):
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


