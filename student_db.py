import sqlite3
import csv

certs = {
    0 : "⚫️⚫️⚫️",
    1 : "⚫️⚫️🟢",
    2 : "⚫️🟢⚫️",
    3 : "⚫️🟢🟢",
    4 : "🟢⚫️⚫️",
    5 : "🟢⚫️🟢",
    6 : "🟢🟢⚫️",
    7 : "🟢🟢🟢"
}

class student:
    def __init__(self, id, name, certifications=0):
        self.id = id
        self.name = name
        # certification level is an integer value
        # 0 : no certs
        # 1 : hand tools only
        # 2 : 3d printer only
        # 3 : hand tools and 3d printer
        # 4 : laser cutter only
        # 5 : hand tools and laser cutter
        # 6 : 3d printer and laser cutter
        # 7 : hand tools, 3d printer, and laser cutter
        self.cert = certifications

    def getID(self):
        print(self.id)

    def getName(self):
        print(self.name)
    
    def getCerts(self):
        print(certs.get(self.cert))


conn = sqlite3.connect("database.sqlite3")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    cert INTEGER
)
""")

student1 = student(555555555, "Ben Smith", 3)

cur.execute("""
INSERT INTO students (id, name, cert)
VALUES (?, ?, ?)
""", (student1.id, student1.name, student1.cert))

conn.commit()

cur.execute("SELECT * FROM students")
rows = cur.fetchall()

with open("students.csv", "w", newline= "", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([description[0] for description in cur.description])
    writer.writerows(rows)

for row in rows:
    print(row)

student1.getCerts()
