from os.path import exists
from PyQt6.QtWidgets import *
from PyQt6.QtSql import *
import sqlite3

def create_table():
    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students
        (ID INTEGER, ФИО TEXT, Бонусы INTEGER)
    """)
    connection.commit()
    connection.close()

def add_student(id, name):
    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO students VALUES ((?), (?), 0)", (id, name,))
    connection.commit()
    connection.close()

def update(id, add):
    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE students SET Бонусы = (?) where id = (?)", (add, id))
    connection.commit()
    connection.close()

if (not exists("students.db")):
    create_table()
    list_of_students = ["Авербах Давид Львович", "Грачев Егор Павлович", "Иванов Иван Иванович"]
    for i in range(len(list_of_students)):
        add_student(i + 1, list_of_students[i])
    update(1, 239)
    update(2, 239)
    update(3, 42)

app = QApplication([])
db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("students.db")
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