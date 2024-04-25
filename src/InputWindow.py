from PyQt6.QtWidgets import QWidget, QVBoxLayout


# класс окна ввода данных
class InputWindow(QWidget):
    # инициализация
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("School.Bonus")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    # переопределение метода closeEvent для того, чтобы снова открыть основное окно после закрытия окна ввода
    def closeEvent(self, event):
        super(InputWindow, self).closeEvent(event)
        self.parent_window.show()
        if self.parent_window.error_win:
            self.parent_window.error_win.close()