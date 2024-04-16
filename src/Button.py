from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QFont


class Button(QPushButton):
    def __init__(self, name, parent):
        super(Button, self).__init__()
        self.setFixedSize(250, 70)
        self.setFlat(True)
        self.setText(name)
        self.setFont(QFont("Helvetica [Cronyx]", 14))