-- Silver layer: cleaned, typed, flattened 311 requests.
-- Built from bronze_requests, applying the Unspecified-status rule from
-- docs/decisions/001-daily-fetch-strategy.md.
CREATE TABLE IF NOT EXISTS silver_requests (
    unique_key TEXT PRIMARY KEY,
    created_date TIMESTAMPTZ,
    closed_date TIMESTAMPTZ,
    status TEXT,
    agency TEXT,
    agency_name TEXT,
    complaint_type TEXT,
    borough TEXT,
    is_open BOOLEAN
);
