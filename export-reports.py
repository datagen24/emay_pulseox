import json
from datetime import datetime, timedelta
from generate_statistics import generate_statistics

# load the sessions data from the JSON file
with open('sessions.json') as f:
    sessions = json.load(f)

# iterate over the sessions and generate a report for each one
for session in sessions:
    start_timestamp_str = session.get('start_timestamp')
    end_timestamp_str = session.get('end_timestamp')
    if not start_timestamp_str or not end_timestamp_str:
        print(f"Skipping session {session.get('id')} due to missing start or end timestamp.")
        continue
    
    start_timestamp = datetime.fromisoformat(start_timestamp_str)
    end_timestamp = datetime.fromisoformat(end_timestamp_str)
    
    stats = generate_statistics(session.get('data'))
    duration_hours = (end_timestamp - start_timestamp).total_seconds() / 3600
    
    # generate the report
    report = f"Session ID: {session.get('id')}\n"
    report += f"Start Time: {start_timestamp}\n"
    report += f"End Time: {end_timestamp}\n"
    report += f"Duration: {duration_hours:.2f} hours\n"
    report += f"Time spent below 94% saturation: {stats.get('time_below_94_percent'):.2f} hours ({stats.get('percent_time_below_94_percent'):.2f}% of total time)\n"
    report += f"Time spent below 89% saturation: {stats.get('time_below_89_percent'):.2f} hours ({stats.get('percent_time_below_89_percent'):.2f}% of total time)\n"
    report += f"Number of dips: {stats.get('num_dips')}\n"
    report += "\n"
    
    # save the report to a file
    filename = f"{session.get('id')}_report.txt"
    with open(filename, 'w') as f:
        f.write(report)
    
    print(f"Report saved to {filename}.")
