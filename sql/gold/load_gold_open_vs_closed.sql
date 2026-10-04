INSERT INTO gold_open_vs_closed (is_open, request_count)
SELECT
    is_open,
    count(*)
FROM silver_requests
GROUP BY is_open
ON CONFLICT (is_open) DO UPDATE SET
    request_count = EXCLUDED.request_count;
