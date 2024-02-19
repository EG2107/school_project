from os.path import exists
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtSql import *
from PyQt6.QtGui import *
import sqlite3
import os


def get_class_db_name(class_number):
    return "student_databases\\students_" + class_number + ".db"

def get_class_file_name(class_number):
    return "student_lists\\" + class_number + ".txt"

def get_activity_db_name(activity_name):
    return "activity_databases\\activity_" + activity_name + ".db"

def get_activity_file_name(activity_name):
    return "activity_lists\\" + activity_name + ".txt"

def delete_end_of_string(string):
    if string[len(string) - 1] == '\n':
        string = string[0 : len(string) - 1]
    return string

def create_table_students(db_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students
        (ID INTEGER, ФИО TEXT, Бонусы INTEGER)
    """)
    connection.commit()
    connection.close()

def create_table_activities(db_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students
        (ФИО TEXT, Класс TEXT)
    """)
    connection.commit()
    connection.close()

def add_student_to_student_database(db_name, id, name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO students VALUES ((?), (?), 0)", (id, name,))
    connection.commit()
    connection.close()

def add_student_to_activity_database(db_name, name, student_class):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO students VALUES ((?), (?))", (name, student_class,))
    connection.commit()
    connection.close()

def create_databases():
    with open("all_classes.txt", "r") as all_classes:
        for cur_class_name in all_classes:
            cur_class_name = delete_end_of_string(cur_class_name)
            if exists(get_class_db_name(cur_class_name)):
                os.remove(get_class_db_name(cur_class_name))
            create_table_students(get_class_db_name(cur_class_name))
            with open(get_class_file_name(cur_class_name), "r") as file:
                id = 0
                for student_name in file:
                    student_name = delete_end_of_string(student_name)
                    id += 1
                    add_student_to_student_database(get_class_db_name(cur_class_name), id, student_name)

    with open("all_activities.txt", "r") as all_activities:
        for cur_activity_name in all_activities:
            cur_activity_name = delete_end_of_string(cur_activity_name)
            if exists(get_activity_db_name(cur_activity_name)):
                os.remove(get_activity_db_name(cur_activity_name))
            create_table_activities(get_activity_db_name(cur_activity_name))
            with open(get_activity_file_name(cur_activity_name), "r") as file:
                for line in file:
                    line = delete_end_of_string(line)
                    student_name, student_class = line.rsplit(' ', 1)
                    add_student_to_activity_database(get_activity_db_name(cur_activity_name), student_name, student_class)


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
        self.setGeometry(100, 100, 1000, 750)
        self.setStyleSheet("background-color: rgb(172, 172, 172);")
        self.create_widgets()
    
    def create_widgets(self):
        self.layout = QVBoxLayout()
        self.create_main_page_buttons()
        self.crate_grade_selection_buttons()
        self.create_class_selection_buttons()
        self.create_acivity_selection_buttons()
        self.setLayout(self.layout)

    def create_main_page_buttons(self):
        button_student_lists = Button("Список классов", self)
        button_student_lists.clicked.connect(self.open_grade_selection_page)
        button_activity_lists = Button("Мероприятия", self)
        button_activity_lists.clicked.connect(self.open_activity_selection_page)
        button_options = Button("Настройки? / ...", self)

        self.main_page_buttons = [button_student_lists, button_activity_lists, button_options]
        for button in self.main_page_buttons:
            self.layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

    def crate_grade_selection_buttons(self):
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
        
    def create_class_selection_buttons(self):
        self.class_selection_buttons = [[] for i in range(12)]
        print("Classes:")
        with open("all_classes.txt", "r") as all_classes:
            for cur_class_name in all_classes:
                cur_class_name = delete_end_of_string(cur_class_name)
                grade = int(cur_class_name[0:1])
                if len(cur_class_name) == 4:
                    grade = int(cur_class_name[0:2])
                button = Button(cur_class_name, self)
                button.clicked.connect(lambda state, x = cur_class_name : self.open_table_students(x))
                self.class_selection_buttons[grade].append(button)
                print(cur_class_name)
        print("Done loading class databases\n")

        for grade in range(12):
            button_go_back_from_class_selection = Button("Назад", self)
            button_go_back_from_class_selection.clicked.connect(self.open_grade_selection_page)
            self.class_selection_buttons[grade].append(button_go_back_from_class_selection)

        for grade in range(12):
            for button in self.class_selection_buttons[grade]:
                self.layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
                button.hide()

    def create_acivity_selection_buttons(self):
        self.activity_selection_buttons = []
        print("Activities:")
        with open("all_activities.txt", "r") as all_activities:
            for cur_activity_name in all_activities:
                cur_activity_name = delete_end_of_string(cur_activity_name)
                button = Button(cur_activity_name, self)
                button.clicked.connect(lambda state, x = cur_activity_name : self.open_table_activities(x))
                self.activity_selection_buttons.append(button)
                print(cur_activity_name)
        print("Done loading activity databases\n")
        button_go_back_from_acivity_selection = Button("Назад", self)
        button_go_back_from_acivity_selection.clicked.connect(self.open_main_page)
        self.activity_selection_buttons.append(button_go_back_from_acivity_selection)

        for button in self.activity_selection_buttons:
            self.layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
            button.hide()

    def hide_all_buttons(self):
        for button in self.main_page_buttons:
            button.hide()
        for button in self.grade_selection_buttons:
            button.hide()
        for grade in range(12):
            for button in self.class_selection_buttons[grade]:
                button.hide()
        for button in self.activity_selection_buttons:
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

    def open_activity_selection_page(self):
        self.hide_all_buttons()
        for button in self.activity_selection_buttons:
            button.show()

    def open_table_students(self, name):
        if self.table is not None:
            self.table.win.close()
            self.table = None
        self.table = Table(get_class_db_name(name), f"Список учеников класса {name}")
        self.table.win.setColumnWidth(0, 20)
        self.table.win.setColumnWidth(1, 300)
        self.table.win.setColumnWidth(2, 80)
        self.table.win.show()

    def open_table_activities(self, name):
        if self.table is not None:
            self.table.win.close()
            self.table = None
        self.table = Table(get_activity_db_name(name), f"Список участников мероприятия {name}")
        self.table.win.setColumnWidth(0, 300)
        self.table.win.setColumnWidth(1, 80)
        self.table.win.show()


class Table(QTableView):
    def __init__(self, datadase_name, title):
        super().__init__()
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(datadase_name)
        db.open()

        model = QSqlTableModel(None, db)
        model.setTable("students")
        model.select()

        self.win = QTableView()
        self.win.setModel(model)
        self.win.setWindowTitle(title)
        self.win.move(100, 100)
        self.win.resize(800, 600)


create_databases()
app = QApplication([])
win = Window()
win.show()
app.exec()