#students tab
#add/remove students
#display the table

import sys
import os
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
    QDialog,
    QCheckBox,
    

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
        addBtn.setText("Confirm")
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


        #add widgets to layout
        changeStudentsLayout.addWidget(self.stuIDLine)
        changeStudentsLayout.addWidget(self.nameLine)
        changeStudentsLayout.addWidget(self.certBox)
        changeStudentsLayout.addWidget(addBtn)
        changeStudentsLayout.addWidget(delBtn)

        #search bar
        searchLayout = QHBoxLayout()               # layout created under changeStedentsLayout
        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Search for student ID or Name")

        updateBtn = QPushButton()
        updateBtn.setText("Update Student")
        updateBtn.clicked.connect(self.openUpdateStu)       # if update button is clicked, open updateStu

        searchLayout.addWidget(self.searchBar)      # add to the searchLayout
        searchLayout.addWidget(updateBtn)


        #add to main layout
        self.mainLayout.addLayout(changeStudentsLayout)
        self.mainLayout.addLayout(searchLayout)     # add to main layout
     

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

    def get_path(self, filename):
        basedir = os.path.dirname(__file__)         # gets the absolute path of the .png's for the icons in certBox
        return os.path.join(basedir, filename)

    def add_student(self):
        self.newToolData = []

        for entry in self.entries:
            self.newToolData.append(entry.text())
            #add all entries to a list
        
        self.newToolData.append("None")                 # tools column
        self.newToolData.append("None")                 # location column


        # Student cert selection
        if self.certBox.currentIndex() != -1:                       # if something is selected                 
            index = self.certBox.currentIndex()                     # save the index 
            if index == 1:                                      
                self.newToolData.append("🛠️")                        # if tools is selected, add the tool icon
                # print("tool")
            elif index == 2:
                self.newToolData.append("❇️")                         # if laser cutter/engravr is selected, add the lzr icon
                # print("lzr")
            elif index == 3:
                self.newToolData.append("🧊")                       # if the 3D print icon is selected, add the 3D print icon
                # print("print")
            else:
                self.newToolData.append("❌")                           # if none/nothing is selected, add None

           

        #needs 4 entries to enter into db, default to none for new student
        
        self.studModel.add_row(self.newToolData)
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

    def get_source_row(self, view, model, proxy):
    # given a view, model, and proxy, find the source row of the currently cliked on views row
    # returns row number in source model, and record: all values in that row
        proxy_index = view.currentIndex()
        #find the index of the view
        source_index = proxy.mapToSource(proxy_index)
        #find index of source model
        source_row = source_index.row()
        #use that to find the row at source index
        record = model.record(source_index.row())
        #get all the data at that row

        return source_row, record

    def openUpdateStu(self):            # method to open the update student pop up
        
        sourceRow, record = self.get_source_row(self.studentsData, self.studModel, self.proxy)
        #source row is row # in source model (meaning the correct one)
        #record is the list of values in that row

        update = updateStu(self.studentsData, self.studModel, record)
        certUpdate = update.getCert()       # check to see which cert was clicked in pop up

        idUpdate = update.getIDChange()     # check to see if ID was changed. cont. in line 247
        print(certUpdate)

        nameUpdate = update.getNameChange() # check to see if the stu name was changed
        print(nameUpdate)

        
        if update.exec():
            certUpdate = update.getCert()       # check to see which cert was clicked in pop up
            print(certUpdate)

            idUpdate = update.getIDChange()     
            print(idUpdate)

            nameUpdate = update.getNameChange()
            print(nameUpdate)

            # Certification Update
            updatedCerts = ""
            if certUpdate.get("tool") == True:         # returned in updateStu method getCert
                updatedCerts = f"{updatedCerts}🛠️"
                # print("+tool")

            if certUpdate.get("laser") == True:
                updatedCerts = f"{updatedCerts}❇️"
                # print("+lzr")

            if certUpdate.get("printer") == True:
                updatedCerts = f"{updatedCerts}🧊"
                # print("+printer")

            self.studModel.change_value(sourceRow, "certs", str(updatedCerts))

            # ID Change
            updatedID = ""                                      
            if idUpdate != "=ID":                                       # if the id was updated
                updatedID = idUpdate                                    # add that too updated id
            else:
                updatedID = str(record.value("id"))

            self.studModel.change_value(sourceRow, "id", updatedID)  # change it 


            # Name Chage
            updatedName = ""
            if nameUpdate != "=Name":
                updatedName = nameUpdate
            else:
                updatedName = str(record.value("name"))

            self.studModel.change_value(sourceRow, "name", updatedName)
            

       




class updateStu(QDialog):               # pop up for updating a student    
    def __init__(self, view, model, record, parent = None):
        super().__init__(parent)

        self.setWindowTitle("Update Student")
        self.setFixedSize(300, 250)

        layout = QVBoxLayout(self)
        topLayout = QHBoxLayout()
        bottomLayout = QHBoxLayout()

        # text boxes
        self.stuIDLine = QLineEdit()
        self.stuIDLine.setPlaceholderText("Enter Student ID Number")

        view.currentIndex()
        #find row
        #use row to find data at student ID
        self.stuIDLine.setText(f"{record.value("id")}")            # populate id entry box with the selected student ID
        self.oldID = str(record.value("id"))

        self.stuNameLine = QLineEdit()
        self.stuNameLine.setPlaceholderText("Enter Student Name") 

        self.stuNameLine.setText(f"{record.value("name")}")        # populate student name in stu name entry box with selected student 
        self.oldName = str(record.value("name"))

        topLayout.addWidget(self.stuIDLine)
        topLayout.addWidget(self.stuNameLine)
        layout.addLayout(topLayout)


        # Cert Group
        cert_group = QGroupBox("Student Certifications")
        cert_layout = QVBoxLayout()

        self.toolCertBox = QCheckBox("🛠️ Hand Tools")

        self.lzrCertBox = QCheckBox("Laser Cutter/Engraver")
        self.lzrCertBox.setIcon(QIcon("lzr_icon.png"))

        self.printerCertBox = QCheckBox("3D Printer")
        self.printerCertBox.setIcon(QIcon("3D_print_icon.png"))

        cert_layout.addWidget(self.toolCertBox)
        cert_layout.addWidget(self.lzrCertBox)
        cert_layout.addWidget(self.printerCertBox)

        cert_group.setLayout(cert_layout)
        layout.addWidget(cert_group)


        
        # buttons
        applyBtn = QPushButton("Apply")
        cancelBtn = QPushButton("Cancel")

        applyBtn.clicked.connect(self.accept)
        cancelBtn.clicked.connect(self.reject)

        bottomLayout.addWidget(applyBtn)
        bottomLayout.addWidget(cancelBtn)

        layout.addLayout(bottomLayout)

    def getCert(self):
# Cert Check box selection
        return { 
            # check what cert is selected
            "tool": self.toolCertBox.isChecked(),
            "laser": self.lzrCertBox.isChecked(),
            "printer": self.printerCertBox.isChecked()
        }
    
    def getIDChange(self):
        self.newID = self.stuIDLine.text()

        if self.newID == self.oldID:      # if current id is the same as old id
            return("=ID")     
        else:                   # if the current id is NOT the same as the old ID
            return(self.newID)
        
    
    def getNameChange(self):
        self.newName = self.stuNameLine.text()

        if self.newName == self.oldName:
            return("=Name")
        else:
            return(self.newName)
            

    
if __name__ == '__main__':

    app = QApplication(sys.argv)

    model = tableModel("students_app")

    # create the main window
    window = myStudents(model)

    # start the event loop
    sys.exit(app.exec())