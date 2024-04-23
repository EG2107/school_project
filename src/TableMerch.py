from PyQt6.QtWidgets import QTableView
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel


class TableMerch(QTableView):
    def __init__(self):
        super().__init__()

        self.db = QSqlDatabase.addDatabase("QSQLITE", "merch")
        self.db.setDatabaseName("merch_database.db")
        self.db.open()

        self.table_model = QSqlTableModel(None, self.db)
        self.table_model.setTable("merch")
        self.table_model.select()

        self.setModel(self.table_model)
        self.move(100, 100)
        self.resize(800, 600)
        self.setColumnWidth(0, 15)
        self.setColumnWidth(1, 300)
        self.setColumnWidth(2, 100)
        self.setWindowTitle("Список мерча")
        self.hideColumn(0)
        self.hide()