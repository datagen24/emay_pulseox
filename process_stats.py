import csv
import hashlib
import os
import sqlite3
from datetime import datetime

# Define the folder containing the CSV files
folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")

# Define the name and location of the SQLite database file
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pulseox.db")

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the tables if they don't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS session (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    filename TEXT,
    checksum TEXT,
    start_time TEXT,
    start_date TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS spo2_pr (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    timestamp TEXT,
    spo2 INTEGER,
    pr INTEGER,
    FOREIGN KEY (session_id) REFERENCES session(session_id)
)
''')

# Get the list of CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Loop over each CSV file and import the data into the database
for filename in csv_files:
    # Check if the file has been previously imported
    with open(os.path.join(folder_path, filename), 'rb') as f:
        file_contents = f.read()
        checksum = hashlib.sha256(file_contents).hexdigest()
    cursor.execute("SELECT COUNT(*) FROM session WHERE checksum=?", (checksum,))
    count = cursor.fetchone()[0]
    if count > 0:
        print(f"{filename} has already been imported.")
        continue
    
    # Extract the start time and date from the file
    with open(os.path.join(folder_path, filename), newline='') as f:
        reader = csv.reader(f)
        # Skip the header
        next(reader)
        # Get the start time and date from the first row
        row = next(reader)
        date_str, time_str, spo2, pr = row
        timestamp_str = f"{date_str} {time_str}"
        timestamp = datetime.strptime(timestamp_str, "%m/%d/%Y %I:%M:%S %p")
        start_time = timestamp.strftime("%H:%M:%S")
        start_date = timestamp.strftime("%Y-%m-%d")
    
    # Generate the session ID based on the start time, start date, and checksum
    session_id = f"{start_date}_{start_time}_{checksum}"
    
    # Insert the session data into the session table
    cursor.execute("INSERT INTO session (session_id, filename, checksum, start_time, start_date) VALUES (?, ?, ?, ?, ?)", (session_id, filename, checksum, start_time, start_date))
    
    # Read the CSV file and insert the SpO2 and PR values into the spo2_pr table
    with open(os.path.join(folder_path, filename), newline='') as f:
        reader = csv.reader(f)
        # Skip the header
        next(reader)
        for row in reader:
            # Check if the row has the expected number of columns
            if len(row) != 4:
                print(f"Skipping row in {filename} due to incorrect number of columns: {row}")
                continue
            date_str, time_str, spo2, pr = row
            timestamp_str = f"{date_str} {time_str}"
            timestamp = datetime.strptime(timestamp_str, "%m/%d/%Y %I:%M:%S %p")
    timestamp_iso = timestamp.isoformat()
    cursor.execute("INSERT INTO spo2_pr (session_id, timestamp, spo2, pr) VALUES (?, ?, ?, ?)", (session_id, timestamp_iso, spo2, pr))
    conn.commit()
    print(f"Data for {filename} has been imported.")

print("All data has been imported successfully.")
