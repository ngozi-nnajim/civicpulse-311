# NYC 311 data notes

## Source
**Dataset name:** 311 Service Requests from 2020 to Present.

**Not used:** The 2010-2019 data is a separate dataset (ID 76ig-c548). This project uses 2020 onwards only.

**ID:** erm2-nwe9

**API addresses:**
- https://data.cityofnewyork.us/resource/erm2-nwe9.json (works without a key)
- https://data.cityofnewyork.us/api/v3/views/erm2-nwe9/query.json (newer address that needs a key)

The key-free address is not officially promised to last, so it may change.

## Size and limits
As of 28 Sep 2026, there are roughly `22614877 rows` in the data. However, the API returns `1,000 rows` at once by default.

## Important fields
- `unique_key`: a unique ID for each request.
- `created_date`: date a request was created.
- `closed_date`: date a request was closed.
- `status`: status of the request (e.g. "Open", "In Progress", "Closed")
- `agency`: the department responsible for handling the request (e.g. NYPD, Department of Transportation, etc.).
- `complaint_type`: what kind of complaint it is.
- `borough`: what borough the complaint address falls under.

## Things that surprised me
- Missing fields are completely excluded from the returned json files.
- All data arrives as text, including dates.
- The `"location"` field is a nested object and needs to be flattened.
- `"computed_region"` fields (probably platform-added map labels, not needed for now)
- The website says the lists of expected values are not exhaustive, so new statuses may appear later.
- In the rows I checked, `resolution_action_updated_date` is sometimes earlier than `created_date`, so it can't be trusted. Don't use it in calculations.
- Some old requests have no `closed_date`. One `Unspecified` example from May 2020 was still unclosed, so the oldest Backlog Ageing bucket will contain very old requests.

## Status values
As of 28 Sep 2026, there are `eight (8) statuses` available, and they have the following counts:
- `"Assigned"`: 24466
- `"Cancel"`: 1
- `"Closed"`: 22151712
- `"In Progress"`: 284181
- `"Open"`: 83576
- `"Pending"`: 63269
- `"Started"`: 4844
- `"Unspecified"`: 2828

## My definitions (draft)
- For this project, statuses that count as "open" include: `"Assigned"`, `"In Progress"`, `"Open"`, `"Pending"` and `"Started"`.

- How long it took for a request to close would be measured using the difference between the `"closed_date"` and the `"created_date"`. This only works for closed requests. For open ones, it is measured from `"created_date"` to today.

- `Cancel` and `Unspecified` requests: `Cancel` requests would be left out of the count because they were neither worked on nor finished. `Unspecified` requests with a `"closed_date"` would be counted as `"Closed"`, while those with no `"closed_date"` would be counted as `"Open"`. A count on 28 Sep 2026 found 100 Unspecified requests with no closed_date, so both parts of this rule are needed.

- **Watch out:** `Unspecified` is a mixed group. In small samples, some rows were closed in seconds with "no action needed" messages, and others were closed with real work done. 100 have no `closed_date` at all (as of 28 Sep 2026). Decide later (in the Gold layer) whether to exclude them from time-to-close and SLA numbers.
