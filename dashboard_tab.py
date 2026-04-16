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
    QGroupBox,
    QTableView,
    QHeaderView 
)

from PyQt6.QtCore import QSortFilterProxyModel, Qt
from table_model import tableModel
import csv

class myDashboard(QWidget):
#needs to be given 3 models, 
    def __init__(self, studentsModel, notesModel, toolsModel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        finalLayout = QVBoxLayout(self)
        #final thing

        #create main layout
        self.mainLayout = QHBoxLayout()

        studModel = studentsModel
        toolModel = toolsModel
        notModel = notesModel
        #create 3 different models for each thing

        #layout for top thing
        topThingLayout = QHBoxLayout()
        idEntry = QLineEdit()
        idEntry.setPlaceholderText("Enter Student ID")
        
        #two buttons for check in and check out
        checkIn = QPushButton()
        checkOut = QPushButton()
        checkIn.setText("Check In")
        checkOut.setText("Check Out")

        #add them to the layout
        topThingLayout.addWidget(idEntry)
        topThingLayout.addWidget(checkIn)
        topThingLayout.addWidget(checkOut)

        #create table layout
        self.create_layout("Who's currently In?", studentsModel)

        #create note layout
        self.create_layout("Student Notes: ", notesModel)

        #create tool layout
        self.create_tools("Available Tools: ", toolsModel)
        
        #compile the layout
        finalLayout.addLayout(topThingLayout)
        finalLayout.addLayout(self.mainLayout)

        self.setLayout(finalLayout)

        self.setGeometry(100, 100, 1000, 700)
        
        # show the window
        self.show()

    def create_layout(self, textBox, model):
    #function repeated for each of the three sections in the dashboard
    #students checked in, tools available, notes
        layout = QVBoxLayout()

        header = QLineEdit()
        header.setText(textBox)
        header.setReadOnly(True)
        layout.addWidget(header)

        table = QTableView()
        table.setModel(model)
        #create table view, set model, add to layout
        layout.addWidget(table)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)     
        
        self.mainLayout.addLayout(layout)

    def create_tools(self, textBox, model):
    #function repeated for each of the three sections in the dashboard
    #students checked in, tools available, notes
        layout = QVBoxLayout()
        table = QTableView()
        location_column = model.fieldIndex("location")

        #section for entering data
        header = QLineEdit()
        header.setText(textBox)
        header.setReadOnly(True)
        layout.addWidget(header)

        #create filter model, based on original model
        proxy = QSortFilterProxyModel()
        proxy.setSourceModel(model)

        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        #make it stretch

        proxy.setFilterKeyColumn(location_column)
        # filter by the location column in the SQLite-backed model
        
        proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        proxy.setFilterFixedString("none")
        #look for tools with no location, i.e. not with someone

        table.setModel(proxy)
        #give the proxy to the view     
        
        layout.addWidget(table)
        self.mainLayout.addLayout(layout)
        #add the view to the layout, and then to the main

if __name__ == '__main__':
    app = QApplication(sys.argv)

    studentsModel = tableModel("students_app")
    notesModel = tableModel("reports_app")
    toolsModel = tableModel("tools_app")
    
    # create the main window
    window = myDashboard(studentsModel, notesModel, toolsModel)

    # start the event loop
    sys.exit(app.exec())
