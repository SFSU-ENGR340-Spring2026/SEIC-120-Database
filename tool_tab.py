#tools tab
#add/remove tools
#display the table

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
    QGroupBox
)
from tables import MyTableWidget


import csv

class myTools(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #create main layout
        self.mainLayout = QVBoxLayout(self)

        self.studentsData = MyTableWidget("sampleData.csv")

        #layout for top thing
        self.create_top_layout()

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
        addBtn.setText("Add")

        delBtn = QPushButton()
        delBtn.setText("Remove")

        #place to enter value
        nameEntry = QLineEdit()
        quanEntry = QLineEdit()
        condEntry = QLineEdit()
        tagEntry = QLineEdit()
        locatEntry = QLineEdit()

        self.entries = [nameEntry, quanEntry, condEntry, tagEntry, locatEntry]
        
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

        newToolData.append(self.nameEntry.text())
        newToolData.append(self.quanEntry.text())
        newToolData.append(self.condEntry.text())
        newToolData.append(self.tagEntry.text())
        newToolData.append(self.locatEntry.text())
        #add all entries to a list

        self.studentsData.addRow(newToolData)
        #add to table

        self.reset_entry_text()
    
    def remove_tool(self):
        self.studentsData.delRow()

    def reset_entry_text(self):
    #helper function to reset the text entries       
        textBoxes = ["Tool Name", "Quantity", "Tool Condition", "High or Low Power", "Location"]
        #the text to reset them to

        for entryItem, text in zip(self.entries, textBoxes):
            entryItem.setText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create the main window
    window = myTools()

    # start the event loop
    sys.exit(app.exec())