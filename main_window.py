from PyQt6.QtWidgets import QMainWindow
from start_window import StartWindow
from play_window import PlayWindow
from settings_window import SettingsWindow
from game_history_window import GameHistoryWindow
from databse import get_data


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        """
        Constructor for MainWindow class.
        It stores game's settings and sets central widget for StartWindow.
        """
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('Gobblety')
        self.setFixedSize(0, 0)
        self.setGeometry(0, 0, 0, 0)
        self.setCentralWidget(StartWindow(self))
        self.statusBar().setSizeGripEnabled(False)

    def set_game_widget(self, game):
        """
        Method changes central widget for PlayWindow
        """
        self.setFixedSize(0, 0)
        self.setCentralWidget(PlayWindow(game, 80, self))

    def set_start_widget(self):
        """
        Method changes centeal widget for StartWindow
        """
        self.setFixedSize(0, 0)
        self.setCentralWidget(StartWindow(self))

    def set_settings_widget(self):
        """
        Method changes centeal widget for SettingsWindow
        """
        self.setFixedSize(0, 0)
        self.setCentralWidget(SettingsWindow(self))

    def set_history_widget(self):
        """
        Method changes centeal widget for GameHistoryWindow
        """
        self.setFixedSize(0, 0)
        self.setCentralWidget(GameHistoryWindow(self, get_data()))
