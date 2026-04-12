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
    QTableView
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

        # open pop up
        filterBtn.clicked.connect(self.showPopUp)       # prompts pop up menu when pressed

        
        # #Filter Drop down list
        # filterDropDown = QComboBox()
        # filterDropDown.addItem('Tools')
        # filterDropDown.addItem('Machinery')
        # filterDropDown.addItem('Tables')
        # filterDropDown.addItem('Time')

        #self.mainLayout.addWidget(filterDropDown)

        


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
    
    def create_layout(self, layoutName, textBox):
        layout = QVBoxLayout()

        header = QLineEdit()
        header.setText(textBox)
        header.setReadOnly(True)
        layout.addWidget(header)

        data = QTableWidget()
        layout.addWidget(data)

        self.mainLayout.addLayout(layout)


    def showPopUp(self):
         # Cosmetics
         msg = QMessageBox()
         msg.setWindowTitle("Apply Filters")
         msg.setText("Select Filters: ")
         msg.setStandardButtons(QMessageBox.StandardButton.Save|QMessageBox.StandardButton.Cancel)      # Create Save and Cancel button
         msg.setDefaultButton(QMessageBox.StandardButton.Save)                                          # Have Save Button be automatically highlighted
         #msg.setStyleSheet("QLable{min-width: 3000px;}")
         msg.resize(400,200)




         disp = msg.exec()                      # opens the window
         
        

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create the main window
    dataModel = tableModel("sampleReports.csv")
    window = myReports(dataModel)

    # start the event loop
    sys.exit(app.exec())