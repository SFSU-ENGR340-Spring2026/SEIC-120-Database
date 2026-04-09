#table tests

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
    QGroupBox
)

from tables import MyTableWidget


import csv

class myDashboard(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #create main layout
        self.mainLayout = QHBoxLayout(self)

        #create table layout
        self.create_layout("Who's currently In?", "sampleStudents.csv")

        #create note layout
        self.create_layout("Student Notes: ", "sampleEvents.csv")

        #create tool layout
        self.create_layout("Available Tools: ", "sampleData.csv")

        self.setLayout(self.mainLayout)

        self.setGeometry(100, 100, 1000, 700)
        
        # show the window
        self.show()
    
    def create_layout(self, textBox, tableName):
        layout = QVBoxLayout()

        header = QLineEdit()
        header.setText(textBox)
        header.setReadOnly(True)
        layout.addWidget(header)

        data = MyTableWidget(tableName)
        layout.addWidget(data)

        self.mainLayout.addLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create the main window
    window = myDashboard()

    # start the event loop
    sys.exit(app.exec())