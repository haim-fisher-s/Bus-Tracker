import pandas as pd
from EDA_mislaka import delete_unique_columns


def main():
    # opening data frame
    path = r"C:\Users\shalt\Documents\final project\data\Pcount_feb2023\Pcount_feb2023.csv"
    pcount = pd.read_csv(path)

    # removing unnecesry data
    pcount = delete_unique_columns(pcount)  # the same value for all instances
    # mislaka = mislaka[mislaka['Direction'] != 0]  # a mistake. direction should be 1,2,3
    # mislaka = mislaka[mislaka['TripId'] != 0] # for now i will get rid of them.

    # calculate day of the week
    # mislaka['PlannedTripStartDate'] = pd.to_datetime(mislaka['PlannedTripStartDate'])
    # mislaka['day_of_week'] = mislaka['PlannedTripStartDate'].dt.day_name()

    # basic data checking
    # print('data set info:', mislaka.info(), sep='\n')
    # print('top 5:', mislaka.head(5), sep='\n')

    # print('Number of unique values per column:')
    # print(value_numbers(mislaka))

    # print('number of trip that didnt start: ', mislaka['TripStartDateTime'].isna().sum())


if __name__ == '__main__':
    main()
