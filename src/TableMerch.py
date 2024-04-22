from PyQt6.QtWidgets import QTableView
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel


class TableMerch(QTableView):
    def __init__(self):
        super().__init__()

        self.db = QSqlDatabase.addDatabase("QSQLITE", "merch")
        self.db.setDatabaseName("merch_database.db")
        self.db.open()

        self.model = QSqlTableModel(None, self.db)
        self.model.setTable("merch")
        self.model.select()

        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.move(100, 100)
        self.view.resize(800, 600)
        self.view.setColumnWidth(0, 15)
        self.view.setColumnWidth(1, 300)
        self.view.setColumnWidth(2, 100)
        self.view.setWindowTitle("Список мерча")
        self.view.hideColumn(0)
        self.view.hide()

        self.row_count = 0
        with open("merch_list.txt", "r", encoding="utf-8") as merch_list:
            for item_name in merch_list:
                self.row_count += 1