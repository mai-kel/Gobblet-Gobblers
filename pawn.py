class Pawn:

    def __init__(self, colour, size) -> None:
        self._colour = colour
        self._size = size

    @property
    def colour(self):
        return self._colour

    @property
    def size(self):
        return self._size

    def is_bigger(self, other):
        """
        Method checks if pawn's size is bigger than other's pawn size given in argument.
        """
        if (other is None):
            return True

        return self._size > other._size
