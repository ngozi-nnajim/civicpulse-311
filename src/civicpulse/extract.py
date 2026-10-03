"""Code that talks to the NYC 311 API and brings data into the program."""

import json  # allows for reading and writing simple data as a file
from datetime import UTC, datetime  # for generating today's date, to use in the filename
from pathlib import Path

import requests  # the library that lets Python make web requests

# where raw, unmodified API data lands (temporary stand-in for Blob Storage's Bronze layer)
RAW_DATA_DIR = Path("data/raw")

# Store and remember the last time this pipeline successfully ran.
LAST_RUN_FILE = Path("data/last_run.json")

# The web address for the dataset
API_URL = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"


def get_requests(limit: int = 5) -> list[dict]:
    """Ask the API for some rows of 311 data and return them.

    limit: how many rows to ask for.
    Returns: a list of rows, where each row is a dictionary.
    """
    response = requests.get(
        API_URL,
        params={"$limit": limit},  # this becomes ?$limit=5 in the actual web address
        timeout=30,  # give up after 30 seconds instead of hanging forever
    )
    response.raise_for_status()  # if the server sent back an error, stop here and say so
    return response.json()  # turn the API's text reply into Python lists/dictionaries


def get_new_requests(since: str, limit: int = 1000) -> list[dict]:
    """Ask the API for requests created after a given point in time.

    since: a date/time string, e.g. "2026-09-29T00:00:00.000"
    limit: how many rows to ask for at once (the API caps this at 1000)
    Returns: a list of rows, where each row is a dictionary.
    """
    response = requests.get(
        API_URL,
        params={
            "$where": f"created_date > '{since}'",  # only rows created after "since"
            "$limit": limit,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def get_open_requests(limit: int = 1000) -> list[dict]:
    """Ask the API for every request that isn't Closed yet.

    limit: how many rows to ask for at once (the API caps this at 1000 anyway)
    Returns: a list of rows, where each row is a dictionary.
    """
    response = requests.get(
        API_URL,
        params={
            # anything not Closed: Open, Assigned, In Progress, etc.
            "$where": "status != 'Closed'",
            "$limit": limit,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def save_last_run(timestamp: str) -> None:
    """Remember the time of this run, so tomorrow's run knows where to start from.

    timestamp: a date/time string, e.g. "2026-09-29T00:00:00.000"
    """
    # make the "data" folder if it doesn't exist yet
    LAST_RUN_FILE.parent.mkdir(parents=True, exist_ok=True)
    LAST_RUN_FILE.write_text(json.dumps({"last_run": timestamp}))


def load_last_run() -> str | None:
    """Read back the last remembered run time, if one exists.

    Returns: the timestamp string, or None if the pipeline has never run before.
    """
    if not LAST_RUN_FILE.exists():
        return None  # first time ever running, nothing to go on yet
    data = json.loads(LAST_RUN_FILE.read_text())
    return data["last_run"]


def save_raw_requests(rows: list[dict], label: str) -> Path:
    """Save fetched rows to a local file, named by today's date and a label.

    rows: the data gotten from the API, exactly as received
    label: what kind of fetch this was, e.g. "new" or "open"
    Returns: the path of the file just written, useful for logging or tests
    """
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    today = datetime.now(UTC).strftime("%Y-%m-%d")  # e.g. "2026-09-30"
    file_path = RAW_DATA_DIR / f"{today}-{label}.json"

    file_path.write_text(json.dumps(rows))
    return file_path
