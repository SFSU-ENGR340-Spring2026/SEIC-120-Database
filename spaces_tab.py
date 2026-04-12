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
    QMessageBox
)

from table_model import tableModel 

import csv

class myTables(QWidget):
    def __init__(self, model,  *args, **kwargs):
        super().__init__(*args, **kwargs)

        model = model

        #create the table
        self.table = tableModel("sampleTables.csv")
        self.table2 = tableModel("sampleTables.csv")
        self.table3 = tableModel("sampleTables.csv")
        self.table4 = tableModel("sampleTables.csv")
        self.table5 = tableModel("sampleTables.csv")


        
        # print(self.items)

        # set the window title
        self.setWindowTitle('Tables')
        self.setGeometry(100, 100, 640, 420)    #set window size

        #set the layout
        mainLayout = QVBoxLayout(self)
        self.setLayout(mainLayout)

        tableLayout = QHBoxLayout()

        #create a button
        button1 = QPushButton()
        button1.setText("Add")

        button2 = QPushButton()
        button2.setText("Remove")
        
        entry = QLineEdit()

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(entry)
        buttonLayout.addWidget(button1)
        buttonLayout.addWidget(button2)

        #add table to layout
        tableLayout.addWidget(self.table)
        tableLayout.addWidget(self.table2)
        tableLayout.addWidget(self.table3)
        tableLayout.addWidget(self.table4)
        tableLayout.addWidget(self.table5)

        mainLayout.addLayout(buttonLayout)
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

    # create the main window
    window = myTables()

    # start the event loop
    sys.exit(app.exec())