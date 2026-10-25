## v5.8.0 — 2026-10-21

### Changed
- **Reports: moved export generation off the request path to the async worker pool.** `POST /reports/{id}/export` now enqueues a job and returns `202 Accepted` with a job handle instead of streaming the file synchronously. Clients poll `GET /jobs/{handle}` or receive a `report.export.ready` webhook. Exports > 50k rows are delivered via presigned URL (TTL 72h) by email; < 50k rows still auto-download in the UI once the job completes (typically < 10s).
- Removed the hard 120s gateway timeout workaround (`EXPORT_STREAM_CHUNKED=1`) — no longer needed.
- Export jobs are idempotent per (`report_id`, `filter_hash`, `requested_by`) for 15 min; duplicate requests return the existing job handle rather than spawning a new job.

### Fixed
- Large exports (> ~200k rows) no longer fail with 504s at the edge (#4471, #4502, #4519).
- Eliminated p99 latency spikes on the dashboard during month-end caused by export requests saturating web worker threads.

### Deprecated
- Legacy `?format=xls` export param. XLSX and CSV only from v6.0. Usage telemetry shows 0.4% of exports still on `.xls`, concentrated in 3 tenants (CS notified).

### Migration notes
- API consumers integrating directly with the export endpoint must handle 202 + polling. Direct integrations (approx. 11 tenants) have been contacted by Solutions Eng. Synchronous behaviour available behind `X-Export-Mode: sync` header until 2027-01-31, capped at 10k rows.
