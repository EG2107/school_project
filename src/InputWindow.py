from PyQt6.QtWidgets import QWidget, QVBoxLayout


class InputWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("School.Bonus")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def closeEvent(self, event):
        super(InputWindow, self).closeEvent(event)
        self.parent.show()
        if self.parent.error_win:
            self.parent.error_win.close()