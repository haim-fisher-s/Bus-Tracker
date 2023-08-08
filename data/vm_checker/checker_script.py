import pickle
import pandas as pd
import matplotlib.pyplot as plt

# Open the pickle file in binary mode for reading
with open('C:/python/class/vm_links.pkl', 'rb') as file:
    # Load the contents of the pickle file
    data = pickle.load(file)
data = data[['TripId', 'LINE_DESC', 'stopOrder', 'Linkref','actualArrivalTime']]

with open('result_df.pickle', 'rb') as file:
    # Load the contents of the pickle file
    data_tester = pickle.load(file)

# Create an empty list to store the data for the new DataFrame
new_data = []

# Iterate through each row in the DataFrame
for index, row in data_tester.iterrows():
    # Access the list in the 'stop_order' column of the current row
    current_list = row['stop_order']

    # Iterate through each element in the current list
    for i, value in enumerate(current_list):
        # If it's the first element, add the entry with only the value
        if i == 0:
            new_data.append([row['line_number'], 1, str(value)])
        else:
            # Retrieve the previous value
            prev_value = current_list[i - 1]

            # Create the link by combining the previous value and current value
            link = f"{prev_value}:{value}"

            # Add the entry with the appropriate "line", "stopOrder", and "linkref" values
            new_data.append([row['line_number'], i + 1, link])

# Create the new DataFrame with columns 'line', 'stopOrder', and 'linkref'
new_df = pd.DataFrame(new_data, columns=['LINE_DESC', 'stopOrder', 'Linkref'])


# Merge the DataFrames based on 'stopOrder' and 'Linkref'
merged_df = data.merge(new_df, on=['LINE_DESC','stopOrder', 'Linkref'],how='left', indicator=True)

print(merged_df)

# Filter the non-matching rows
non_matching_rows = merged_df[merged_df['_merge'] != 'both']

if non_matching_rows.empty:
    print("Good")
else:
    print(f"Ratio of non-matching rows to total rows: {round(len(non_matching_rows) / len(data),2)}\n")

    # Calculate the number of unique DESC_LINE values in non_matching_rows
    unique_desc_line_count_non_matching = non_matching_rows['LINE_DESC'].nunique()
    unique_desc_line_count_vm = data['LINE_DESC'].nunique()

    # Print the result
    print(f"Number of unique LINE_DESC in non_matching_rows: {unique_desc_line_count_non_matching}")
    print(f"Number of unique LINE_DESC in VM: {unique_desc_line_count_vm}\n")

    # Calculate the percentage of unique LINE_DESC values in non_matching_rows
    percentage_unique_desc_line_non_matching = (unique_desc_line_count_non_matching / unique_desc_line_count_vm) * 100

    print(f"Percentage of unique LINE_DESC in non_matching_rows: {round(percentage_unique_desc_line_non_matching, 2)}%\n")

    # Calculate the number of unique DESC_LINE values in non_matching_rows
    unique_TripId_count_non_matching = non_matching_rows['TripId'].nunique()
    unique_TripId_count_vm = data['TripId'].nunique()

    # Print the result
    print(f"Number of unique TripId in non_matching_rows: {unique_TripId_count_non_matching}")
    print(f"Number of unique TripId in VM: {unique_TripId_count_vm}\n")

    # Calculate the percentage of unique LINE_DESC values in non_matching_rows
    percentage_unique_TripId_non_matching = (unique_TripId_count_non_matching / unique_TripId_count_vm) * 100


    # Print the percentage
    print(f"Percentage of unique TripId in non_matching_rows: {round(percentage_unique_TripId_non_matching, 2)}%\n")

    # Calculate the number of unique DESC_LINE values in non_matching_rows
    unique_Linkref_count_non_matching = non_matching_rows['Linkref'].nunique()
    unique_Linkref_count_vm = data['Linkref'].nunique()

    # Print the result
    print(f"Number of unique Linkref in non_matching_rows: {unique_Linkref_count_non_matching}")
    print(f"Number of unique Linkref in VM: {unique_Linkref_count_vm}\n")

    # Calculate the percentage of unique LINE_DESC values in non_matching_rows
    percentage_unique_Linkref_non_matching = (unique_Linkref_count_non_matching / unique_Linkref_count_vm) * 100


    # Print the percentage
    print(f"Percentage of unique Linkref in non_matching_rows: {round(percentage_unique_Linkref_non_matching, 2)}%\n")

    print("Indices of rows in df2 that do not have a match:")
    print(non_matching_rows)

# Calculate the percentage of mismatched rows compared to the total rows
mismatched_rows_percentage = round(len(non_matching_rows) / len(data) * 100, 2)

# Calculate the percentage of unique LINE_DESC values in non_matching_rows
mismatched_line_desc_percentage = round(percentage_unique_desc_line_non_matching, 2)

# Calculate the percentage of unique TripId values in non_matching_rows
mismatched_trip_id_percentage = round(percentage_unique_TripId_non_matching, 2)

# Calculate the percentage of unique Linkref values in non_matching_rows
mismatched_linkref_percentage = round(percentage_unique_Linkref_non_matching, 2)
# Create a list of labels for the pie charts
row_labels = ['Matching Rows', 'Mismatched Rows']
line_desc_labels = ['Matching LINE_DESC', 'Mismatched LINE_DESC']
trip_id_labels = ['Matching TripId', 'Mismatched TripId']
linkref_labels = ['Matching Linkref', 'Mismatched Linkref']

