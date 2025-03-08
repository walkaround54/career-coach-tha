import pytest
from scenario_2.carpark_api_fetcher_module import fetch_carpark_availability, carpark_api


def test_fetch_carpark_availability(monkeypatch):
    """
    test fetching mock API data
    """

    class MockResponse:
        @staticmethod
        def json():
            return {"items": [{"carpark_data": [{"carpark_number": "A123", "update_datetime": "2025-03-07 10:00:00"}]}]}

        @staticmethod
        def raise_for_status():
            pass

    monkeypatch.setattr("requests.get", lambda url, timeout: MockResponse())

    result = fetch_carpark_availability("dummy_url")
    assert isinstance(result, list)
    assert len(result) > 0
    assert result[0]["carpark_number"] == "A123"
