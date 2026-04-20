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

        #place to enter student id
        idEntry = QLineEdit()
        idEntry.setPlaceholderText("Enter Student ID")

        #for spaces
        spaceName = QLineEdit()
        spaceName.setPlaceholderText("What table section?")
        spaceIn = QPushButton()
        spaceIn.setText("Assign Table")
            #no need for unassign table, happens when they check out
        
        #two buttons for check in and check out
        checkIn = QPushButton()
        checkOut = QPushButton()
        checkIn.setText("Check In")
        checkOut.setText("Check Out")

        #add them to the layout
        topThingLayout.addWidget(idEntry)
        topThingLayout.addWidget(spaceName)
        topThingLayout.addWidget(spaceIn)
        topThingLayout.addWidget(checkIn)
        topThingLayout.addWidget(checkOut)

        #layout for check in for tools
        checkInLayout = QHBoxLayout()

        #create table layout
        self.create_students("Who's currently In?", studentsModel)

        #create note layout
        self.create_notes("Student Notes: ", notesModel)

        #create tool layout
        self.create_tools("Available Tools: ", toolsModel)
        
        #compile the layout
        finalLayout.addLayout(topThingLayout)
        finalLayout.addLayout(checkInLayout)
        finalLayout.addLayout(self.mainLayout)

        self.setLayout(finalLayout)

        self.setGeometry(100, 100, 1000, 700)
        
        # show the window
        self.show()

    def create_students(self, textBox, model):
    #function repeated for each of the three sections in the dashboard
    #students checked in, tools available, notes
        layout = QVBoxLayout()

        topLay = QHBoxLayout()

        header = QLineEdit()
        header.setText(textBox)
        header.setReadOnly(True)
        topLay.addWidget(header)

        #for tools
        # toolName = QLineEdit()
        # toolName.setPlaceholderText("Tool Name")

        toolIn = QPushButton()
        toolOut = QPushButton()
        toolIn.setText("Give Tool")
        toolOut.setText("Return Tool")
                
        # checkInLayout.addWidget(toolName)
        topLay.addWidget(toolIn)
        topLay.addWidget(toolOut)

        table = QTableView()
        table.setModel(model)
        #create table view, set model, add to layout
        layout.addLayout(topLay)
        layout.addWidget(table)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch) 

        #upon clicking on the some student, the table will load in
        table.clicked.connect(lambda:self.showReports(table))     
        
        self.mainLayout.addLayout(layout)

    def create_notes(self, textBox, model):
    #function repeated for each of the three sections in the dashboard
    #students checked in, tools available, notes
        layout = QVBoxLayout()

        #header section of the layout
        headerLayout = QHBoxLayout()

        header = QLineEdit()
        header.setText(textBox)
        header.setReadOnly(True)
        headerLayout.addWidget(header)

        addNote = QPushButton()
        addNote.setText("Add Note")
        headerLayout.addWidget(addNote)

        layout.addLayout(headerLayout)

        table = QTableView()
        #create table view

        self.proxyView = QSortFilterProxyModel()
        #create a proxy view, needs to be accessible so i can futz with it later
        self.proxyView.setSourceModel(model)
        #set proxy's source
        self.proxyView.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        #change filters case sensitivity
        self.proxyView.setFilterKeyColumn(0)
        #searches names (should be id), for the correct one to display

        table.setModel(self.proxyView)
        #set model to view
        layout.addWidget(table)
        #add view to layout
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
        self.toolProxy = QSortFilterProxyModel()
        self.toolProxy.setSourceModel(model)

        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        #make it stretch

        self.toolProxy.setFilterKeyColumn(location_column)
        # filter by the location column in the SQLite-backed model
        
        self.toolProxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.toolProxy.setFilterFixedString("none")
        #look for tools with no location, i.e. not with someone

        table.setModel(self.toolProxy)
        #give the proxy to the view     
        
        layout.addWidget(table)
        self.mainLayout.addLayout(layout)
        #add the view to the layout, and then to the main

    def showReports(self, table):
        row = table.currentIndex()
        #get the person who's been clicked on
        
        print(row.data())           #for testing

        #check that it's an id (or at least an integer)
            #return if not
        
        #search id for reports on it (filter by the day?)

        #then create model for it, and load into note view
        self.proxyView.setFilterFixedString(str(row.data()))
        

if __name__ == '__main__':
    app = QApplication(sys.argv)

    studentsModel = tableModel("students_app")
    notesModel = tableModel("reports_app")
    toolsModel = tableModel("tools_app")
    
    # create the main window
    window = myDashboard(studentsModel, notesModel, toolsModel)

    # start the event loop
    sys.exit(app.exec())
