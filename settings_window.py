from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QComboBox, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import settings


class SettingsWindow(QWidget):

    def __init__(self, parent=None):
        """
        Constructor for SettingsWindow class, it creates widget that contains combo boxes and line edits which allow user
        to change settings.
        """
        super().__init__()
        self._parent = parent
        self.make_gui()

    def make_gui(self):
        """
        Method creates main layout and attaches it to SettingsWindow objects.
        """
        main_vbox = QVBoxLayout()
        self.make_main_vbox(main_vbox)
        # setting SettingsWindow layout as main_vbox
        self.setLayout(main_vbox)

    def make_main_vbox(self, main_vbox: QVBoxLayout):
        """
        Method creates top_hbox, comunicate and bottom_hbox inside of main_vbox given as an argument.
        """
        # creating layouts
        top_hbox = QHBoxLayout()
        top_hbox.setAlignment(Qt.AlignmentFlag.AlignTop)
        comunicate = QLabel()
        bottom_hbox = QHBoxLayout()
        self.make_top_hbox(top_hbox)
        self.make_comunicate(comunicate)
        self.make_bottom_hbox(bottom_hbox)

        # adding layouts and comunicate to main_vbox
        main_vbox.addLayout(top_hbox)
        main_vbox.addItem(QSpacerItem(0, 100, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        main_vbox.addWidget(comunicate)
        main_vbox.addLayout(bottom_hbox)

    def make_top_hbox(self, top_hbox: QHBoxLayout):
        """
        Method creates names_vbox, table_size_and_ai_vbox, pawns_number_vbox inside of top_hbox given as an argument.
        """
        names_vbox = QVBoxLayout()
        table_size_and_ai_vbox = QVBoxLayout()
        pawns_number_vbox = QVBoxLayout()
        self.make_names_vbox(names_vbox)
        self.make_table_size_and_ai_vbox(table_size_and_ai_vbox)
        self.make_pawns_number_vbox(pawns_number_vbox)

        # settings layouts, stretches to top_hbox
        top_hbox.addStretch()
        top_hbox.addLayout(names_vbox)
        top_hbox.addSpacerItem(QSpacerItem(100, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        top_hbox.addLayout(table_size_and_ai_vbox)
        top_hbox.addSpacerItem(QSpacerItem(100, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        top_hbox.addLayout(pawns_number_vbox)
        top_hbox.addStretch()

    def make_names_vbox(self, names_vbox):
        """
        Method creates name labels and names line edits for both players inside of names_vbox given as an argument.
        """
        # creating players name labels and line edits
        player1_name_label = QLabel(text="Nazwa gracza 1")
        player1_name_line_edit = QLineEdit()
        player1_name_line_edit.setFixedSize(200, 25)
        player1_name_line_edit.setText(settings.player1Name)

        player2_name_label = QLabel(text="Nazwa gracza 2")
        player2_name_line_edit = QLineEdit()
        player2_name_line_edit.setFixedSize(200, 25)
        player2_name_line_edit.setText(settings.player2Name)

        name_spacer = QSpacerItem(0, 50, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # adding widgets to names_vbox
        names_vbox.addWidget(player1_name_label)
        names_vbox.addWidget(player1_name_line_edit)
        names_vbox.addItem(name_spacer)
        names_vbox.addWidget(player2_name_label)
        names_vbox.addWidget(player2_name_line_edit)

        self._player1_name_line_edit = player1_name_line_edit
        self._player2_name_line_edit = player2_name_line_edit

    def make_table_size_and_ai_vbox(self, table_size_and_ai_vbox):
        """
        Method creates table size and if ai comboboxes inside of table_size_and_ai_vbox given as an argument.
        """
        # creating table_size and if_ai combobx and label
        table_size_label = QLabel(text="Rozmiar planszy")
        table_size_combobox = QComboBox()
        table_size_combobox.setFixedSize(50, 25)
        table_size_combobox.addItems(['2', '3', '4', '5', '6', '7'])
        for i in range(table_size_combobox.count()):
            if (table_size_combobox.itemText(i) == settings.tableDimension):
                table_size_combobox.setCurrentIndex(i)
                break

        if_ai_label = QLabel(text='Graj przeciwko komputerowi')
        if_ai_combobox = QComboBox()
        if_ai_combobox.setFixedSize(50, 25)
        if_ai_combobox.addItems(['Nie', 'Tak'])
        for i in range(if_ai_combobox.count()):
            if (if_ai_combobox.itemText(i) == settings.ifAi):
                if_ai_combobox.setCurrentIndex(i)
                break

        table_size_spacer = QSpacerItem(0, 50, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # adding widgets to table_size_and_ai_vbox
        table_size_and_ai_vbox.addWidget(table_size_label)
        table_size_and_ai_vbox.addWidget(table_size_combobox)
        table_size_and_ai_vbox.addItem(table_size_spacer)
        table_size_and_ai_vbox.addWidget(if_ai_label)
        table_size_and_ai_vbox.addWidget(if_ai_combobox)
        table_size_and_ai_vbox.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._table_size_combobox = table_size_combobox
        self._if_ai_combobox = if_ai_combobox

    def make_pawns_number_vbox(self, pawns_number_vbox):
        """
        Method creates pawn sizes and each pawn quantity comboboxes inside of pawns_number_vbox given as an argument.
        """
        # creating pawn size and each pawn labels and comboboxes
        pawn_sizes_label = QLabel(text="Ilość rozmiarów pionków")
        pawn_sizes_combobox = QComboBox()
        pawn_sizes_combobox.setFixedSize(50, 25)
        pawn_sizes_combobox.addItems(['1', '2', '3', '4', '5'])
        for i in range(pawn_sizes_combobox.count()):
            if (pawn_sizes_combobox.itemText(i) == settings.pawnSizes):
                pawn_sizes_combobox.setCurrentIndex(i)
                break

        pawn_spacer = QSpacerItem(0, 50, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        each_pawn_label = QLabel(text='Ilość pionków danego rozmiaru')
        each_pawn_combobox = QComboBox()
        each_pawn_combobox.setFixedSize(50, 25)
        each_pawn_combobox.addItems(['1', '2', '3', '4'])
        for i in range(each_pawn_combobox.count()):
            if (each_pawn_combobox.itemText(i) == settings.quantityOfEachSize):
                each_pawn_combobox.setCurrentIndex(i)
                break

        # adding widgets to pawns_number_vbox
        pawns_number_vbox.addWidget(pawn_sizes_label)
        pawns_number_vbox.addWidget(pawn_sizes_combobox)
        pawns_number_vbox.addItem(pawn_spacer)
        pawns_number_vbox.addWidget(each_pawn_label)
        pawns_number_vbox.addWidget(each_pawn_combobox)

        self._pawn_sizes_combobox = pawn_sizes_combobox
        self._each_pawn_combobox = each_pawn_combobox

    def make_comunicate(self, comunicate: QLabel):
        """
        Method creates comunicate label, which informs user when settings are saved.
        """
        # creating comunicate
        comunicate.setText('Wybierz ustawienia rozgrywki')
        comunicate.setFont(QFont('Times',  18))
        comunicate.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._comunicate = comunicate

    def make_bottom_hbox(self, bottom_hbox: QHBoxLayout):
        """
        Method creates save_vbox and exit_vbox inside of bottom_hbox gien as an argument.
        """
        # creating save_vbox and exit_vbox layouts
        save_vbox = QVBoxLayout()
        save_vbox.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        exit_vbox = QHBoxLayout()
        exit_vbox.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        self.make_save_vbox(save_vbox)
        self.make_exit_vbox(exit_vbox)

        # adding spacer and layouts to bottom_hbox
        bottom_hbox.addItem(QSpacerItem(0, 200, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        bottom_hbox.addLayout(exit_vbox)
        bottom_hbox.addLayout(save_vbox)
        pass

    def make_save_vbox(self, save_vbox):
        """
        Method creates save_button inside of save_vbox given as an argument.
        This button is responsible for saving user's settings.
        """
        # making save_button
        save_button = QPushButton()
        save_button.setFixedSize(220, 75)
        save_button.setText('Zapisz ustawienia')
        save_button.setFont(QFont('Times',  18))
        save_button.clicked.connect(self.on_click_save)
        save_vbox.addWidget(save_button)

    def make_exit_vbox(self, exit_vbox):
        """
        Method creates exit_button inside of exit_vbox given as an argument.
        This button is responsible for exiting to StartWindow.
        """
        # making exit_button
        exit_button = QPushButton()
        exit_button.setFixedSize(220, 75)
        exit_button.setText('Wyjdź')
        exit_button.setFont(QFont('Times',  18))
        exit_button.clicked.connect(self.on_click_exit)
        exit_vbox.addWidget(exit_button)

    def on_click_save(self):
        """
        Method is called when save_button is clicked.
        It saves chosen settings to parent's fields, if players names are different.
        Otherwise it informs user to change players name
        """
        player1_name = self._player1_name_line_edit.text()
        player2_name = self._player2_name_line_edit.text()
        if (player1_name == player2_name):
            self._comunicate.setText('Nazwy graczy nie mogą być identyczne')
            return

        settings.player1Name = player1_name
        settings.player2Name = player2_name
        settings.tableDimension = self._table_size_combobox.currentText()
        settings.pawnSizes = self._pawn_sizes_combobox.currentText()
        settings.quantityOfEachSize = self._each_pawn_combobox.currentText()
        settings.ifAi = self._if_ai_combobox.currentText()
        self._comunicate.setText('Pomyślnie zapisano ustawienia')

    def on_click_exit(self):
        """
        Method is called when exit_button is clicked.
        It changes MainWindow central widget to StartWindow.
        """
        self._parent.set_start_widget()
