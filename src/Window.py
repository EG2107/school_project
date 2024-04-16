from PyQt6.QtCore import *
from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtSql import *
from PyQt6.QtGui import *
import sqlite3
from functions import *
from Button import *
from Table import *
from InputWindow import *
from variables import *


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.table = Table()
        self.setWindowTitle("Название приложения")
        self.setGeometry(100, 100, 1000, 750)
        self.setStyleSheet("background-color: rgb(172, 172, 172);")
        self.create_widgets()
        self.open_main_page()
    
    def create_widgets(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.create_main_page_buttons()
        self.crate_grade_selection_buttons()
        self.create_class_selection_buttons()
        self.create_activity_selection_buttons()
        self.create_activity_inner_page()
        self.create_activity_description_pages()
        self.hide_all_buttons()
        self.input_win = None

    def create_main_page_buttons(self):
        button_guide = Button("Руководство", self)
        # add window that tells how tf you need to use this
        button_student_lists = Button("Список классов", self)
        button_student_lists.clicked.connect(self.open_grade_selection_page)
        button_activity_lists = Button("Мероприятия", self)
        button_activity_lists.clicked.connect(self.open_activity_selection_page)
        button_merch = Button("Мерч", self)

        self.main_page_buttons = [button_guide, button_student_lists, button_activity_lists, button_merch]
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

        button_create_activity = Button("Добавить мероприятие", self)
        self.activity_selection_buttons.append(button_create_activity)

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

                button_done = Button("Отметить проведение", self)
                button_done.clicked.connect(lambda state, x = cur_activity_name : self.mark_activity_done(x))
                self.activity_inner_page_widgets[cur_activity_name].append(button_done)

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

    def open_table_class(self, class_name):
        self.table.view.hide()
        self.table.view.setWindowTitle(f"Список учеников класса {class_name}")
        self.table.view.show()
        for i in range(column_count):
            self.table.view.showColumn(i)
        for i in range(row_count):
            self.table.view.showRow(i)
            index = self.table.view.model().index(i, 2)
            cur_class_name = self.table.view.model().data(index)
            print(cur_class_name, class_name)
            if (cur_class_name != class_name):
                self.table.view.hideRow(i)
        self.table.view.hideColumn(0)
        self.table.view.hideColumn(2)

    def open_table_activity(self, activity_name):
        self.table.view.hide()
        self.table.view.setWindowTitle(f"Список участников мероприятия '{activity_name}'")
        self.table.view.show()
        for i in range(column_count):
            self.table.view.showColumn(i)
        for i in range(row_count):
            self.table.view.showRow(i)
            if (not (activity_name in students_activities[i])):
                self.table.view.hideRow(i)
        self.table.view.hideColumn(0)

    def get_value_in_cell(self, row, column):
        index = self.table.view.model().index(row, column)
        return self.table.view.model().data(index)

    def add_value_in_cell(self, row, column, value):
        index = self.table.view.model().index(row, column)
        old_value = self.table.view.model().data(index)
        self.table.view.model().setData(index, old_value + value)
        self.table.view.model().submit()

    def mark_activity_done(self, activity_name):
        self.hide()
        self.input_win = InputWindow()
        self.input_win.show()

        button_go_back = QPushButton("Отмена")
        button_go_back.clicked.connect(lambda state, x = activity_name : self.return_from_activity(x))
        self.input_win.layout.addWidget(button_go_back)

        button_commit = QPushButton("Подтвердить")
        button_commit.clicked.connect(lambda state, x = activity_name : self.add_value_for_activity(x))
        self.input_win.layout.addWidget(button_commit)

    def add_value_for_activity(self, activity_name):
        text = self.input_win.input.text()
        if text.isdigit():
            amount_to_add = int(text)
            self.input_win.close()

            for i in range(len(self.activity_selection_buttons)):
                if (self.activity_selection_buttons[i].text() == activity_name):
                    self.activity_selection_buttons.remove(self.activity_selection_buttons[i])
                    break

            connection = sqlite3.connect("student_database.db")
            cursor = connection.cursor()
            with open(get_activity_file_name(activity_name), "r") as file:
                for student_name in file:
                    student_name = delete_end_of_string(student_name)

                    cursor.execute("UPDATE students SET Бонусы = Бонусы + ? WHERE ID = ?", (amount_to_add, student_id[student_name]))
                    connection.commit()
                    self.add_value_in_cell(student_id[student_name], 3, amount_to_add)

            connection.close()
            delete_activity_files(activity_name)
            self.show()
            self.open_activity_selection_page()

        else:
            # send error message
            self.input_win.input.clear()

    def return_from_activity(self, activity_name):
        self.input_win.close()
        self.show()
        self.open_activity_inner_page(activity_name)