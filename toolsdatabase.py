import sqlite3
import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "tools.sqlite3")
CSV_PATH = os.path.join(BASE_DIR, "tools.csv")


class Tool:
    def __init__(self, id, level, quantity, location, name, category):
        self.id = id
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


class HighLevel(Tool):
    pass


class LowLevel(Tool):
    pass


def createTable():
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

    conn.commit()
    conn.close()

def exportToCSV():
    conn = sqlite3.connect("tools.sqlite3")
    cur = conn.cursor()

    cur.execute("SELECT * FROM tools")
    rows = cur.fetchall()

    with open("tools.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([description[0] for description in cur.description])
        writer.writerows(rows)

    conn.close()
    print("CSV exported successfully.")

def addTool():
    id = input("ID: ")
    level = input("Level: ")
    quantity = int(input("Quantity: "))
    location = input("Location: ")
    name = input("Name: ")
    category = input("Category: ")

    new_tool = Tool(level, quantity, location, name, category)

    conn = sqlite3.connect("tools.sqlite3")
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO tools (id, level, quantity, location, name, category)
    VALUES (?, ?, ?, ?, ?)
    """, (new_tool.id, new_tool.level, new_tool.quantity, new_tool.location, new_tool.name, new_tool.category))

    conn.commit()
    exportToCSV()
    conn.close()


    print("Tool added successfully.")

def searchTool():
    conn = sqlite3.connect("tools.sqlite3")
    cur = conn.cursor()

    tool_name = input("Enter the tool name to search: ")

    cur.execute("SELECT quantity FROM tools WHERE name = ?", (tool_name,))
    result = cur.fetchone()

    if result:
        print(f"You have {result[0]} {tool_name}(s).")
    else:
        print("Tool not found")
    
    conn.close()

def removeTool():
    conn = sqlite3.connect("tools.sqlite3")
    cur = conn.cursor()

    tool_name = input("Enter the tool name to delete: ")

    cur.execute("DELETE FROM tools WHERE name = ?", (tool_name,))
    conn.commit()
    exportToCSV()

    if cur.rowcount > 0:
        print(f"{tool_name} removed successfully.")
    else:
        print("Tool not found")
    
    conn.close()

def showTools():
    conn = sqlite3.connect("tools.sqlite3")
    cur = conn.cursor()

    cur.execute("SELECT * FROM tools")
    rows = cur.fetchall()

    for row in rows:
        print(row)

    conn.close()

def changeQuantity():
    conn = sqlite3.connect("tools.sqlite3")
    cur = conn.cursor()

    cur.execute("SELECT * FROM tools")
    rows = cur.fetchall()

    for row in rows:
        print(row)

    conn.close()


createTable()

while True:
    addTool()
    again = input("Add another tool? (y/n): ")
    if again.lower() != "y":
        break

removeTool()
searchTool()
showTools()
exportToCSV()
