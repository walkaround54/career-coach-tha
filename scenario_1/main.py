import os
from pathlib import Path
from preprocessing_module import restaurant_json_parser, json_to_restaurant_details_csv, json_to_event_details_csv
from extraction_module_1 import filter_restaurant_details
from extraction_module_2 import filter_events_by_date
from analysis_module import analyze_ratings

# get base directory
BASE_DIR = Path(__file__).resolve().parent

RAW_DATA_DIR = BASE_DIR / "raw_data"
PREPROCESSED_DATA_DIR = BASE_DIR / "preprocessed_data"
OUTPUT_DIR_TASK_1 = BASE_DIR / "output/task_1"
OUTPUT_DIR_TASK_2 = BASE_DIR / "output/task_2"
OUTPUT_DIR_TASK_3 = BASE_DIR / "output/task_3"

# file paths
restaurant_json_path = RAW_DATA_DIR / "restaurants.json"
country_excel_path = RAW_DATA_DIR / "Country-Code.xlsx"
preprocessed_restaurant_csv = PREPROCESSED_DATA_DIR / \
    "preprocessed_restaurant_details.csv"
preprocessed_event_csv = PREPROCESSED_DATA_DIR / "preprocessed_event_data.csv"
restaurant_details_output_path = OUTPUT_DIR_TASK_1 / "restaurant_details.csv"
event_details_output_path = OUTPUT_DIR_TASK_2 / "restaurant_events.csv"
ratings_pdf_output_path = OUTPUT_DIR_TASK_3 / "ratings_analysis.pdf"


def main():
    """
    runs scenario 1 pipeline
    """

    print("\n Step 1: Preprocessing Raw JSON Data \n")
    raw_data = restaurant_json_parser(restaurant_json_path)

    print("\n Step 2: Extracting Restaurant Details \n")
    json_to_restaurant_details_csv(raw_data, preprocessed_restaurant_csv)

    print("\n Step 3: Extracting Event Details \n")
    json_to_event_details_csv(raw_data, preprocessed_event_csv)

    print("\n Step 4: Filtering Restaurant Details with Valid Country Codes \n")
    filter_restaurant_details(
        preprocessed_restaurant_csv, country_excel_path, restaurant_details_output_path)

    print("\n Step 5: Filtering Events for April 2019 \n")
    filter_events_by_date(preprocessed_event_csv,
                          event_details_output_path, "2019-04-01", "2019-04-30")

    print("\n Step 6: Performing Rating Analysis \n")
    analyze_ratings(preprocessed_restaurant_csv, ratings_pdf_output_path)

    print("\n Scenario 1 Pipeline Completed")


if __name__ == "__main__":
    main()