# Create a list of percentage values for each category
row_sizes = [100 - mismatched_rows_percentage, mismatched_rows_percentage]
line_desc_sizes = [100 - mismatched_line_desc_percentage, mismatched_line_desc_percentage]
trip_id_sizes = [100 - mismatched_trip_id_percentage, mismatched_trip_id_percentage]
linkref_sizes = [100 - mismatched_linkref_percentage, mismatched_linkref_percentage]

# Create subplots
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

# Pie plot for mismatched rows
axs[0].pie(row_sizes, labels=row_labels, autopct='%1.1f%%', startangle=90)
axs[0].set_title('Ratio of Mismatched Rows')
# Pie plot for mismatched LINE_DESC
axs[1].pie(line_desc_sizes, labels=line_desc_labels, autopct='%1.1f%%', startangle=90)
axs[1].set_title('Ratio of Mismatched LINE_DESC')

# Pie plot for mismatched TripId
axs[2].pie(trip_id_sizes, labels=trip_id_labels, autopct='%1.1f%%', startangle=90)
axs[2].set_title('Ratio of Mismatched TripId')

# Adjust the spacing between subplots
plt.subplots_adjust(wspace=0.3)

# Display the plots
plt.show()

# # for test:
# non_matching_rows_13016 = non_matching_rows[non_matching_rows['LINE_DESC'].str.contains("10904-1-#")]
# new_df_13016 = new_df[new_df['LINE_DESC'].str.contains("10904-1-#")]
# data_13016 = data[data['LINE_DESC'].str.contains("10904-1-#")]
# # print(non_matching_rows_13016)
# # print(new_df_13016)
# # print(data_13016.head(35))
# # print("test:/n")
# non_matching_rows['Hour'] = pd.to_datetime(non_matching_rows['actualArrivalTime']).dt.hour
# data['Hour'] = pd.to_datetime(data['actualArrivalTime']).dt.hour
#
# # Add 'DayOfWeek' column to 'non_matching_rows' and 'data'
# non_matching_rows['DayOfWeek'] = non_matching_rows['actualArrivalTime'].dt.day_name()
# data['DayOfWeek'] = data['actualArrivalTime'].dt.day_name()
#
# # Add 'DayOfMonth' column to 'non_matching_rows' and 'data'
# non_matching_rows['DayOfMonth'] = non_matching_rows['actualArrivalTime'].dt.day
# data['DayOfMonth'] = data['actualArrivalTime'].dt.day
#
#
# # Calculate the total count of records for each hour in the 'data' dataframe
# data_hour_counts = data.groupby('Hour').size()
#
# # Calculate the count of non-matching records for each hour in the 'non_matching_rows' dataframe
# non_matching_hour_counts = non_matching_rows.groupby('Hour').size()
#
# # Calculate the percentage of mismatch for each hour
# percentage_mismatch_by_hour = (non_matching_hour_counts / data_hour_counts) * 100
#
# # Print the percentage of mismatch for each hour
# print("Percentage of mismatch for each hour:")
# print(percentage_mismatch_by_hour)
#
#
# # Assuming 'non_matching_rows' and 'data' dataframes with the 'DayOfWeek' and 'DayOfMonth' columns added
#
# # Calculate the total count of records for each day of the week in the 'data' dataframe
# data_day_of_week_counts = data.groupby('DayOfWeek').size()
#
# # Calculate the count of non-matching records for each day of the week in the 'non_matching_rows' dataframe
# non_matching_day_of_week_counts = non_matching_rows.groupby('DayOfWeek').size()
#
# # Calculate the percentage of mismatch for each day of the week
# percentage_mismatch_by_day_of_week = (non_matching_day_of_week_counts / data_day_of_week_counts) * 100
# percentage_mismatch_by_day_of_week = percentage_mismatch_by_day_of_week.reindex(['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])
#
# # Print the percentage of mismatch for each day of the week
# print("Percentage of mismatch for each day of the week:")
# print(percentage_mismatch_by_day_of_week)
#
# plt.figure(figsize=(8, 6))
# percentage_mismatch_by_day_of_week.plot(kind='bar')
# plt.title("Percentage of Mismatch by Day of the Week")
# plt.xlabel("Day of the Week")
# plt.ylabel("Percentage of Mismatch")
# plt.xticks(rotation=45)
# plt.savefig('percentage_mismatch_by_day_of_week.png')
# plt.show()
#
# # Calculate the total count of records for each day of the month in the 'data' dataframe
# data_day_of_month_counts = data.groupby('DayOfMonth').size()
#
# # Calculate the count of non-matching records for each day of the month in the 'non_matching_rows' dataframe
# non_matching_day_of_month_counts = non_matching_rows.groupby('DayOfMonth').size()
#
# # Calculate the percentage of mismatch for each day of the month
# percentage_mismatch_by_day_of_month = (non_matching_day_of_month_counts / data_day_of_month_counts) * 100
#
# # Print the percentage of mismatch for each day of the month
# print("Percentage of mismatch for each day of the month:")
# print(percentage_mismatch_by_day_of_month)
#
# plt.figure(figsize=(8, 6))
# percentage_mismatch_by_day_of_month.plot(kind='bar')
# plt.title("Percentage of Mismatch by Day")
# plt.xlabel("Day")
# plt.ylabel("Percentage of Mismatch")
# plt.xticks(rotation=45)
# plt.savefig('percentage_mismatch_by_day.png')
#
# plt.show()



