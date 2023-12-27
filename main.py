from PySide6 import QtCore, QtWidgets

import sys
from peewee import SelectQuery
from src.mainwindow import Ui_MainWindow as Ui_Dashboard
from src.models import Set, WordPair, SetModel


class Dashboard(QtWidgets.QMainWindow, Ui_Dashboard):
    def __init__(self):
        super(Dashboard, self).__init__()
        self.setupUi(self)

        self.setWindowTitle("Főmenü")

        self.new_button.clicked.connect(self.new_clicked)
        self.open_button.clicked.connect(self.open_clicked)
        self.modify_button.clicked.connect(self.modify_clicked)
        self.delete_button.clicked.connect(self.delete_clicked)
        self.exit_button.clicked.connect(self.close)


        self.model = SetModel()
        self.set_list_view.setModel(self.model)
        self.set_list_view.setModelColumn(0)
        self.set_list_view.setSelectionRectVisible(False)

        self.sets = Set.select()

        if self.sets is not None:
            for _set in self.sets:
                self.model.sets.append((_set.id, _set.title.title()))

            self.model.layoutChanged.emit()

    # event handlers for the buttons
    def new_clicked(self):
        self.new_button.setEnabled(False)
        print("uj szett")

    def open_clicked(self):
        print("open")

    def modify_clicked(self):
        print("modify")

    def delete_clicked(self):
        print("delete")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    w = Dashboard()
    w.show()

    app.exec()
