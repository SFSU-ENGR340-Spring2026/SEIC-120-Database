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
    QComboBox
)
from table_tests import MyTableWidget


import csv

class myReports(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #create main layout
        self.mainLayout = QVBoxLayout(self)


        #layout for top thing
        changeStudentsLayout = QHBoxLayout()
        
        #buttons
        addBtn = QPushButton()                      # Create button
        addBtn.setText("Pull")                       # Add text to button
        delBtn = QPushButton()
        delBtn.setText("Apply Filter")                    # Drop down list

        #Filter Drop down list
        filterDropDown = QComboBox()
        filterDropDown.addItem('Tools')
        filterDropDown.addItem('Machinery')
        filterDropDown.addItem('Tables')
        filterDropDown.addItem('Time')

        self.mainLayout.addWidget(filterDropDown)


        #place to enter value
        entryLine = QLineEdit()

        #add widgets to layout
        changeStudentsLayout.addWidget(entryLine)
        changeStudentsLayout.addWidget(addBtn)
        changeStudentsLayout.addWidget(delBtn)

        #add to main layout
        self.mainLayout.addLayout(changeStudentsLayout)

        #layout for bottom table
        studentsData = QTableWidget()
        studentsDataLayout = QVBoxLayout()

        studentsDataLayout.addWidget(studentsData)

        self.mainLayout.addLayout(studentsDataLayout)

        #set the created layout to the widget
        self.setLayout(self.mainLayout)

        #set the widnow size
        self.setGeometry(100, 100, 1000, 700)             #xpos, ypos, x size, y size
        
        # show the window
        self.show()
    
    def create_layout(self, layoutName, textBox):
        layout = QVBoxLayout()

        header = QLineEdit()
        header.setText(textBox)
        header.setReadOnly(True)
        layout.addWidget(header)

        data = QTableWidget()
        layout.addWidget(data)

        self.mainLayout.addLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create the main window
    window = myReports()

    # start the event loop
    sys.exit(app.exec())