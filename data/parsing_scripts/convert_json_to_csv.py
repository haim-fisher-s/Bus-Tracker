import pandas as pd
import os
import json

# from here we will start 'walk' (only line 16 for now)
directory = "test/13016_1"

# Define a function to parse the JSON string
def parse_json_string(json_string):
    return json.loads(json_string)

# Define your column names as a list
column_names = ['DatedVehicleJourneyRef', 'stopOrder', 'stopId', 'actualArrivalTime', 'actualDepartureTime', 'VehicleRef']

error_lines = 0 
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".csv"):
            # Create an empty DataFrame with the specified column names
            df_to_save = pd.DataFrame(columns=column_names)

            csv_file_path = os.path.join(root, file)
            df = pd.read_csv(csv_file_path)

            # Apply the function to the 'jsonString' column and store the result in a new column called 'jsonData'
            df['jsonData'] = df['jsonString'].apply(parse_json_string)

            # Now you can access the parsed JSON data for a given row like this:
            data = df.iloc[0]['jsonData']
            time = df.iloc[0]['DatedVehicleJourneyRef']
            vehicl_id = df.iloc[0]['VehicleRef']
            
            for record in data['tripMessages']:
                try:
                    for report in record['tripMessage']:
                        try:
                            if report['previousCalls']:
                                try:
                                    actualArrivalTime = report['previousCalls'][0]['actualArrivalTime']
                                except:
                                    actualArrivalTime = df.iloc[0]['OriginAimedDepartureTime']
                                    assert(report['previousCalls'][0]['stopOrder'] == 1)

                                new_row_data = {
                                    'DatedVehicleJourneyRef': time,
                                    'stopOrder': report['previousCalls'][0]['stopOrder'],
                                    'stopId': report['previousCalls'][0]['stopId'],
                                    'actualArrivalTime': actualArrivalTime,
                                    'actualDepartureTime': report['previousCalls'][0]['actualDepartureTime'],
                                    'VehicleRef': vehicl_id
                                }

                                df_to_save = pd.concat([df_to_save, pd.DataFrame(new_row_data, index=[0])], ignore_index=True)
                        except:
                            #not an error not all entry's have the section previousCalls
                            pass
                except:
                    print('bad json')
                    error_lines += 1
            
            df_to_save.drop_duplicates(inplace=True)
            df_to_save.to_csv(csv_file_path)

# indicates for corrupted json's (not empty)
print(f'num of errors {error_lines}')
                
