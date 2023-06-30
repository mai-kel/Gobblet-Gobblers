
class Move:

    def __init__(self, from_where, from_index, to_where, to_index) -> None:
        """
        Constructor for Move class.
        Parameters:
            from_where: Describes from where pawn is moved. If it is moved from stack, parameter value is "stack".
                        If it is moved from table its value is "table".
            from_index: Describes index of pawn which is moved. If it is moved from stack parameter value is int.
                        If pawn is moved from table parameter value is tuple (row, column)
            to_where: Describes to where pawn is moved. It can only be "table"
            to_index: Describes index of cell to which pawn is moved to. Parameter value is tuple (row, column)
        """
        if (from_where != 'stack' and from_where != 'table'):
            raise ValueError
        if (to_where != 'table'):
            raise ValueError

        self._from_where = from_where
        self._from_index = from_index
        self._to_where = to_where
        self._to_index = to_index
        pass

    @property
    def from_where(self):
        return self._from_where

    @property
    def from_index(self):
        return self._from_index

    @property
    def to_where(self):
        return self._to_where

    @property
    def to_index(self):
        return self._to_index
