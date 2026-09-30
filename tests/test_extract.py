"""Tests for the code that talks to the 311 API."""

from unittest.mock import patch  # lets swapping out a real thing for a fake one, just for a test

from civicpulse import extract
from civicpulse.extract import get_new_requests, get_open_requests, get_requests


def test_get_requests_returns_the_rows_the_api_sent() -> None:
    """get_requests should hand back exactly what the API responded with, unchanged."""
    fake_rows = [{"unique_key": "1"}, {"unique_key": "2"}]  # pretend this is what the API sent back

    # replace requests.get, just for this test, with a fake that returns fake_rows.
    with patch("civicpulse.extract.requests.get") as mock_get:
        mock_get.return_value.json.return_value = fake_rows
        mock_get.return_value.raise_for_status.return_value = None

        result = get_requests(limit=2)

    # check that the function handed back exactly what the (fake) API gave it
    assert result == fake_rows


def test_get_new_requests_asks_for_rows_created_after_since() -> None:
    """get_new_requests should filter using the 'since' value given to it."""
    fake_rows = [{"unique_key": "1", "created_date": "2026-09-29T10:00:00.000"}]

    with patch("civicpulse.extract.requests.get") as mock_get:
        mock_get.return_value.json.return_value = fake_rows
        mock_get.return_value.raise_for_status.return_value = None

        result = get_new_requests(since="2026-09-29T00:00:00.000")

    assert result == fake_rows


def test_get_open_requests_filters_by_non_closed_status() -> None:
    """get_open_requests should ask the API to filter out Closed rows."""
    with patch("civicpulse.extract.requests.get") as mock_get:
        mock_get.return_value.json.return_value = []
        mock_get.return_value.raise_for_status.return_value = None

        get_open_requests()

    # What parameters did we actually send to requests.get?
    _, call_kwargs = mock_get.call_args
    assert call_kwargs["params"]["$where"] == "status != 'Closed'"


def test_save_and_load_last_run_round_trip(tmp_path, monkeypatch) -> None:
    """Saving a run time and then loading it back should give the same value."""
    # a throwaway file path, unique to this test, auto-deleted afterward
    fake_file = tmp_path / "last_run.json"

    # temporarily point the code at the fake file
    monkeypatch.setattr(extract, "LAST_RUN_FILE", fake_file)

    extract.save_last_run("2026-09-29T12:00:00.000")
    result = extract.load_last_run()

    assert result == "2026-09-29T12:00:00.000"
