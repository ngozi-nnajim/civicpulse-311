-- Transform bronze_requests into silver_requests.
-- Upserts so re-running this is always safe (matches the ADR's upsert strategy).
INSERT INTO silver_requests (
    unique_key, created_date, closed_date, status,
    agency, agency_name, complaint_type, borough, is_open
)
SELECT
    raw_data->>'unique_key',
    (raw_data->>'created_date')::TIMESTAMPTZ,
    (raw_data->>'closed_date')::TIMESTAMPTZ,
    raw_data->>'status',
    raw_data->>'agency',
    raw_data->>'agency_name',
    raw_data->>'complaint_type',
    raw_data->>'borough',
    CASE
    WHEN raw_data->>'closed_date' IS NOT NULL THEN FALSE
    ELSE TRUE
END
FROM bronze_requests
ON CONFLICT (unique_key) DO UPDATE SET
    closed_date = EXCLUDED.closed_date,
    status = EXCLUDED.status,
    is_open = EXCLUDED.is_open;
