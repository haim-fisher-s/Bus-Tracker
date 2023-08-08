import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error
import matplotlib.pyplot as plt
from tqdm import tqdm
tqdm.pandas()

def link_average_per_TOD(links):
    # for now i will do just average, but it needs to change to TOD based
    # Group the DataFrame by 'Linkref' and calculate the mean 'linkTime' for each group
    average_times = links.groupby('Linkref')['linkTime'].mean()
    # Merge the average_times Series back to the original DataFrame based on 'Linkref'
    links = links.merge(average_times, left_on='Linkref', right_index=True, suffixes=('', '_avg'))
    # Rename the new column to 'averageTime'
    links.rename(columns={'linkTime_avg': 'averageTime'}, inplace=True)
    return links


def calculate_rolling_mean_previous_n(df, n):
    # Sort the DataFrame by 'Linkref' and 'actualArrivalTime'
    df_sorted = df.sort_values(by=['Linkref', 'actualArrivalTime'])

    # Calculate the rolling mean for each 'Linkref' group based on the previous n buses
    df[f'rolling_{n}'] = df_sorted.groupby('Linkref')['linkTime'].apply(lambda x: x.shift(1).rolling(window=n, min_periods=1).mean())

    # Reset the index of the DataFrame to align with the original DataFrame
    df.reset_index(drop=True, inplace=True)

    return df

def calculate_rolling_mean_previous_n(df, n):
    # Sort the DataFrame by 'Linkref' and 'actualArrivalTime'
    df_sorted = df.sort_values(by=['Linkref', 'actualArrivalTime'])
    # Calculate the rolling mean for each 'Linkref' group based on the previous n buses
    df_sorted[f'rolling_{n}'] = df_sorted.groupby('Linkref')['linkTime'].shift(1).fillna(0).rolling(window=n, min_periods=1).mean()
    return df_sorted



def plot_histograms(data, col1, col2):
    # Create histograms for the "linkTime" and "averageTime" columns
    plt.figure(figsize=(10, 6))  # Optional: Adjust the size of the plot
    plt.hist(data[col1], bins=1000, alpha=0.7, label=col1)
    plt.hist(data[col2], bins=1000, alpha=0.7, label=col2)
    plt.xlabel("Time")
    plt.ylabel("Frequency")
    plt.title(f"Distribution of {col1} and {col2}")
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_MEA_vs_feature(feature_values, MAE_values):
    """
    Create a graph to visualize the change in MEA values with the change of a feature.

    Parameters:
        feature_values (list): List of feature values.
        MAE_values (list): List of corresponding MAE (Mean Absolute Error) values.

    Returns:
        None (displays the plot)
    """
    # Plot the data
    plt.plot(feature_values, MAE_values, marker='o', linestyle='-')

    # Add labels and title
    plt.xlabel('Feature Values')
    plt.ylabel('MAE Values')
    plt.title('MAE vs. Feature')

    # Show the plot
    plt.grid(True)
    plt.show()


def test(actual_times, calculated_times):
    mae = mean_absolute_error(actual_times, calculated_times)
    pmae = (abs(actual_times - calculated_times) / actual_times).mean()
    variance = ((actual_times - calculated_times) ** 2).mean()

    # Calculate the absolute errors
    abs_errors = abs(actual_times - calculated_times)

    # Calculate the percentage of times the error is higher than 60
    percentage_smaller_than_60 = (abs_errors < 60).mean() * 100

    print("Mean Absolute Error (MAE):", mae)
    print("Mean Absolute Percentage Error (MAPE):", pmae)
    print("Variance:", variance)
    print("Percentage of times the error is higher than 60%:", percentage_smaller_than_60)

    return mae



def calculate_rolling_mean_before_time_for_link(df, n, time_threshold, link_ref):
    # Filter the DataFrame to keep only rows for the specified link_ref and before the time_threshold
    df_filtered = df[(df['Linkref'] == link_ref) & (df['actualArrivalTime'] < time_threshold)]

    # Sort the filtered DataFrame by 'actualArrivalTime' in descending order (newest first)
    df_sorted = df_filtered.sort_values(by='actualArrivalTime', ascending=False)

    # Calculate the rolling mean for the specified link_ref based on the first n buses before the time threshold
    rolling_mean = df_sorted['linkTime'].head(n).mean()

    return rolling_mean


def calculate_time_to_end(line_description, station, time, links):
    lines = pd.read_pickle(r'C:\Users\shalt\Documents\final project\data\lines.pickle')
    stop_order = lines["stop_order"][lines['line_number'] == line_description].values[0]
    return None


def main():
    path = r'C:\Users\shalt\Documents\final project\data\vm_links.pkl'
    links = pd.read_pickle(path)

    mae = []
    n_value = []
    for n in range(2, 15):
        links = calculate_rolling_mean_previous_n(links,n)
        n_value.append(n)
        mae.append(test(links['linkTime'], links[f'rolling_{n}']))

    plot_MEA_vs_feature(n_value, mae)


if __name__ == '__main__':
    main()
