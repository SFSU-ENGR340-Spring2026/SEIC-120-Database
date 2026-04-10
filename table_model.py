import sys
from PyQt6.QtCore import Qt, QAbstractTableModel, QSortFilterProxyModel, QModelIndex
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget,
    QVBoxLayout, QTableView, QTableWidgetItem
)
import csv

class tableModel(QAbstractTableModel):
    def __init__(self, file):
        super().__init__()
        self._data = self.loadCSV(file)


    def rowCount(self, parent=None):
    #built in necessary func
    #sets table row count
        return len(self._data)

    def columnCount(self, parent=None):
    #same, sets col count
        return len(self._data[0]) if self._data else 0
    
    def addRow(self, newData):
        self._data.append(newData)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
    #loads given data point into the self.data thing
        if not index.isValid():
            return None

        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            return self._data[index.row()][index.column()]

        return None

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
    #changes the edit part of the data
    #tells the views looking at model that a thing changed
        if not index.isValid() or role != Qt.ItemDataRole.EditRole:
            return False

        self._data[index.row()][index.column()] = value

        # notify all attached views that this cell changed
        self.dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])
        return True

    def flags(self, index):
    #?
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        
        return (
            Qt.ItemFlag.ItemIsSelectable
            | Qt.ItemFlag.ItemIsEnabled
            | Qt.ItemFlag.ItemIsEditable
        )
    
    def loadCSV(self, fileName):
    #load csv into lists 
    #input csv, output total dataset
        with open(fileName, "r", newline="", encoding="utf-8") as fileInput:
            reader = csv.reader(fileInput)
            rows = list(reader)
            self.headers = rows[0]
            items = rows[1:]
            return items
    
    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.headers[section]
        return None
    
    def add_row(self, values):
    #function to add a row to the model
        row = self.rowCount()
        #where to insert

        self.beginInsertRows(QModelIndex(), row, row)
        self._data.append(values)
        self.endInsertRows()
    
    def del_row(self, row):
        if row < 0 or row >= len(self._data):
            return False

        self.beginRemoveRows(QModelIndex(), row, row)
        del self._data[row]
        self.endRemoveRows()

        return True


class TabPage1(QWidget):
    def __init__(self, model, name):
        super().__init__()
        layout = QVBoxLayout(self)

        # table = QTableView()
        # table.setModel(model)

        proxy_model = QSortFilterProxyModel()
        #create the model for filtering
        proxy_model.setSourceModel(model)
        proxy_model.setFilterKeyColumn(4)
        #column 4 (0 index), checks to filter by this thing
        proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        proxy_model.setFilterFixedString("none")

        table = QTableView()
        table.setModel(proxy_model)

        layout.addWidget(table)

class TabPage(QWidget):
    def __init__(self, model, name):
        super().__init__()
        layout = QVBoxLayout(self)

        table = QTableView()
        table.setModel(model)

        layout.addWidget(table)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shared table across tabs")

        # data = [
        #     ["Alice", "24"],
        #     ["Bob", "31"],
        #     ["Carol", "28"],
        # ]

        # one shared model
        self.model = tableModel("sampleData.csv")

        tabs = QTabWidget()
        tabs.addTab(TabPage1(self.model, "Tab 1"), "Tab 1")
        tabs.addTab(TabPage(self.model, "Tab 2"), "Tab 2")
        tabs.addTab(TabPage(self.model, "Tab 3"), "Tab 3")

        self.setCentralWidget(tabs)

if __name__ == '__main__': 
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(500, 300)
    window.show()
    sys.exit(app.exec())