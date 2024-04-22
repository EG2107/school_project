from PyQt6.QtWidgets import QWidget, QVBoxLayout


class InputWindow(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("School.Bonus")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def closeEvent(self, event):
        super(InputWindow, self).closeEvent(event)
        self.parent_window.show()
        if self.parent_window.error_win:
            self.parent_window.error_win.close()