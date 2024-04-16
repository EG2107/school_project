from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit


class InputWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Окно ввода данных")
        self.setGeometry(400, 300, 300, 300)
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.input = QLineEdit()
        self.layout.addWidget(self.input, alignment=Qt.AlignmentFlag.AlignCenter)