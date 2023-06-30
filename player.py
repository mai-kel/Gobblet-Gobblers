from pawn import Pawn


class Player:
    def __init__(self, name, colour, pawn_stack) -> None:
        self._name = name
        self._colour = colour
        self._pawn_stack = pawn_stack

    @property
    def name(self):
        return self._name

    @property
    def colour(self):
        return self._colour

    @property
    def pawn_stack(self):
        return self._pawn_stack

    def __str__(self) -> str:
        return self.name

    def get_pawn_from_pawn_stack(self, index):
        """
        Method returns pawn from pawn_stack[index]
        """
        return self._pawn_stack[index]

    def del_pawn_from_player_stack(self, pawn):
        """
        Method deletes pawn given in argument from pawn_stack

        Parameters:
        pawn (Pawn) : pawn to delete from pawn_stack
        """
        if (self._pawn_stack == []):
            return
        for i in range(len(self._pawn_stack)):
            if (self._pawn_stack[i] == pawn):
                del self._pawn_stack[i]
                return

    def is_player_stack_empty(self):
        """
        Method checks if pawn_stack is empty
        """
        return not bool(self.pawn_stack)

    @staticmethod
    def generate_pawn_stack(sizes, quantity_of_each_size, colour):
        """
        Method creates and returns pawn stack according to number of pawns and colour given as arguments.

        Parameters:
        number_of_pawns (int) : number of pawns in stack
        colour (string) : colour of pawns in stack
        """
        pawn_stack = []
        for i in range(1, sizes+1):
            for j in range(quantity_of_each_size):
                pawn = Pawn(colour, i)
                pawn_stack.append(pawn)
        return pawn_stack
