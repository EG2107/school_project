from os.path import exists
from PyQt6.QtWidgets import *
from PyQt6.QtSql import *
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

app = QApplication([])
db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("students_10-1.db")
db.open()

model = QSqlTableModel(None, db)
model.setTable("students")
model.select()

win = QTableView()
win.setModel(model)
win.setWindowTitle("Список учеников")
win.move(100, 100)
win.resize(800, 600)
win.setColumnWidth(0, 20)
win.setColumnWidth(1, 200)
win.setColumnWidth(2, 80)
win.show()

app.exec()