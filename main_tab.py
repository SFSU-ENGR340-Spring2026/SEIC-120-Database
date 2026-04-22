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
from spaces_tab import myTables
from tool_tab import myTools
from reports_tab import myReports

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'SEIC 120 Database'
        self.left = 0
        self.top = 0
        self.width = 600
        self.height = 400
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.table_widget = TableWidget(self)
        self.setCentralWidget(self.table_widget)
        
        self.show()
    
class TableWidget(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()

        #create the tabs
        self.tab1 = myDashboard((studentsModel, notesModel, toolsModel)
)
        self.tab2 = myTables()
        self.tab3 = myStudents()
        self.tab4 = myTools()
        self.tab5 = myReports()
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