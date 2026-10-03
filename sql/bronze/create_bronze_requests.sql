-- Bronze layer: raw, unmodified 311 request data, exactly as the API returned it.
-- Each row is one fetch of one request (new or open), tagged by type and time.
CREATE TABLE IF NOT EXISTS bronze_requests (
    unique_key TEXT,
    fetch_type TEXT,
    fetched_at TIMESTAMPTZ DEFAULT now(),
    raw_data JSONB
);
