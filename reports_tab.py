#Reports

#Search students history
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
    QGroupBox,
    QComboBox,
    QHeaderView,
    QTableView,
    QDialog,
    QCheckBox
)
from table_model import tableModel


import csv

class myReports(QWidget):
    def __init__(self, model,  *args, **kwargs):
        super().__init__(*args, **kwargs)

        #create main layout
        self.mainLayout = QVBoxLayout(self)
        
        self.model = model                     #create a model
        self.studentsData = QTableView()      # have model look at the data
        self.studentsData.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.studentsData.setModel(self.model)


        #layout for top thing
        changeStudentsLayout = QHBoxLayout()
        
        #buttons
        pullBtn = QPushButton()                      # Create button
        pullBtn.setText("Pull")                       # Add text to button | Acts as a "Enter" button

        filterBtn = QPushButton()                          
        filterBtn.setText("Filters")                    # Button to open filter menu

        filterBtn.clicked.connect(self.openFilters)     # connecting this click function to opening pop up

        #place to enter value
        entryLine = QLineEdit()

        #add widgets to layout
        changeStudentsLayout.addWidget(entryLine)
        changeStudentsLayout.addWidget(pullBtn)
        changeStudentsLayout.addWidget(filterBtn)

        #add to main layout
        self.mainLayout.addLayout(changeStudentsLayout)

        #layout for bottom table
        studentsData = tableModel("sampleReports.csv")              
        studentsDataLayout = QVBoxLayout()

        studentsDataLayout.addWidget(self.studentsData)

        self.mainLayout.addLayout(studentsDataLayout)

        #set the created layout to the widget
        self.setLayout(self.mainLayout)

        #set the widnow size
        self.setGeometry(100, 100, 1000, 700)             #xpos, ypos, x size, y size
        
        # show the window
        self.show()
    
    def openFilters(self):
        dialog = filter_dialog(self)

        if dialog.exec():                               # open pop up if "Filters" button is clicked
            filters = dialog.getFilters()
            print(filters)



    def create_layout(self, layoutName, textBox):
        layout = QVBoxLayout()

        header = QLineEdit()
        header.setText(textBox)
        header.setReadOnly(True)
        layout.addWidget(header)

        data = QTableWidget()
        layout.addWidget(data)

        self.mainLayout.addLayout(layout)




class filter_dialog(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle("Apply Filters")
        self.setFixedSize(500, 700)

        layout = QVBoxLayout(self)

        #checkboxes
        self.toolsBox = QCheckBox("Tools")
        self.machineBox = QCheckBox("Machinery")
        self.spacesBox = QCheckBox("Table")

        layout.addWidget(self.toolsBox)
        layout.addWidget(self.machineBox)               # add checkboxes to window
        layout.addWidget(self.spacesBox)

        # choice buttons
        btnLayout = QHBoxLayout()

        applyBtn = QPushButton("Apply")
        cancelBtn = QPushButton("Cancel")

        applyBtn.clicked.connect(self.accept)           
        cancelBtn.clicked.connect(self.reject)

        btnLayout.addWidget(applyBtn)                    # add choice buttons to window
        btnLayout.addWidget(cancelBtn)

        layout.addLayout(btnLayout)

    def getFilters(self):
        return {
            "tools": self.toolsBox.isChecked(),
            "machinery": self.machineBox.isChecked(),       # check if checkboxes are selected
            "tables": self.spacesBox.isChecked()
        }


        

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create the main window
    dataModel = tableModel("sampleReports.csv")
    window = myReports(dataModel)

    # start the event loop
    sys.exit(app.exec())