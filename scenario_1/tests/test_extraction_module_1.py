import pytest
import pandas as pd
from pathlib import Path
from scenario_1.extraction_module_1 import filter_restaurant_details

TEST_DATA_DIR = Path(__file__).resolve().parent / "test_data"

# sample Restaurant Data
SAMPLE_RESTAURANT_DF = pd.DataFrame({
    "restaurant_id": ["12345", "67890"],
    "restaurant_name": ["Test Restaurant", "Another Place"],
    "country": ["SG", "NA"],
    "city": ["Singapore", "Unknown"],
    "user_rating_votes": ["100", "50"],
    "user_aggregate_rating": ["4.5", "3.2"],
    "cuisines": ["Asian, Japanese", "Italian"],
    "event_date": ["2025-03-10", "NA"]
})

# sample Country Code Mapping data
SAMPLE_COUNTRY_MAPPING_DF = pd.DataFrame({
    "Country Code": ["SG", "US"],
    "Country": ["Singapore", "United States"]
}, index=[0, 1])


@pytest.fixture
def sample_restaurant_csv(tmp_path):
    """
    creates a temporary sample restaurant CSV file for testing
    """
    file_path = tmp_path / "restaurant_details.csv"
    SAMPLE_RESTAURANT_DF.to_csv(file_path, index=False)
    return file_path


@pytest.fixture
def sample_country_excel(tmp_path):
    """Creates a temporary sample country code Excel file for testing."""
    file_path = tmp_path / "Country-Code.xlsx"
    SAMPLE_COUNTRY_MAPPING_DF.to_excel(
        file_path, index=False, engine="openpyxl")
    return file_path


def test_filter_restaurant_details(tmp_path, sample_restaurant_csv, sample_country_excel):
    """Test filtering of restaurant details based on valid country codes"""
    output_path = tmp_path / "filtered_restaurant_details.csv"
    country_mapping = SAMPLE_COUNTRY_MAPPING_DF

    def mock_load_country_codes(_):
        return country_mapping

    filter_restaurant_details(sample_restaurant_csv,
                              sample_country_excel, output_path)

    df = pd.read_csv(output_path)
    assert not df.empty
    assert "restaurant_id" in df.columns
    assert "country" in df.columns
    # ensure country mapping applied
    assert df["country"].iloc[0] == "Singapore"
