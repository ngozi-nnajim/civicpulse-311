-- Gold layer: open requests bucketed by age, for the Backlog Ageing dashboard.
CREATE TABLE IF NOT EXISTS gold_backlog_ageing (
    age_bucket TEXT PRIMARY KEY,
    request_count INTEGER
);
