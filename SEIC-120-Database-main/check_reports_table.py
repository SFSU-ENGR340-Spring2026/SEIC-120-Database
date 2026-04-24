import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "database.sqlite3"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("DELETE FROM reports_app WHERE name = ?", ("Kwa",))

conn.commit()
print("Rows deleted:", cur.rowcount)

conn.close()