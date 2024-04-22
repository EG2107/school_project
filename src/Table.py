from PyQt6.QtWidgets import QTableView
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from functions import delete_end_of_string, get_class_list_name, get_activity_list_name


class Table(QTableView):
    def __init__(self):
        super().__init__()

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("student_database.db")
        self.db.open()

        self.model = QSqlTableModel(None, self.db)
        self.model.setTable("students")
        self.model.select()

        self.init_additional_data()

        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.move(100, 100)
        self.view.resize(800, 600)
        self.view.setColumnWidth(0, 15)
        self.view.setColumnWidth(1, 300)
        self.view.setColumnWidth(2, 70)
        self.view.setColumnWidth(3, 85)
        self.view.hide()

    def init_additional_data(self):
        self.row_count = 0
        self.column_count = 4
        self.students_activities = []
        self.student_id = dict()

        with open("all_classes.txt", "r", encoding="utf-8") as all_classes:
            id = 0
            for cur_class_name in all_classes:
                cur_class_name = delete_end_of_string(cur_class_name)
                with open(get_class_list_name(cur_class_name), "r", encoding="utf-8") as file:
                    for student_name in file:
                        student_name = delete_end_of_string(student_name)
                        self.student_id[student_name + " " + cur_class_name] = id
                        self.students_activities.append(set())
                        id += 1
            self.row_count = id

        with open("all_activities.txt", "r", encoding="utf-8") as all_activities:
            for cur_activity_name in all_activities:
                cur_activity_name = delete_end_of_string(cur_activity_name)
                with open(get_activity_list_name(cur_activity_name), "r", encoding="utf-8") as file:
                    for student_name in file:
                        student_name = delete_end_of_string(student_name)
                        self.students_activities[self.student_id[student_name]].add(cur_activity_name)