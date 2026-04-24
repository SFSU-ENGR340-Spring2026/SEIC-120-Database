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
import csv, datetime

class myDashboard(QWidget):
#needs to be given 3 models, 
    def __init__(self, studentsModel, notesModel, toolsModel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        finalLayout = QVBoxLayout(self)
        #final thing

        #create main layout
        self.mainLayout = QHBoxLayout()

        self.studModel = studentsModel
        self.toolModel = toolsModel
        self.noteModel = notesModel
        #create 3 different models for each thing

        #layout for top thing
        topThingLayout = QHBoxLayout()

        #place to enter student id
        self.idEntry = QLineEdit()
        self.idEntry.setPlaceholderText("Enter Student ID")

        #for spaces
        self.spaceName = QLineEdit()
        self.spaceName.setPlaceholderText("What table section?")
        self.spaceIn = QPushButton()
        self.spaceIn.setText("Assign Table")
            #no need for unassign table, happens when they check out
        
        #two buttons for check in and check out
        checkIn = QPushButton()
        checkOut = QPushButton()
        checkIn.setText("Check In")
        checkOut.setText("Check Out")
        checkIn.clicked.connect(lambda:self.checkIn())
        checkOut.clicked.connect(lambda:self.checkOut())

        #add them to the layout
        topThingLayout.addWidget(self.idEntry)
        topThingLayout.addWidget(self.spaceName)
        topThingLayout.addWidget(self.spaceIn)
        topThingLayout.addWidget(checkIn)
        topThingLayout.addWidget(checkOut)

        #layout for check in for tools
        checkInLayout = QHBoxLayout()

        #create table layout
        self.create_students("Who's currently In?", self.studModel)

        #create note layout
        self.create_notes("Student Notes: ", self.noteModel)

        #create tool layout
        self.create_tools("Available Tools: ", self.toolModel)
        
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
        
        #create the buttons, set their text, 
        toolIn = QPushButton()
        toolOut = QPushButton()
        toolIn.setText("Give Tool")
        toolOut.setText("Return Tool")
        toolIn.clicked.connect(lambda:self.assignTool(self.studView))
        toolOut.clicked.connect(lambda:self.returnTool(self.studView))
                
        # checkInLayout.addWidget(toolName)
        topLay.addWidget(toolIn)
        topLay.addWidget(toolOut)

        self.studView = QTableView()
        #create view

        location_column = model.fieldIndex("location")
        proxy = myFilterProxyModel(excluded_values=["none", "None"], column=location_column)
        #create proxy
        proxy.setSourceModel(model)
        #set model
        self.studView.setModel(proxy)
        #attach view to model

        layout.addLayout(topLay)
        layout.addWidget(self.studView)
        self.studView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch) 

        #upon clicking on the some student, the table will load in
        self.studView.clicked.connect(lambda:self.showReports(self.studView))   
        
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

        self.noteProxy = QSortFilterProxyModel()
        #create a proxy view, needs to be accessible so i can futz with it later
        self.noteProxy.setSourceModel(model)
        #set proxy's source
        self.noteProxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        #change filters case sensitivity
        self.noteProxy.setFilterKeyColumn(0)
        #searches names (should be id), for the correct one to display

        table.setModel(self.noteProxy)
        #set model to view
        layout.addWidget(table)
        #add view to layout
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.mainLayout.addLayout(layout)

    def create_tools(self, textBox, model):
    #function repeated for each of the three sections in the dashboard
    #students checked in, tools available, notes
        layout = QVBoxLayout()
        self.toolView = QTableView()
        location_column = model.fieldIndex("quantity")

        #section for entering data
        header = QLineEdit()
        header.setText(textBox)
        header.setReadOnly(True)
        layout.addWidget(header)

        #create filter model, based on original model
        self.toolProxy = myFilterProxyModel(excluded_values=[0], column=location_column)
        self.toolProxy.setSourceModel(model)

        self.toolView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        #make it stretch

        self.toolProxy.setFilterKeyColumn(location_column)
        # filter by the location column in the SQLite-backed model

        self.toolView.clicked.connect(lambda:self.getTool(self.toolView))
        
        self.toolProxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        #look for tools with not 0 quantity, i.e. avaiable

        self.toolView.setModel(self.toolProxy)
        #give the proxy to the view     
        
        layout.addWidget(self.toolView)
        self.mainLayout.addLayout(layout)
        #add the view to the layout, and then to the main

    def showReports(self, table):
        row = table.currentIndex()
        #get the person who's been clicked on
        
        # print(row.data())           #for testing

        #check that it's an id (or at least an integer)
            #return if not
        
        #search id for reports on it (filter by the day?)

        #then create model for it, and load into note view
        self.noteProxy.setFilterFixedString(str(row.data()))
        
    def getTool(self, table):
    #function to get the currently selected tool and store it somewhere
        currentToolIndex = table.currentIndex()

        self.currentTool = currentToolIndex.data()

    def assignTool(self, table):
    #given table of currently in students, give them tool thats currently clicked
        #grab the row and name of clicked tool
        #if there are 0 tools, error msg
        #add it to the tool section of the clicked on student
            #if theres already something, add a comma
        #decrement quantity
        #create note that they borrowed it
 
        toolRow = self.toolView.currentIndex()
        #find the tool

        studRow = self.studView.currentIndex()
        searchColumn = "tool"
        #find the student, and the students' tool to change

        toolList = str(studRow.data())  #text of students tool list
        currTool = str(toolRow.data())  #text of tool to be added
        
        if toolList == "":
        #if first time
            currTool = f"+{str(toolRow.data())}"
            self.studModel.change_value(studRow.row(), searchColumn, currTool) 
            #add tool with + at start
        else:
            toolList = f"{toolList}\n+{currTool}"
            #add existing list and new tool

            self.studModel.change_value(studRow.row(), searchColumn, toolList) 
            #change students tool list with new string
            table.resizeRowsToContents()
            #change row height

        #check for 0 tools
        #decrement tool quantity
        #generate note
    
    def returnTool(self, table):
    #given a clicked on tool, remove from the student, increment quantity
    #make note
        return  
    
    def checkIn(self):
    #function to check a student in
        #grabs id and table section (section not necessary, defaults to In?)
        #changes location
        return

    def checkOut(self):
    #function to check a student out
        #click on the student getting out
        #checks if anything needs to be returned
        #sets location to none
        #makes note of day/time and that they left
        return

class myFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, excluded_values=None, column=1, parent=None):
        super().__init__(parent)
        self.excluded_values = set(excluded_values or [])
        self.column = column

    def filterAcceptsRow(self, source_row, source_parent):
        index = self.sourceModel().index(source_row, self.column, source_parent)
        value = self.sourceModel().data(index, Qt.ItemDataRole.DisplayRole)

        # Exclude rows whose value is in the blacklist
        #inverse of normal logic, returning rows that do not meet the filter
        return value not in self.excluded_values

if __name__ == '__main__':
    app = QApplication(sys.argv)

    studentsModel = tableModel("students_app")
    notesModel = tableModel("reports_app")
    toolsModel = tableModel("tools_app")
    
    # create the main window
    window = myDashboard(studentsModel, notesModel, toolsModel)

    # start the event loop
    sys.exit(app.exec())
