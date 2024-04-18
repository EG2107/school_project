from PyQt6.QtWidgets import QApplication
from os.path import exists
from functions import *
from Button import *
from Table import *
from InputWindow import *
from Window import *


if __name__ == "__main__":
    if not exists("student_database.db"):
        create_database()
    app = QApplication([])
    win = Window()
    win.show()
    app.exec()