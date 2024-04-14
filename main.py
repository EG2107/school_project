from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtSql import *
from PyQt6.QtGui import *
import sqlite3
from os.path import exists
import os


global db_name
db_name = "student_database.db"

global row_count
row_count = 0

global column_count
column_count = 4

global students_activities
students_activities = []

global student_id
student_id = dict()


def get_class_file_name(class_number):
    return "student_lists\\" + class_number + ".txt"

def get_activity_file_name(activity_name):
    return "activity_lists\\" + activity_name + ".txt"

def get_activity_description_name(activity_name):
    return "activity_description\\" + activity_name + ".txt"

def delete_end_of_string(string):
    if string[len(string) - 1] == '\n':
        string = string[0 : len(string) - 1]
    return string

def init_data():
    with open("all_classes.txt", "r") as all_classes:
        id = 0
        for cur_class_name in all_classes:
            cur_class_name = delete_end_of_string(cur_class_name)
            with open(get_class_file_name(cur_class_name), "r") as file:
                for student_name in file:
                    student_name = delete_end_of_string(student_name)
                    student_id[student_name + " " + cur_class_name] = id
                    students_activities.append(set())
                    id += 1
        global row_count
        row_count = id

    with open("all_activities.txt", "r") as all_activities:
        for cur_activity_name in all_activities:
            cur_activity_name = delete_end_of_string(cur_activity_name)
            with open(get_activity_file_name(cur_activity_name), "r") as file:
                for line in file:
                    line = delete_end_of_string(line)
                    students_activities[student_id[line]].add(cur_activity_name)

