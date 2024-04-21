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