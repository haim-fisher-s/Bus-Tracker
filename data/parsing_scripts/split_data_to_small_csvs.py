import pandas as pd
import pickle
import os.path
import re


if not os.path.isfile('examplePickle'):
    # Read the CSV file
    df = pd.read_csv('VM_feb2023_1.csv', encoding="utf-8")
    dbfile = open('examplePickle', 'ab')
    # source, destination
    pickle.dump(df, dbfile)                     
    dbfile.close()
else:
    dbfile = open('examplePickle', 'rb')     
    df = pickle.load(dbfile)
data_dir = 'test'
os.mkdir(data_dir)

# split LINE_DESC column by '-' and take the 0th element to create 'ID' column
df['ID'] = df['LINE_DESC'].str.split('-').str[0]
# split LINE_DESC column by '-' and take the 1st element to create 'DIRECTION' column
df['DIRECTION'] = df['LINE_DESC'].str.split('-').str[1]
df['ID'] = df['ID'].astype(str) + '_' + df['DIRECTION'].astype(str)

# Loop through each line in the data #LINE_ID LINE_SHORT_NAME
for line_id in df['ID'].unique():
    # Create a folder for the line if it doesn't exist
    if not os.path.exists(f"{data_dir}/{line_id}"):
        os.mkdir(f"{data_dir}/{line_id}")
        
    # Loop through each day in the data
    for day in df['DataFrameRef'].unique():
        
        # Create a folder for the day if it doesn't exist
        if not os.path.exists(f"{data_dir}/{line_id}/{day}"):
            os.mkdir(f"{data_dir}/{line_id}/{day}")
            
        # Extract the data for the current line and day
        current_data = df[(df['ID'] == line_id) & (df['DataFrameRef'] == day)]
        
        # Loop through each trip and write it to a CSV file
        for index, row in current_data.iterrows():
            time = row['OriginAimedDepartureTime'].replace(' ','_').replace(':','-').replace('.','-')
            trip_id = row['DatedVehicleJourneyRef']
            current_data.loc[index:index].to_csv(f"{data_dir}/{line_id}/{day}/{time}_{trip_id}.csv", index=False)
