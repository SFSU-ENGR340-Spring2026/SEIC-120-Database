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
    QMessageBox
)


import csv

class MyTableWidget(QWidget):
    def __init__(self, filename, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.filename = filename
        self.items = []
        self.headers = []

        #create the table
        self.table = QTableWidget(self)

        self.loadCSV(str(self.filename))

        # print(self.headers)
        rows = len(self.items)
        col = len(self.headers)
        
        # print(self.items)

        # set the window title
        self.setWindowTitle('Table test')
        self.setGeometry(100, 100, 1000, 700)    #set window size

        #set the layout
        mainLayout = QVBoxLayout(self)
        self.setLayout(mainLayout)
        
        # print(f"Item count is: {rows}")
        # print(f"Column count is: {col}")

        self.table.setRowCount(rows)
        self.table.setColumnCount(col)
        
        self.table.setHorizontalHeaderLabels(self.headers)

        for i, row in enumerate(self.items):
        #grabs item no. and row
            for z, values in enumerate(row):
                self.table.setItem(i, z, QTableWidgetItem(values))
        
        #resize to content
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

        #create a button
        button1 = QPushButton()
        button1.clicked.connect(self.button1_clicked)
        button1.setText("Load")

        button2 = QPushButton()
        button2.clicked.connect(self.button2_clicked)
        button2.setText("Save")
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(button1)
        buttonLayout.addWidget(button2)

        #add table to layout
        mainLayout.addWidget(self.table)
        mainLayout.addLayout(buttonLayout)

        """ print("table visible?", self.table.isVisible())
        print("table size:", self.table.size())
        print("geometry:", self.table.geometry())
        print("layout on window:", self.layout())
         """
        
        #remove ability to edit table directly
        # self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # show the window
        self.show()
    
    def currentButton_clicked(self):
    #find and print item at x,y pos in table
        print("clicked!")
        
        print(f"item at 0,0 is {str(self.table.item(1,1))}")

        currentQTableWidgetItem = self.table.currentItem()
        print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
    
    def button1_clicked(self):
        self.loadCSV(self.filename)
        QMessageBox.information(self, "Loaded", "CSV Loaded.")

    def button2_clicked(self):
        self.saveCSV(self.filename)
        QMessageBox.information(self, "Saved", "Table saved to CSV.")
    
    def loadCSV(self, fileName):
        t = 0
        with open(fileName, "r", newline="", encoding="utf-8") as fileInput:
            reader = csv.reader(fileInput)
            rows = list(reader)
            self.headers = rows[0]
            self.items = rows[1:]

        self.table.clear()
        self.table.setRowCount(len(self.items))
        self.table.setColumnCount(len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)

        for row_index, row_data in enumerate(self.items):
            for col_index, value in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(value))       
    
    def saveCSV(self, fileName):
        with open(fileName, "w", newline="", encoding="utf-8") as fileOutput:
            writer = csv.writer(fileOutput)
            writer.writerow(self.headers)

            for row in range(self.table.rowCount()):
                row_data = []
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    row_data.append(item.text() if item else "")
                writer.writerow(row_data)

    def addRow(self, items):
    #helper function to add a row, and populate it
        rowPos = self.table.rowCount()
        self.table.insertRow(rowPos)
        #count the rows and add a blank one

        #for the items in the list of data, fill each row with that
        for colPos, colData in enumerate(items):
            self.table.setItem(rowPos, colPos, QTableWidgetItem(colData))

    def delRow(self):
    #function to delete entire selected row
        currItem = self.table.currentItem()
        self.table.removeRow(currItem.row())

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create the main window
    window = MyTableWidget("sampleData.csv")

    # start the event loop
    sys.exit(app.exec())

    """ import sys
    from PyQt6.QtGui import QColor
    from PyQt6.QtWidgets import (QApplication, QTableWidget,
                               QTableWidgetItem)
    
    colors = [("Red", "#FF0000"),
          ("Green", "#00FF00"),
          ("Blue", "#0000FF"),
          ("Black", "#000000"),
          ("White", "#FFFFFF"),
          ("Electric Green", "#41CD52"),
          ("Dark Blue", "#222840"),
          ("Yellow", "#F9E56d")]
    
    def get_rgb_from_hex(code):
        code_hex = code.replace("#", "")
        rgb = tuple(int(code_hex[i:i+2], 16) for i in (0, 2, 4))
        return QColor.fromRgb(rgb[0], rgb[1], rgb[2])
    
    app = QApplication(sys.argv)

    table = QTableWidget()
    table.setRowCount(len(colors))
    table.setColumnCount(len(colors[0]) + 1)
    table.setHorizontalHeaderLabels(["Name", "Hex Code", "Color"])

    for i, (name, code) in enumerate(colors):
        item_name = QTableWidgetItem(name)
        item_code = QTableWidgetItem(code)
        item_color = QTableWidgetItem()
        item_color.setBackground(get_rgb_from_hex(code))
        table.setItem(i, 0, item_name)
        table.setItem(i, 1, item_code)
        table.setItem(i, 2, item_color)

    table.show()
    sys.exit(app.exec()) """