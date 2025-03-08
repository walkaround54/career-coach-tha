import pandas as pd
from pathlib import Path

# this module merges static carpark data with updated live API data and saves it to processed_merged_data.csv

# get base directory
BASE_DIR = Path(__file__).resolve().parent

PREPROCESSED_DATA_DIR = BASE_DIR / "preprocessed_data"
PROCESSED_DATA_DIR = BASE_DIR / "processed_data"

API_CARPARK_DATA_PATH = PREPROCESSED_DATA_DIR / "api_carpark_data.csv"
STATIC_CARPARK_DATA_PATH = PROCESSED_DATA_DIR / \
    "processed_static_carpark_data.csv"
MERGED_DATA_PATH = PROCESSED_DATA_DIR / "processed_merged_data.csv"


def load_csv(file_path):
    """
    loads a CSV file to a pandas dataframe if it exists, otherwise returns an empty dataframe
    """
    if file_path.exists():
        return pd.read_csv(file_path, dtype=str)
    else:
        print(f"{file_path} not found. Returning empty DataFrame.")
        return pd.DataFrame()


def merge_initial():
    """
    performs the initial merge of static carpark data with API data (if no previous merged file exists)
    uses a left join on car_park_no to ensure all static carparks are retained
    """
    static_data = load_csv(STATIC_CARPARK_DATA_PATH)
    api_data = load_csv(API_CARPARK_DATA_PATH)

    if static_data.empty:
        print("Static carpark data is missing. Cannot perform merge.")
        return

    # merge using left join to retain all static carpark rows
    merged_data = static_data.merge(
        api_data, on="car_park_no", how="left")

    merged_data = merged_data.fillna("Data Not Available")

    # drop duplicates
    merged_data = merged_data.drop_duplicates()

    merged_data.to_csv(MERGED_DATA_PATH, index=False)
    print(f"Initial merge complete. Data saved to {MERGED_DATA_PATH}")


def update_merged():
    """
    updates the existing merged dataset by incorporating new API data
    only updates rows if the API data has a more recent timestamp
    """
    merged_data = load_csv(MERGED_DATA_PATH)
    api_data = load_csv(API_CARPARK_DATA_PATH)

    if merged_data.empty:
        print("No existing merged data found. Running initial merge instead.")
        merge_initial()
        return

    if api_data.empty:
        print("No new API data available. No updates made.")
        return

    # convert update_datetime to datetime for comparison
    merged_data["update_datetime"] = pd.to_datetime(
        merged_data["update_datetime"], errors="coerce")
    api_data["update_datetime"] = pd.to_datetime(
        api_data["update_datetime"], errors="coerce")

    # perform left join on car_park_no, add _new suffix to merged API columns
    updated_data = merged_data.merge(
        api_data, on="car_park_no", how="left", suffixes=("", "_new")
    )

    # ensure original and new update_datetime columns exist before proceeding
    if "update_datetime" in updated_data.columns and "update_datetime_new" in updated_data.columns:
        # existing datetime is missing or == "Data Not Available"
        # new API datetime is valid and is more recent than existing datetime
        rows_to_update = (
            (updated_data["update_datetime"].isna()) |
            (updated_data["update_datetime"] == "Data Not Available") |
            (
                updated_data["update_datetime_new"].notna() &
                (updated_data["update_datetime"] <
                 updated_data["update_datetime_new"])
            )
        )

        # identify API columns to update
        api_columns_to_use = [col for col in api_data.columns if col not in [
            "car_park_no", "update_datetime"]]

        # update relevant columns
        for col in api_columns_to_use:
            updated_data.loc[rows_to_update,
                             col] = updated_data.loc[rows_to_update, f"{col}_new"]

        # update datetime
        updated_data.loc[rows_to_update,
                         "update_datetime"] = updated_data.loc[rows_to_update, "update_datetime_new"]

        # drop new datetime column
        updated_data = updated_data.drop(columns=["update_datetime_new"])

        # drop extra _new columns after updating
        updated_data = updated_data.drop(
            columns=[col + "_new" for col in api_columns_to_use])

    # fill remaining null values with "Data Not Available"
    updated_data = updated_data.fillna("Data Not Available")

    # drop duplicates
    updated_data = updated_data.drop_duplicates()
    updated_data.to_csv(MERGED_DATA_PATH, index=False)
    print(f"Updated merged data saved to {MERGED_DATA_PATH}")


def main():
    """
    runs merged_data_processing_module standalone
    determines whether to perform an initial merge or update an existing merged dataset
    """
    if MERGED_DATA_PATH.exists():
        print("Existing merged data found. Updating merged data...")
        update_merged()
    else:
        print("No merged data found. Performing initial merge...")
        merge_initial()


if __name__ == "__main__":
    main()
