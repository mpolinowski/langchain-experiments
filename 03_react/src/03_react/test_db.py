import sqlite3
from pathlib import Path

db_path = Path('src/03_react/db/events.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# create camera event table
cursor.execute('''
    SELECT * FROM events
''')
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.commit()
conn.close()
