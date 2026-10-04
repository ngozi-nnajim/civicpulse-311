-- Gold layer: SLA compliance (resolved within 7 days) for closed requests.
CREATE TABLE IF NOT EXISTS gold_sla_compliance (
    metric TEXT PRIMARY KEY,
    request_count INTEGER
);
