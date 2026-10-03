# 001: Daily fetch strategy

## Context
The API has no reliable way to fetch only new and changed requests each day. The `"resolution_action_updated_date"` field was considered, however, upon investigation, it was found that it can be earlier than `"created_date"` on the same row, which makes no sense for a `"last updated"` field.

## Decision
Since there is no reliable way to check what changed `("last updated")`, I decided to fetch two separate things everyday:

1. `Brand-new requests` — filtered by `"created_date"` being after the last run. This field is trustworthy because it is set once when a request is created and never edited.

2. Every request that isn't Closed yet — i.e. re-fetch all requests that are not closed yet, regardless of when they were created, because any one of them could have changed status since they were last observed as there is no way to know which ones without checking.

## Why not just re-fetch everything daily?
Re-fetching about `460,000` rows of requests with a `non-closed status` is more realistic than re-fetching all the data with about `22.6 million rows`.

## Consequences
Two queries are needed as outlined in `Decision` above (Query for `Brand-new requests` where `"created_date"` is after the last run, and query for `Re-fetch` all `non-closed` statuses regardless of when they were created.)

When a row that already exists is fetched (say, a request that moved from Open to Assigned), its existing copy would need to be updated, not added as a duplicate. This only works because every request has a unique_key. This kind of "update if it exists, insert if it's new" operation is called an upsert.

## Implementation
The `get_open_requests` function fetches data for all statuses that are not Closed, including all Unspecified rows, regardless of closed_date.

This is intentional because it is important to keep re-checking `Unspecified` rows until their status becomes `Closed`, so that a row transitioning from `no-closed_date` to having one is not missed or left out.

The actual open/closed interpretation for `Unspecified` happens later, in SQL, not in this fetch. This way, the extraction code stays intact in an event where the rules for `Unspecified` changes; only the SQL query changes.

## When to record the last run
`save_last_run` must only be called after data has been successfully saved to Blob Storage, not before or during the fetch. If it were called earlier and the save to Blob Storage step failed, those rows would be lost forever, it would be wrongly assumed that the new rows for that time period have been saved when they've not. Calling it only after success means a failed run just gets retried tomorrow, safe because loading uses an upsert, so repeating a row causes no harm, as the row is updated not duplicated.

## Open questions
There needs to be a way to remember when the last run was to determine how far back to search for new requests. It is not yet decided where this information should be stored.

## Known limitations
1. The functions to get new and open requests (`get_new_requests`, and `get_open_requests`) have a limit of 1000 rows returned per request which mirrors the API's own threshold. If more than 1000 new or open requests exist since the last check, only the first 1000 are fetched, the rest are silently dropped and lost forever, since `since` moves forward past them once `save_last_run` runs.

2. The pipeline currently doesn't have logging to record progress. If it fails partway through, there is no way to know what failed, where the failure came from and when it happened.
