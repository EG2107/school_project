from PyQt6.QtWidgets import QTableView
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from variables import *


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