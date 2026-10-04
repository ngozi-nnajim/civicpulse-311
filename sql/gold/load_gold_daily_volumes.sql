-- Rebuild daily volumes from silver_requests.
-- Full rebuild (not incremental) since this is a simple aggregate over all data.
INSERT INTO gold_daily_volumes (request_date, request_count)
SELECT
    created_date::DATE,
    count(*)
FROM silver_requests
GROUP BY created_date::DATE
ON CONFLICT (request_date) DO UPDATE SET
    request_count = EXCLUDED.request_count;
