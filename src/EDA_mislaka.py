import pandas as pd


def delete_unique_columns(df):
    """
    gets a dataframe and removes columns with only one unique value.
    prints the columns and values it deletes
    returns the new data frame
    """
    columns = df.columns
    for col in columns:
        if df[col].nunique() == 1:
            print(col, ':', df[col][0])
            df.drop(columns=[col], inplace=True)
    return df


def value_numbers(df):
    """
    prints how many unique vlues each column has.
    for columns with less than 10 values, prints the vlues.
    """
    columns = df.columns
    for col in columns:
        val_num = df[col].nunique()
        print(f'{col} : {val_num}')

        if df[col].nunique() <= 10:
            print(list(df[col].unique()))



def main():
    # opening data frame
    path = r"C:\Users\shalt\Documents\final project\data\mislaka_feb2023\mislaka_feb2023.csv"
    mislaka = pd.read_csv(path)

    # removing unnecesry data
    mislaka = delete_unique_columns(mislaka)

    # basic data checking
    print('data set info:', mislaka.info(), sep='\n')
    print('top 5:', mislaka.head(5), sep='\n')

    print('Number of unique values per column:')
    print(value_numbers(mislaka))

    print('number of trip that didnt start: ', mislaka['TripStartDateTime'].isna().sum())


if __name__ == '__main__':
    main()
