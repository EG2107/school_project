from os.path import exists
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtSql import *
from PyQt6.QtGui import *
import sqlite3

def get_class_db_name(class_number):
    return "student_databases\\students_" + class_number + ".db"

def get_class_file_name(class_number):
    return "stdent_lists\\" + class_number + ".txt"

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


class Button(QPushButton):
    def __init__(self, name, parent):
        super(Button, self).__init__()
        self.setFixedSize(200, 70)
        self.setFlat(True)
        self.setText(name)
        self.setFont(QFont("Helvetica [Cronyx]", 14))
        self.show()


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.table = None
        self.setWindowTitle("Название приложения")
        self.setGeometry(100, 100, 1200, 900)
        self.setStyleSheet("background-color: rgb(172, 172, 172);")
        self.create_widgets()
    
    def create_widgets(self):
        layout = QVBoxLayout()

        button_all_classes = Button("Список классов", self)
        button_all_classes.clicked.connect(self.button_clicked)
        button_all_events = Button("Мероприятия", self)
        button_options = Button("Настройки? / ...", self)

        layout.addWidget(button_all_classes, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(button_all_events, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(button_options, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
    
    def button_clicked(self):
        if (self.table is None):
            self.table = Table("10-1")
        self.table.win.show()


class Table(QTableView):
    def __init__(self, class_name):
        super().__init__()
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(get_class_db_name(class_name))
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


app = QApplication([])
win = Window()
win.show()
app.exec()