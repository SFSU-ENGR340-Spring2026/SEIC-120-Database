import sqlite3
import csv

class tool:
    def __init__(self, level, quantity, location, name, category):
        self.level = level
        self.quantity = quantity
        self.location = location
        self.name = name
        self.category = category

    def getLevel(self):
        print(self.level)

    def getQuantity(self):
        print(self.quantity)

    def toolLocation(self):
        print(self.location)

    def getName(self):
        print(self.name)


class highLevel(tool):
    pass


class lowLevel(tool):
    pass


conn = sqlite3.connect("tools.sqlite3")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS tools (
    id INTEGER PRIMARY KEY,
    level TEXT,
    quantity INTEGER,
    location TEXT,
    name TEXT,
    category TEXT
)
""")

tool1 = tool("high", 5, "Shelf A", "Hammer", "Hand Tool")

cur.execute("""
INSERT INTO tools (level, quantity, location, name, category)
VALUES (?, ?, ?, ?, ?)
""", (tool1.level, tool1.quantity, tool1.location, tool1.name, tool1.category))

conn.commit()

cur.execute("SELECT * FROM tools")
rows = cur.fetchall()

with open("tools.csv", "w", newline= "", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([description[0] for description in cur.description])
    writer.writerows(rows)

for row in rows:
    print(row)
