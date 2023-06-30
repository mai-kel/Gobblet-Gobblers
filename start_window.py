from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout
from PyQt6.QtGui import QFont
from game import Game
from table import Table
from player import Player
from PyQt6.QtCore import Qt
import settings


class StartWindow(QWidget):
    def __init__(self, parent=None):
        """
        Constructor for StartWindow class. It creates widget which contains:
            - play button
            - config button
            - history button
            - exit button
        """
        super(StartWindow, self).__init__(parent)
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox.setSpacing(30)
        vbox.setContentsMargins(100, 50, 100, 50)

        play_button = QPushButton()
        play_button.setText('Graj')
        play_button.setFont(QFont('Times', 40))
        play_button.setFixedSize(600, 100)
        play_button.clicked.connect(self.on_click_play)

        config_button = QPushButton()
        config_button.setText('Ustawienia')
        config_button.setFont(QFont('Times', 40))
        config_button.setFixedSize(600, 100)
        config_button.clicked.connect(self.on_click_config)

        history_button = QPushButton()
        history_button.setText('Historia rozgrywek')
        history_button.setFont(QFont('Times', 40))
        history_button.setFixedSize(600, 100)
        history_button.clicked.connect(self.on_click_history)

        exit_button = QPushButton()
        exit_button.setText('Wyjdź')
        exit_button.setFont(QFont('Times', 40))
        exit_button.setFixedSize(600, 100)
        exit_button.clicked.connect(self.on_click_exit)

        vbox.addWidget(play_button)
        vbox.addWidget(config_button)
        vbox.addWidget(history_button)
        vbox.addWidget(exit_button)

        self.setLayout(vbox)
        self._parent = parent

    def on_click_history(self):
        """
        Method is called when history_button is clicked.
        It changes MainWindow central widget for GameHistoryWindow.
        """
        self._parent.set_history_widget()
        return

    def on_click_exit(self):
        """
        Method is called when exit_button is clicked.
        It closes application.
        """
        exit()

    def on_click_config(self):
        """
        Method is called when config_button is clicked.
        It changes MainWindow central widget for SettingsWindow.
        """
        self._parent.set_settings_widget()
        return

    def on_click_play(self):
        """
        Method is called when play_button is clicked.
        It changes MainWindow central widget for PlayWindow according to settings stored in parent's fields.
        """
        table_dimension = int(settings.tableDimension)
        sizes = int(settings.pawnSizes)
        quantity_of_each_size = int(settings.quantityOfEachSize)
        player1 = Player(settings.player1Name, settings.player1Colour, Player.generate_pawn_stack(sizes, quantity_of_each_size, settings.player1Colour))
        player2 = Player(settings.player2Name, settings.player2Colour, Player.generate_pawn_stack(sizes, quantity_of_each_size, settings.player2Colour))
        table = Table((Table.generate_empty_cells_list(table_dimension)))
        game = Game(table, player1, None, player1, player2)
        self._parent.set_game_widget(game)
