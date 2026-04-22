#dashboard

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
    QHeaderView,
    QTableView
)
from table_model import tableModel


import csv

class myTools(QWidget):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #create main layout
        self.mainLayout = QVBoxLayout(self)

        self.model = model
        #create the model for the data

        self.studentsData = QTableView()
        #create the view to look at the model

        #format output
        self.studentsData.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        #select only one at a time
        self.studentsData.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        #contents will stretch to fit window

        self.studentsData.setModel(self.model)

        #layout for top thing
        self.create_top_layout()

        #search bar
        searchBar = QLineEdit()
        searchBar.setPlaceholderText("Search for student ID or Name")
        self.mainLayout.addWidget(searchBar)

        #layout for bottom table
        self.create_bot_layout()

        #set the created layout to the widget
        self.setLayout(self.mainLayout)

        #set the widnow size
        self.setGeometry(100, 100, 1000, 700)
        
        # show the window
        self.show()
    
    def create_top_layout(self):
        changeStudentsLayout = QHBoxLayout()
       
        #buttons
        addBtn = QPushButton()
        addBtn.setText("Add Tool")

        delBtn = QPushButton()
        delBtn.setText("Remove Tool")

        #place to enter value
        self.nameEntry = QLineEdit()
        self.quanEntry = QLineEdit()
        self.condEntry = QLineEdit()
        self.tagEntry = QLineEdit()
        self.locatEntry = QLineEdit()

        self.entries = [self.nameEntry, self.quanEntry, self.condEntry, self.tagEntry, self.locatEntry]
        
        self.reset_entry_text()

        addBtn.clicked.connect(lambda:self.add_Tool())
        delBtn.clicked.connect(lambda:self.remove_tool())

        #add widgets to layout
        for entry in self.entries:
            changeStudentsLayout.addWidget(entry)

        changeStudentsLayout.addWidget(addBtn)
        changeStudentsLayout.addWidget(delBtn)

        self.mainLayout.addLayout(changeStudentsLayout)

    def create_bot_layout(self):
        #layout for bottom table
    
        studentsDataLayout = QVBoxLayout()

        studentsDataLayout.addWidget(self.studentsData)

        self.mainLayout.addLayout(studentsDataLayout)

    def add_Tool(self):
        newToolData = []

        for entry in self.entries:
            newToolData.append(entry.text())
            #add all entries to a list

        self.model.add_row(newToolData)
        #add list to table
    
    def remove_tool(self):
    #remove a single selected row from the db
        index = self.studentsData.currentIndex()
        #find the row of the item

        print(index.row())

        if index.isValid():
            self.model.del_row(index.row())
            #remove it


    def reset_entry_text(self):
    #helper function to reset the text entries       
        textBoxes = ["Tool Name", "Quantity", "Tool Condition", "High or Low Power", "Location"]
        #the text to reset them to

        for entryItem, text in zip(self.entries, textBoxes):
            entryItem.setPlaceholderText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    dataModel = tableModel("tools_app")

    # create the main window
    window = myTools(dataModel)

    # start the event loop
    sys.exit(app.exec())
