INSERT INTO gold_sla_compliance (metric, request_count)
SELECT
    CASE
        WHEN closed_date - created_date <= INTERVAL '7 days' THEN 'within_sla'
        ELSE 'breached_sla'
    END,
    count(*)
FROM silver_requests
WHERE is_open = FALSE AND closed_date IS NOT NULL
GROUP BY 1
ON CONFLICT (metric) DO UPDATE SET
    request_count = EXCLUDED.request_count;
