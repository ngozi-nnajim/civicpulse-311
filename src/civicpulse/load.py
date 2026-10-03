"""Code that loads raw fetched data into PostgreSQL."""

import json

import psycopg

from civicpulse.config import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)


def load_bronze_requests(rows: list[dict], fetch_type: str) -> None:
    """Insert rows into the bronze_requests table.

    rows: the data fetched from the API
    fetch_type: "new" or "open", which query produced these rows
    """
    with psycopg.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    ) as conn:
        with conn.cursor() as cur:
            for row in rows:
                cur.execute(
                    """
                    INSERT INTO bronze_requests (unique_key, fetch_type, raw_data)
                    VALUES (%s, %s, %s)
                    """,
                    (row.get("unique_key"), fetch_type, json.dumps(row)),
                )
        conn.commit()
