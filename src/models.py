from peewee import *
import os
from PySide6 import QtCore
from PySide6.QtCore import Qt

basedir = os.path.abspath(os.path.dirname(__file__))
db = SqliteDatabase(os.path.join(basedir, 'db.sqlite'), pragmas={'foreign_keys': 1})


class Set(Model):
    id = PrimaryKeyField(null=False)
    title = CharField(unique=True)

    class Meta:
        database = db
        db_tabel = 'set'


class WordPair(Model):
    id = PrimaryKeyField(null=False)
    original = CharField()
    translation = CharField()
    set = ForeignKeyField(Set, backref='wordpairs', on_delete='CASCADE')

    class Meta:
        database = db
        db_tabel = 'wordpair'


# Qt model for the qlistview of the dashboard
class SetModel(QtCore.QAbstractListModel):
    def __init__(self, *args, sets=None, **kwargs):
        super(SetModel, self).__init__(*args, **kwargs)
        self.sets = sets or []

    def data(self, index, role):
        if role == Qt.DisplayRole:

            _, title = self.sets[index.row()]

            return title

        elif role == Qt.EditRole:

            setid, _ = self.sets[index.row()]

            return setid

    def rowCount(self, index):
        return len(self.sets)


if __name__ == '__main__':
    db.connect()
    db.create_tables([Set, WordPair])

