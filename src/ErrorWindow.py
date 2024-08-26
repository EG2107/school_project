from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt6.QtGui import QFont


class ErrorWindow(QWidget):
    def __init__(self, text):
        super().__init__()
        self.setWindowTitle("School.Bonus")
        self.setGeometry(425, 400, 250, 150)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        label = QLabel(text)
        label.setFont(QFont("Helvetica [Cronyx]", 12))
        self.layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)

        button_go_back = QPushButton("Вернуться назад")
        button_go_back.clicked.connect(self.close)
        self.layout.addWidget(button_go_back)

        self.show()