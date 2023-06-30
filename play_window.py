from enum import Enum
from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from game import Game
from pawn import Pawn
from databse import save_game
from random import choice
from move import Move
import settings

class Pawn_position(Enum):
        TABLE = 1
        DOWN_STACK = 2
        TOP_STACK = 3

class PlayWindow(QWidget):


    def __init__(self, game: Game, grid_buttons_size, parent=None) -> None:
        """
        Constructor for PlayWindow class. It creates widget that contains:
            - grid which is game table
            - both players pawn stacks
            - exit button
            - save and exit button
        """
        super().__init__()
        self._colors = {
            'standard_pawn': '#FBFDB0',
            'clicked_pawn': '#B9F965',
            'standard_grid': '#B9D8FF'
        }
        self.create_gui(game, grid_buttons_size, parent)
        self.setFixedSize(self.sizeHint())

    def get_grid_stacks_hbox(self):
        return self._grid_stacks_hbox

    def create_gui(self, game: Game, grid_buttons_size, parent=None):
        """
        Method creates main layout and attaches it to PlayWindow objects.
        """
        # creating main_vbox which contains grid_stacks_hbox and bottom_buttons_hbox
        main_vbox = QVBoxLayout()
        grid_stacks_hbox = QHBoxLayout()
        bottom_buttons_hbox = QHBoxLayout()

        main_vbox.addLayout(grid_stacks_hbox)
        main_vbox.addStretch()
        main_vbox.addLayout(bottom_buttons_hbox)

        # grid_stacks_hbox contains grid and stacks_vbox
        self.make_grid_stacks_hbox(grid_stacks_hbox, game, grid_buttons_size)
        self.make_bottom_buttons_hbox(bottom_buttons_hbox)

        # setting PlayWindow layout to main_vbox
        self.setLayout(main_vbox)

        # saving variables needed in other methods to objects private fields
        self.from_pawn = (None, None)
        self.to_pawn = (None, None)
        self._game = game
        self._button_szie = grid_buttons_size
        self._main_vbox = main_vbox
        self._parent = parent
        self._grid_stacks_hbox = grid_stacks_hbox

    def make_grid_stacks_hbox(self, grid_stacks_hbox: QHBoxLayout, game, grid_buttons_size):
        """
        Method creates grid and stacks_vbox inside of grid_stacks_hbox given as an argument.
        """
        grid = QGridLayout()
        stacks_vbox = QVBoxLayout()
        grid_stacks_hbox.addLayout(grid)
        grid_stacks_hbox.addItem(QSpacerItem(15, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        grid_stacks_hbox.addLayout(stacks_vbox)
        grid_stacks_hbox.addStretch()

        self.make_grid(grid, game, grid_buttons_size)
        self.make_stacks_vbox(stacks_vbox, game)

        self._stacks_vbox = stacks_vbox

    def make_grid(self, grid: QGridLayout, game: Game, grid_buttons_size: int):
        """
        Method creates buttons, which represent table's cells, insdie of grid given as an argument
        """
        # adding buttons to grid according to game's table dimension
        grid.setSpacing(0)
        for i in range(len(game.table.cells_list)):
            for j in range(len(game.table.cells_list)):
                button = QPushButton()
                button.setText('')
                button.setFixedSize(grid_buttons_size, grid_buttons_size)
                button.clicked.connect(self.on_table_clicked)
                button.setStyleSheet(f"background-color: {self._colors['standard_grid']};")
                grid.addWidget(button, i, j)
        self._grid = grid

    def make_stacks_vbox(self, stacks_vbox: QVBoxLayout, game: Game):
        """
        Method creates inner_vbox_top_stack and make_inner_vbox_down_stack in stacks_vbox given as an argument
        """
        # adding inner_vbox_top_stack, comunicate and inner_vbox_down_stack to stacks_vbox
        inner_vbox_top_stack = QVBoxLayout()
        inner_vbox_top_stack.setAlignment(Qt.AlignmentFlag.AlignTop)
        inner_vbox_down_stack = QVBoxLayout()
        inner_vbox_down_stack.setAlignment(Qt.AlignmentFlag.AlignBottom)
        comunicate = QLabel()
        comunicate.setText(f'Ruch gracza {game.turn.name}')
        comunicate.setFont(QFont('Times', 18))
        stacks_vbox.addLayout(inner_vbox_top_stack)
        stacks_vbox.addWidget(comunicate)
        stacks_vbox.addLayout(inner_vbox_down_stack)

        self.make_inner_vbox_top_stack(inner_vbox_top_stack, game)
        self.make_inner_vbox_down_stack(inner_vbox_down_stack, game)

        self._comunicate = comunicate

    def make_inner_vbox_top_stack(self, inner_vbox_top_stack: QVBoxLayout, game: Game):
        """
        Method creates player1_name_line_edit and top_stack_hbox inside inner_vbox_top_stack given as an argument.
        """
        # adding player1_name_line_edit and top_stack_hbox to inner_vbox_top_stack
        top_stack_hbox = QHBoxLayout()
        top_stack_hbox.setAlignment(Qt.AlignmentFlag.AlignTop)

        player1_name_line_edit = QLabel()
        player1_name_line_edit.setText(f'Pionki gracza {game.player1.name}')
        player1_name_line_edit.setFont(QFont('Times', 18))

        inner_vbox_top_stack.addWidget(player1_name_line_edit)
        inner_vbox_top_stack.addLayout(top_stack_hbox)

        # creating top pawn stack, which is adding buttons representing pawns to top_stack_hbox
        pawn: Pawn
        for pawn in game.player1.pawn_stack:
            button = QPushButton()
            button.setText(str(pawn.size))
            button.setStyleSheet(f"background-color: {self._colors['standard_pawn']};" + f" color: {pawn.colour}")
            button.setFixedSize((25 + pawn.size*4), (25 + pawn.size*4))
            button.setFont(QFont('Times', (10 + pawn.size*2)))
            button.clicked.connect(self.on_top_stack_clicked)
            top_stack_hbox.addWidget(button)

        self._top_stack_hbox = top_stack_hbox

    def make_inner_vbox_down_stack(self, inner_vbox_down_stack: QVBoxLayout, game: Game):
        """
        Method creates player2_name_line_edit and down_stack_hbox inside inner_vbox_down_stack given as an argument.
        """
        # adding player2_name_line_edit and down_stack_hbox to inner_vbox_down_stack
        down_stack_hbox = QHBoxLayout()
        down_stack_hbox.setAlignment(Qt.AlignmentFlag.AlignBottom)

        player2_name_line_edit = QLabel()
        player2_name_line_edit.setText(f'Pionki gracza {game.player2.name}')
        player2_name_line_edit.setFont(QFont('Times', 18))

        inner_vbox_down_stack.addWidget(player2_name_line_edit)
        inner_vbox_down_stack.addLayout(down_stack_hbox)

        # creating down stack, which is adding buttons representing pawns to down_stack_hbox
        pawn: Pawn
        for pawn in game.player2.pawn_stack:
            button = QPushButton()
            button.setText(str(pawn.size))
            button.setStyleSheet(f"background-color: {self._colors['standard_pawn']};" + f" color: {pawn.colour}")
            button.setFixedSize((25 + pawn.size*4), (25 + pawn.size*4))
            button.setFont(QFont('Times', (10 + pawn.size*2)))
            button.clicked.connect(self.on_down_stack_clicked)
            down_stack_hbox.addWidget(button)

        self._down_hbox = down_stack_hbox

    def make_bottom_buttons_hbox(self, bottom_buttons_hbox: QHBoxLayout):
        """
        Method creates two exit and save buttons inside bottom_buttons_hbox given as an argument.
        """
        # adding bottom_left_hbox and bottom_right_hbox to bottom_buttons_hbox
        bottom_buttons_hbox.setContentsMargins(0, 20, 0, 0)
        bottom_left_hbox = QHBoxLayout()
        bottom_left_hbox.setAlignment(Qt.AlignmentFlag.AlignLeft)

        bottom_right_hbox = QHBoxLayout()
        bottom_right_hbox.setAlignment(Qt.AlignmentFlag.AlignRight)

        bottom_buttons_hbox.addLayout(bottom_left_hbox)
        bottom_buttons_hbox.addLayout(bottom_right_hbox)

        # adding save_button to bottom_right_hbox
        save_button = QPushButton()
        save_button.setFixedSize(250, 50)
        save_button.setText("Zapisz grę i wyjdź")
        save_button.setFont(QFont('Times',  18))
        save_button.clicked.connect(self.on_click_save)
        save_button.setDisabled(True)
        bottom_right_hbox.addWidget(save_button)

        # adding exit_button to bottom_left_hbox
        exit_button = QPushButton()
        exit_button.setFixedSize(150, 50)
        exit_button.setText('Wyjdź')
        exit_button.setFont(QFont('Times',  18))
        exit_button.clicked.connect(self.on_click_exit)
        bottom_left_hbox.addWidget(exit_button)
        self._save_button = save_button

    def on_click_save(self):
        """
        Method is called when save_button is clicked. Save_button can be clicked only if game has ended.
        This method saves game to database.pkl and changes MainWindow's central widget to StartWindow.
        """
        save_game(self._game)
        self._parent.set_start_widget()

    def on_click_exit(self):
        """
        Method is called when exit_button is clicked. This method changes MainWindow's central widget to StartWindow.
        """
        self._parent.set_start_widget()

    def delete_button_top_stack(self, index):
        """
        Method deletes button from top_stack_hbox according to index given as an argument.
        """
        button = self._top_stack_hbox.itemAt(index).widget()
        self._top_stack_hbox.removeWidget(button)

    def delete_button_down_stack(self, index):
        """
        Method deletes button from down_stack_hbox according to index given as an argument.
        """
        button = self._down_hbox.itemAt(index).widget()
        self._down_hbox.removeWidget(button)

    def _on_stack_clicked(self, pawn_stack):
        """
        Method is called when pawns in any of stacks are clicked.
        """
        # if any player has already won the game method does nothing
        if (self._game.state is not None):
            return

        # assigning hbox, player and stack according to pawn_stack given as an argument
        hbox = None
        player = None
        if (pawn_stack == Pawn_position.TOP_STACK):
            hbox = self._top_stack_hbox
            player = self._game.player1
        else:
            hbox = self._down_hbox
            player = self._game.player2


        # if clicked pawn doesn't belong to player whose turn is, method does nothing
        if (player != self._game.turn):
            return

        # assigning clicked pawn index
        sender: QPushButton = self.sender()
        pawn_index = None
        for i in range(hbox.count()):
            if (sender == hbox.itemAt(i).widget()):
                pawn_index = i
                break

        # case when pawn that was clicked is the same as the pawn that had been clicked before
        if (self.from_pawn[1] == pawn_index):
            self.from_pawn = (None, None)
            sender.setStyleSheet(f"background-color: {self._colors['standard_pawn']};" + f" color: {player.colour}")
            return
        # case when there is no pawn that had been clicked before
        elif (self.from_pawn == (None, None)):
            self.from_pawn = (pawn_stack, pawn_index)
            sender.setStyleSheet(f"background-color: {self._colors['clicked_pawn']};" + f" color: {player.colour}")
            return
        # case when pawn that had been clicked before is in player's stack
        elif (self.from_pawn[0] == pawn_stack):
            from_pawn_button: QPushButton = hbox.itemAt(self.from_pawn[1]).widget()
            from_pawn_button.setStyleSheet(f"background-color: {self._colors['standard_pawn']};" + f" color: {player.colour}")
            sender.setStyleSheet(f"background-color: {self._colors['clicked_pawn']};" + f" color: {player.colour}")
            self.from_pawn = (pawn_stack, pawn_index)
            return
        # case when pawn that had been clicked before is on the table
        elif (self.from_pawn[0] == 'table'):
            from_pawn_row, from_pawn_column = self.from_pawn[1]
            from_pawn_button: QPushButton = self._grid.itemAtPosition(from_pawn_row, from_pawn_column).widget()
            from_pawn_button.setStyleSheet(f"background-color: {self._colors['standard_pawn']};" + f" color: {self._game.table.cells_list[from_pawn_row][from_pawn_column].colour}")
            sender.setStyleSheet(f"background-color: {self._colors['clicked_pawn']};" + f" color: {player.colour}")
            self.from_pawn = (pawn_stack, pawn_index)
            return

    def on_down_stack_clicked(self):
        """
        Method is called when pawn in down_stack is clicked
        """
        self._on_stack_clicked(Pawn_position.DOWN_STACK)

    def on_top_stack_clicked(self):
        """
        Method is called when pawn in top_stack is clicked
        """
        self._on_stack_clicked(Pawn_position.TOP_STACK)

    def on_table_clicked(self):
        """
        Method is called when table is clicked
        """
        # if any player has already won the game method does nothing
        if (self._game.state is not None):
            return

        # assigning clicked cell's row and column
        sender: QPushButton = self.sender()
        row = None
        column = None
        for i in range(len(self._game._table._cells_list)):
            for j in range(len(self._game._table._cells_list)):
                if (self._grid.itemAtPosition(i, j).widget() == sender):
                    row = i
                    column = j

        # case when there is no pawn that had been clicked before
        if (self.from_pawn == (None, None)):
            # case when on clicked cell there is no any pawn
            if (self._game.table.cells_list[row][column].get_most_important_pawn() is None):
                return
            # case when pawn on clicked cell does not belong to the player whose turn is
            elif (self._game.table.cells_list[row][column].get_most_important_pawn().colour != self._game.turn.colour):
                return
            else:
                self.from_pawn = (Pawn_position.TABLE, (row, column))
                sender.setStyleSheet(f"background-color: {self._colors['clicked_pawn']};" + f" color: {self._game.table.cells_list[row][column].get_most_important_pawn().colour}")
                return

        # case when pawn that had been clicked before in on table
        if (self.from_pawn[0] == Pawn_position.TABLE):
            from_row, from_column = self.from_pawn[1]
            # case when pawn that was clicked is the same as the pawn that had been clicked before
            if ((from_row, from_column) == (row, column)):
                self.from_pawn = (None, None)
                sender.setStyleSheet(f"background-color: {self._colors['standard_grid']};" + f" color: {self._game.table.cells_list[row][column].get_most_important_pawn().colour}")
                return
            # case when pawn that was clicked is not bigger that pawn that had been clicked before
            elif (not self._game.table.cells_list[from_row][from_column].get_most_important_pawn().is_bigger(self._game.table.cells_list[row][column].get_most_important_pawn())):
                return
            # case when pawn that was clicked is bigger that pawn that had been clicked before
            elif (self._game.table.cells_list[from_row][from_column].get_most_important_pawn().is_bigger(self._game.table.cells_list[row][column].get_most_important_pawn())):
                self._game.move_pawn_from_table(from_row, from_column, row, column)
                self.from_pawn = (None, None)
                self.to_pawn = (None, None)
                self.synchronize_game()
                # case when playing against AI is enabled and game is not ended
                if (self._game.state is None and settings.ifAi == 'Tak'):
                    self.make_random_move()
                return

        # case when pawn that had been clicked was in the top stack
        if (self.from_pawn[0] == Pawn_position.TOP_STACK):
            from_pawn: Pawn = self._game.player1.pawn_stack[self.from_pawn[1]]
            to_pawn: Pawn = self._game.table.cells_list[row][column].get_most_important_pawn()
            # case when pawn that was clicked is not bigger that pawn that had been clicked before
            if (not from_pawn.is_bigger(to_pawn)):
                return
            # case when pawn that was clicked is bigger that pawn that had been clicked before
            elif (from_pawn.is_bigger(to_pawn)):
                self._game.move_pawn_from_players_stack(self.from_pawn[1], row, column)
                self.delete_button_top_stack(self.from_pawn[1])
                self.from_pawn = (None, None)
                self.to_pawn = (None, None)
                self.synchronize_game()
                # case when playing against AI is enabled and game is not ended
                if (self._game.state is None and settings.ifAi == 'Tak'):
                    self.make_random_move()
                return

        # case when pawn that had been clicked was in the down stack
        if (self.from_pawn[0] == Pawn_position.DOWN_STACK):
            from_pawn: Pawn = self._game.player2.pawn_stack[self.from_pawn[1]]
            to_pawn: Pawn = self._game.table.cells_list[row][column].get_most_important_pawn()
            # case when pawn that was clicked is not bigger that pawn that had been clicked before
            if (not from_pawn.is_bigger(to_pawn)):
                return
            # case when pawn that was clicked is bigger that pawn that had been clicked before
            elif (from_pawn.is_bigger(to_pawn)):
                self._game.move_pawn_from_players_stack(self.from_pawn[1], row, column)
                self.delete_button_down_stack(self.from_pawn[1])
                self.from_pawn = (None, None)
                self.to_pawn = (None, None)
                self.synchronize_game()
                # case when playing against AI is enabled and game is not ended
                if (self._game.state is None and settings.ifAi == 'Tak'):
                    self.make_random_move()
                return

    def synchronize_game(self):
        """
        Method synchronizes gui with game
        """
        self._game.check_game_status()
        if (self._game.state is None):
            self._comunicate.setText(f'Ruch gracza {self._game.turn}')
        elif (self._game.state is True):
            self._comunicate.setText(f'Wygrał gracz {self._game.player1.name}')
            self._save_button.setDisabled(False)
        else:
            self._comunicate.setText(f'Wygrał gracz {self._game.player2.name}')
            self._save_button.setDisabled(False)

        self.synchronize_grid_with_game()

    def synchronize_grid_with_game(self):
        """
        Method synchronizes grid with game
        """
        for i in range(len(self._game.table.cells_list)):
            for j in range(len(self._game.table.cells_list)):
                pawn = self._game.table.cells_list[i][j].get_most_important_pawn()
                button: QPushButton = self._grid.itemAtPosition(i, j).widget()
                if (pawn is None):
                    button.setText('')
                    button.setStyleSheet(f"background-color: {self._colors['standard_grid']};")
                else:
                    button.setText(str(pawn.size))
                    button.setStyleSheet(f"background-color: {self._colors['standard_grid']};" + f" color: {pawn.colour}")
                    button.setFont(QFont('Times', (20 + pawn.size*8)))

    def make_random_move(self):
        """
        Method make random move and synchronizes it with gui
        """
        random_move: Move = choice(Game.get_all_valid_moves(self._game))
        if (random_move.from_where == 'stack'):
            from_index = random_move.from_index
            if (self._game.player1 == self._game.turn):
                self.delete_button_top_stack(from_index)
            elif (self._game.player2 == self._game.turn):
                self.delete_button_down_stack(from_index)
        self._game.make_move(random_move)
        self.synchronize_game()
