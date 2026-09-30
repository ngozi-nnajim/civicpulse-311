"""Tests for the code that talks to the 311 API."""

from unittest.mock import patch  # lets swapping out a real thing for a fake one, just for a test

from civicpulse.extract import get_requests


def test_get_requests_returns_the_rows_the_api_sent(monkeypatch=None) -> None:
    """get_requests should hand back exactly what the API responded with, unchanged."""
    fake_rows = [{"unique_key": "1"}, {"unique_key": "2"}]  # pretend this is what the API sent back

    # replace requests.get, just for this test, with a fake that returns fake_rows.
    with patch("civicpulse.extract.requests.get") as mock_get:
        mock_get.return_value.json.return_value = fake_rows
        mock_get.return_value.raise_for_status.return_value = None

        result = get_requests(limit=2)

    # check that the function handed back exactly what the (fake) API gave it
    assert result == fake_rows
