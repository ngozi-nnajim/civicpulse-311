-- Gold layer: count of requests created per day, for the Daily Volumes dashboard.
CREATE TABLE IF NOT EXISTS gold_daily_volumes (
    request_date DATE PRIMARY KEY,
    request_count INTEGER
);
