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
    QHeaderView,
    QComboBox,

)
from PyQt6.QtCore import QSortFilterProxyModel, Qt
from PyQt6.QtGui import QIcon
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

        self.entries = [self.stuIDLine, self.nameLine]

        # Drop down menu for Student Certifications
        self.certBox = QComboBox()
        # icons
        printIcon = QIcon('3D_print_icon')
        lzrIcon = QIcon('lzr_icon')
        toolIcon = QIcon('tool_Icon')

        self.certBox.addItem("Student Certifications")
        self.certBox.addItem(toolIcon, "Hand Tool")
        self.certBox.addItem(lzrIcon, "Laser Cutter/Engraver")
        self.certBox.addItem(printIcon, '3D Printer')
        self.certBox.addItem("❌ None")

        # cant select "Student Certifications" as an option, acts more as a title for drop down
        item = self.certBox.model().item(0)
        item.setEnabled(False) 


        #add widgets to layout
        changeStudentsLayout.addWidget(self.stuIDLine)
        changeStudentsLayout.addWidget(self.nameLine)
        changeStudentsLayout.addWidget(self.certBox)
        changeStudentsLayout.addWidget(addBtn)
        changeStudentsLayout.addWidget(delBtn)

        #search bar
        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Search for student ID or Name")

        #add to main layout
        self.mainLayout.addLayout(changeStudentsLayout)
        self.mainLayout.addWidget(self.searchBar)

        self.studModel = model
        #create the model for the data

        self.studentsData = QTableView()
        #create a view to look at the model
        self.studentsData.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.proxy = QSortFilterProxyModel()
        self.proxy.setSourceModel(self.studModel)

        location_column = self.studModel.fieldIndex("id")
        #where to search
        self.proxy.setFilterKeyColumn(location_column)
        # filter by the location column in the SQLite-backed model
        
        self.proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive) 
        #make filter case insensitive
        self.searchBar.textChanged.connect(lambda: self.search())
        #upon search bar being typed, activate search  

        self.studentsData.setModel(self.proxy)
        #give proxy to view
        
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
    
    def search(self):
    #search function
        self.proxy.setFilterFixedString(self.searchBar.text())
        #just grabs text in search bar, searches for it
    
if __name__ == '__main__':

    app = QApplication(sys.argv)

    model = tableModel("students_app")

    # create the main window
    window = myStudents(model)

    # start the event loop
    sys.exit(app.exec())