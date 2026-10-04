INSERT INTO gold_backlog_ageing (age_bucket, request_count)
SELECT
    CASE
        WHEN now() - created_date <= INTERVAL '7 days' THEN '0-7 days'
        WHEN now() - created_date <= INTERVAL '30 days' THEN '8-30 days'
        ELSE '30+ days'
    END,
    count(*)
FROM silver_requests
WHERE is_open = TRUE
GROUP BY 1
ON CONFLICT (age_bucket) DO UPDATE SET
    request_count = EXCLUDED.request_count;
