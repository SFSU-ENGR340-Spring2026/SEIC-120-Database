#table tests

import sys
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QLabel, 
    QVBoxLayout,
    QHBoxLayout, 
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QMainWindow,
    QAbstractItemView,
    QMessageBox,
    QTableView
)

from PyQt6.QtCore import QSortFilterProxyModel, Qt

from table_model import tableModel 

import csv

class mySpaces(QWidget):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)

        model = model

        #create the views
        self.table1 = QTableView()
        self.table2 = QTableView()
        self.table3 = QTableView()
        self.table4 = QTableView()
        self.table5 = QTableView()

        self.spaces = [self.table1, self.table2, self.table3, self.table4, self.table5]
        #list of views
        self.filters = ["a*", "b*", "c*", "d*", "e*"]
        #list of what filters each table uses

        location_column = model.fieldIndex("location")

        for space, filter in zip(self.spaces, self.filters):
            
            proxy_model = QSortFilterProxyModel()
            #create the model for filtering
            proxy_model.setSourceModel(model)
            
            proxy_model.setFilterKeyColumn(location_column)
            # filter by the location column in the SQLite-backed model
            
            proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            proxy_model.setFilterWildcard(filter)
            #the filter is case insensitive, and wildcard, meaning anything starting 
            # with the relevant filter is found
            
            #set the model
            space.setModel(proxy_model) 
        
        # print(self.items)

        # set the window title
        self.setWindowTitle('Tables')
        self.setGeometry(100, 100, 1500, 700)    #set window size

        #set the layout
        mainLayout = QVBoxLayout(self)
        self.setLayout(mainLayout)

        tableLayout = QHBoxLayout()

        """ #create a button
        button1 = QPushButton()
        button1.setText("Add")

        button2 = QPushButton()
        button2.setText("Remove")
        
        entry = QLineEdit()

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(entry)
        buttonLayout.addWidget(button1)
        buttonLayout.addWidget(button2) """

        #add table to layout
        for table in self.spaces:
            tableLayout.addWidget(table)

        # mainLayout.addLayout(buttonLayout)
        mainLayout.addLayout(tableLayout)

        """ print("table visible?", self.table.isVisible())
        print("table size:", self.table.size())
        print("geometry:", self.table.geometry())
        print("layout on window:", self.layout())
         """
        
        #remove ability to edit table directly
        # self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # show the window
        self.show()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)

    model = tableModel("spaces_app")

    # create the main window
    window = mySpaces(model)

    # start the event loop
    sys.exit(app.exec())
