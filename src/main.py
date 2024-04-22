from PyQt6.QtWidgets import QApplication
from os.path import exists
from functions import create_database
from Window import Window


if __name__ == "__main__":
    if not exists("student_database.db"):
        create_database()
    app = QApplication([])
    win = Window()
    win.show()
    app.exec()