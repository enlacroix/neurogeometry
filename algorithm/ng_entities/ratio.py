
class Ratio:
    """
    Отношение между двумя величинами (отрезки/углы/площади). Применяются в теоремах про подобные треугольники.
    Ratio может принимать отношение разных сущностей (длина разделить на синус угла)
    print(Ratio(Line(L, A), Line(B, T)) == Ratio(Line(B, T), Line(L, A))) # False
    print(Ratio(Line(A, L), Line(B, T)) == Ratio(Line(L, A), Line(T, B))) # True
    """
    def __init__(self, numerator, denominator):
        self.numerator = numerator # Числитель
        self.denominator = denominator
        self.sgm = [numerator, denominator]
        self.lst = numerator.lst + denominator.lst

    def __eq__(self, other):
        """
        1. х/у != у/х
        2. перемена мест точек в х или у эквивалентное преобразование.
        print(Ratio(Line(L, A), Line(B, T)) == Ratio(Line(B, T), Line(L, A))) # False
        print(Ratio(Line(A, L), Line(B, T)) == Ratio(Line(L, A), Line(T, B))) # True
        """
        return isinstance(other, Ratio) and self.sgm == other.sgm

    def invert(self): return Ratio(self.sgm[1], self.sgm[0])

    def __hash__(self):
        """
        print({Ratio(Line(L, A), Line(B, T)), Ratio(Line(A, L), Line(B, T))}) # {LA / BT}
        """
        return hash(self.sgm[0]) ^ hash(self.sgm[1])

    def __repr__(self):
        return f'{str(self.numerator)} / {str(self.denominator)}'