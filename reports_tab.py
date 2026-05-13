# Reports
# Search students history
# Display the table

import sys
import csv

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
    QCheckBox,
    QTextEdit
)

from table_model import tableModel
from datetime import datetime


class myReports(QWidget):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create main layout
        self.mainLayout = QVBoxLayout(self)

        # Create model/table view
        self.model = model
        self.studentsData = QTableView()
        self.studentsData.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.studentsData.setModel(self.model)

        # self.model.setFilter("tool_name = 'Report'")
        # self.model.select()

        # Hide report_id column
        self.studentsData.hideColumn(self.model.fieldIndex("note_id"))
        self.studentsData.hideColumn(self.model.fieldIndex("temp"))

        # Layout for search/buttons
        changeStudentsLayout = QHBoxLayout()

        # Pull button
        pullBtn = QPushButton()
        pullBtn.setText("Pull")
        pullBtn.clicked.connect(self.pull_reports)

        # Filter button
        filterBtn = QPushButton()
        filterBtn.setText("Filters")
        filterBtn.clicked.connect(self.openFilters)

        # Make report button
        reportBtn = QPushButton()
        reportBtn.setText("Make Student Report")
        reportBtn.clicked.connect(self.openMakeReport_dialog)

        # Place to enter student ID
        self.entryLine = QLineEdit()
        self.entryLine.setPlaceholderText("Enter Student ID")

        # Add widgets to top layout
        changeStudentsLayout.addWidget(self.entryLine)
        changeStudentsLayout.addWidget(pullBtn)
        changeStudentsLayout.addWidget(filterBtn)
        changeStudentsLayout.addWidget(reportBtn)

        # Add top layout to main layout
        self.mainLayout.addLayout(changeStudentsLayout)

        # Stretch table columns
        self.studentsData.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Table layout
        studentsDataLayout = QVBoxLayout()
        studentsDataLayout.addWidget(self.studentsData)

        self.mainLayout.addLayout(studentsDataLayout)

        # Set layout
        self.setLayout(self.mainLayout)

        # Window size
        self.setGeometry(100, 100, 1000, 700)

        # Show window
        self.show()

    def openFilters(self):
        dialog = filter_dialog(self)

        if dialog.exec():
            filters = dialog.getFilters()
            print(filters)

    def openMakeReport_dialog(self):
        reporting = makeReport_dialog(self)

        if reporting.exec():
            report = reporting.getConfirmReport()
            print(report)

            if report == "Report Created.":
                student_id, name, report_text = reporting.getReportData()

                self.add_report(
                    student_id,
                    name,
                    None,
                    None,
                    None,
                    None,
                    report_text
                )

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setText("Report Created.")
                msg.setWindowTitle("Confirmed")
                msg.exec()

            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setText("Please Enter Information.")
                msg.setWindowTitle("Denied")
                msg.exec()

    def add_report(self, student_id, name, time, machinery, table_name, tools, notes):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.model.add_row([
            student_id,
            "Report",
            "None",
            notes,
            timestamp,
            0
        ])

        self.model.select()


    def pull_reports(self):
        student_id = self.entryLine.text().strip()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not student_id:
            self.model.setFilter("")
            self.model.select()
            return

        if not student_id.isdigit():
            QMessageBox.warning(self, "Invalid ID", "Please enter a numeric student ID.")
            return

        self.model.load_reports_by_student(student_id)

    def create_layout(self, layoutName, textBox):
        layout = QVBoxLayout()

        header = QLineEdit()
        header.setText(textBox)
        header.setReadOnly(True)
        layout.addWidget(header)

        data = QTableWidget()
        layout.addWidget(data)

        self.mainLayout.addLayout(layout)


