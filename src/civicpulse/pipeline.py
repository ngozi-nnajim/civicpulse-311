from datetime import UTC, datetime

from civicpulse.extract import (
    get_new_requests,
    get_open_requests,
    load_last_run,
    save_last_run,
    save_raw_requests,
)


def run_daily_fetch() -> None:
    """Run the pipeline to fetch data needed daily.

    It gets the date for the last run, fetches both
    new and open data from the API, saves the raw data,
    and then saves the date of the last run after the
    data has been successfully saved to storage.
    """
    current_time = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
    since = load_last_run()

    # use current time if data is being loaded for the first time
    if not since:
        since = current_time

    new_requests = get_new_requests(since)
    open_requests = get_open_requests()

    save_raw_requests(new_requests, "new")
    save_raw_requests(open_requests, "open")

    save_last_run(current_time)


if __name__ == "__main__":
    run_daily_fetch()
