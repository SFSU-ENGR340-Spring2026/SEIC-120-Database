# Hold all of the tabs, the combined UI 
#tab tests

import sys
from PyQt6.QtWidgets import (
    QMainWindow, 
    QApplication, 
    QPushButton, 
    QWidget, 
    QTabWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSlot
import csv
from table_model import tableModel as dataTable

from student_tab import myStudents
from dashboard_tab import myDashboard
from spaces_tab import mySpaces
from tool_tab import myTools
from reports_tab import myReports

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'SEIC 120 Database'
        self.left = 0
        self.top = 0
        width = 600
        height = 400
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, width, height)
        
        self.table_widget = TableWidget(self)
        self.setCentralWidget(self.table_widget)
        
        self.show()
    
class TableWidget(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()

        #create models
        studModel = dataTable("students_app")
        noteModel = dataTable("reports_app")
        spacesModel = dataTable("spaces_app")
        toolModel = dataTable("tools_app")

        #create the tabs
        self.tab1 = myDashboard(studModel, noteModel, toolModel)   #3 models: students, notes, and tools
        self.tab2 = mySpaces(spacesModel)      #1 model: spaces
        self.tab3 = myStudents(studModel)    #1 model: students
        self.tab4 = myTools(toolModel)       #1 model: tools
        self.tab5 = myReports(noteModel)     #1 model: notes
        # self.tabs.resize(300,200)
        
        # Add tabs to the tabs widget
        self.tabs.addTab(self.tab1,"Dashboard")
        self.tabs.addTab(self.tab2,"Table")
        self.tabs.addTab(self.tab3, "Students")
        self.tabs.addTab(self.tab4, "Tools")
        self.tabs.addTab(self.tab5, "Reports")

        #add the tabs to the layout
        self.layout.addWidget(self.tabs)
        self.setGeometry(100, 100, 1200, 800)
        self.setLayout(self.layout)

        self.show()
        

    @pyqtSlot()
    def on_click(self):
        print("\n")
        currentQTableWidgetItem = self.table.table.currentItem()
        print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
