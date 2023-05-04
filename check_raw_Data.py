import os
import csv

# Define the folder containing the CSV files
folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")

# Get the list of CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Define the expected number of columns in the CSV files
expected_columns = 4

# Loop over each CSV file and check the number of columns
for filename in csv_files:
    with open(os.path.join(folder_path, filename), newline='') as f:
        reader = csv.reader(f)
        # Skip the header
        next(reader)
        for row in reader:
            if len(row) != expected_columns:
                print(f"Incorrect number of columns in {filename}: {row}")

print("CSV file check complete.")
