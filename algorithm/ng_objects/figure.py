from utils import logger, toStrAllElems
from tskmanager import Task


class GeomFigure:
    def totalConfirm(self, thname, descr, premises) -> bool:
        if self.confirm():
            logger(f'{thname}: {toStrAllElems(premises)} => {self}')
            Task.DF().addString((thname, descr, premises, [Task.DF().getFactIndex(prem) for prem in premises], self))
            self.postConfirm()
            return True
        return False

    def confirm(self) -> bool:
        if self not in Task.Instance().figures:
            Task.Instance().figures.append(self)
            self.numerize()
            return True
        return False

    def numerize(self):
        pass

    def postConfirm(self):
        pass

