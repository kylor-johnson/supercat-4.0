# Q-09: Import Health & Sync Reliability — Kindel Furniture (kkc, org_id=99)
- **Maps to**: VM-09
- **Source**: Postgres MCP (`user-supercat-postgres-vpn`) — `import_events` table
- **Run date**: 2026-04-20

## Monthly Import Trend (Last 6 Months)

| Month | Import Count |
|-------|-------------|
| April 2026 | 29 |
| October 2025 | 4 |

**Note**: No import events recorded November 2025 through March 2026 (5-month gap). Activity resumed in April 2026.

- Total import events (all-time): 1,190
- Most recent import: 2026-04-16

## Recent Import Error Check (Last 10 Events)

| Timestamp | Type | Errors |
|-----------|------|--------|
| 2026-04-16 00:24 | Images | None — `:information` only (successful image imports) |
| 2026-04-16 00:18 | Images | None — `:information` only |
| 2026-04-16 00:15 | Images | None — `:information` only |
| 2026-04-16 00:03 | Images | None — `:information` only |
| 2026-04-16 00:00 | Images | None — `:information` only |
| 2026-04-15 23:54 | Images | None — `:information` only |
| 2026-04-15 23:51 | Images | None — `:information` only |
| 2026-04-15 23:42 | Images | None — `:information` only |
| 2026-04-15 23:36 | Images | None — `:information` only |
| 2026-04-15 23:30 | Images | None — `:information` only |

**Import health**: No `:error` or `:fatal` keys found in recent import data. All recent activity is image imports (successful). Pipeline gap from Nov 2025 – Mar 2026 likely reflects account inactivity period.
