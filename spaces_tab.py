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
    QTableView,
    QComboBox,
    QHeaderView,
    QGroupBox,
)

from PyQt6.QtCore import QSortFilterProxyModel, Qt, QRegularExpression

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
        self.table6 = QTableView()

        self.spaces = [self.table1, self.table2, self.table3, self.table4, self.table5, self.table6]
        #list of views
        self.filters = ["a*", "b*", "c*", "d*", "e*", "f*"]
        #list of what filters each table uses

        location_column = model.fieldIndex("location")
        tableLayout1 = QHBoxLayout()
        tableLayout2 = QHBoxLayout()
        finalTables = QVBoxLayout()

        t = 0

        for space, filter in zip(self.spaces, self.filters):
            proxy_model = QSortFilterProxyModel()
            #create the model for filtering

            group = QGroupBox(title=f"Section {filter}")
            gLayout = QHBoxLayout()

            proxy_model.setSourceModel(model)
            #give the proxy model a source
            
            proxy_model.setFilterKeyColumn(location_column)
            # filter by the location column in the SQLite-backed model
            
            proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

            if space is self.table5:
                proxy_model.setFilterRegularExpression(
                    QRegularExpression(r"^(?!none$)e.*", QRegularExpression.PatternOption.CaseInsensitiveOption)
                )
                # print("did it")
                #for e specifically, dont want none to be included in the filter
            else:
                proxy_model.setFilterWildcard(filter)
            #the filter is case insensitive, and wildcard, meaning anything starting 
            # with the relevant filter is found
            
            #set the proxy into view
            space.setModel(proxy_model)
            space.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch) 
            
            gLayout.addWidget(space)
            group.setLayout(gLayout)
            
            #add view to layout
            t += 1
            if t <= 3:
                tableLayout1.addWidget(group)
                #this way, 2 rows of 3 columns
            elif t > 3:
                tableLayout2.addWidget(group)

        
        # print(self.items)

        finalTables.addLayout(tableLayout1)
        finalTables.addLayout(tableLayout2)

        # set the window title
        self.setWindowTitle('Tables')
        self.setGeometry(100, 100, 1500, 700)    #set window size

        #set the layout
        mainLayout = QVBoxLayout(self)
        self.setLayout(mainLayout)

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


        # mainLayout.addLayout(buttonLayout)
        mainLayout.addLayout(finalTables)

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
