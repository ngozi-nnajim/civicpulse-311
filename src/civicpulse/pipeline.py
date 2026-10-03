import logging
from datetime import UTC, datetime

from civicpulse.config import LOG_FILE, LOG_LEVEL
from civicpulse.extract import (
    get_new_requests,
    get_open_requests,
    load_last_run,
    save_last_run,
    save_raw_requests,
)
from civicpulse.load import load_bronze_requests

LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=LOG_LEVEL,
    filename=LOG_FILE,
    format="%(asctime)s %(levelname)s %(message)s",  # timestamp, severity, message
)
logger = logging.getLogger(__name__)


def run_daily_fetch() -> None:
    """Run the pipeline to fetch data needed daily.

    It gets the date for the last run, fetches both
    new and open data from the API, saves the raw data,
    and then saves the date of the last run after the
    data has been successfully saved to storage.
    """
    logger.info("Starting daily fetch")

    current_time = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
    since = load_last_run()

    # use current time if data is being loaded for the first time
    if not since:
        since = current_time

    try:
        logger.info("Fetching new requests since %s", since)
        new_requests = get_new_requests(since)
        logger.info("Got %d new requests", len(new_requests))
    except Exception:
        logger.exception("Failed while fetching new requests")
        raise

    try:
        logger.info("Fetching open requests")
        open_requests = get_open_requests()
        logger.info("Got %d open requests", len(open_requests))
    except Exception:
        logger.exception("Failed while fetching open requests")
        raise

    save_raw_requests(new_requests, "new")
    save_raw_requests(open_requests, "open")
    logger.info("Saved raw data locally")

    load_bronze_requests(new_requests, "new")
    load_bronze_requests(open_requests, "open")
    logger.info("Loaded data into PostgreSQL")

    save_last_run(current_time)
    logger.info("Daily fetch complete")


if __name__ == "__main__":
    run_daily_fetch()
