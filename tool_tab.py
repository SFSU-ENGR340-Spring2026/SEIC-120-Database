#dashboard

import sys
import os
from PyQt6.QtCore import QSortFilterProxyModel, Qt
from PyQt6.QtGui import QIcon
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
    QTableView,
    QComboBox
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

        #layout for top thing
        self.create_top_layout()

        #search bar
        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Search for tool")
        self.mainLayout.addWidget(self.searchBar)

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
        self.entries = [self.nameEntry, self.quanEntry, self.condEntry]


      
        # Drop down menu for Student Certifications
        self.certBox = QComboBox()
        # icons
        self.printIcon = QIcon(self.get_path("3D_print_icon.png"))
        self.lzrIcon = QIcon(self.get_path("lzr_icon.png"))
        self.toolIcon = QIcon(self.get_path("tool_Icon.png"))

        self.certBox.addItem("Student Certifications")
        self.certBox.addItem(self.toolIcon, "Hand Tool")
        self.certBox.addItem(self.lzrIcon, "Laser Cutter/Engraver")
        self.certBox.addItem(self.printIcon, '3D Printer')
        self.certBox.addItem("❌ None")

        # cant select "Student Certifications" as an option, acts more as a title for drop down
        item = self.certBox.model().item(0)
        item.setEnabled(False) 

        
        self.reset_entry_text()

        addBtn.clicked.connect(lambda:self.add_Tool())
        delBtn.clicked.connect(lambda:self.remove_tool())

        #add widgets to layout
        for entry in self.entries:
            changeStudentsLayout.addWidget(entry)

        changeStudentsLayout.addWidget(self.certBox)
        changeStudentsLayout.addWidget(addBtn)
        changeStudentsLayout.addWidget(delBtn)
       

        self.mainLayout.addLayout(changeStudentsLayout)

    def create_bot_layout(self):
        #layout for bottom table
    
        studentsDataLayout = QVBoxLayout()

        self.studentsData = QTableView()
        #create the view to look at the model

        #format output
        self.studentsData.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        #select only one at a time
        self.studentsData.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        #contents will stretch to fit window

        self.proxy = QSortFilterProxyModel()

        self.proxy.setSourceModel(self.model)
        #give the proxy model a source
        
        location_column = self.model.fieldIndex("name")
        #where to search
        self.proxy.setFilterKeyColumn(location_column)
        # filter by the location column in the SQLite-backed model
        
        self.proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive) 
        #make filter case insensitive
        self.searchBar.textChanged.connect(lambda: self.search())
        #upon search bar being typed, activate search  

        self.studentsData.setModel(self.proxy)
        #give proxy to view

        studentsDataLayout.addWidget(self.studentsData)
        #add view to layout

        self.mainLayout.addLayout(studentsDataLayout)
        #add layout to main layout

    def add_Tool(self):
        newToolData = []

        for entry in self.entries:
            newToolData.append(entry.text())
            #add all entries to a list

        self.model.add_row(newToolData)
        #add list to table

           # Student cert selection
        if self.certBox.currentIndex() != -1:                       # if something is selected                 
            index = self.certBox.currentIndex()                     # save the index 
            if index == 1:                                      
                newToolData.append("🛠️")                        # if tools is selected, add the tool icon
                print("tool")
            elif index == 2:
                newToolData.append("❇️Lazer")                         # if laser cutter/engravr is selected, add the lzr icon
                print("lzr")
            elif index == 3:
                newToolData.append("🧊")                       # if the 3D print icon is selected, add the 3D print icon
                print("print")
            else:
                newToolData.append("❌")                           # if none/nothing is selected, add None
    
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
        textBoxes = ["Tool Name", "Quantity", "Tool Condition"]
        #the text to reset them to

        for entryItem, text in zip(self.entries, textBoxes):
            entryItem.setPlaceholderText(text)

    def search(self):
    #search function
        self.proxy.setFilterFixedString(self.searchBar.text())
        #just grabs text in search bar, searches for it


    def get_path(self, filename):
        basedir = os.path.dirname(__file__)         # gets the absolute path of the .png's for the icons in certBox
        return os.path.join(basedir, filename)
    



if __name__ == '__main__':
    app = QApplication(sys.argv)

    dataModel = tableModel("tools_app")

    # create the main window
    window = myTools(dataModel)

    # start the event loop
    sys.exit(app.exec())
