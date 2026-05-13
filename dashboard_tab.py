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
    QMessageBox,
    QGroupBox,
    QTableView,
    QHeaderView,
    QDialog,
    QTextEdit,
    QListWidget, QListWidgetItem,

)

from PyQt6.QtCore import QSortFilterProxyModel, Qt
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from table_model import tableModel
import csv
from datetime import datetime

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
        
        # self.spaceIn = QPushButton()
        # self.spaceIn.setText("Assign Table")
        #     #no need for unassign table, happens when they check out
        
        #two buttons for check in and check out
        checkIn = QPushButton()
        checkOut = QPushButton()
        checkIn.setText("Check In")
        checkOut.setText("Check Out")

        studID = self.idEntry.text()            #Id number of student being checked in
        studLocation = self.spaceName.text()    #location of student to be checked into
        #breaks func, gives just text at time of running, not the actual location

        checkIn.clicked.connect(lambda:self.checkIn(self.idEntry.text(), self.spaceName.text()))
        checkOut.clicked.connect(lambda:self.checkOut(self.studView, self.studModel, self.studProxy))

        #add them to the layout
        topThingLayout.addWidget(self.idEntry)
        topThingLayout.addWidget(self.spaceName)
        # topThingLayout.addWidget(self.spaceIn)
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

        self.studView = QTableView()
        #create view

        location_column = model.fieldIndex("location")
        self.studProxy = myFilterProxyModel(excluded_values=["none", "None"], column=location_column)
        #create proxy
        self.studProxy.setSourceModel(model)
        #set model
        self.studView.setModel(self.studProxy)
        #attach view to model

        layout.addLayout(topLay)
        layout.addWidget(self.studView)
        self.studView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.studView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents) 

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

        table = QTableView()
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        #create table view

        layout.addLayout(headerLayout)

        self.noteProxy = QSortFilterProxyModel()
        #create a proxy view, needs to be accessible so i can futz with it later
        self.noteProxy.setSourceModel(model)
        #set proxy's source
        self.noteProxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        #change filters case sensitivity
        self.noteProxy.setFilterKeyColumn(self.noteModel.fieldIndex("student_id"))
        #searches names (should be id), for the correct one to display

        table.setModel(self.noteProxy)
        #set model to view

        table.setColumnHidden(self.noteModel.fieldIndex("note_id"), True)
        #note id
        table.setColumnHidden(self.noteModel.fieldIndex("temp"), True)
        #temp or not

        layout.addWidget(table)
        #add view to layout

        # table.resizeRowsToContents()
        
        addNote.clicked.connect(lambda:self.add_note(table))
        
        self.mainLayout.addLayout(layout)

    def create_tools(self, textBox, model):
    #function repeated for each of the three sections in the dashboard
    #students checked in, tools available, notes
        layout = QVBoxLayout()
        topLayout = QHBoxLayout()

        self.toolView = QTableView()
        location_column = model.fieldIndex("current_quantity")
        location_column = model.fieldIndex("current_quantity")

        #section for entering data
        header = QLineEdit()
        header.textChanged.connect(lambda:self.search_tools(model, header.text()))
        header.setPlaceholderText(textBox)
        # header.setReadOnly(True)
        topLayout.addWidget(header)

        #create the buttons, set their text, 
        toolIn = QPushButton()
        toolOut = QPushButton()
        toolIn.setText("Give Tool")
        toolOut.setText("Return Tool")
        toolIn.clicked.connect(lambda:self.assign_tool(self.studView, self.studModel))
        toolOut.clicked.connect(lambda:self.return_tool(self.studView, self.studModel))
                
        # checkInLayout.addWidget(toolName)
        topLayout.addWidget(toolIn)
        topLayout.addWidget(toolOut)

        #create filter model, based on original model
        self.toolProxy = MultiColumnFilterProxy()
        self.toolProxy.setSourceModel(model)

        self.toolProxy.set_exclude_filter(model.fieldIndex("current_quantity"), "0")

        print(model.fieldIndex("name"))
        print(model.fieldIndex("current_quantity"))

        self.toolView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        #make it stretch

        self.toolProxy.setFilterKeyColumn(location_column)
        # filter by the location column in the SQLite-backed model

        self.toolView.clicked.connect(lambda:self.getTool(self.toolView))
        
        self.toolProxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        #show all tools, including those currently at 0 available

        self.toolView.setModel(self.toolProxy)
        #give the proxy to the view     
        
        layout.addLayout(topLayout)
        layout.addWidget(self.toolView)
        self.mainLayout.addLayout(layout)
        #add the view to the layout, and then to the main

    def search_tools(self, model, text):
        self.toolProxy.set_include_filter(model.fieldIndex("name"), text)

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

    def assign_tool(self, table, model):
    #given table of currently in students, and a model to modify, give them tool thats currently clicked
        
        sourceStudRow, record = self.get_source_row(table, model, self.studProxy)
        #find the original row index (source_row), and the values in that row (record)

        sourceToolRow, toolRecord = self.get_source_row(self.toolView, self.toolModel, self.toolProxy)

        tool = record.value("tool")
        #get the value at this specified field
        
        # toolIndex = self.toolView.currentIndex()
        #index (row, col, data) of currently clicked on tool
        toolRow = sourceToolRow                       #find its row

        # print(toolRow)
        if toolRow < 0:
            QMessageBox.critical(
                self,
                "Failed",
                "Current Quantity of tool is too low. lmao"
            )
            return

        toolCol = self.toolModel.fieldIndex("name")     #find col for names
        index = self.toolModel.index(toolRow, toolCol)   #index it

        searchColumn = "tool"
        #find the student, and the students' tool to change

        toolList = "" if tool in (None, "", "None") else str(tool)
        #if person has no tool to begin with

        currTool = str(self.toolModel.data(index))  
        #get text of tool to be added using that index

        # print(f"tool to add: {currTool}")

        current_quantity = self.toolModel.data(
            self.toolModel.index(toolRow, self.toolModel.fieldIndex("current_quantity"))
        )
        if int(current_quantity) <= 0:
            QMessageBox.critical(
                self,
                "Failed",
                "Current Quantity of tool is too low."
            )
            return
        
        if toolList == "":
        #if first time
            # print(f"test {currTool}")
            model.change_value(sourceStudRow, searchColumn, currTool) 
            #add tool to blank string
        else:
            toolList = f"{tool}\n{currTool}"
            # print(f"not empty")
            #add existing list and new tool
            model.change_value(sourceStudRow, searchColumn, toolList) 
            #change students tool list with new string
        
        # table.resizeRowsToContents()

        #decrement quantity
        if self.toolView.selectionModel() is not None:
            self.toolView.selectionModel().clearCurrentIndex()
            self.toolView.clearSelection()
        self.toolModel.adjust_value(toolRow, "current_quantity", -1, minimum=0)

        #make note
        self.auto_report(record.value("id"), currTool, record.value("location"), f"Checked out tool: {currTool}")

    
    def return_tool(self, view, model):
    #given a view and a model of students, get the checked out tools, and give a list, 
    # increment quantity, make note
        #find the students checked out tools
        #split the list into data
        #create a checkbox from the data
        #for each check, remove from list
        #increment quantity
        #make note

        col = model.fieldIndex("tool")
        #find the students' tools to be returned

        row, record = self.get_source_row(view, model, self.studProxy)

        raw = record.value("tool") or ""
        items = [line.strip() for line in raw.split("\n") if line.strip()]
        #get the raw data, and turn into list

        dialog = QDialog()
        layout = QVBoxLayout()
        list_widget = QListWidget()
        dialog.setWindowTitle("Tool Return Checklist")
        #setup for the dialog box

        for item in items:
            lw_item = QListWidgetItem(item)
            lw_item.setFlags(lw_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            lw_item.setCheckState(Qt.CheckState.Unchecked)
            list_widget.addItem(lw_item)

        layout.addWidget(list_widget)

        btn = QPushButton("Check Back Tools")
        layout.addWidget(btn)

        dialog.setLayout(layout)

        def remove_checked():
            remaining = []
            returned_tools = []
            returned_tools = []
            for i in range(list_widget.count()):
                item = list_widget.item(i)
                if item.checkState() == Qt.CheckState.Unchecked:
                    remaining.append(item.text())
                else:
                    returned_tools.append(item.text())

            # Join back into newline string
            new_value = "\n".join(remaining)

            model.change_value(row, "tool", new_value)

            for tool_name in returned_tools:
                toolRow = self.toolModel.find_row_by_value("name", tool_name)
                if toolRow < 0:
                    continue

                max_quantity = self.toolModel.data(
                    self.toolModel.index(toolRow, self.toolModel.fieldIndex("max_quantity"))
                )
                self.toolModel.adjust_value(
                    toolRow,
                    "current_quantity",
                    1,
                    minimum=0,
                    maximum=int(max_quantity) if max_quantity not in (None, "") else None,
                )
                self.auto_report(record.value("id"), tool_name, record.value("location"), f"Returned tool: {tool_name}")

            dialog.accept()

        btn.clicked.connect(remove_checked)
        dialog.exec()
    
    def checkIn(self, targetId, targetText):
    #function to change a students location
    #used for both checking in, and checkout out a student
        #grabs id and table section (section not necessary, defaults to In?)
        #changes location
        # print(targetId)
        # print(targetText) 
        col = self.studModel.fieldIndex("id")
        # print(col)
        matches = self.studModel.match(
            self.studModel.index(0, col),   #where to start
            Qt.ItemDataRole.DisplayRole,    #what role to search
            targetId,                       #what to look for 
            hits=1,                         #how many to return
            flags=Qt.MatchFlag.MatchExactly #what flag
        )   #returns set of values

        # print(matches)

        targetText = targetText.strip()
        normalized_location = targetText if targetText else "None"

        if matches:
            index = matches[0]
            row = index.row()
            old_location = self.studModel.data(self.studModel.index(row, self.studModel.fieldIndex("location")))

            #now with row, just change the text of the location to whatever was entered
            self.studModel.change_value(row, "location", normalized_location)

            #make auto note
            if normalized_location == "None":
                note_text = "Checked in without a location"
            elif old_location in (None, "", "None"):
                note_text = f"Checked in to {normalized_location}"
            elif str(old_location) != str(normalized_location):
                note_text = f"Moved from {old_location} to {normalized_location}"
            else:
                note_text = f"Checked in to {normalized_location}"

            self.auto_report(targetId, "None", normalized_location, note_text)
            
        else:
            #dialog to say not found
            QMessageBox.critical(
                self,
                "Failed",
                "Student ID not found."
            )

    def checkOut(self, view, model, proxy):
    #function to check a student out
        #click on the student getting out
        #checks if anything needs to be returned
        #sets location to none
        #makes note of day/time and that they left

        row, record = self.get_source_row(view, model, proxy)

        if view.selectionModel() is not None:
            view.selectionModel().clearCurrentIndex()
            view.clearSelection()
        model.change_value(row, "location", "None")
        self.auto_report(record.value("id"), "None", "None", f"Checked out from {record.value('location')}")
        # return

    
    def add_note(self, view):
        self.reporting = makeNote_dialog(self)
        #create the report box

        if self.reporting.exec():
        #if the thing is executing

            # noteid, studid, toolid, location, note, time
            report = self.reporting.getConfirmReport()        # returns if report has been made
            # print(report)

            # confirm/deny pop up window
            if report == "Report Created.":
                text = self.reporting.return_text()
                # Create a timestamp integer to save the time
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                #grab the current text in all entries
                # print(f"text: {text}")
                text.append(0)              #if temp or not, 0 means permanent
                self.noteModel.add_row(text)
                #add it to the model

                # view.resizeRowsToContents()

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
    
    def auto_report(self, student_id, tool_name, location, note_text):
        #generates auto report, for assigning tools, students
        #  noteid, studid, toolid, location, note, time
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.noteModel.add_row([student_id, tool_name, location, note_text, timestamp, 1])
    
    def get_source_row(self, view, model, proxy):
    # given a view, model, and proxy, find the source row of the currently cliked on views row
    # returns row number in source model, and record: all values in that row
        proxy_index = view.currentIndex()
        #find the index of the view
        source_index = proxy.mapToSource(proxy_index)
        #find index of source model
        source_row = source_index.row()
        #use that to find the row at source index
        record = model.record(source_index.row())
        #get all the data at that row

        return source_row, record

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
        self.entryText = []

        # top layout
        self.stuIDLine = QLineEdit()
        self.stuIDLine.setPlaceholderText("Enter Student ID Number")
        self.entryText.append(self.stuIDLine)

        self.toolIDLine = QLineEdit()
        self.toolIDLine.setPlaceholderText("Enter Tool Name")
        self.entryText.append(self.toolIDLine)

        self.locationLine = QLineEdit()
        self.locationLine.setPlaceholderText("Enter Location")
        self.entryText.append(self.locationLine)

        self.timeLine = QLineEdit()
        self.timeLine.setPlaceholderText("YYYY-MM-DD-HH:MM")

        #grab current time and date
        ct = datetime.now()
        self.timeLine.setText(str(ct)[:-7])
        #chop off last few digits
        # print(self.timeLine.text())
        
        topLayout.addWidget(self.stuIDLine)
        topLayout.addWidget(self.toolIDLine)
        topLayout.addWidget(self.locationLine)
        topLayout.addWidget(self.timeLine)
        layout.addLayout(topLayout)

        self.stuReport = QTextEdit()
        self.stuReport.setPlaceholderText("Enter Student Report")
        layout.addWidget(self.stuReport, 1)
        self.entryText.append(self.stuReport)
        self.entryText.append(self.timeLine)        #timeline must be here for the table

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
        if self.stuIDLine.text().strip() and self.stuReport.toPlainText().strip():
            return("Report Created.")

        else:
            return("Please fill in information.")
        
    def warning(self):
            pass
    
    def return_text(self):
        text = []

        # text.append(1)      #note id?

        for entry in self.entryText:
            if isinstance(entry, QTextEdit):
                text.append(entry.toPlainText())
                continue
            
            text.append(entry.text())
            # print(text)
        
        return text

class MultiColumnFilterProxy(QSortFilterProxyModel):
    from PyQt6.QtCore import QSortFilterProxyModel, Qt


class MultiColumnFilterProxy(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.include_filters = {}  # column -> text that must be present
        self.exclude_filters = {}  # column -> text that must NOT be present

    def set_include_filter(self, column, text):
        self.include_filters[column] = text.lower().strip()
        self.invalidateFilter()

    def set_exclude_filter(self, column, text):
        self.exclude_filters[column] = text.lower().strip()
        self.invalidateFilter()

    def clear_include_filter(self, column):
        self.include_filters.pop(column, None)
        self.invalidateFilter()

    def clear_exclude_filter(self, column):
        self.exclude_filters.pop(column, None)
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        model = self.sourceModel()

        # Include logic: row must match all include filters
        for column, filter_text in self.include_filters.items():
            if not filter_text:
                continue

            index = model.index(source_row, column, source_parent)
            value = model.data(index, Qt.ItemDataRole.DisplayRole)

            if value is None:
                return False

            if filter_text not in str(value).lower():
                return False

        # Exclude logic: row must NOT match any exclude filters
        for column, filter_text in self.exclude_filters.items():
            if not filter_text:
                continue

            index = model.index(source_row, column, source_parent)
            value = model.data(index, Qt.ItemDataRole.DisplayRole)

            if value is None:
                continue

            if filter_text in str(value).lower():
                return False

        return True

if __name__ == '__main__':
    app = QApplication(sys.argv)

    studentsModel = tableModel("students_app")
    notesModel = tableModel("notes_app")
    toolsModel = tableModel("tools_app")
    
    # create the main window
    window = myDashboard(studentsModel, notesModel, toolsModel)

    # start the event loop
    sys.exit(app.exec())
