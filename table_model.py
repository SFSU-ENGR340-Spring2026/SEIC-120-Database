import csv
import sqlite3
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database.sqlite3"
CONNECTION_NAME = "seic_database"

TABLE_SPECS = {
    "students_app": {
        "aliases": {"sampleStudents.csv", "students_app"},
        "schema": """
            CREATE TABLE IF NOT EXISTS students_app (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                tool TEXT DEFAULT 'None',
                location TEXT DEFAULT 'None',
                certs TEXT DEFAULT 'None'
            )
        """,
        "headers": ["ID", "Name", "Tools", "Location", "Certifications"],
        "editable_columns": ["id", "name", "tool", "location", "certs"],
        "seed_file": BASE_DIR / "sampleStudents.csv",
        "seed_columns": ["id", "name", "tool", "location", "certs"],
        "seed_transform": lambda row: (
            row.get("ID", "").strip(),
            row.get("Name", "").strip(),
            row.get("Tools", "").strip(),
            row.get("Location", "").strip(),
            row.get("Certifications", "").strip(),
        ),
    },
    "tools_app": {
        "aliases": {"sampleData.csv", "tools_app"},
        "schema": """
            CREATE TABLE IF NOT EXISTS tools_app (
                name TEXT PRIMARY KEY,
                current_quantity INTEGER,
                max_quantity INTEGER,
                certification TEXT
            )
        """,
        "headers": ["Tool", "Available Quantity", "Max Quantity", "Certification"],
        "editable_columns": ["name", "current_quantity", "max_quantity", "certification"],
        "seed_file": BASE_DIR / "sampleData.csv",
        "seed_columns": ["name", "current_quantity", "max_quantity", "certification"],
        "seed_transform": lambda row: (
            row.get("Tool", "").strip(),
            row.get("Available Quantity", "").strip(),
            row.get("Max Quantity", "").strip(),
            row.get("Certification", "").strip()
        ),
    },
    # "reports_app": {
    #     "aliases": {"sampleReports.csv", "reports_app"},
    #     "schema": """
    #         CREATE TABLE IF NOT EXISTS reports_app (
    #             name TEXT,
    #             time TEXT,
    #             machinery TEXT,
    #             table_name TEXT,
    #             tools TEXT,
    #             notes TEXT
    #         )
    #     """,
    #     "headers": ["Name", "Time", "Machinery", "Table", "Tools", "Notes"],
    #     "editable_columns": ["name", "time", "machinery", "table_name", "tools", "notes"],
    #     "seed_file": BASE_DIR / "sampleReports.csv",
    #     "seed_columns": ["name", "time", "machinery", "table_name", "tools", "notes"],
    #     "seed_transform": lambda row: (
    #         row.get("Name: ", "").strip(),
    #         row.get("Time:", "").strip(),
    #         row.get("Machinery:", "").strip(),
    #         row.get("Table:", "").strip(),
    #         row.get("Tools:", "").strip(),
    #         row.get("Notes:", "").strip(),
    #     ),
    # },
    "spaces_app": {
        "aliases": {"sampleTables.csv", "spaces_app"},
        "schema": """
            CREATE TABLE IF NOT EXISTS spaces_app (
                student_id TEXT,
                name TEXT,
                tool TEXT,
                location TEXT DEFAULT 'None'
            )
        """,
        "headers": ["Student ID", "Name", "Tool", "Location"],
        "editable_columns": ["student_id", "name", "tool", "location"],
        "seed_file": BASE_DIR / "sampleTables.csv",
        "seed_columns": ["student_id", "name", "tool", "location"],
        "seed_transform": lambda row: (
            row.get("StudentID", "").strip(),
            row.get("Name", "").strip(),
            row.get("Tool", "").strip(),
            "None",
        ),
    },
    "notes_app": {
        "aliases": {"sampleReports.csv","notesApp.csv", "notes_app"},
        "schema": """
            CREATE TABLE IF NOT EXISTS notes_app (
                note_id INTEGER PRIMARY KEY,
                student_id INTEGER NOT NULL,
                tool_name TEXT DEFAULT 'None',
                location TEXT DEFAULT 'None',
                note_text TEXT DEFAULT 'None',
                time TEXT DEFAULT 'None',
                temp INTEGER DEFAULT 1
            )
        """,
        "headers": ["Note ID", "Student ID", "Tool Name", "Location", "Note", "Time","Temporary"],
        "editable_columns": ["student_id", "tool_name", "location", "note_text", "time", "temp"],
        "seed_file": BASE_DIR / "sampleReports.csv",
        "seed_columns": ["note_id", "student_id", "tool_name", "location", "note_text", "time", "temp"],
        "seed_transform": lambda row: (
            row.get("Note ID", "").strip(),
            row.get("Student ID", "").strip(),
            row.get("Tool Name", "").strip(),
            row.get("Location", "").strip(),
            row.get("Note", "").strip(),
            row.get("Time", "").strip(),
            row.get("Temporary", "").strip(),
        ),
    },
}