def create_database():
    connection = sqlite3.connect("student_database.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students
        (ID INTEGER, ФИО TEXT, Класс TEXT, Бонусы INTEGER)
    """)

    with open("all_classes.txt", "r") as all_classes:
        id = 0
        for cur_class_name in all_classes:
            cur_class_name = delete_end_of_string(cur_class_name)
            with open(get_class_file_name(cur_class_name), "r") as file:
                for student_name in file:
                    student_name = delete_end_of_string(student_name)
                    cursor.execute("INSERT INTO students VALUES ((?), (?), (?), 0)", (id, student_name, cur_class_name, ))
                    id += 1

    connection.commit()
    connection.close()


class Button(QPushButton):
    def __init__(self, name, parent):
        super(Button, self).__init__()
        self.setFixedSize(200, 70)
        self.setFlat(True)
        self.setText(name)
        self.setFont(QFont("Helvetica [Cronyx]", 14))


class Table(QTableView):
    def __init__(self):
        super().__init__()
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(db_name)
        self.db.open()

        self.model = QSqlTableModel(None, self.db)
        self.model.setTable("students")
        self.model.select()

        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.move(100, 100)
        self.view.resize(800, 600)
        self.view.setColumnWidth(0, 15)
        self.view.setColumnWidth(1, 300)
        self.view.setColumnWidth(2, 70)
        self.view.setColumnWidth(3, 70)
        self.view.hide()


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.table = Table()
        self.setWindowTitle("Название приложения")
        self.setGeometry(100, 100, 1000, 750)
        self.setStyleSheet("background-color: rgb(172, 172, 172);")
        self.create_widgets()
    
    def create_widgets(self):
        self.layout = QVBoxLayout()
        self.create_main_page_buttons()
        self.crate_grade_selection_buttons()
        self.create_class_selection_buttons()
        self.create_activity_selection_buttons()
        self.create_activity_inner_page()
        self.create_activity_description_pages()
        self.setLayout(self.layout)
        self.hide_all_buttons()
        self.open_main_page()

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
        
    def create_class_selection_buttons(self):
        self.class_selection_buttons = [[] for i in range(12)]
        with open("all_classes.txt", "r") as all_classes:
            for cur_class_name in all_classes:
                cur_class_name = delete_end_of_string(cur_class_name)
                grade = int(cur_class_name[0:1])
                if len(cur_class_name) == 4:
                    grade = int(cur_class_name[0:2])
                button = Button(cur_class_name, self)
                button.clicked.connect(lambda state, x = cur_class_name : self.open_table_class(x))
                self.class_selection_buttons[grade].append(button)

        for grade in range(12):
            button_go_back_from_class_selection = Button("Назад", self)
            button_go_back_from_class_selection.clicked.connect(self.open_grade_selection_page)
            self.class_selection_buttons[grade].append(button_go_back_from_class_selection)

            for button in self.class_selection_buttons[grade]:
                self.layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

    def create_activity_selection_buttons(self):
        self.activity_selection_buttons = []
        with open("all_activities.txt", "r") as all_activities:
            for cur_activity_name in all_activities:
                cur_activity_name = delete_end_of_string(cur_activity_name)
                button = Button(cur_activity_name, self)
                button.clicked.connect(lambda state, x = cur_activity_name : self.open_activity_inner_page(x))
                self.activity_selection_buttons.append(button)

        button_go_back_from_activity_selection = Button("Назад", self)
        button_go_back_from_activity_selection.clicked.connect(self.open_main_page)
        self.activity_selection_buttons.append(button_go_back_from_activity_selection)

        for button in self.activity_selection_buttons:
            self.layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

    def create_activity_inner_page(self):
        self.activity_inner_page_widgets = {}
        with open("all_activities.txt", "r") as all_activities:
            for cur_activity_name in all_activities:
                cur_activity_name = delete_end_of_string(cur_activity_name)
                self.activity_inner_page_widgets[cur_activity_name] = []

                label_activity_name = QLabel(cur_activity_name)
                label_activity_name.setFont(QFont("Helvetica [Cronyx]", 18))
                self.activity_inner_page_widgets[cur_activity_name].append(label_activity_name)

                button_participants_list = Button("Участники", self)
                button_participants_list.clicked.connect(lambda state, x = cur_activity_name : self.open_table_activity(x))
                self.activity_inner_page_widgets[cur_activity_name].append(button_participants_list)

                button_description = Button("Описание", self)
                button_description.clicked.connect(lambda state, x = cur_activity_name : self.open_activity_description(x))
                self.activity_inner_page_widgets[cur_activity_name].append(button_description)

                button_go_back_from_activity_inner_page = Button("Назад", self)
                button_go_back_from_activity_inner_page.clicked.connect(self.open_activity_selection_page)
                self.activity_inner_page_widgets[cur_activity_name].append(button_go_back_from_activity_inner_page)

                for widget in self.activity_inner_page_widgets[cur_activity_name]:
                    self.layout.addWidget(widget, alignment=Qt.AlignmentFlag.AlignCenter)

    def create_activity_description_pages(self):
        self.activity_description_page_widgets = {}
        with open("all_activities.txt", "r") as all_activities:
            for cur_activity_name in all_activities:
                cur_activity_name = delete_end_of_string(cur_activity_name)

                with open(get_activity_description_name(cur_activity_name)) as description:
                    self.activity_description_page_widgets[cur_activity_name] = []

                    label_description = QLabel(*description)
                    label_description.setFont(QFont("Helvetica [Cronyx]", 12))
                    self.layout.addWidget(label_description, alignment=Qt.AlignmentFlag.AlignCenter)
                    self.activity_description_page_widgets[cur_activity_name].append(label_description)

                    button_go_back_from_activity_description = Button("Назад", self)
                    button_go_back_from_activity_description.clicked.connect(lambda state, x = cur_activity_name : self.open_activity_inner_page(x))
                    self.layout.addWidget(button_go_back_from_activity_description, alignment=Qt.AlignmentFlag.AlignCenter)
                    self.activity_description_page_widgets[cur_activity_name].append(button_go_back_from_activity_description)

    def hide_all_buttons(self):
        self.table.view.hide()
        for button in self.main_page_buttons:
            button.hide()
        for button in self.grade_selection_buttons:
            button.hide()
        for grade in range(12):
            for button in self.class_selection_buttons[grade]:
                button.hide()
        for button in self.activity_selection_buttons:
            button.hide()
        for widgets in self.activity_inner_page_widgets.values():
            for widget in widgets:
                widget.hide()
        for widgets in self.activity_description_page_widgets.values():
            for widget in widgets:
                widget.hide()
    
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

    def open_activity_inner_page(self, activity_name):
        self.hide_all_buttons()
        for button in self.activity_inner_page_widgets[activity_name]:
            button.show()

    def open_activity_description(self, activity_name):
        self.hide_all_buttons()
        for widget in self.activity_description_page_widgets[activity_name]:
            widget.show()

    def open_table_class(self, name):
        self.table.view.hide()
        self.table.view.setWindowTitle(f"Список учеников класса {name}")
        self.table.view.show()
        for i in range(column_count):
            self.table.view.showColumn(i)
        for i in range(row_count):
            self.table.view.showRow(i)
            index = self.table.view.model().index(i, 2)
            cur_class_name = self.table.view.model().data(index)
            if (cur_class_name != name):
                self.table.view.hideRow(i)
        self.table.view.hideColumn(0)
        self.table.view.hideColumn(2)

    def open_table_activity(self, name):
        self.table.view.hide()
        self.table.view.setWindowTitle(f"Список участников мероприятия '{name}'")
        self.table.view.show()
        for i in range(column_count):
            self.table.view.showColumn(i)
        for i in range(row_count):
            self.table.view.showRow(i)
            if (not (name in students_activities[i])):
                self.table.view.hideRow(i)
        self.table.view.hideColumn(0)


if __name__ == "__main__":
    init_data()
    if not exists(db_name):
        create_database()
    app = QApplication([])
    win = Window()
    win.show()
    app.exec()