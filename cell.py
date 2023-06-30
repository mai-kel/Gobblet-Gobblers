class Cell:

    def __init__(self, index_x, index_y, pawns_list) -> None:
        self._index_x = index_x
        self._index_y = index_y
        self._pawns_list = pawns_list

    @property
    def index_x(self):
        return self._index_x

    @property
    def index_y(self):
        return self._index_y

    @property
    def pawns_list(self):
        return self._pawns_list

    def add_pawn(self, pawn):
        """
        Method adds pawn given in arguemnt to cell's pawns_list
        """
        self._pawns_list.append(pawn)

    def del_pawn(self, pawn):
        """
        Method deletes pawn given in arguemnt from cell's pawns_list
        """
        for i in range(len(self._pawns_list)):
            if (pawn == self._pawns_list[i]):
                del self._pawns_list[i]
                return

    def get_most_important_pawn(self):
        """
        Method returns pawn with biggest size from cell's pawns_list
        """
        if (not self._pawns_list):
            return None
        most_important_pawn = self._pawns_list[0]
        for pawn in self._pawns_list:
            if (pawn.is_bigger(most_important_pawn)):
                most_important_pawn = pawn
        return most_important_pawn

    def is_empty(self):
        """
        Method returns True if cell's pawns_list is empty.
        If cell's pawns_list is not empty method returns False.
        """
        if (self._pawns_list == []):
            return True
        else:
            return False
