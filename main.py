from os.path import exists
from PyQt6.QtWidgets import *
from PyQt6.QtSql import *
from PyQt6.QtGui import QFont
import sqlite3

def get_class_db_name(class_number):
    return "students_" + class_number + ".db"

def get_class_file_name(class_number):
    return class_number + ".txt"

def delete_end_of_string(string):
    if (string[len(string) - 1] == '\n'):
        string = string[0 : len(string) - 1]
    return string

def create_table(db_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students
        (ID INTEGER, ФИО TEXT, Бонусы INTEGER)
    """)
    connection.commit()
    connection.close()

def add_student(db_name, id, name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO students VALUES ((?), (?), 0)", (id, name,))
    connection.commit()
    connection.close()

with open("all_classes.txt", "r") as all_classes:
    for cur_class_name in all_classes:
        cur_class_name = delete_end_of_string(cur_class_name)
        if (not exists(get_class_db_name(cur_class_name))):
            create_table(get_class_db_name(cur_class_name))
            with (open(get_class_file_name(cur_class_name), "r") as file):
                id = 0
                for line in file:
                    line = delete_end_of_string(line)
                    id += 1
                    add_student(get_class_db_name(cur_class_name), id, line)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.t = None
        self.setWindowTitle("Название приложения")
        self.setGeometry(100, 100, 1200, 900)
        self.create_widgets()
        self.setStyleSheet("background-color: rgb(172, 172, 172);")
    
    def create_widgets(self):
        button1 = QPushButton("Список классов", self)
        button1.setGeometry(500, 300, 200, 70)
        button1.setFont(QFont("Helvetica [Cronyx]", 14))
        button1.setFlat(True)
        button1.clicked.connect(self.button_clicked)
        button2 = QPushButton("Мероприятия", self)
        button2.setGeometry(500, 400, 200, 70)
        button2.setFont(QFont("Helvetica [Cronyx]", 14))
        button2.setFlat(True)
        button3 = QPushButton("Настройки? / ...", self)
        button3.setGeometry(500, 500, 200, 70)
        button3.setFont(QFont("Helvetica [Cronyx]", 14))
        button3.setFlat(True)
    
    def button_clicked(self):
        if (self.t is None):
            self.t = Table()
        self.t.showw()


class Table(QTableView):
    def __init__(self):
        super().__init__()
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("students_10-1.db")
        db.open()

        model = QSqlTableModel(None, db)
        model.setTable("students")
        model.select()

        self.win = QTableView()
        self.win.setModel(model)
        self.win.setWindowTitle("Список учеников")
        self.win.move(100, 100)
        self.win.resize(800, 600)
        self.win.setColumnWidth(0, 20)
        self.win.setColumnWidth(1, 200)
        self.win.setColumnWidth(2, 80)

    def showw(self):
        self.win.show()


app = QApplication([])
win = Window()
win.show()
app.exec()