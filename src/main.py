from PyQt6.QtWidgets import QApplication
from os.path import exists
from functions import get_db_path, create_student_database
from MainWindow import MainWindow


if not exists(get_db_path()):
    create_student_database()
app = QApplication([])
win = MainWindow()
win.show()
app.exec()