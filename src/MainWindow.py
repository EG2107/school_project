from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QScrollArea, QWidget, QPushButton, QVBoxLayout
from Window import Window
from Button import Button

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.want_to_close = False
    
    def initUI(self):
        self.widget = Window()
        button_exit = Button("Закрыть", self)
        button_exit.clicked.connect(self.open_window_closing_menu)
        self.widget.main_page_buttons.append(button_exit)
        self.widget.layout.addWidget(button_exit, alignment=Qt.AlignmentFlag.AlignCenter)

        self.scroll = QScrollArea()

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

        self.setGeometry(100, 100, 1000, 750)
        self.setStyleSheet("background-color: rgb(172, 172, 172)")
        self.setWindowTitle("School.Bonus")
        self.show()

    def closeEvent(self, event):
        if self.want_to_close:
            super().closeEvent(event)
            self.widget.close()
            self.widget.table_students.close()
            if (self.widget.input_win):
                self.widget.input_win.close()
            if (self.widget.error_win):
                self.widget.error_win.close()
        else:
            event.ignore()
            self.open_window_closing_menu()

    def open_window_closing_menu(self):
        self.hide()
        self.exit_win = QWidget()
        self.exit_win.setWindowTitle("School.Bonus")
        self.exit_win.setGeometry(500, 400, 250, 130)

        self.exit_win.layout = QVBoxLayout()
        self.exit_win.setLayout(self.exit_win.layout)

        button_go_back = QPushButton("Вернуться назад")
        button_go_back.clicked.connect(self.return_from_exit_page)
        self.exit_win.layout.addWidget(button_go_back)

        button_exit = QPushButton("Закрыть приложение")
        button_exit.clicked.connect(self.exit)
        self.exit_win.layout.addWidget(button_exit)

        self.exit_win.show()

    def return_from_exit_page(self):
        self.exit_win.close()
        self.show()

    def exit(self):
        self.want_to_close = True
        self.exit_win.close()
        self.close()