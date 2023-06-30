from cell import Cell
from table import Table
from player import Player
from game import Game
from pawn import Pawn
from move import Move


def test():
    assert True


# Testing Pawn class
def test_pawn_is_bigger():
    pawn1 = Pawn('red', 5)
    pawn2 = Pawn('blue', 5)
    pawn3 = Pawn('red', 6)

    assert not pawn1.is_bigger(pawn2)
    assert pawn3.is_bigger(pawn1)
    assert pawn2.is_bigger(None)


# Testing Cell class
def test_add_pawn():
    cell = Cell(0, 0, [])
    pawn1 = Pawn('red', 5)
    cell.add_pawn(pawn1)
    assert cell.pawns_list == [pawn1]


def test_del_pawn():
    cell = Cell(0, 0, [])
    pawn1 = Pawn('red', 5)
    pawn2 = Pawn('blue', 5)
    pawn3 = Pawn('red', 6)
    cell.add_pawn(pawn1)
    cell.add_pawn(pawn2)
    cell.add_pawn(pawn3)
    assert cell.pawns_list == [pawn1, pawn2, pawn3]
    cell.del_pawn(pawn1)
    cell.del_pawn(pawn3)
    assert cell.pawns_list == [pawn2]


def test_get_most_important_pawn():
    cell = Cell(0, 0, [])
    assert cell.get_most_important_pawn() is None
    pawn1 = Pawn('red', 5)
    pawn2 = Pawn('blue', 5)
    pawn3 = Pawn('red', 6)
    cell.add_pawn(pawn1)
    cell.add_pawn(pawn2)
    cell.add_pawn(pawn3)
    assert cell.get_most_important_pawn() == pawn3


def test_is_empty_cell():
    cell = Cell(1, 5, [])
    assert cell.is_empty()
    pawn1 = Pawn('purple', 6)
    cell.add_pawn(pawn1)
    assert not cell.is_empty()


# Testing Table class
def test_get_dimension():
    cells_list = Table.generate_empty_cells_list(3)
    table = Table(cells_list)
    assert table.get_dimension() == 3


def test_get_cell_by_index():
    cells_list = Table.generate_empty_cells_list(3)
    pawn1 = Pawn('red', 5)
    pawn2 = Pawn('blue', 5)
    cell = Cell(2, 2, [pawn1, pawn2])
    cells_list[2][2] = cell
    table = Table(cells_list)
    assert table.get_cell_by_index(2, 2) == cell


def test_is_empty_table():
    cells_list = Table.generate_empty_cells_list(3)
    pawn1 = Pawn('red', 5)
    pawn2 = Pawn('blue', 5)
    cell = Cell(2, 2, [pawn1, pawn2])
    table = Table(cells_list)
    assert table.is_empty()
    cells_list[2][2] = cell
    assert not table.is_empty()


# Testing Player class
def test_get_pawn_from_pawn_stack():
    pawn_stack1 = Player.generate_pawn_stack(3, 2, 'red')
    player1 = Player('Player1', 'red', pawn_stack1)
    pawn1: Pawn = player1.get_pawn_from_pawn_stack(0)
    assert pawn1.size == 1
    assert pawn1.colour == 'red'
    pawn2: Pawn = player1.get_pawn_from_pawn_stack(5)
    assert pawn2.size == 3
    assert pawn2.colour == 'red'


def test_del_pawn_from_player_stack():
    pawn_stack1 = Player.generate_pawn_stack(3, 1, 'red')
    player1 = Player('Player1', 'red', pawn_stack1)
    pawn1: Pawn = player1.get_pawn_from_pawn_stack(0)
    assert pawn1.size == 1
    assert pawn1.colour == 'red'
    player1.del_pawn_from_player_stack(pawn1)
    pawn2: Pawn = player1.get_pawn_from_pawn_stack(0)
    assert pawn2.size == 2
    assert pawn2.colour == 'red'


def test_is_player_stack_empty():
    pawn_stack1 = Player.generate_pawn_stack(3, 1, 'red')
    player1 = Player('Player1', 'red', pawn_stack1)
    assert not player1.is_player_stack_empty()
    for i in range(3):
        player1.del_pawn_from_player_stack(player1.get_pawn_from_pawn_stack(0))

    assert player1.is_player_stack_empty()


