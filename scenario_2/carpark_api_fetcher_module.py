import requests
import time
import pandas as pd
from pathlib import Path

# this module fetches live API data and preprocesses it before saving to preprocessed_carpark_api_data.csv

# get base directory
BASE_DIR = Path(__file__).resolve().parent

# define input and output directories dynamically
PREPROCESSED_DATA_DIR = BASE_DIR / "preprocessed_data"

carpark_api = "https://api.data.gov.sg/v1/transport/carpark-availability"


def fetch_carpark_availability(carpark_api, max_retries=2, retry_delay=2, timeout=5):
    """
    fetches API data for carpark availability with 
    configurable retries, delay, and timeout

    parameters:
        max_retries (int): Number of retry attempts before failing
        retry_delay (int): Delay in seconds between retries
        timeout (int): Timeout for each API request in seconds

    returns carpark data from API or empty list if request fails
    """
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(carpark_api, timeout=timeout)

            # raise an error for HTTP issues
            response.raise_for_status()

            data = response.json()
            print(f"API request successful on attempt {attempt}")

            # return car park data
            return data.get("items", [])[0].get("carpark_data", [])

        except requests.Timeout:
            print(
                f"Attempt {attempt}: API request timed out (timeout={timeout}s).")
        except requests.HTTPError as e:
            print(
                f"Attempt {attempt}: HTTP error {e.response.status_code} - {e}")
        except requests.RequestException as e:
            print(f"Attempt {attempt}: Network error - {e}")

        if attempt < max_retries:
            print(f"Retrying in {retry_delay} seconds")
            time.sleep(retry_delay)
        else:
            print("Max retries reached. No data retrieved.")
            return []

# preview individual entry for carpark data
# print(fetch_carpark_availability(carpark_api)[0])


def get_lot_types(carpark_data):
    """
    gets list of lot types from API carpark data
    """
    # initialize set so unique lot types can be stored
    lot_types = set()

    for entry in carpark_data:
        for lot_data in entry.get("carpark_info", []):
            lot_types.add(lot_data["lot_type"])

    return lot_types


def save_carpark_api_data(carpark_data, carpark_api_data_output_path):
    """
    takes in parsed json data, extracts relevant fields and saves this data to "api_carpark_data.csv"
    capacity for each lot type is is saved as well
    """

    structured_data = []
    # obtain lot_types dynamically
    lot_types = get_lot_types(carpark_data)

    for entry in carpark_data:
        carpark_number = entry.get("carpark_number", "")
        update_datetime = entry.get("update_datetime", "")

        # initialize a dictionary for relevant data
        carpark_entry = {
            "carpark_number": carpark_number,
            "update_datetime": update_datetime,
        }

        # initialize all lot type columns with default values
        for lot in lot_types:
            carpark_entry[f"capacity_{lot}_lots"] = 0
            carpark_entry[f"available_{lot}_lots"] = 0

        # process nested carpark_info
        for lot_data in entry.get("carpark_info", []):
            lot_type = lot_data["lot_type"]
            if lot_type in lot_types:
                carpark_entry[f"capacity_{lot_type}_lots"] = int(
                    lot_data["total_lots"])
                carpark_entry[f"available_{lot_type}_lots"] = int(
                    lot_data["lots_available"])

        structured_data.append(carpark_entry)

    df = pd.DataFrame(structured_data)
    # standardize column names with static carpark data
    df = df.rename(columns={"carpark_number": "car_park_no"})

    df.to_csv(carpark_api_data_output_path, index=False)
    print(f"Data successfully saved to {carpark_api_data_output_path}")


def main():
    """
    runs the API fetcher module standalone
    """
    capark_api_data_output_path = PREPROCESSED_DATA_DIR / \
        "api_carpark_data.csv"
    api_carpark_data = fetch_carpark_availability(
        carpark_api, max_retries=2, retry_delay=2, timeout=5)

    if api_carpark_data:
        # print(f'\n Preview of fetched API data:\n \n {api_carpark_data[:2]}\n')
        save_carpark_api_data(api_carpark_data, capark_api_data_output_path)
    else:
        print("No data fetched. No csv written.")


if __name__ == "__main__":
    main()
