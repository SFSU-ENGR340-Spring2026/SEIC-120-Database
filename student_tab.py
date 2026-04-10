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
    QTableView
)
from table_model import tableModel


import csv

class myStudents(QWidget):
    def __init__(self, *args, **kwargs):
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
        entryLine = QLineEdit()
        entryLine.setPlaceholderText("put thing")
        #add widgets to layout
        changeStudentsLayout.addWidget(entryLine)
        changeStudentsLayout.addWidget(addBtn)
        changeStudentsLayout.addWidget(delBtn)
        #add to main layout
        self.mainLayout.addLayout(changeStudentsLayout)

        #layout for bottom table
        model = tableModel("sampleStudents.csv")

        studentsData = QTableView()
        studentsData.setModel(model)
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

    # create the main window
    window = myStudents()

    # start the event loop
    sys.exit(app.exec())