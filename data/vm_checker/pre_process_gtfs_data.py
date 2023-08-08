import pandas as pd
import zipfile


def read_csv_from_zip(zip_file_path, txt_file_path):
    with zipfile.ZipFile(zip_file_path, "r") as zip_file:
        with zip_file.open(txt_file_path) as txt_file:
            df = pd.read_csv(txt_file)
    return df


def main():
    # Define the path to the zip file
    zip_file_path = "israel-public-transportation.zip"

    # Define the path to the text files inside the zip file
    txt_file_paths = ["trips.txt", "stop_times.txt", "routes.txt", "stops.txt"]

    # Read the text files into separate Pandas DataFrames
    df1 = read_csv_from_zip(zip_file_path, txt_file_paths[0])
    df2 = read_csv_from_zip(zip_file_path, txt_file_paths[1])
    df3 = read_csv_from_zip(zip_file_path, txt_file_paths[2])
    df4 = read_csv_from_zip(zip_file_path, txt_file_paths[3])

    # Perform merges
    df_merged = pd.merge(df1, df2, on="trip_id", how="outer")
    df_merged = pd.merge(df_merged, df3, on="route_id", how="outer")
    full_df = pd.merge(df_merged, df4, on="stop_id", how="outer")

    # Filter rows with missing trip_id
    full_df = full_df.dropna(axis=0, how="any", subset=["trip_id"])

    # Iterate through line_number values and store the dictionaries in a list
    line_numbers = full_df['route_desc'].unique()
    result_data = []

    for line_number in line_numbers:
        stop_order = full_df[full_df['route_desc'] == line_number].sort_values('stop_sequence')[
            'stop_code'].unique().tolist()
        result_data.append({'line_number': line_number, 'stop_order': stop_order})

    # Create the DataFrame from the list of dictionaries
    result_df = pd.DataFrame(result_data)

    result_df.to_pickle('result_df.pickle')


if __name__ == "__main__":
    main()
