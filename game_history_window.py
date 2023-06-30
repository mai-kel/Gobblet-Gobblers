from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QListWidget, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from game import Game
from databse import get_data
from play_window import PlayWindow


class GameHistoryWindow(QWidget):

    def __init__(self, parent, games_list):
        """
        Constructor for GameHistoryWindow class.
        It takes parent and games_list as arguments.
        It makes widget containing:
            - ListWidget with representation of games list given as an argument
            - Widget containing grahpic representation of chosen game
            - Button which returns do menu
        """
        super().__init__()

        # main vbox contains top_hbox and bottom_hbox
        main_vbox = QVBoxLayout()
        top_hbox = QHBoxLayout()
        bottom_hbox = QHBoxLayout()
        bottom_hbox.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        main_vbox.addLayout(top_hbox)
        main_vbox.addItem(QSpacerItem(0, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        main_vbox.addLayout(bottom_hbox)

        # creating list_widget, which will store text representation of all games list
        list_widget = QListWidget()
        list_widget.setFixedWidth(200)
        list_widget.setMinimumHeight(300)
        list_widget.currentItemChanged.connect(self.on_list_item_changed)
        # adding items to list_widget
        game: Game
        for game in games_list:
            outcome = ''
            if (game.state is True):
                outcome = '1 - 0'
            elif (game.state is False):
                outcome = '0 - 1'
            else:
                outcome = 'Gra nierozstrzygnięta'

            list_widget.addItem(f'{game.player1.name} vs {game.player2.name};   {outcome}')

        # _game_preview is Widget which contains graphic representation of Game objects, it shows end result of game

        self._game_preview = QWidget()
        self._game_preview_hbox = QHBoxLayout()

        # adding list_widget and _game_preview to top_hobx
        top_hbox.addWidget(list_widget)
        top_hbox.addWidget(self._game_preview)

        top_hbox.addSpacing(20)

        # creating exit_button which will be responsible for changing MainWindow's central widget to StartWindow
        exit_button = QPushButton()
        exit_button.setText('Wyjdź')
        exit_button.clicked.connect(self.on_clicked_exit)
        exit_button.setFont(QFont('Times',  18))
        exit_button.setFixedWidth(200)
        bottom_hbox.addWidget(exit_button)

        # setting main_vbox as GameHistoryWindow object layout
        self.setLayout(main_vbox)

        # saving variables needed in other methods to objects private fields
        self._parent = parent
        self._list_widget = list_widget
        self._top_hbox = top_hbox

    def on_clicked_exit(self):
        """
        Method is called when exit_button is clicked.
        It changes MainWindow's central widget to StartWindow.
        """
        self._parent.set_start_widget()

    def on_list_item_changed(self):
        """
        Method is called when item in list_widget is changed.
        Method displays visualization of ending state of chosen game.
        It also rezisez window so that game preview fit inside it.
        """
        chosen_item_index = self._list_widget.currentRow()
        self._top_hbox.removeWidget(self._game_preview)
        self._game_preview = QWidget()
        vbox_preview = QVBoxLayout()
        play_window = PlayWindow(get_data()[chosen_item_index], 80)
        play_window.synchronize_game()
        hbox = play_window.get_grid_stacks_hbox()
        hbox.setParent(None)
        vbox_preview.addLayout(hbox)
        vbox_preview.addStretch()
        self._game_preview.setLayout(vbox_preview)
        self._top_hbox.addWidget(self._game_preview)
        self._parent.setFixedSize(0, 0)
