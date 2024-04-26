from PyQt6.QtWidgets import QWidget, QVBoxLayout


# класс окна ввода данных
class InputWindow(QWidget):
    # инициализация
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("School.Bonus")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    # переопределение метода closeEvent для того, чтобы снова открыть основное окно после закрытия окна ввода
    def closeEvent(self, event):
        super(InputWindow, self).closeEvent(event)
        self.parent.show()
        if self.parent.error_win:
            self.parent.error_win.close()