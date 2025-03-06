import pandas as pd
from pathlib import Path
import datetime

# this module extracts April 2019 events to restaurant_events.csv:

# get base directory
BASE_DIR = Path(__file__).resolve().parent

# Define input and output directories dynamically
PREPROCESSED_DATA_DIR = BASE_DIR / "preprocessed_data"
OUTPUT_DATA_DIR = BASE_DIR / "output/task_2"


def filter_events_by_date(preprocessed_csv_path, output_path, start_date, end_date):
    """
    reads preprocessed event data and filters for events within a start and end date
    saves filtered data to "restaurant_events.csv"
    """

    # check if user inputted date is properly formatted
    try:
        # convert to pandas compatible format
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)

        if start_date > end_date:
            raise ValueError("Start date must be equal to or before end date.")
    except Exception as e:
        print(f'Error: Invalid date format. {e}')
        return

    # load preprocessed event data
    event_df = pd.read_csv(preprocessed_csv_path, index_col=None)

    event_df["event_start_date"] = pd.to_datetime(
        event_df["event_start_date"], errors="coerce")
    event_df["event_end_date"] = pd.to_datetime(
        event_df["event_end_date"], errors="coerce")

    # filter for events that fall within start and end date
    filtered_df = event_df[
        (
            (event_df["event_end_date"] >= start_date) & (
                event_df["event_start_date"] <= end_date)
        ) |
        # allow for valid start date but missing/invalid end date
        (
            (event_df["event_start_date"] >=
             start_date) & event_df["event_end_date"].isna()
        ) |
        # allow for valid end date but missing/invalid start date
        (
            (event_df["event_end_date"] <=
             end_date) & event_df["event_start_date"].isna()
        )
    ]

    # select required columns, change accordingly
    columns_to_keep = [
        "event_id", "restaurant_id", "restaurant_name",
        "photo_url", "event_title", "event_start_date", "event_end_date"
    ]

    # filter for selected columns
    filtered_df = filtered_df[columns_to_keep]

    # replace missing values with "NA"
    filtered_df = filtered_df.fillna("NA")
    filtered_df.to_csv(output_path, index=False)

    print(
        f"\nData Preview for Events from {start_date} to {end_date}\n\n{filtered_df.head()}")


def main():
    """
    runs extraction module 2 standalone
    """
    preprocessed_event_csv_path = PREPROCESSED_DATA_DIR / "preprocessed_event_data.csv"
    output_event_csv_path = OUTPUT_DATA_DIR / "restaurant_events.csv"

    start_date = "2019-04-01"
    end_date = "2019-04-30"

    filter_events_by_date(preprocessed_event_csv_path,
                          output_event_csv_path, start_date, end_date)


if __name__ == "__main__":
    main()
