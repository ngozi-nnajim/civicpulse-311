-- Gold layer: current count of open vs closed requests.
CREATE TABLE IF NOT EXISTS gold_open_vs_closed (
    is_open BOOLEAN PRIMARY KEY,
    request_count INTEGER
);
