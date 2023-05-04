import sqlite3
import os
from datetime import datetime
from generate_statistics import generate_statistics

# Define the name and location of the SQLite database file
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pulseox.db")

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get the list of session IDs from the session table
cursor.execute("SELECT session_id FROM session")
session_ids = [row[0] for row in cursor.fetchall()]

# Loop over each session and generate a report
for session_id in session_ids:
    # Get the session data from the session table
    cursor.execute("SELECT filename, start_time, start_date FROM session WHERE session_id=?", (session_id,))
    filename, start_time, start_date = cursor.fetchone()

    # Generate the statistics for the session
    duration_hours, time_below_94_hours, time_below_94_percent, time_below_89_hours, time_below_89_percent, num_dips = generate_statistics(session_id)

    # Generate the report
    report = f"Session ID: {session_id}\n"
    report += f"Filename: {filename}\n"
    report += f"Start Time: {start_time}\n"
    report += f"Start Date: {start_date}\n"
    report += f"Duration: {duration_hours:.2f} hours\n"
    report += f"Time Spent Below 94%: {time_below_94_hours:.2f} hours ({time_below_94_percent:.2f}% of total time)\n"
    report += f"Time Spent Below 89%: {time_below_89_hours:.2f} hours ({time_below_89_percent:.2f}% of total time)\n"
    report += f"Number of Dips: {num_dips}\n"
    report += "\n"

    # Print the report
    print(report)

conn.close()
