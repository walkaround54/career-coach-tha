import pandas as pd
from pathlib import Path

# this module reads raw static carpark data and writes it to processed_static_carpark.csv

# get base directory
BASE_DIR = Path(__file__).resolve().parent

# define input and output directories dynamically
RAW_DATA_DIR = BASE_DIR / "raw_data"
PROCESSED_DATA_DIR = BASE_DIR / "processed_data"


def process_static_carpark_data(raw_carpark_data_path, processed_static_carpark_output_path):
    """
    processes static carpark data
    """
    df = pd.read_csv(raw_carpark_data_path, index_col=False)

    # check for missing values
    print(df.isna().count())
    # no missing values

    # drop extra instances of identical rows
    df = df.drop_duplicates()

    # check for carparks with duplicate carpark no. or address
    duplicate_carpark_no = df[df.duplicated(
        subset=['car_park_no'], keep=False)]
    print(duplicate_carpark_no)

    duplicate_address = df[df.duplicated(subset=['address'], keep=False)]
    print(duplicate_address)
    # since there are carparks with duplicate addresses,
    # display all carparks with same address when querying by address

    df.to_csv(processed_static_carpark_output_path, index=False)
    print(f"\n Data Preview for Carpark Details: \n \n {df.head()}")


def main():
    """
    runs static carpark processing module standalone
    """
    raw_carpark_data_input_path = RAW_DATA_DIR / "HDBCarparkInformation.csv"
    carpark_details_output_path = PROCESSED_DATA_DIR / \
        "processed_static_carpark_data.csv"
    process_static_carpark_data(
        raw_carpark_data_input_path, carpark_details_output_path)


if __name__ == "__main__":
    main()
