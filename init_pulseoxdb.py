import sqlite3

# Define the name and location of the SQLite database file
db_path = "pulseox.db"

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the tables
cursor.execute('''
CREATE TABLE session (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    filename TEXT,
    checksum TEXT,
    start_time TEXT,
    start_date TEXT
)
''')

cursor.execute('''
CREATE TABLE spo2_pr (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    timestamp TEXT,
    spo2 INTEGER,
    pr INTEGER,
    FOREIGN KEY (session_id) REFERENCES session(session_id)
)
''')

cursor.execute('''
CREATE TABLE session_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    odi_3 REAL,
    odi_4 REAL,
    time_below_94 REAL,
    time_below_89 REAL,
    num_89_dips INTEGER,
    recovery_time REAL,
    FOREIGN KEY (session_id) REFERENCES session(session_id)
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database initialized.")
