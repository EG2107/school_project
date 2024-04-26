from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QFont


# класс кнопки
class Button(QPushButton):
    # инициализация
    def __init__(self, text, parent):
        super(Button, self).__init__()
        self.setFixedSize(300, 70)
        self.setFlat(True)
        self.setText(text)
        self.setFont(QFont("Helvetica [Cronyx]", 14))