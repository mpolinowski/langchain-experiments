import sqlite3
from pathlib import Path

db_path = Path('src/03_react/db/events.db')
db_path.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# create camera event table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TEXT NOT NULL,
        name TEXT NOT NULL,
        trigger TEXT NOT NULL,
        face_ids INTEGER NOT NULL,
        license_plate TEXT NOT NULL
    )
''')

# create camera event data
cursor.execute('''
    INSERT INTO events (time, name, trigger, face_ids, license_plate) VALUES
    ('Mon Oct 12 06:39:16 AM HKT 2026', 'Motion Detected', 'Motion Area 1', 0, 'SU:GB:678'),
    ('Mon Oct 13 06:39:16 AM HKT 2026', 'Motion Detected', 'Motion Area 2', 1, 'None'),
    ('Mon Oct 14 06:39:16 AM HKT 2026', 'Motion Detected', 'Motion Area 3', 34, 'None'),
    ('Mon Oct 15 06:39:16 AM HKT 2026', 'Motion Detected', 'Motion Area 4', 0, 'SU:RT:22')
''')

conn.commit()
conn.close()
