import pandas as pd
import os
import csv
from datetime import datetime

# from here we will start 'walk' (only line 16 for now)
directory = "test/13016_1"

# Define your column names as a list
column_names = ['Timestamp', 'Linkref', 'Link travel time (s)', 'time_in_stop(s)']

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".csv"):
            df_to_save = pd.DataFrame(columns=column_names)
            csv_file_path = os.path.join(root, file)
            df = pd.read_csv(csv_file_path)

            prev_row = None
            output_rows = []

            for index, row in df.iterrows():
                if prev_row is not None:
                    # Calculate the link travel time in seconds
                    prev_time = pd.to_datetime(prev_row['actualDepartureTime'])
                    curr_time = pd.to_datetime(row['actualArrivalTime'])
                    link_travel_time = int((curr_time - prev_time).total_seconds())

                    # Calculate the time spent at the previous stop in seconds
                    prev_arrival_time = pd.to_datetime(prev_row['actualArrivalTime'])
                    prev_departure_time = pd.to_datetime(prev_row['actualDepartureTime'])
                    time_in_stop = int((prev_departure_time - prev_arrival_time).total_seconds())

                    # Create a new dictionary with the calculated data
                    output_row = {
                        'Timestamp': prev_row['actualDepartureTime'],
                        'Linkref': f"{prev_row['stopId']}:{row['stopId']}",
                        'Link travel time (s)': link_travel_time,
                        'Time in stop (s)': time_in_stop
                    }

                    # Add the new row to the output list
                    output_rows.append(output_row)

                prev_row = row
            # Write the output list to a new CSV file
            output_df = pd.DataFrame(output_rows)
            output_df.to_csv(csv_file_path, index=False)