SOURCE_TO_TABLE = {
    alias: table_name
    for table_name, spec in TABLE_SPECS.items()
    for alias in spec["aliases"]
}


def _resolve_table_name(source_name):
    try:
        return SOURCE_TO_TABLE[source_name]
    except KeyError as exc:
        valid_sources = ", ".join(sorted(SOURCE_TO_TABLE))
        raise ValueError(f"Unknown table source '{source_name}'. Expected one of: {valid_sources}") from exc


def _seed_table_if_empty(connection, table_name, spec):
    seed_file = spec["seed_file"]
    if not seed_file.exists():
        return

    cursor = connection.cursor()
    row_count = cursor.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    if row_count:
        return

    with seed_file.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = [spec["seed_transform"](row) for row in reader]

    if not rows:
        return

    placeholders = ", ".join("?" for _ in spec["seed_columns"])
    columns = ", ".join(spec["seed_columns"])
    cursor.executemany(
        f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})",
        rows,
    )
    connection.commit()


def initialize_database():
    connection = sqlite3.connect(DB_PATH)
    try:
        for table_name, spec in TABLE_SPECS.items():
            connection.execute(spec["schema"])
            _seed_table_if_empty(connection, table_name, spec)
    finally:
        connection.close()


def create_connection():
    initialize_database()

    if QSqlDatabase.contains(CONNECTION_NAME):
        db = QSqlDatabase.database(CONNECTION_NAME)
    else:
        db = QSqlDatabase.addDatabase("QSQLITE", CONNECTION_NAME)
        db.setDatabaseName(str(DB_PATH))

    if not db.isOpen() and not db.open():
        return None

    return db


class tableModel(QSqlTableModel):
    def __init__(self, source_name, parent=None):
        self.table_name = _resolve_table_name(source_name)
        self.spec = TABLE_SPECS[self.table_name]
        self.db = create_connection()
        if self.db is None:
            raise RuntimeError(f"Could not open SQLite database at {DB_PATH}")

        super().__init__(parent, self.db)
        self.setTable(self.table_name)
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

        if not self.select():
            raise RuntimeError(self.lastError().text())

        for column, header in enumerate(self.spec["headers"]):
            self.setHeaderData(column, Qt.Orientation.Horizontal, header)

    def add_row(self, values):
        if len(values) != len(self.spec["editable_columns"]):
            raise ValueError(
                f"Expected {len(self.spec['editable_columns'])} values for {self.table_name}, "
                f"received {len(values)}."
            )

        row = self.rowCount()
        if not self.insertRow(row):
            raise RuntimeError(self.lastError().text())

        for value, column_name in zip(values, self.spec["editable_columns"]):
            column_index = self.fieldIndex(column_name)
            self.setData(self.index(row, column_index), value)

        if not self.submitAll():
            self.revertAll()
            raise RuntimeError(self.lastError().text())

        self.select()

    def del_row(self, row):
        if row < 0 or row >= self.rowCount():
            return False

        if not self.removeRow(row):
            return False

        if not self.submitAll():
            self.revertAll()
            return False

        self.select()
        return True
    
    def change_value(self, row, colName, value):
        column_index = self.fieldIndex(colName)
        self.setData(self.index(row, column_index), value)

        if not self.submitAll():
            self.revertAll()
            raise RuntimeError(self.lastError().text())

        self.select()

    def find_row_by_value(self, colName, value):
        column_index = self.fieldIndex(colName)
        for row in range(self.rowCount()):
            if str(self.data(self.index(row, column_index))) == str(value):
                return row
        return -1

    def adjust_value(self, row, colName, delta, minimum=None, maximum=None):
        column_index = self.fieldIndex(colName)
        current_value = self.data(self.index(row, column_index))

        try:
            new_value = int(current_value) + int(delta)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Column '{colName}' does not contain an integer value.") from exc

        if minimum is not None:
            new_value = max(minimum, new_value)

        if maximum is not None:
            new_value = min(maximum, new_value)

        self.setData(self.index(row, column_index), new_value)

        if not self.submitAll():
            self.revertAll()
            raise RuntimeError(self.lastError().text())

        self.select()
        return new_value