import pytest
import pandas as pd
import re
from datetime import datetime
import os

# Benchmark metrics for data drift from reference dataset
existing_avg_rating = 4.0685714285714285
existing_avg_stdev = 0.7458938852902691

# Load the rate_events.csv dataset from a specified path
@pytest.fixture
def rate_events_data():
    """Load rate_events.csv into a DataFrame."""
    file_path = os.path.join(os.path.dirname(__file__), '../data/rate_events.csv')
    with open(file_path, 'r') as rate_file:
        return pd.read_csv(rate_file)

def test_schema(rate_events_data):
    """Test that the dataset has the required fields with correct types."""
    # Expected columns
    expected_columns = ['timestamp', 'user_id', 'movie_id', 'rating']
    # Check for column presence
    assert all(column in rate_events_data.columns for column in expected_columns), "Missing required columns."
    # Check data types
    assert rate_events_data['timestamp'].apply(lambda x: isinstance(x, str)).all(), "Invalid data type for timestamp."
    assert rate_events_data['user_id'].apply(lambda x: isinstance(x, int)).all(), "Invalid data type for user_id."
    # Check `movie_id` format: title+year (e.g., "the+dark+knight+2008")
    movie_id_pattern = re.compile(r'^[a-z]+(\+[a-z]+)*\+\d{4}$')
    assert rate_events_data['movie_id'].apply(lambda x: bool(movie_id_pattern.match(x))).all(), (
        "Invalid movie_id format. Expected format 'title+year' (e.g., 'the+dark+knight+2008').")
    assert rate_events_data['rating'].apply(lambda x: isinstance(x, (int, float)) and 1 <= x <= 5).all(), "Invalid rating value."

def test_timestamp_format(rate_events_data):
    """Test that timestamps are in a valid format."""
    def is_valid_timestamp(ts):
        try:
            datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
            return True
        except ValueError:
            return False
    assert rate_events_data['timestamp'].apply(is_valid_timestamp).all(), "Invalid timestamp format in dataset."

def test_data_drift(rate_events_data):
    """Test for data drift based on benchmark dataset."""
    # Calculate current metrics
    current_avg_rating = rate_events_data['rating'].mean()
    current_stdev = rate_events_data['rating'].std()

    # Set thresholds for acceptable differences (tune these as needed)
    avg_rating_threshold = 0.5
    stdev_threshold = 0.1

    # Check if current metrics significantly deviate from benchmark metrics
    assert abs(current_avg_rating - existing_avg_rating) < avg_rating_threshold, (
        f"Data drift detected in average rating: {current_avg_rating} vs {existing_avg_rating}"
    )
    assert abs(current_stdev - existing_avg_stdev) < stdev_threshold, (
        f"Data drift detected in rating standard deviation: {current_stdev} vs {existing_avg_stdev}"
    )

