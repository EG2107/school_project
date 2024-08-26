from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QTextEdit
from PyQt6.QtGui import QFont
import os
import sqlite3
from functions import delete_end_of_string, get_activity_list_path, get_activity_description_path, get_all_classes_path, get_all_activities_path, get_guide_path, set_to_str
from Button import Button
from TableStudents import TableStudents
from TableMerch import TableMerch
from InputWindow import InputWindow
from ErrorWindow import ErrorWindow


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.want_to_close = False
        self.input_win = None
        self.error_win = None
        self.table_students = TableStudents()
        self.table_merch = TableMerch()
        self.setWindowTitle("School.Bonus")
        self.setGeometry(100, 100, 1000, 750)
        self.setStyleSheet("background-color: rgb(172, 172, 172)")
        self.create_widgets()
        self.open_main_page()
    
    def create_widgets(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.create_main_page_buttons()
        self.crate_grade_selection_buttons()
        self.create_class_selection_buttons()
        self.create_activity_selection_buttons()
        self.create_activity_inner_pages()
        self.create_activity_description_pages()
        self.hide_all_buttons()

    def create_main_page_buttons(self):
        self.main_page_buttons = []

        button_guide = Button("Руководство пользователя", self)
        button_guide.clicked.connect(self.open_guide)
        self.main_page_buttons.append(button_guide)

        button_student_lists = Button("Список классов", self)
        button_student_lists.clicked.connect(self.open_grade_selection_page)
        self.main_page_buttons.append(button_student_lists)

        button_activity_lists = Button("Мероприятия", self)
        button_activity_lists.clicked.connect(self.open_activity_selection_page)
        self.main_page_buttons.append(button_activity_lists)
        
        button_merch = Button("Мерч", self)
        button_merch.clicked.connect(self.table_merch.show)
        self.main_page_buttons.append(button_merch)
        
        button_exit = Button("Закрыть", self)
        button_exit.clicked.connect(self.open_window_closing_menu)
        self.main_page_buttons.append(button_exit)

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
        with open(get_all_classes_path(), "r", encoding="utf-8") as all_classes:
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
        button_create_activity.clicked.connect(self.open_create_new_activity_window)
        self.activity_selection_buttons.append(button_create_activity)

        with open(get_all_activities_path(), "r", encoding="utf-8") as all_activities:
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

    def create_activity_inner_pages(self):
        self.activity_inner_page_widgets = {}
        with open(get_all_activities_path(), "r", encoding="utf-8") as all_activities:
            for cur_activity_name in all_activities:
                cur_activity_name = delete_end_of_string(cur_activity_name)
                self.create_activity_inner_page(cur_activity_name)

    def create_activity_inner_page(self, activity_name):
        self.activity_inner_page_widgets[activity_name] = []

        label_activity_name = QLabel(activity_name, self)
        label_activity_name.setFont(QFont("Helvetica [Cronyx]", 18))
        self.activity_inner_page_widgets[activity_name].append(label_activity_name)

        button_edit = Button("Редактировать", self)
        button_edit.clicked.connect(lambda state, x = activity_name : self.open_activity_edit_window(x))
        self.activity_inner_page_widgets[activity_name].append(button_edit)

        button_participants_list = Button("Участники", self)
        button_participants_list.clicked.connect(lambda state, x = activity_name : self.open_table_activity(x))
        self.activity_inner_page_widgets[activity_name].append(button_participants_list)

        button_description = Button("Описание", self)
        button_description.clicked.connect(lambda state, x = activity_name : self.open_activity_description(x))
        self.activity_inner_page_widgets[activity_name].append(button_description)

        button_delete = Button("Удалить", self)
        button_delete.clicked.connect(lambda state, x = activity_name : self.open_delete_activity_window(x))
        self.activity_inner_page_widgets[activity_name].append(button_delete)

        button_go_back_from_activity_inner_page = Button("Назад", self)
        button_go_back_from_activity_inner_page.clicked.connect(self.open_activity_selection_page)
        self.activity_inner_page_widgets[activity_name].append(button_go_back_from_activity_inner_page)

        for widget in self.activity_inner_page_widgets[activity_name]:
            self.layout.addWidget(widget, alignment=Qt.AlignmentFlag.AlignCenter)

    def create_activity_description_pages(self):
        self.activity_description_page_widgets = {}
        with open(get_all_activities_path(), "r", encoding="utf-8") as all_activities:
            for cur_activity_name in all_activities:
                cur_activity_name = delete_end_of_string(cur_activity_name)
                with open(get_activity_description_path(cur_activity_name), "r", encoding="utf-8") as description:
                    self.create_activity_description_page(cur_activity_name, description.read())

    def create_activity_description_page(self, activity_name, activity_description):
        self.activity_description_page_widgets[activity_name] = []

        label_description = QLabel(activity_description, self)
        label_description.setFont(QFont("Helvetica [Cronyx]", 12))
        self.layout.addWidget(label_description, alignment=Qt.AlignmentFlag.AlignCenter)
        self.activity_description_page_widgets[activity_name].append(label_description)

        button_go_back_from_activity_description = Button("Назад", self)
        button_go_back_from_activity_description.clicked.connect(lambda state, x = activity_name : self.open_activity_inner_page(x))
        self.layout.addWidget(button_go_back_from_activity_description, alignment=Qt.AlignmentFlag.AlignCenter)
        self.activity_description_page_widgets[activity_name].append(button_go_back_from_activity_description)

    def hide_all_buttons(self):
        self.table_students.hide()
        self.table_merch.hide()
        if self.error_win:
            self.error_win.close()
        if self.input_win:
            self.input_win.close()
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
        for widget in self.activity_inner_page_widgets[activity_name]:
            widget.show()

    def open_activity_description(self, activity_name):
        self.hide_all_buttons()
        for widget in self.activity_description_page_widgets[activity_name]:
            widget.show()

    def open_guide(self):
        self.hide()

        self.guide_win = InputWindow(self)
        self.guide_win.setGeometry(250, 250, 600, 600)
        self.guide_win.setStyleSheet("background-color: rgb(200, 200, 200)")

        label_guide = QLabel("Руководство пользователя", self)
        label_guide.setFont(QFont("Helvetica [Cronyx]", 18))
        self.guide_win.layout.addWidget(label_guide, alignment=Qt.AlignmentFlag.AlignCenter)

        with open(get_guide_path(), "r", encoding="utf-8") as guide_text:
            label_text = QLabel(guide_text.read(), self)
            label_text.setFont(QFont("Helvetica [Cronyx]", 14))
            self.guide_win.layout.addWidget(label_text, alignment=Qt.AlignmentFlag.AlignCenter)

        button_go_back = Button("Назад", self.guide_win)
        button_go_back.clicked.connect(self.guide_win.close)
        self.guide_win.layout.addWidget(button_go_back, alignment=Qt.AlignmentFlag.AlignCenter)

        self.guide_win.show()

    def open_table_class(self, class_name):
        self.table_students.hide()
        self.table_students.setWindowTitle(f"Список учеников класса {class_name}")
        self.table_students.show()

        for i in range(self.table_students.table_model.columnCount()):
            self.table_students.showColumn(i)
        for i in range(self.table_students.table_model.rowCount()):
            self.table_students.showRow(i)
            index = self.table_students.table_model.index(i, 2)
            cur_class_name = self.table_students.table_model.data(index)
            if (cur_class_name != class_name):
                self.table_students.hideRow(i)
            else:
                self.table_students.set_value_in_cell(i, 3, len(self.table_students.student_activities[i]))
                self.table_students.set_value_in_cell(i, 4, set_to_str(self.table_students.student_activities[i]))

        self.table_students.hideColumn(0)
        self.table_students.hideColumn(2)

    def open_table_activity(self, activity_name):
        self.table_students.hide()
        self.table_students.setWindowTitle(f"Список участников мероприятия '{activity_name}'")
        self.table_students.show()

        for i in range(self.table_students.table_model.columnCount()):
            self.table_students.showColumn(i)
        for i in range(self.table_students.table_model.rowCount()):
            self.table_students.showRow(i)
            if (not (activity_name in self.table_students.student_activities[i])):
                self.table_students.hideRow(i)
            else:
                self.table_students.set_value_in_cell(i, 3, len(self.table_students.student_activities[i]))
                self.table_students.set_value_in_cell(i, 4, set_to_str(self.table_students.student_activities[i]))

        self.table_students.hideColumn(0)

    def open_create_new_activity_window(self):
        self.hide()

        self.input_win = InputWindow(self)
        self.input_win.setGeometry(400, 250, 450, 600)

        label_name = QLabel("Введите название мероприятия:", self)
        label_name.setFont(QFont("Helvetica [Cronyx]", 12))
        self.input_win.layout.addWidget(label_name, alignment=Qt.AlignmentFlag.AlignCenter)

        self.input_win.input_name = QLineEdit()
        self.input_win.layout.addWidget(self.input_win.input_name, alignment=Qt.AlignmentFlag.AlignCenter)

        label_description = QLabel("Введите описание мероприятия (не обязательно):", self)
        label_description.setFont(QFont("Helvetica [Cronyx]", 12))
        self.input_win.layout.addWidget(label_description, alignment=Qt.AlignmentFlag.AlignCenter)

        self.input_win.input_description = QTextEdit()
        self.input_win.input_description.setMinimumWidth(380)
        self.input_win.layout.addWidget(self.input_win.input_description, alignment=Qt.AlignmentFlag.AlignCenter)

        label_participants = QLabel("Введите ФИО и класс участников мероприятия:", self)
        label_participants.setFont(QFont("Helvetica [Cronyx]", 12))
        self.input_win.layout.addWidget(label_participants, alignment=Qt.AlignmentFlag.AlignCenter)

        self.input_win.input_participants = QTextEdit()
        self.input_win.input_participants.setMinimumWidth(380)
        self.input_win.layout.addWidget(self.input_win.input_participants, alignment=Qt.AlignmentFlag.AlignCenter)

        button_go_back = QPushButton("Отмена")
        button_go_back.clicked.connect(self.return_from_activity_creation)
        self.input_win.layout.addWidget(button_go_back)

        button_commit = QPushButton("Подтвердить")
        button_commit.clicked.connect(self.create_new_activity)
        self.input_win.layout.addWidget(button_commit)

        self.input_win.show()

    def check_new_activity(self, activity_name, activity_participants):
        if len(activity_name) == 0:
            self.error_win = ErrorWindow("Пожалуйста, введите название мероприятия.")
            return False

        with open(get_all_activities_path(), "r", encoding="utf-8") as all_activities:
            for cur_activity_name in all_activities:
                cur_activity_name = delete_end_of_string(cur_activity_name)
                if (activity_name == cur_activity_name):
                    self.error_win = ErrorWindow(f"Мероприятие с таким названием уже существует.\nПожалуйста, выберите другое название.")
                    return False
                
        str_ind = 0
        student_line = {}
        for student_name in activity_participants.split('\n'):
            str_ind += 1
            if (len(student_name) == 0):
                continue

            if (student_line.get(student_name) is None):
                student_line[student_name] = str_ind
            else:
                self.error_win = ErrorWindow(f"Ученик '{student_name}' встречается\nв двух строках, а именно в {student_line[student_name]}-ой и {str_ind}-ой.\nПожалуйста, проверьте, правильно ли Вы ввели данные.")
                return False
            
            if (self.table_students.student_id.get(student_name) is None):
                self.error_win = ErrorWindow(f"Ученика '{student_name}'\n(строка {str_ind}) нет в базе.\nУбедитесь, что данные введены корректно.\nФормат ввода:\n'Фамилия имя отчество класс' (без кавычек)")
                return False

        return True

    def create_new_activity(self):
        self.error_win = None

        activity_name = self.input_win.input_name.text()
        activity_description = self.input_win.input_description.toPlainText()
        activity_participants = self.input_win.input_participants.toPlainText()

        if (self.check_new_activity(activity_name, activity_participants)):
            self.activity_selection_buttons[-1].setText(activity_name)
            self.activity_selection_buttons[-1].clicked.connect(lambda state, x = activity_name : self.open_activity_inner_page(x))

            button_go_back_from_activity_selection = Button("Назад", self)
            button_go_back_from_activity_selection.clicked.connect(self.open_main_page)
            self.layout.addWidget(button_go_back_from_activity_selection, alignment=Qt.AlignmentFlag.AlignCenter)
            self.activity_selection_buttons.append(button_go_back_from_activity_selection)
            self.hide_all_buttons()

            self.create_activity_inner_page(activity_name)
            self.create_activity_description_page(activity_name, activity_description)

            with open(get_all_activities_path(), "a", encoding="utf-8") as all_activities:
                all_activities.write(activity_name + '\n')

            with open(get_activity_list_path(activity_name), "w", encoding="utf-8") as participants_list:
                for student_name in activity_participants.split('\n'):
                    if (len(student_name) == 0):
                        continue
                    participants_list.write(student_name + '\n')
                    self.table_students.student_activities[self.table_students.student_id[student_name]].add(activity_name)
                
            with open(get_activity_description_path(activity_name), "w", encoding="utf-8") as description:
                description.write(activity_description)

            self.input_win.close()
            self.open_activity_selection_page()

    def return_from_activity_creation(self):
        if self.error_win:
            self.error_win.close()
        self.input_win.close()
        self.show()
        self.open_activity_selection_page()

    def open_activity_edit_window(self, activity_name):
        self.hide()

        self.input_win = InputWindow(self)
        self.input_win.setGeometry(400, 250, 450, 600)

        label_description = QLabel("Введите описание мероприятия:\n(Если не хотите менять описание мероприятия,\nоставьте поле пустым.)", self)
        label_description.setFont(QFont("Helvetica [Cronyx]", 12))
        self.input_win.layout.addWidget(label_description, alignment=Qt.AlignmentFlag.AlignCenter)

        self.input_win.input_description = QTextEdit()
        self.input_win.input_description.setMinimumWidth(380)
        self.input_win.layout.addWidget(self.input_win.input_description, alignment=Qt.AlignmentFlag.AlignCenter)

        label_participants = QLabel("Введите ФИО и класс участников мероприятия:\n(Если не хотите менять участников мероприятия,\nоставьте поле пустым.)", self)
        label_participants.setFont(QFont("Helvetica [Cronyx]", 12))
        self.input_win.layout.addWidget(label_participants, alignment=Qt.AlignmentFlag.AlignCenter)

        self.input_win.input_participants = QTextEdit()
        self.input_win.input_participants.setMinimumWidth(380)
        self.input_win.layout.addWidget(self.input_win.input_participants, alignment=Qt.AlignmentFlag.AlignCenter)

        button_go_back = QPushButton("Отмена")
        button_go_back.clicked.connect(lambda state, x = activity_name : self.return_from_activity_edit_or_deletion(x))
        self.input_win.layout.addWidget(button_go_back)

        button_commit = QPushButton("Подтвердить")
        button_commit.clicked.connect(lambda state, x = activity_name : self.edit_activity(x))
        self.input_win.layout.addWidget(button_commit)

        self.input_win.show()

    def check_edited_activity(self, activity_participants):
        str_ind = 0
        student_line = {}
        for student_name in activity_participants.split('\n'):
            str_ind += 1
            if (len(student_name) == 0):
                continue
            self.input_win.want_to_change_participants = True

            if (student_line.get(student_name) is None):
                student_line[student_name] = str_ind
            else:
                self.error_win = ErrorWindow(f"Ученик '{student_name}' встречается\nв двух строках, а именно в {student_line[student_name]}-ой и {str_ind}-ой.\nПожалуйста, проверьте, правильно ли Вы ввели данные.")
                return False
            
            if (self.table_students.student_id.get(student_name) is None):
                self.error_win = ErrorWindow(f"Ученика '{student_name}' (строка {str_ind}) нет в базе.\nУбедитесь, что данные введены корректно.\nФормат ввода:\n'Фамилия имя отчество класс' (без кавычек)")
                return False
        
        return True

    def edit_activity(self, activity_name):
        self.error_win = None

        activity_description = self.input_win.input_description.toPlainText()
        activity_participants = self.input_win.input_participants.toPlainText()

        self.input_win.want_to_change_participants = False
        if (self.check_edited_activity(activity_participants)):
            if self.input_win.want_to_change_participants:
                with open(get_activity_list_path(activity_name), "r", encoding="utf-8") as participants_list:
                    for student_name in participants_list:
                        student_name = delete_end_of_string(student_name)
                        self.table_students.student_activities[self.table_students.student_id[student_name]].remove(activity_name)

                with open(get_activity_list_path(activity_name), "w", encoding="utf-8") as participants_list:
                    for student_name in activity_participants.split('\n'):
                        if (len(student_name) == 0):
                            continue
                        participants_list.write(student_name + '\n')
                        self.table_students.student_activities[self.table_students.student_id[student_name]].add(activity_name)
            
            if (len(activity_description)):
                self.activity_description_page_widgets[activity_name][0].setText(activity_description)
                with open(get_activity_description_path(activity_name), "w", encoding="utf-8") as description:
                    description.write(activity_description)

            self.input_win.close()
            self.open_activity_inner_page(activity_name)

    def open_delete_activity_window(self, activity_name):
        self.hide()

        self.input_win = InputWindow(self)
        self.input_win.setGeometry(400, 300, 400, 300)

        label = QLabel(f"Вы уверены, что хотите удалить мероприятие '{activity_name}'?", self)
        label.setFont(QFont("Helvetica [Cronyx]", 12))
        self.input_win.layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)

        button_go_back = QPushButton("Отмена")
        button_go_back.clicked.connect(lambda state, x = activity_name : self.return_from_activity_edit_or_deletion(x))
        self.input_win.layout.addWidget(button_go_back)

        button_commit = QPushButton("Подтвердить")
        button_commit.clicked.connect(lambda state, x = activity_name : self.delete_activity(x))
        self.input_win.layout.addWidget(button_commit)

        self.input_win.show()

    def delete_activity(self, activity_name):
        for i in range(len(self.activity_selection_buttons)):
            if (self.activity_selection_buttons[i].text() == activity_name):
                self.activity_selection_buttons.remove(self.activity_selection_buttons[i])
                break

        with open(get_activity_list_path(activity_name), "r", encoding="utf-8") as file:
            for student_name in file:
                student_name = delete_end_of_string(student_name)
                self.table_students.student_activities[self.table_students.student_id[student_name]].pop(activity_name)

        self.delete_activity_files(activity_name)
        self.show()
        self.open_activity_selection_page()

    def delete_activity_files(self, activity_name):
        os.remove(get_activity_list_path(activity_name))
        os.remove(get_activity_description_path(activity_name))

        new_activities = []
        with open(get_all_activities_path(), "r", encoding="utf-8") as all_activities:
            for line in all_activities:
                line = delete_end_of_string(line)
                if (line != activity_name):
                    new_activities.append(line + '\n')

        with open(get_all_activities_path(), "w", encoding="utf-8") as all_activities:
            all_activities.writelines(new_activities)

    def return_from_activity_edit_or_deletion(self, activity_name):
        if self.error_win:
            self.error_win.close()
        self.input_win.close()
        self.show()
        self.open_activity_inner_page(activity_name)

    def closeEvent(self, event):
        if self.want_to_close:
            super(Window, self).closeEvent(event)
            self.table_students.close()
            self.table_merch.close()
        else:
            event.ignore()
            self.open_window_closing_menu()

    def open_window_closing_menu(self):
        self.hide()
        self.exit_win = QWidget()
        self.exit_win.setWindowTitle("School.Bonus")
        self.exit_win.setGeometry(500, 400, 250, 130)

        self.exit_win.layout = QVBoxLayout()
        self.exit_win.setLayout(self.exit_win.layout)

        button_go_back = QPushButton("Вернуться назад")
        button_go_back.clicked.connect(self.return_from_exit_page)
        self.exit_win.layout.addWidget(button_go_back)

        button_exit = QPushButton("Закрыть приложение")
        button_exit.clicked.connect(self.exit)
        self.exit_win.layout.addWidget(button_exit)

        self.exit_win.show()

    def return_from_exit_page(self):
        self.exit_win.close()
        self.show()

    def exit(self):
        self.want_to_close = True
        self.exit_win.close()
        self.close()