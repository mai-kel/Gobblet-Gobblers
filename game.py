from cell import Cell
from table import Table
from player import Player
from move import Move


class Game:

    def __init__(self, table: Table, turn: Player, state, player1: Player, player2: Player) -> None:
        # state == None <=> game in progress; state == True <=> player1 won; state == False <=> player2 won
        self._table = table
        self._turn = turn
        self._state = state
        self._player1 = player1
        self._player2 = player2

    @property
    def turn(self):
        return self._turn

    @property
    def table(self):
        return self._table

    @property
    def player1(self):
        return self._player1

    @property
    def player2(self):
        return self._player2

    @property
    def state(self):
        return self._state

    def set_turn(self, new_turn):
        self._turn = new_turn

    def set_state(self, new_state):
        self._state = new_state

    def check_game_status(self):
        """
        Method analyzes game's table and updates game's state
        """
        if (self._did_player_win(self.player1)):
            self.set_state(True)
        elif (self._did_player_win(self.player2)):
            self.set_state(False)
        else:
            self.set_state(None)

    def _did_player_win(self, player: Player):
        """
        Private method used in check_game_status().
        It analyzes game's table and checks if player given in argument has won the game.
        """
        cells_list = self.table.cells_list
        player_colour = player.colour

        # checking horizontally
        counter = 0
        for i in range(len(cells_list)):
            for j in range(len(cells_list)):
                if (cells_list[i][j].get_most_important_pawn() is not None):
                    if (cells_list[i][j].get_most_important_pawn().colour == player_colour):
                        counter += 1
            if (counter == len(cells_list)):
                return True
            else:
                counter = 0

        # checking vertically
        counter = 0
        for i in range(len(cells_list)):
            for j in range(len(cells_list)):
                if (cells_list[j][i].get_most_important_pawn() is not None):
                    if (cells_list[j][i].get_most_important_pawn().colour == player_colour):
                        counter += 1
            if (counter == len(cells_list)):
                return True
            else:
                counter = 0

        # checking diagonally from top-left to down-right
        counter = 0
        for i in range(len(cells_list)):
            if (cells_list[i][i].get_most_important_pawn() is not None):
                if (cells_list[i][i].get_most_important_pawn().colour == player_colour):
                    counter += 1
        if (counter == len(cells_list)):
            return True
        else:
            counter = 0

        # chchecking diagonally from top-right to down-left
        counter = 0
        for i in range(len(cells_list)):
            if (cells_list[i][-(i+1)].get_most_important_pawn() is not None):
                if (cells_list[i][-(i+1)].get_most_important_pawn().colour == player_colour):
                    counter += 1
        if (counter == len(cells_list)):
            return True
        else:
            counter = 0

        return False

    def move_pawn_from_table(self, from_row, from_column, to_row, to_column):
        """
        Method moves pawn from given cell to another given cell.

        Parameters:
        from_row (int) : Row of cell from which player wants to move pawn
        from_column (int) : Column of cell from which player wants to move pawn
        to_row (int) : Row of cell to which player wants to move pawn
        to_column (int) : Column of cell to which player wants to move pawn
        """
        from_cell = self.table.get_cell_by_index(from_row, from_column)
        moving_pawn = from_cell.get_most_important_pawn()
        self.table.get_cell_by_index(to_row, to_column).add_pawn(moving_pawn)
        self.table.get_cell_by_index(from_row, from_column).del_pawn(moving_pawn)
        self.change_turn()

    def move_pawn_from_players_stack(self, from_stack_index, to_row, to_column):
        """
        Method move given pawn from stack to given cell.

        Parameters:
        from_stack_index (int) : Index of pawn in player's stack, which user wants to move
        to_row (int) : Row of cell to which player wants to move pawn
        to_column (int) : Column of cell to which player wants to move pawn
        """
        moving_pawn = self.turn.get_pawn_from_pawn_stack(from_stack_index)
        self.table.get_cell_by_index(to_row, to_column).add_pawn(moving_pawn)
        self.turn.del_pawn_from_player_stack(moving_pawn)
        self.change_turn()

    def change_turn(self):
        """
        Method changes game's turn
        """
        if (self.turn == self.player1):
            self.set_turn(self.player2)
        else:
            self.set_turn(self.player1)

    def is_move_valid(self, move: Move):
        """
        Method checks if move given as an argument is valid for player whose turn is.
        It returns True if so. Otherwise it returns False
        """
        # checking moves which requrie moving pawn from table
        if (move.from_where == 'table'):
            from_row, from_column = move.from_index
            from_cell: Cell = self.table.cells_list[from_row][from_column]
            to_row, to_column = move.to_index
            to_cell: Cell = self.table.cells_list[to_row][to_column]

            # case when pawn is moved from the same cell as it is moved to
            if (move.from_index == move.to_index):
                return False
            # case when cell from which pawn is supposed to be moved does not contain any pawn
            elif (from_cell.get_most_important_pawn() is None):
                return False
            # case when moving pawn is not bigger than pawn on cell destination
            elif (not from_cell.get_most_important_pawn().is_bigger(to_cell.get_most_important_pawn())):
                return False
            # case when biggest pawn of cell, from which pawn is supposed to be moved, doesn't belong to player whoose turn is
            elif (from_cell.get_most_important_pawn().colour != self.turn.colour):
                return False

        # checking moves which require moving pawn from stack
        if (move.from_where == 'stack'):
            from_index = move.from_index
            to_row, to_column = move.to_index
            to_cell: Cell = self.table.cells_list[to_row][to_column]
            if (not self.turn.pawn_stack[from_index].is_bigger(to_cell.get_most_important_pawn())):
                return False

        return True

    def make_move(self, move: Move):
        """
        Method applies move, given as an agrument, to game.
        """
        to_row, to_column = move.to_index
        if (move.from_where == 'stack'):
            self.move_pawn_from_players_stack(move.from_index, to_row, to_column)
        elif (move.from_where == 'table'):
            from_row, from_column = move.from_index
            self.move_pawn_from_table(from_row, from_column, to_row, to_column)

    @staticmethod
    def get_all_valid_moves(game: 'Game'):
        """
        Method takes Game object as a parameter, and returns list of Move objects which are valid for player whose turn is
        """
        valid_moves = []

        # checking all moves, which require moving pawns form player's stack
        for i in range(len(game.turn.pawn_stack)):
            from_where = 'stack'
            from_index = i
            for j in range(len(game.table.cells_list)):
                for n in range(len(game.table.cells_list)):
                    to_where = 'table'
                    to_index = (j, n)
                    move = Move(from_where, from_index, to_where, to_index)
                    if (game.is_move_valid(move)):
                        valid_moves.append(move)

        # checking all moves, which require moving pawns from table
        # selecting all cells that we migh move pawn from
        for i in range(len(game.table.cells_list)):
            for j in range(len(game.table.cells_list)):
                from_where = 'table'
                from_index = (i, j)
                if (game.table.cells_list[i][j].get_most_important_pawn() is None):
                    continue
                elif (game.table.cells_list[i][j].get_most_important_pawn().colour != game.turn.colour):
                    continue

                # selecting all cells that we migh move pawn to
                for n in range(len(game.table.cells_list)):
                    for m in range(len(game.table.cells_list)):
                        to_where = 'table'
                        to_index = (n, m)
                        move = Move(from_where, from_index, to_where, to_index)
                        if (game.is_move_valid(move)):
                            valid_moves.append(move)

        return valid_moves
