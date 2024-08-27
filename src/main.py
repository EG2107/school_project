from PyQt6.QtWidgets import QApplication
from os.path import exists
from functions import create_student_database
from Window import Window


if not exists("student_database.db"):
    create_student_database()
app = QApplication([])
win = Window()
win.show()
app.exec()