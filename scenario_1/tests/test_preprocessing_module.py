import pytest
import pandas as pd
import json
from pathlib import Path
from scenario_1.preprocessing_module import json_to_restaurant_details_csv, json_to_event_details_csv

# test data directory
TEST_DATA_DIR = Path(__file__).resolve().parent / "test_data"

# sample JSON Data
SAMPLE_JSON = [
    {
        "restaurants": [
            {
                "restaurant": {
                    "R": {"res_id": "12345"},
                    "name": "Test Restaurant",
                    "location": {"city": "Singapore", "country_id": "SG"},
                    "user_rating": {"votes": "100", "aggregate_rating": "4.5", "rating_text": "Excellent"},
                    "cuisines": "Asian, Japanese",
                    "zomato_events": [{"event": {"event_id": "E1", "start_date": "2025-03-10"}}]
                }
            }
        ]
    }
]


@pytest.fixture
def sample_json_file(tmp_path):
    """
    creates a temporary sample JSON file for testing
    """
    file_path = tmp_path / "test_restaurants.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(SAMPLE_JSON, f)
    return file_path


def test_json_to_restaurant_details_csv(tmp_path, sample_json_file):
    """Test extraction of restaurant details from JSON"""
    output_path = tmp_path / "restaurant_details.csv"
    raw_data = SAMPLE_JSON
    json_to_restaurant_details_csv(raw_data, output_path)

    df = pd.read_csv(output_path)
    assert not df.empty
    assert "restaurant_id" in df.columns
    assert df.loc[0, "restaurant_name"] == "Test Restaurant"


def test_json_to_event_details_csv(tmp_path, sample_json_file):
    """Test extraction of event details from JSON"""
    output_path = tmp_path / "event_details.csv"
    raw_data = SAMPLE_JSON
    json_to_event_details_csv(raw_data, output_path)

    df = pd.read_csv(output_path)
    assert not df.empty
    assert "event_id" in df.columns
    assert df.loc[0, "event_title"] != "NA"
