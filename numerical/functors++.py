
class TrigonometricFunctors:
    def is_known(self):
        """
        Если известна хотя бы одна из тригонометрический функций (наследников этого класса), то мы знаем и о других.
        """
        pass
    pass


class Cos(TrigonometricFunctors):
    pass


class Sin(TrigonometricFunctors):
    pass


class Tan(TrigonometricFunctors):
    pass