class makeReport_dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Make Student Report")
        self.setFixedSize(500, 700)

        layout = QVBoxLayout(self)
        topLayout = QHBoxLayout()

        # Student ID input
        self.stuIDLine = QLineEdit()
        self.stuIDLine.setPlaceholderText("Enter Student ID Number")

        # Student name input
        self.stuNameLine = QLineEdit()
        self.stuNameLine.setPlaceholderText("Enter Student Name")

        topLayout.addWidget(self.stuIDLine)
        topLayout.addWidget(self.stuNameLine)

        layout.addLayout(topLayout)

        # Report text box
        self.stuReport = QTextEdit()
        self.stuReport.setPlaceholderText("Enter Student Report")
        layout.addWidget(self.stuReport, 1)

        # Buttons
        btnLayout = QHBoxLayout()

        submitBtn = QPushButton("Submit")
        cancelBtn = QPushButton("Cancel")

        submitBtn.clicked.connect(self.accept)
        cancelBtn.clicked.connect(self.reject)

        btnLayout.addWidget(submitBtn)
        btnLayout.addWidget(cancelBtn)

        layout.addLayout(btnLayout)

    def getConfirmReport(self):
        if self.stuIDLine.text().strip() and self.stuReport.toPlainText().strip():
            return "Report Created."
        else:
            return "Please fill in information."

    def getReportData(self):
        student_id = self.stuIDLine.text().strip()
        name = self.stuNameLine.text().strip()
        report_text = self.stuReport.toPlainText().strip()

        return student_id, name, report_text


class filter_dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Apply Filters")
        self.setFixedSize(500, 700)

        layout = QVBoxLayout(self)


        # group boxes

        # # Tools Group
        # tool_group = QGroupBox("Tools")                 # Create Group box for tools   
        # tool_layout = QVBoxLayout()                     # Create VERTICAL layout for tool layout

        # self.screwdriverBox = QCheckBox("Screwdriver")       # create check box
        # self.hammerBox = QCheckBox("Hammer")
        # tool_layout.addWidget(self.screwdriverBox)           # add checkbox to grup
        # tool_layout.addWidget(self.hammerBox)

        # tool_group.setLayout(tool_layout)               # add layout to group
        # layout.addWidget(tool_group)                    # add tool group to main pop up layout

        # Tables Group
        spaces_group = QGroupBox("Tables")
        spaces_layout = QHBoxLayout()

        # Section A
        layoutA = QVBoxLayout()

        self.tableA1Box = QCheckBox("A1")
        self.tableA2Box = QCheckBox("A2")
        self.tableA3Box = QCheckBox("A3")
        self.tableA4Box = QCheckBox("A4")
        self.tableA5Box = QCheckBox("A5")

        layoutA.addWidget(self.tableA1Box)
        layoutA.addWidget(self.tableA2Box)
        layoutA.addWidget(self.tableA3Box)
        layoutA.addWidget(self.tableA4Box)
        layoutA.addWidget(self.tableA5Box)

        # Section B
        layoutB = QVBoxLayout()

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

        # Section C
        layoutC = QVBoxLayout()

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

        # Section D
        layoutD = QVBoxLayout()

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

        # Section E
        layoutE = QVBoxLayout()

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

        # Section F
        layoutF = QVBoxLayout()

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

        # Add sections to table layout
        spaces_layout.addLayout(layoutA)
        spaces_layout.addLayout(layoutB)
        spaces_layout.addLayout(layoutC)
        spaces_layout.addLayout(layoutD)
        spaces_layout.addLayout(layoutE)
        spaces_layout.addLayout(layoutF)

        spaces_group.setLayout(spaces_layout)
        layout.addWidget(spaces_group)

        # Choice buttons
        btnLayout = QHBoxLayout()

        applyBtn = QPushButton("Apply")
        cancelBtn = QPushButton("Cancel")

        applyBtn.clicked.connect(self.accept)
        cancelBtn.clicked.connect(self.reject)

        btnLayout.addWidget(applyBtn)
        btnLayout.addWidget(cancelBtn)

        layout.addLayout(btnLayout)

    def getFilters(self):
        return {
          
            # # tools
            # "Screwdriver": self.screwdriverBox.isChecked(),
            # "Hammer:": self.hammerBox.isChecked(),

            # Spaces
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

            "F1": self.tableF1Box.isChecked(),
            "F2": self.tableF2Box.isChecked(),
            "F3": self.tableF3Box.isChecked(),
            "F4": self.tableF4Box.isChecked(),
            "F5": self.tableF5Box.isChecked(),
        }


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create the model using reports_app
    dataModel = tableModel("notes_app")

    # Create the reports window
    window = myReports(dataModel)

    # Start the event loop
    sys.exit(app.exec())