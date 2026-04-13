#students tab
#add/remove students
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
    QTableView,
    QHeaderView
)
from table_model import tableModel


import csv

class myStudents(QWidget):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #create main layout
        self.mainLayout = QVBoxLayout(self)

        #layout for top thing
        changeStudentsLayout = QHBoxLayout()

        #buttons
        addBtn = QPushButton()
        addBtn.setText("Add")
        delBtn = QPushButton()
        delBtn.setText("Remove")

        #place to enter value
        self.nameLine = QLineEdit()
        self.nameLine.setPlaceholderText("Enter Student Name")

        self.stuIDLine = QLineEdit()
        self.stuIDLine.setPlaceholderText("Enter Student ID Number")

  
        

        #add widgets to layout
        changeStudentsLayout.addWidget(self.nameLine)
        changeStudentsLayout.addWidget(self.stuIDLine)
        changeStudentsLayout.addWidget(addBtn)
        changeStudentsLayout.addWidget(delBtn)

        #add to main layout
        self.mainLayout.addLayout(changeStudentsLayout)

        studModel = model
        #create the model for the data

        studentsData = QTableView()
        #create a view to look at the model
        studentsData.setModel(studModel)
        studentsData.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        #layout for bottom table
        studentsDataLayout = QVBoxLayout()

        studentsDataLayout.addWidget(studentsData)

        self.mainLayout.addLayout(studentsDataLayout)

        #set the created layout to the widget
        self.setLayout(self.mainLayout)
        #set the widnow size
        self.setGeometry(100, 100, 1000, 700)
        
        # show the window
        self.show()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)

    model = tableModel("sampleStudents.csv")

    # create the main window
    window = myStudents(model)

    # start the event loop
    sys.exit(app.exec())