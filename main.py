from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QMainWindow

from src.mainwindow import Ui_MainWindow as Ui_Dashboard
from src.newset import Ui_MainWindow as Ui_NewSet
from src.modify import Ui_MainWindow as Ui_Modify
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

        self.new_set_window = None
        self.modify_window = None

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
        self.new_set_window.save_button.clicked.connect(self.save_button_clicked)

        self.new_set_window.show()

    def open_clicked(self):
        print("open")

    def modify_clicked(self):
        index = self.set_list_view.selectedIndexes()[0]

        set_id = self.model.itemData(index)[2]

        self.modify_window = ModifyWindow(set_id)

        self.modify_window.exit_button.clicked.connect(self.return_button_clicked)
        self.modify_window.save_button.clicked.connect(self.save_button_clicked)

        self.modify_window.show()

    def delete_clicked(self):
        index = self.set_list_view.selectedIndexes()[0]

        Set.delete_by_id(self.model.itemData(index)[2])

        del self.model.sets[index.row()]
        self.model.layoutChanged.emit()

        self.set_list_view.clearSelection()

# Event handlers for buttons not on the main page
    def return_button_clicked(self):
        self.new_button.setEnabled(True)

    def save_button_clicked(self):
        self.new_button.setEnabled(True)

        self.sets = Set.select()

        if self.sets is not None:
            for _set in self.sets:
                self.model.sets.append((_set.id, _set.title.title()))

        self.model.layoutChanged.emit()


class NewSetWindow(QtWidgets.QMainWindow, Ui_NewSet):
    def __init__(self):
        super(NewSetWindow, self).__init__()
        self.setupUi(self)

        self.setWindowTitle("Új Szett Létrehozása")

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
        self.save_button.clicked.connect(self.save_button_clicked)
        self.exit_button.clicked.connect(self.exit_button_clicked)

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

        self.word_edit.clear()
        self.translation_edit.clear()

    def delete_button_clicked(self):
        row = self.tableView.currentIndex().row()

        self.tableView.model().removeRow(row)

        self.word_edit.clear()
        self.translation_edit.clear()

    def save_button_clicked(self):
        new_set = Set(title=self.title_edit.text())
        new_set.save()

        for i in range(self.tableView.model().rowCount()):
            word = self.tableView.model().index(i, 0).data()
            translation = self.tableView.model().index(i, 1).data()

            new_pair = WordPair(original=word, translation=translation, set=new_set.id)
            new_pair.save()

        self.close()

    def exit_button_clicked(self):
        self.close()


class ModifyWindow(QtWidgets.QMainWindow, Ui_Modify):
    def __init__(self, set_id):
        super(ModifyWindow, self).__init__()
        self.setupUi(self)

        self.setWindowTitle("Szett Módosítása")

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

        _set = Set.get_by_id(set_id)

        self.label_4.setText(_set.title)
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        for wordpair in _set.wordpairs:
            word = wordpair.original
            translation = wordpair.translation

            word_item = QtGui.QStandardItem(word)
            word_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            translation_item = QtGui.QStandardItem(translation)
            translation_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            self.model.appendRow([word_item, translation_item])

        self.append_button.clicked.connect(self.append_button_clicked)
        self.modify_button.clicked.connect(self.modify_button_clicked)
        self.delete_button.clicked.connect(self.delete_button_clicked)
        self.save_button.clicked.connect(self.save_button_clicked)
        self.exit_button.clicked.connect(self.exit_button_clicked)

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

        self.word_edit.clear()
        self.translation_edit.clear()

    def delete_button_clicked(self):
        row = self.tableView.currentIndex().row()

        self.tableView.model().removeRow(row)

        self.word_edit.clear()
        self.translation_edit.clear()

    def save_button_clicked(self):
        # TODO: update wordpairs

        self.close()

    def exit_button_clicked(self):
        self.close()



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    w = Dashboard()
    w.show()

    app.exec()
