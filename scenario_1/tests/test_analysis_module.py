import pytest
import pandas as pd
from pathlib import Path
import matplotlib as plt
from scenario_1.analysis_module import analyze_ratings

TEST_DATA_DIR = Path(__file__).resolve().parent / "test_data"

# sample Ratings Data
SAMPLE_RATINGS_DF = pd.DataFrame({
    "restaurant_id": ["10001", "10002", "10003", "10004", "10005"],
    "restaurant_name": ["Low Rated Cafe", "Decent Diner", "Good Eats", "Fine Cuisine", "Luxury Dining"],
    "rating_text": ["Poor", "Average", "Good", "Very Good", "Excellent"],
    "user_aggregate_rating": [2.5, 3.2, 3.8, 4.2, 4.8]
})


@pytest.fixture
def sample_ratings_csv(tmp_path):
    """
    creates a temporary sample ratings CSV file for testing
    """
    file_path = tmp_path / "ratings_data.csv"
    SAMPLE_RATINGS_DF.to_csv(file_path, index=False)
    return file_path


def test_analyze_ratings(tmp_path, sample_ratings_csv):
    """
    test the analysis module to ensure it runs without error
    """
    pdf_output_path = tmp_path / "ratings_analysis.pdf"
    analyze_ratings(sample_ratings_csv, pdf_output_path)

    # check if PDF was generated
    assert pdf_output_path.exists()

    df = pd.read_csv(sample_ratings_csv)

    # check that originally different language rating mapped to English
    assert df.loc[df["restaurant_name"] == "Food Haven",
                  "rating_text"].values[0] == "Very Good"

    # check that a histogram was plotted
    fig, ax = plt.subplots()
    df["user_aggregate_rating"].hist(ax=ax)
    assert len(ax.patches) > 0, "Histogram plot did not generate bars"

    # check that a bar plot for rating counts exists
    fig, ax = plt.subplots()
    df["rating_text"].value_counts().plot(kind="bar", ax=ax)
    assert len(ax.patches) == len(df["rating_text"].unique(
    )), "Bar plot does not match unique rating texts"
