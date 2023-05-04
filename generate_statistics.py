import sqlite3
from datetime import datetime

# Define the name and location of the SQLite database file
db_path = "pulseox.db"

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get the list of session IDs
cursor.execute("SELECT session_id FROM session")
session_ids = [row[0] for row in cursor.fetchall()]

# Calculate the statistics for each session
for session_id in session_ids:
    cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM spo2_pr WHERE session_id = ?", (session_id,))
    start_timestamp_str, end_timestamp_str = cursor.fetchone()
    if start_timestamp_str is None or end_timestamp_str is None:
        print(f"Skipping session {session_id} due to missing start or end timestamp.")
        continue
    start_timestamp = datetime.fromisoformat(start_timestamp_str)
    end_timestamp = datetime.fromisoformat(end_timestamp_str)
    duration_hours = (end_timestamp - start_timestamp).total_seconds() / 3600
    cursor.execute("SELECT COUNT(*) FROM spo2_pr WHERE session_id = ? AND spo2 < 94", (session_id,))
    time_below_94_seconds = cursor.fetchone()[0]
    time_below_94_hours = time_below_94_seconds / 3600
    time_below_94_percent = time_below_94_seconds / duration_hours * 100
    cursor.execute("SELECT COUNT(*) FROM spo2_pr WHERE session_id = ? AND spo2 < 89", (session_id,))
    time_below_89_seconds = cursor.fetchone()[0]
    time_below_89_hours = time_below_89_seconds / 3600
    time_below_89_percent = time_below_89_seconds / duration_hours * 100
    cursor.execute("SELECT COUNT(*) FROM spo2_pr WHERE session_id = ? AND spo2 < 89 AND spo2 >= 80", (session_id,))
    num_89_dips = cursor.fetchone()[0]
    cursor.execute("SELECT AVG(recovery_time) FROM (SELECT (strftime('%s', timestamp) - strftime('%s', prev_timestamp)) / 60.0 AS recovery_time FROM (SELECT timestamp, LAG(timestamp) OVER (ORDER BY timestamp) AS prev_timestamp FROM spo2_pr WHERE session_id = ? AND spo2 >= 94) WHERE prev_timestamp IS NOT NULL)", (session_id,))
    avg_recovery_time_minutes = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM spo2_pr WHERE session_id = ? AND spo2 < 80", (session_id,))
    num_80_dips = cursor.fetchone()[0]
    odi_3 = num_89_dips / duration_hours
    odi_4 = num_80_dips / duration_hours
    cursor.execute("INSERT INTO session_stats (session_id, odi_3, odi_4, time_below_94, time_below_89, num_89_dips, recovery_time) VALUES (?, ?, ?, ?, ?, ?, ?)", (session_id, odi_3, odi_4, time_below_94_hours, time_below_89_hours, num_89_dips, avg_recovery_time_minutes))
    conn.commit()

# Close the connection
conn.close()
