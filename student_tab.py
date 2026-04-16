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
        addBtn.setText("Add Student")
        addBtn.clicked.connect(lambda:self.add_student())

        delBtn = QPushButton()
        delBtn.setText("Remove Student")
        delBtn.clicked.connect(lambda:self.rem_student())

        #place to enter values
        self.nameLine = QLineEdit()
        self.nameLine.setPlaceholderText("Enter Student Name")

        self.stuIDLine = QLineEdit()
        self.stuIDLine.setPlaceholderText("Enter Student ID Number")  

        self.entries = [self.nameLine, self.stuIDLine]

        #add widgets to layout
        changeStudentsLayout.addWidget(self.stuIDLine)
        changeStudentsLayout.addWidget(self.nameLine)
        changeStudentsLayout.addWidget(addBtn)
        changeStudentsLayout.addWidget(delBtn)

        #add to main layout
        self.mainLayout.addLayout(changeStudentsLayout)

        self.studModel = model
        #create the model for the data

        self.studentsData = QTableView()
        #create a view to look at the model
        self.studentsData.setModel(self.studModel)
        self.studentsData.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        #layout for bottom table
        studentsDataLayout = QVBoxLayout()

        studentsDataLayout.addWidget(self.studentsData)

        self.mainLayout.addLayout(studentsDataLayout)

        #set the created layout to the widget
        self.setLayout(self.mainLayout)
        #set the widnow size
        self.setGeometry(100, 100, 1000, 700)
        
        # show the window
        self.show()

    def add_student(self):
        newToolData = []

        for entry in self.entries:
            newToolData.append(entry.text())
            #add all entries to a list
        
        newToolData.append("None")
        newToolData.append("None")
        #needs 4 entries to enter into db, default to none for new student
        
        self.studModel.add_row(newToolData)
        #add list to table
    
    def rem_student(self):
        #remove a single selected row from the db
        index = self.studentsData.currentIndex()
        #find the row of the item

        print(index.row())

        if index.isValid():
            self.studModel.del_row(index.row())
    
if __name__ == '__main__':
    app = QApplication(sys.argv)

    model = tableModel("students_app")

    # create the main window
    window = myStudents(model)

    # start the event loop
    sys.exit(app.exec())