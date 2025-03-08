import pytest
import pandas as pd
from scenario_2.merged_data_processing_module import update_merged
from pathlib import Path

TEST_DATA_DIR = Path(__file__).resolve().parent.parent / "test_data"

# paths for test CSV files
TEST_MERGED_DATA_PATH = TEST_DATA_DIR / "test_merged_data.csv"
TEST_API_DATA_PATH = TEST_DATA_DIR / "test_api_data.csv"

# sample data for testing merging functionality
MERGED_DATA = pd.DataFrame({
    "car_park_no": ["A123", "B456"],
    "update_datetime": ["2025-03-07 10:00:00", "Data Not Available"],
    "capacity_C_lots": [100, 200],
    "available_C_lots": [50, 100]
})

API_DATA = pd.DataFrame({
    "car_park_no": ["A123", "B456"],
    "update_datetime": ["2025-03-07 11:00:00", "2025-03-07 12:00:00"],
    "capacity_C_lots": [120, 220],
    "available_C_lots": [60, 90]
})


@pytest.fixture(scope="function", autouse=True)
def setup_test_data():
    """
    writes sample test data to the test_data folder before running each test.
    """
    MERGED_DATA.to_csv(TEST_MERGED_DATA_PATH, index=False)
    API_DATA.to_csv(TEST_API_DATA_PATH, index=False)
    yield
    # remove mock data after test
    TEST_MERGED_DATA_PATH.unlink(missing_ok=True)
    TEST_API_DATA_PATH.unlink(missing_ok=True)


def test_update_merged(monkeypatch):
    """
    Test merging of updated API data using test_data folder.
    """
    # mock file paths in module
    monkeypatch.setattr(
        "scenario_2.merged_data_processing_module.MERGED_DATA_PATH", TEST_MERGED_DATA_PATH)
    monkeypatch.setattr(
        "scenario_2.merged_data_processing_module.API_CARPARK_DATA_PATH", TEST_API_DATA_PATH)

    # run the update function now using test_data
    update_merged()

    updated_df = pd.read_csv(TEST_MERGED_DATA_PATH, dtype=str)

    # ensure update_datetime is updated correctly
    assert updated_df.loc[updated_df["car_park_no"] == "A123",
                          "update_datetime"].values[0] == "2025-03-07 11:00:00"
    assert updated_df.loc[updated_df["car_park_no"] == "B456",
                          "update_datetime"].values[0] == "2025-03-07 12:00:00"

    # ensure capacity and availability updates correctly
    assert updated_df.loc[updated_df["car_park_no"] ==
                          "A123", "capacity_C_lots"].values[0] == "120"
    assert updated_df.loc[updated_df["car_park_no"] ==
                          "A123", "available_C_lots"].values[0] == "60"
    assert updated_df.loc[updated_df["car_park_no"] ==
                          "B456", "capacity_C_lots"].values[0] == "220"
    assert updated_df.loc[updated_df["car_park_no"] ==
                          "B456", "available_C_lots"].values[0] == "90"
