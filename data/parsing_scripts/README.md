# Data Structure from VM's Zip Files

This repository contains Python scripts for extracting data from VM's zip files and converting them into a structured directory of CSV files.

## Getting Started

1. Extract the VM zip file to a folder. Your folder structure should look like this:

    ```
    folder/
        |-VM.csv
    ```

2. Copy all the Python scripts from this directory to the same folder. Your folder structure should now look like this:

    ```
    folder/
        |-VM.csv
        |-split_data_to_small_csvs.py
        |-convert_json_to_csv.py
        |-prepper_final_csvs.py
    ```

3. Run the Python scripts in the following order:

    a. `split_data_to_small_csvs.py`
    
    b. `convert_json_to_csv.py`
    
    c. `prepper_final_csvs.py`
    
Congratulations, you have now successfully extracted and structured the data from the VM's zip files!

## Directory Structure

The final directory structure will be as follows:

```
datatest/
    |-lineid/
        |-date/
            |-final_rout.csv
            .
            .
        .
        .
```

Each `final_rout.csv` file in the directory structure will contain the relevant data for that specific date and line ID.

## Contributing

If you find any issues or have any suggestions for improvement, please feel free to submit a pull request or open an issue.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).