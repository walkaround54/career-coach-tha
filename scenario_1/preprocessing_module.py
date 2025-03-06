import pandas as pd
import json
from pathlib import Path

# this module reads raw json data and writes it to a preprocessed_restaurant_data.csv file

# get base directory
BASE_DIR = Path(__file__).resolve().parent

# define input and output directories dynamically
RAW_DATA_DIR = BASE_DIR / "raw_data"
PREPROCESSED_DATA_DIR = BASE_DIR / "preprocessed_data"


def restaurant_json_parser(restaurant_json_path):
    """
    parses raw json data
    """
    with open(restaurant_json_path, "r", encoding="utf-8") as file:
        restaurant_data = json.load(file)
        return restaurant_data


# def inspect_json(data, indent=0):
#     """
#     prints JSON structure with key names and value types to understand how to subsequently process
#     """
#     if isinstance(data, dict):
#         for key, value in data.items():
#             print("  " * indent + f"{key}: {type(value).__name__}")
#             inspect_json(value, indent + 1)
#     elif isinstance(data, list):
#         print("  " * indent +
#               f"List of {len(data)} items: [{type(data[0]).__name__}]" if data else "Empty List")
#         if data and isinstance(data[0], (dict, list)):
#             inspect_json(data[0], indent + 1)


# restaurant_json_path = RAW_DATA_DIR / "restaurants.json"
# raw_data = restaurant_json_parser(restaurant_json_path)
# inspect_json(raw_data)


def json_to_restaurant_details_csv(raw_data, output_path):
    """
    extracts relevant restaurant detail json fields to "preprocessed_restaurant_data.csv"
    """
    extracted_data = []

    for item in raw_data:
        restaurants = item.get("restaurants", [])

        for entry in restaurants:
            restaurant = entry.get("restaurant", {})

            # extract relevant fields and replace missing values with "NA",
            # add more fields to extract accordingly based on requirements
            restaurant_id = restaurant.get("R", {}).get("res_id", "NA")
            restaurant_name = restaurant.get("name", "NA")
            city = restaurant.get("location", {}).get("city", "NA")
            country = restaurant.get("location", {}).get("country_id", "NA")
            user_rating_votes = restaurant.get(
                "user_rating", {}).get("votes", "NA")
            user_aggregate_rating = restaurant.get(
                "user_rating", {}).get("aggregate_rating", "NA")
            cuisines = restaurant.get("cuisines", "NA")
            rating_text = restaurant.get(
                "user_rating", {}).get("rating_text", "NA")
            # extract date of first event in the list? not sure whether to list all or 1
            event_date = "NA"
            events = restaurant.get("zomato_events", [])
            if events:
                event_date = events[0].get("event", {}).get("start_date", "NA")

            extracted_data.append({
                "restaurant_id": restaurant_id,
                "restaurant_name": restaurant_name,
                "country": country,
                "city": city,
                "user_rating_votes": user_rating_votes,
                "user_aggregate_rating": user_aggregate_rating,
                "cuisines": cuisines,
                "event_date": event_date,
                "rating_text": rating_text
            })

    # write extracted data to csv
    restaurant_df = pd.DataFrame(extracted_data)
    # drop duplicates, must be identical because restaurant could have updated rating, cuisine, location etc.
    restaurant_df = restaurant_df.drop_duplicates()
    restaurant_df.to_csv(output_path, index=False)
    print(
        f"\n Data Preview for Restaurant Details \n \n {restaurant_df.head()}")


def json_to_event_details_csv(raw_data, output_path):
    """extracts relevant event json fields to preprocessed_event_data.csv"""
    extracted_data = []

    for item in raw_data:
        restaurants = item.get("restaurants", [])

        for entry in restaurants:
            restaurant = entry.get("restaurant", {})
            restaurant_id = restaurant.get("R", {}).get("res_id", "NA")
            restaurant_name = restaurant.get("name", "NA")

            # extract events
            events = restaurant.get("zomato_events", [])
            # iterate through events and extract relevant info
            # add more fields based on requirements accordingly
            if events:
                for event_listing in events:
                    event = event_listing.get("event", {})
                    event_id = event.get("event_id", "NA")
                    event_title = event.get("title", "NA")
                    event_start_date = event.get("start_date", "NA")
                    event_end_date = event.get("end_date", "NA")

                    # assume that only first photo URL is taken
                    photo_url = "NA"
                    photos = event.get("photos", [])
                    if photos:
                        photo_url = photos[0].get("photo", {}).get("url", "NA")

                    extracted_data.append({
                        "event_id": event_id,
                        "restaurant_id": restaurant_id,
                        "restaurant_name": restaurant_name,
                        "photo_url": photo_url,
                        "event_title": event_title,
                        "event_start_date": event_start_date,
                        "event_end_date": event_end_date
                    })

    # write extracted event data to csv
    event_df = pd.DataFrame(extracted_data)
    # drop duplicate events (start and end on same day with same event title and restaurant id and name)
    event_df = event_df.drop_duplicates(
        subset=["restaurant_id", "restaurant_name", "event_title", "event_start_date", "event_end_date"])
    event_df.to_csv(output_path, index=False)
    print(f"\n Data Preview for Event Details: \n \n {event_df.head()}")


restaurant_json_path = RAW_DATA_DIR / "restaurants.json"
raw_data = restaurant_json_parser(restaurant_json_path)

restaurant_details_output_path = PREPROCESSED_DATA_DIR / \
    "preprocessed_restaurant_details.csv"
json_to_restaurant_details_csv(raw_data, restaurant_details_output_path)

event_details_output_path = PREPROCESSED_DATA_DIR / "preprocessed_event_data.csv"
json_to_event_details_csv(raw_data, event_details_output_path)
