import csv
import datetime
import sys

if len(sys.argv) != 2:
    print("Usage: python script.py input_file.csv")
    sys.exit(1)

input_file = sys.argv[1]
apple_output_file = input_file.replace(".csv", "_apple.csv")
somnopose_output_file = input_file.replace(".csv", "_somnopose.csv")

somnopose_headers = [
    "Date_Time",
    "Head_up_down",
    "Lying_on_left",
    "Lying_on_right",
    "SpO2",
    "Pulse_rate",
]

with open(input_file, "r") as infile, \
        open(apple_output_file, "w", newline="") as apple_outfile, \
        open(somnopose_output_file, "w", newline="") as somnopose_outfile:

    reader = csv.reader(infile)
    apple_writer = csv.writer(apple_outfile)
    somnopose_writer = csv.writer(somnopose_outfile)

    headers = next(reader)
    headers.append('timestamp')
    apple_writer.writerow(headers)

    somnopose_writer.writerow(somnopose_headers)

    for row in reader:
        date = datetime.datetime.strptime(row[0], '%m/%d/%Y')
        time = datetime.datetime.strptime(row[1], '%I:%M:%S %p').time()
        dt = datetime.datetime.combine(date, time)
        iso_dt = dt.isoformat()
        somnopose_dt = dt.strftime("%Y-%m-%d %H:%M:%S")

        row.append(iso_dt)
        apple_writer.writerow(row)

        spo2 = row[2]
        pulse_rate = row[3]

        # Set other Somnopose values to zero, as they are not available in your input data
        head_up_down = 0
        lying_on_left = 0
        lying_on_right = 0

        somnopose_row = [somnopose_dt, head_up_down, lying_on_left, lying_on_right, spo2, pulse_rate]
        somnopose_writer.writerow(somnopose_row)
