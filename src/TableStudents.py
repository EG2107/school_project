from PyQt6.QtWidgets import QTableView
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from functions import delete_end_of_string, get_class_list_path, get_activity_list_path, get_all_classes_path, get_all_activities_path


# класс таблицы учеников
class TableStudents(QTableView):
    # инициализация
    def __init__(self):
        super().__init__()

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("student_database.db")
        self.db.open()

        self.table_model = QSqlTableModel(None, self.db)
        self.table_model.setTable("students")
        self.table_model.select()
        while (self.table_model.canFetchMore()):
            self.table_model.fetchMore()

        self.init_additional_data()

        self.setModel(self.table_model)
        self.move(100, 100)
        self.resize(800, 600)
        self.setColumnWidth(0, 15)
        self.setColumnWidth(1, 300)
        self.setColumnWidth(2, 70)
        self.setColumnWidth(3, 85)
        self.hide()

    # инициализация дополнительной информации
    def init_additional_data(self):
        self.student_activities = []
        self.student_id = dict()

        with open(get_all_classes_path(), "r", encoding="utf-8") as all_classes:
            id = 0
            for cur_class_name in all_classes:
                cur_class_name = delete_end_of_string(cur_class_name)
                with open(get_class_list_path(cur_class_name), "r", encoding="utf-8") as file:
                    for student_name in file:
                        student_name = delete_end_of_string(student_name)
                        self.student_id[student_name + " " + cur_class_name] = id
                        self.student_activities.append(set())
                        id += 1

        with open(get_all_activities_path(), "r", encoding="utf-8") as all_activities:
            for cur_activity_name in all_activities:
                cur_activity_name = delete_end_of_string(cur_activity_name)
                with open(get_activity_list_path(cur_activity_name), "r", encoding="utf-8") as file:
                    for student_name in file:
                        student_name = delete_end_of_string(student_name)
                        self.student_activities[self.student_id[student_name]].add(cur_activity_name)

    # узнать значение в ячейке таблицы
    def get_value_in_cell(self, row, column):
        index = self.table_model.index(row, column)
        return self.table_model.data(index)

    # прибавить значение в ячейке таблицы
    def add_value_in_cell(self, row, column, value):
        index = self.table_model.index(row, column)
        old_value = self.table_model.data(index)
        self.table_model.setData(index, old_value + value)
        self.table_model.submit()