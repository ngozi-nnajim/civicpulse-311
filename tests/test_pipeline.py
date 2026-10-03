from unittest.mock import patch

from civicpulse import pipeline


def test_run_daily_fetch_calls_everything_in_the_right_order() -> None:
    """run_daily_fetch should load the last run, fetch new and open requests,
    save both, and only then record the new last-run time."""
    with (
        patch("civicpulse.pipeline.load_last_run") as mock_load,
        patch("civicpulse.pipeline.get_new_requests") as mock_new,
        patch("civicpulse.pipeline.get_open_requests") as mock_open,
        patch("civicpulse.pipeline.save_raw_requests") as mock_save_raw,
        patch("civicpulse.pipeline.save_last_run") as mock_save_last,
    ):
        mock_load.return_value = "2026-09-01T00:00:00.000"

        pipeline.run_daily_fetch()

    mock_new.assert_called_once_with("2026-09-01T00:00:00.000")
    mock_open.assert_called_once()
    assert mock_save_raw.call_count == 2
    mock_save_last.assert_called_once()
