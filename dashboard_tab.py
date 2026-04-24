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
    QHeaderView,
    QDialog,
    QTextEdit
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
        toolIn.clicked.connect(lambda:self.assignTool(table))
        toolOut.clicked.connect(lambda:self.returnTool(table))
                
        # checkInLayout.addWidget(toolName)
        topLay.addWidget(toolIn)
        topLay.addWidget(toolOut)

        table = QTableView()
        #create view

        location_column = model.fieldIndex("location")
        proxy = myFilterProxyModel(excluded_values=["none", "None"], column=location_column)
        #create proxy
        proxy.setSourceModel(model)
        #set model
        table.setModel(proxy)
        #attach view to model

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

        addNote.clicked.connect(self.add_note)

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
        location_column = model.fieldIndex("quantity")

        #section for entering data
        header = QLineEdit()
        header.setText(textBox)
        header.setReadOnly(True)
        layout.addWidget(header)

        #create filter model, based on original model
        self.toolProxy = myFilterProxyModel(excluded_values=[0], column=location_column)
        self.toolProxy.setSourceModel(model)

        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        #make it stretch

        self.toolProxy.setFilterKeyColumn(location_column)
        # filter by the location column in the SQLite-backed model

        table.clicked.connect(lambda:self.getTool(table))
        
        self.toolProxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        #look for tools with not 0 quantity, i.e. avaiable

        table.setModel(self.toolProxy)
        #give the proxy to the view     
        
        layout.addWidget(table)
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
        self.proxyView.setFilterFixedString(str(row.data()))
        
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
        return
    
    def returnTool(self):
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
    
    def add_note(self):
        reporting = makeNote_dialog(self)

        if reporting.exec():
            report = reporting.getConfirmReport()        # returns if report has been made
            print(report)


            # confirm/deny pop up window
            if report == "Report Created.":
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setText("Note Created.")
                msg.setWindowTitle("Confirmed")
                msg.exec()
            else: 
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setText("Please Enter Information.")
                msg.setWindowTitle("Denied")
                msg.exec()

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
    
class makeNote_dialog(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle("Make Note")
        self.setFixedSize(700,700)

        layout = QVBoxLayout(self)
        topLayout = QHBoxLayout(self)


        # Entery Text 

        # top layout
        self.stuIDLine = QLineEdit()
        self.stuIDLine.setPlaceholderText("Enter Student ID Number")

        self.toolIDLine = QLineEdit()
        self.toolIDLine.setPlaceholderText("Enter Tool ID")

        self.locationLine = QLineEdit()
        self.locationLine.setPlaceholderText("Enter Location")

        self.timeLine = QLineEdit()
        self.timeLine.setPlaceholderText("YYYY-MM-DD-HH:MM")
        
        topLayout.addWidget(self.stuIDLine)
        topLayout.addWidget(self.toolIDLine)
        topLayout.addWidget(self.locationLine)
        topLayout.addWidget(self.timeLine)
        layout.addLayout(topLayout)

        self.stuReport = QTextEdit()
        self.stuReport.setPlaceholderText("Enter Student Report")
        layout.addWidget(self.stuReport, 1)

        # Buttons
        btnLayout = QHBoxLayout()

        submitBtn = QPushButton("Submit")
        cancelBtn = QPushButton("Cancel")

        submitBtn.clicked.connect(self.accept)           
        cancelBtn.clicked.connect(self.reject)

        btnLayout.addWidget(submitBtn)
        btnLayout.addWidget(cancelBtn)

        layout.addLayout(btnLayout)

    def getConfirmReport(self):
        if self.stuIDLine.int().strip() and self.stuReport.toPlainText().strip():
            return("Report Created.")

        else:
            return("Please fill in information.")
        
    def warning(self):
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)

    studentsModel = tableModel("students_app")
    notesModel = tableModel("notes_app")
    toolsModel = tableModel("tools_app")
    
    # create the main window
    window = myDashboard(studentsModel, notesModel, toolsModel)

    # start the event loop
    sys.exit(app.exec())
