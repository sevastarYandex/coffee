import sys
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('coffee.sqlite')
        self.db.open()
        self.model = QSqlQueryModel(self)
        req = """SELECT coffee.ID, variety.title, degree.title, making.title, 
        coffee.storage, coffee.taste, coffee.price, coffee.size FROM 
        coffee INNER JOIN variety INNER JOIN degree INNER JOIN making ON 
        coffee.varietyID = variety.ID AND coffee.degreeID = degree.ID AND
        coffee.makingID = making.ID ORDER BY coffee.ID ASC"""
        self.model.setQuery(self.db.exec(req))
        self.TITLES = ['ИД', 'сорт', 'степень обжарки', 'название напитка', 'хранение',
                       'вкус', 'цена за 1 упаковку (в рублях)', 'объём 1 упаковки (в мл)']
        for i in range(len(self.TITLES)):
            self.model.setHeaderData(i, Qt.Orientation.Horizontal, self.TITLES[i])
        self.view.setModel(self.model)
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(self.layout)

    def closeEvent(self, a0) -> None:
        self.db.close()
        a0.accept()
        super().closeEvent(a0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
