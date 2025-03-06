import pandas as pd
import openpyxl
from pathlib import Path

# this module extracts and saves restaurant details to restaurant_details.csv
# only include restaurants with matching Country Codes from Country-Code.xlsx


# get base directory
BASE_DIR = Path(__file__).resolve().parent

# define input and output directories dynamically
RAW_DATA_DIR = BASE_DIR / "raw_data"
PREPROCESSED_DATA_DIR = BASE_DIR / "preprocessed_data"
OUTPUT_DATA_DIR = BASE_DIR / "output/task_1"


def load_country_codes(country_excel_path):
    """
    returns a dictionary with country code mappings
    """
    country_df = pd.read_excel(country_excel_path, engine='openpyxl')

    # create dictionary with country code mappings
    country_mapping = dict(
        zip(country_df["Country Code"], country_df["Country"]))

    return country_mapping


def filter_restaurant_details(preprocessed_csv_path, country_excel_path, output_path):
    """
    reads preprocessed restaurant data, filters based on valid country codes, and extracts required fields
    saves the filtered restaurant details to "restaurant_details.csv"
    """
    # load preprocessed restaurant data
    restaurant_df = pd.read_csv(preprocessed_csv_path, index_col=None)

    # load country code mappings
    country_mapping = load_country_codes(country_excel_path)

    # convert country codes to country names
    restaurant_df["country"] = restaurant_df["country"].map(
        country_mapping).fillna("NA")

    # filter out rows where country is "NA"
    restaurant_df = restaurant_df[restaurant_df["country"] != "NA"]

    # ensure correct data types
    restaurant_df["user_aggregate_rating"] = pd.to_numeric(
        restaurant_df["user_aggregate_rating"], errors='coerce')

    # select required columns
    columns_to_keep = [
        "restaurant_id", "restaurant_name", "country", "city",
        "user_rating_votes", "user_aggregate_rating", "cuisines", "event_date"
    ]

    # filter df for columns to keep
    filtered_df = restaurant_df[columns_to_keep]
    # replace missing values with "NA"
    filtered_df = filtered_df.fillna("NA")

    filtered_df.to_csv(output_path, index=False)

    print(f"\n Data Preview \n \n {filtered_df.head()}")


preprocessed_csv_path = PREPROCESSED_DATA_DIR / \
    "preprocessed_restaurant_details.csv"
country_excel_path = RAW_DATA_DIR / "Country-Code.xlsx"
output_csv_path = OUTPUT_DATA_DIR / "restaurant_details.csv"

filter_restaurant_details(preprocessed_csv_path,
                          country_excel_path, output_csv_path)
