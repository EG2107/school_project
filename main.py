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
        self.layout = QVBoxLayout()

        self.main_page_buttons = [Button("Список классов", self), Button("Мероприятия", self), Button("Настройки? / ...", self)]
        self.main_page_buttons[0].clicked.connect(self.open_grade_selection_page)
        for button in self.main_page_buttons:
            self.layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.grade_selection_buttons = []
        for grade in range(5, 12):
            button = Button(str(grade), self)
            button.clicked.connect(lambda state, x = grade : self.open_class_selection_page(x))
            self.grade_selection_buttons.append(button)
        
        button_go_back_from_grade_selection = Button("Назад", self)
        button_go_back_from_grade_selection.clicked.connect(self.open_main_page)
        self.grade_selection_buttons.append(button_go_back_from_grade_selection)

        for button in self.grade_selection_buttons:
            self.layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
            button.hide()

        self.class_selection_buttons = [[] for i in range(12)]
        with open("all_classes.txt", "r") as all_classes:
            for cur_class_name in all_classes:
                cur_class_name = delete_end_of_string(cur_class_name)
                grade = int(cur_class_name[0:1])
                if (len(cur_class_name) == 4):
                    grade = int(cur_class_name[0:2])
                button = Button(cur_class_name, self)
                print(cur_class_name)
                button.clicked.connect(lambda state, x = cur_class_name : self.open_table(x))
                self.class_selection_buttons[grade].append(button)

        for grade in range(12):
            button_go_back_from_class_selection = Button("Назад", self)
            button_go_back_from_class_selection.clicked.connect(self.open_grade_selection_page)
            self.class_selection_buttons[grade].append(button_go_back_from_class_selection)

        for grade in range(12):
            for button in self.class_selection_buttons[grade]:
                self.layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
                button.hide()

        self.setLayout(self.layout)

    def hide_all_buttons(self):
        for button in self.main_page_buttons:
            button.hide()
        for button in self.grade_selection_buttons:
            button.hide()
        for grade in range(5, 12):
            for button in self.class_selection_buttons[grade]:
                button.hide()
    
    def open_main_page(self):
        self.hide_all_buttons()
        for button in self.main_page_buttons:
            button.show()

    def open_grade_selection_page(self):
        self.hide_all_buttons()
        for button in self.grade_selection_buttons:
            button.show()

    def open_class_selection_page(self, grade):
        self.hide_all_buttons()
        for button in self.class_selection_buttons[grade]:
            button.show()

    def open_table(self, name):
        if (self.table is not None):
            self.table.win.close()
            self.table = None
        self.table = Table(name)
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