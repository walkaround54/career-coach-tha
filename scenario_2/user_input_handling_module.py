import pandas as pd
from pathlib import Path
from fuzzywuzzy import process
from cli_module import display_results, display_menu
import carpark_api_fetcher_module as carpark_api_fetcher_module
import merged_data_processing_module as merged_data_processing_module

# Set base directories
BASE_DIR = Path(__file__).resolve().parent
PREPROCESSED_DATA_DIR = BASE_DIR / "preprocessed_data"
PROCESSED_DATA_DIR = BASE_DIR / "processed_data"

STATIC_CARPARK_DATA_PATH = PROCESSED_DATA_DIR / \
    "processed_static_carpark_data.csv"
MERGED_DATA_PATH = PROCESSED_DATA_DIR / "processed_merged_data.csv"


def load_static_data():
    """
    load static carpark data
    """
    if STATIC_CARPARK_DATA_PATH.exists():
        return pd.read_csv(STATIC_CARPARK_DATA_PATH, dtype=str)
    else:
        print(f"Error: {STATIC_CARPARK_DATA_PATH} not found.")
        return pd.DataFrame()


def validate_carpark_number(carpark_number, static_data):
    """
    check if the carpark number exists in static data, case insensitive
    """
    # standardize capitalization
    carpark_number = carpark_number.upper().strip()
    if carpark_number in static_data["car_park_no"].str.upper().values:
        return carpark_number
    else:
        # no fuzzy matching for carpark numbers since there are only a few characters
        print("\nInvalid Carpark Number. No exact match found.")
        return None


def fuzzy_match_address(query, static_data):
    """
    fuzzy match input address with static carpark data
    """
    choices = static_data["address"].dropna().tolist()
    matches = process.extract(query, choices, limit=5)

    # show top 5 results
    print("\nNo exact match found. Did you mean:\n")
    for i, (match, score) in enumerate(matches, start=1):
        print(f"{i}. {match} (Confidence: {score}%)")

    print("6. Search Again")
    print("7. Return to Menu")

    while True:
        selection = input(
            "\nSelect 1-5 to choose a match, enter 6 to search again, or 7 to return to menu: ").strip()
        if selection in ["1", "2", "3", "4", "5"]:
            best_match = matches[int(selection) - 1][0]
            matched_row = static_data[static_data["address"] == best_match]
            carpark_number = matched_row["car_park_no"].values[0]
            print(f"\nSelected: {best_match} → Carpark No: {carpark_number}")
            return carpark_number
        elif selection == "6":
            return "search_again"
        elif selection == "7":
            return "return_to_menu"
        else:
            print(
                "Invalid selection. Please enter 1-5 to select, 6 to retry search, or 7 to return to menu.")


def handle_user_input():
    """
    handles user input validation and triggers appropriate modules and functions
    """
    static_data = load_static_data()
    if static_data.empty:
        print("Error: No static carpark data available.")
        return

    while True:
        display_menu()
        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "1":
            # return to Carpark Number search if no match
            while True:
                carpark_number = input(
                    "\nEnter Carpark Number: ").strip().upper()
                valid_carpark = validate_carpark_number(
                    carpark_number, static_data)

                if valid_carpark:
                    break
                else:
                    print("\nNo exact match found.")
                    print("1. Search Again")
                    print("2. Return to Menu")
                    retry_choice = input("\nEnter your choice: ").strip()
                    if retry_choice == "2":
                        break
                    elif retry_choice != "1":
                        print("Invalid input. Returning to Carpark Number search.")

        elif choice == "2":
            # return Address search if no match
            while True:
                address_query = input("\nEnter Address: ").strip()
                valid_carpark = fuzzy_match_address(address_query, static_data)

                if valid_carpark == "search_again":
                    continue
                elif valid_carpark == "return_to_menu":
                    break
                elif valid_carpark:
                    break

        elif choice == "3":
            print("Exiting app.")
            return

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            continue

        if valid_carpark and valid_carpark not in ["search_again", "return_to_menu"]:
            print(f"\nFetching live data for carpark: {valid_carpark}...\n")

            # fetch latest API data
            carpark_api_fetcher_module.main()

            # update merged data with the latest API data
            merged_data_processing_module.main()

            # load merged data to display results
            merged_data = pd.read_csv(MERGED_DATA_PATH, dtype=str)
            result = merged_data[merged_data["car_park_no"].str.upper(
            ) == valid_carpark]

            if not result.empty:
                display_results(result)

                # prompt user for next action
                while True:
                    exit_option = input(
                        "\nEnter 1 to return to menu, 2 to quit: ").strip()
                    if exit_option == "1":
                        break
                    elif exit_option == "2":
                        print("Exiting app.")
                        return
                    else:
                        print(
                            "Invalid input. Please enter 1 to return to menu or 2 to quit.")
            else:
                print("Error: No data found after merging. Please try again.")

        else:
            print("Returning to search menu...\n")


if __name__ == "__main__":
    handle_user_input()
