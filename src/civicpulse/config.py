"""Central place for tunable values used across the pipeline.

Keeping these in one file means changing a timeout, limit, or delay
only requires editing one place, not hunting through every function
that uses it.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

API_URL = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"  # The web address for the dataset
PAGE_LIMIT = 1000  # how many rows to ask for per page (the API caps this at 1000)
REQUEST_TIMEOUT_SECONDS = 30  # how long to wait for one page's response before giving up
SLEEP_BETWEEN_PAGES_SECONDS = 3  # a polite pause between pages, to avoid hammering the API

# where raw, unmodified API data lands (temporary stand-in for Blob Storage's Bronze layer)
RAW_DATA_DIR = Path("data/raw")

# Store and remember the last time this pipeline successfully ran.
LAST_RUN_FILE = Path("data/last_run.json")
LOG_FILE = Path("data/pipeline.log")
LOG_LEVEL = "INFO"  # INFO = normal progress; DEBUG = more detail; ERROR = only failures

# Postgres credentials
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
