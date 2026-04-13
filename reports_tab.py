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


        # group boxes

        # Tools Group
        tool_group = QGroupBox("Tools")                 # Create Group box for tools   
        tool_layout = QVBoxLayout()                     # Create VERTICAL layout for tool layout

        self.screwdriverBox = QCheckBox("Screwdriver")       # create check box
        self.hammerBox = QCheckBox("Hammer")
        tool_layout.addWidget(self.screwdriverBox)           # add checkbox to grup
        tool_layout.addWidget(self.hammerBox)

        tool_group.setLayout(tool_layout)               # add layout to group
        layout.addWidget(tool_group)                    # add tool group to main pop up layout

        # spaces group
        spaces_group = QGroupBox("Tables")
        spaces_layout = QHBoxLayout()

        #section A
        layoutA = QVBoxLayout()
        
        self.tableA1Box = QCheckBox("A1")
        self.tableA2Box = QCheckBox("A2")
        self.tableA3Box = QCheckBox("A3")
        self.tableA4Box = QCheckBox("A4")
        self.tableA5Box = QCheckBox("A5")

        spaces_layout.addWidget(self.tableA1Box)
        spaces_layout.addWidget(self.tableA2Box)
        spaces_layout.addWidget(self.tableA3Box)
        spaces_layout.addWidget(self.tableA4Box)
        spaces_layout.addWidget(self.tableA5Box)

        # section B
        layoutB = QHBoxLayout()

        self.tableB1Box = QCheckBox("B1")
        self.tableB2Box = QCheckBox("B2")
        self.tableB3Box = QCheckBox("B3")
        self.tableB4Box = QCheckBox("B4")
        self.tableB5Box = QCheckBox("B5")

        layoutB.addWidget(self.tableB1Box)
        layoutB.addWidget(self.tableB2Box)
        layoutB.addWidget(self.tableB3Box)
        layoutB.addWidget(self.tableB4Box)
        layoutB.addWidget(self.tableB5Box)

        # section C
        layoutC = QHBoxLayout()

        self.tableC1Box = QCheckBox("C1")
        self.tableC2Box = QCheckBox("C2")
        self.tableC3Box = QCheckBox("C3")
        self.tableC4Box = QCheckBox("C4")
        self.tableC5Box = QCheckBox("C5")

        layoutC.addWidget(self.tableC1Box)
        layoutC.addWidget(self.tableC2Box)
        layoutC.addWidget(self.tableC3Box)
        layoutC.addWidget(self.tableC4Box)
        layoutC.addWidget(self.tableC5Box)


        # section D
        layoutD = QHBoxLayout()

        self.tableD1Box = QCheckBox("D1")
        self.tableD2Box = QCheckBox("D2")
        self.tableD3Box = QCheckBox("D3")
        self.tableD4Box = QCheckBox("D4")
        self.tableD5Box = QCheckBox("D5")

        layoutD.addWidget(self.tableD1Box)
        layoutD.addWidget(self.tableD2Box)
        layoutD.addWidget(self.tableD3Box)
        layoutD.addWidget(self.tableD4Box)
        layoutD.addWidget(self.tableD5Box)

        # section E
        layoutE = QHBoxLayout()

        self.tableE1Box = QCheckBox("E1")
        self.tableE2Box = QCheckBox("E2")
        self.tableE3Box = QCheckBox("E3")
        self.tableE4Box = QCheckBox("E4")
        self.tableE5Box = QCheckBox("E5")

        layoutE.addWidget(self.tableE1Box)
        layoutE.addWidget(self.tableE2Box)
        layoutE.addWidget(self.tableE3Box)
        layoutE.addWidget(self.tableE4Box)
        layoutE.addWidget(self.tableE5Box)

        # section F
        layoutF = QHBoxLayout()

        self.tableF1Box = QCheckBox("F1")
        self.tableF2Box = QCheckBox("F2")
        self.tableF3Box = QCheckBox("F3")
        self.tableF4Box = QCheckBox("F4")
        self.tableF5Box = QCheckBox("F5")

        layoutF.addWidget(self.tableF1Box)
        layoutF.addWidget(self.tableF2Box)
        layoutF.addWidget(self.tableF3Box)
        layoutF.addWidget(self.tableF4Box)
        layoutF.addWidget(self.tableF5Box)


        # add sections B-E to section A, makes thr tables grouping in a 6x5 grid
        layoutA.addLayout(layoutB)             
        layoutA.addLayout(layoutC)
        layoutA.addLayout(layoutD)
        layoutA.addLayout(layoutE)
        layoutA.addLayout(layoutF)
        layoutA.addLayout(spaces_layout)

      
      
        spaces_group.setLayout(layoutA)
        layout.addWidget(spaces_group)       

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
          
            # tools
            "Screwdriver": self.screwdriverBox.isChecked(),
            "Hammer:": self.hammerBox.isChecked(),

            # spaces
            "A1": self.tableA1Box.isChecked(),
            "A2": self.tableA2Box.isChecked(),
            "A3": self.tableA3Box.isChecked(),
            "A4": self.tableA4Box.isChecked(),
            "A5": self.tableA5Box.isChecked(),

            "B1": self.tableB1Box.isChecked(),
            "B2": self.tableB2Box.isChecked(),
            "B3": self.tableB3Box.isChecked(),
            "B4": self.tableB4Box.isChecked(),
            "B5": self.tableB5Box.isChecked(),    

            "C1": self.tableC1Box.isChecked(),
            "C2": self.tableC2Box.isChecked(),
            "C3": self.tableC3Box.isChecked(),
            "C4": self.tableC4Box.isChecked(),
            "C5": self.tableC5Box.isChecked(),        

            "D1": self.tableD1Box.isChecked(),
            "D2": self.tableD2Box.isChecked(),
            "D3": self.tableD3Box.isChecked(),
            "D4": self.tableD4Box.isChecked(),
            "D5": self.tableD5Box.isChecked(),

            "E1": self.tableE1Box.isChecked(),
            "E2": self.tableE2Box.isChecked(),
            "E3": self.tableE3Box.isChecked(),
            "E4": self.tableE4Box.isChecked(),
            "E5": self.tableE5Box.isChecked(),

        }

        
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create the main window
    dataModel = tableModel("sampleReports.csv")
    window = myReports(dataModel)

    # start the event loop
    sys.exit(app.exec())