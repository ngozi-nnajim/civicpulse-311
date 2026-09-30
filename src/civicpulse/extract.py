"""Code that talks to the NYC 311 API and brings data into the program."""

import requests  # the library that lets Python make web requests

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
