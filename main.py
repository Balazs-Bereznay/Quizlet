from PySide6 import QtCore, QtWidgets, QtGui
from src.mainwindow import Ui_MainWindow as Ui_Dashboard
from src.newset import Ui_MainWindow as Ui_NewSet
from src.models import Set, WordPair, SetModel, append_word_pairs


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

        self.new_set_window = None

        self.model = SetModel()
        self.set_list_view.setModel(self.model)
        self.set_list_view.setModelColumn(0)
        self.set_list_view.setSelectionRectVisible(False)
        self.set_list_view.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.sets = Set.select()

        if self.sets is not None:
            for _set in self.sets:
                self.model.sets.append((_set.id, _set.title.title()))

            self.model.layoutChanged.emit()

    # event handlers for the buttons
    def new_clicked(self):
        self.new_button.setEnabled(False)
        self.new_set_window = NewSetWindow()

        self.new_set_window.exit_button.clicked.connect(self.return_button_clicked)
        self.new_set_window.save_button.clicked.connect(self.create_button_clicked)

        self.new_set_window.show()

    def open_clicked(self):
        print("open")

    def modify_clicked(self):
        print("modify")

    def delete_clicked(self):
        print("delete")

    def return_button_clicked(self):
        self.new_button.setEnabled(True)
        self.new_set_window.close()

    def create_button_clicked(self):
        self.new_button.setEnabled(True)


class NewSetWindow(QtWidgets.QMainWindow, Ui_NewSet):
    def __init__(self):
        super(NewSetWindow, self).__init__()
        self.setupUi(self)

        self.setWindowTitle("Új szett létrehozása")

        self.model = QtGui.QStandardItemModel()
        self.model.setColumnCount(2)

        self.tableView.setModel(self.model)
        self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.tableView.horizontalHeader().hide()
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.verticalHeader().hide()
        self.selected = False
        self.row_memory = None
        self.tableView.clicked.connect(self.row_clicked)

        self.append_button.clicked.connect(self.append_button_clicked)
        self.modify_button.clicked.connect(self.modify_button_clicked)
        self.delete_button.clicked.connect(self.delete_button_clicked)

    def append_button_clicked(self):
        word = self.word_edit.text()
        translation = self.translation_edit.text()

        word_item = QtGui.QStandardItem(word)
        word_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        translation_item = QtGui.QStandardItem(translation)
        translation_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.model.appendRow([word_item, translation_item])

        self.word_edit.clear()
        self.translation_edit.clear()

    def row_clicked(self):
        row = self.tableView.currentIndex().row()

        if self.selected:
            if self.row_memory == row:
                self.tableView.clearSelection()

                self.word_edit.clear()
                self.translation_edit.clear()

                self.selected = False

            else:
                self.word_edit.setText(self.tableView.model().index(row, 0).data())
                self.translation_edit.setText(self.tableView.model().index(row, 1).data())

                self.row_memory = row

        else:
            self.word_edit.setText(self.tableView.model().index(row, 0).data())
            self.translation_edit.setText(self.tableView.model().index(row, 1).data())

            self.row_memory = row
            self.selected = True

    def modify_button_clicked(self):
        row = self.tableView.currentIndex().row()

        self.tableView.model().setData(self.tableView.model().index(row, 0), self.word_edit.text())
        self.tableView.model().setData(self.tableView.model().index(row, 1), self.translation_edit.text())

    def delete_button_clicked(self):
        row = self.tableView.currentIndex().row()

        self.tableView.model().removeRow(row)

        self.word_edit.clear()
        self.translation_edit.clear()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    w = Dashboard()
    w.show()

    app.exec()