# Testing Game class
def test_did_player_win_diagonally():
    table_size = 3
    pawn_sizes = 3
    quantity_of_each_size = 2
    player1 = Player('Gracz 1', 'red', Player.generate_pawn_stack(pawn_sizes, quantity_of_each_size, 'red'))
    player2 = Player('Gracz 2', 'blue', Player.generate_pawn_stack(pawn_sizes, quantity_of_each_size, 'blue'))
    table = Table(Table.generate_empty_cells_list(table_size))
    game = Game(table, player1, None, player1, player2)

    assert not game._did_player_win(player1) and not game._did_player_win(player2)

    game.make_move(Move('stack', 0, 'table', (0, 0)))
    game.change_turn()
    game.make_move(Move('stack', 0, 'table', (1, 1)))
    game.change_turn()
    game.make_move(Move('stack', 0, 'table', (2, 2)))

    assert game._did_player_win(player1) and not game._did_player_win(player2)


def test_did_player_win_horizontally():
    table_size = 3
    pawn_sizes = 3
    quantity_of_each_size = 2
    player1 = Player('Gracz 1', 'red', Player.generate_pawn_stack(pawn_sizes, quantity_of_each_size, 'red'))
    player2 = Player('Gracz 2', 'blue', Player.generate_pawn_stack(pawn_sizes, quantity_of_each_size, 'blue'))
    table = Table(Table.generate_empty_cells_list(table_size))
    game = Game(table, player1, None, player1, player2)

    assert not game._did_player_win(player1) and not game._did_player_win(player2)

    game.make_move(Move('stack', 0, 'table', (0, 0)))
    game.change_turn()
    game.make_move(Move('stack', 0, 'table', (0, 1)))
    game.change_turn()
    game.make_move(Move('stack', 0, 'table', (0, 2)))

    assert game._did_player_win(player1) and not game._did_player_win(player2)


def test_did_player_win_vertically():
    table_size = 3
    pawn_sizes = 3
    quantity_of_each_size = 2
    player1 = Player('Gracz 1', 'red', Player.generate_pawn_stack(pawn_sizes, quantity_of_each_size, 'red'))
    player2 = Player('Gracz 2', 'blue', Player.generate_pawn_stack(pawn_sizes, quantity_of_each_size, 'blue'))
    table = Table(Table.generate_empty_cells_list(table_size))
    game = Game(table, player1, None, player1, player2)

    assert not game._did_player_win(player1) and not game._did_player_win(player2)

    game.make_move(Move('stack', 0, 'table', (0, 0)))
    game.change_turn()
    game.make_move(Move('stack', 0, 'table', (1, 0)))
    game.change_turn()
    game.make_move(Move('stack', 0, 'table', (2, 0)))

    assert game._did_player_win(player1) and not game._did_player_win(player2)


def test_make_move():
    table_size = 3
    pawn_sizes = 3
    quantity_of_each_size = 2
    player1 = Player('Gracz 1', 'red', Player.generate_pawn_stack(pawn_sizes, quantity_of_each_size, 'red'))
    player2 = Player('Gracz 2', 'blue', Player.generate_pawn_stack(pawn_sizes, quantity_of_each_size, 'blue'))
    table = Table(Table.generate_empty_cells_list(table_size))
    game = Game(table, player1, None, player1, player2)

    game.make_move(Move('stack', 0, 'table', (0, 0)))
    assert not table.cells_list[0][0].is_empty()
    game.change_turn()
    game.make_move(Move('table', (0, 0), 'table', (2, 2)))
    assert table.cells_list[0][0].is_empty()
    assert not table.cells_list[2][2].is_empty()


def test_is_move_valid():
    table_size = 3
    pawn_sizes = 3
    quantity_of_each_size = 2
    player1 = Player('Gracz 1', 'red', Player.generate_pawn_stack(pawn_sizes, quantity_of_each_size, 'red'))
    player2 = Player('Gracz 2', 'blue', Player.generate_pawn_stack(pawn_sizes, quantity_of_each_size, 'blue'))
    table = Table(Table.generate_empty_cells_list(table_size))
    game = Game(table, player1, None, player1, player2)

    assert not game.is_move_valid(Move('table', (0, 0), 'table', (2, 2)))
    assert game.is_move_valid(Move('stack', 0, 'table', (2, 2)))
    game.make_move(Move('stack', 0, 'table', (0, 0)))
    assert not game.is_move_valid(Move('table', (0, 0), 'table', (2, 2)))
    assert not game.is_move_valid(Move('stack', 0, 'table', (0, 0)))
    assert game.is_move_valid(Move('stack', 3, 'table', (0, 0)))
