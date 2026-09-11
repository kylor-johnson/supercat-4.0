---
name: supercat-mcp-access
description: How to change data in a live SuperCat client org. MCP is read-only (Postgres = SELECT only), but writes ARE possible via Admin Console HTTP automation logged in as Kylor_Johnson with ~/.supercat/mcp-credentials.json. Includes the entity-to-endpoint map (library items, user territories, user groups, categories, collections), the dry-run/one-step-at-a-time safety pattern, the carry-forward rule for regenerated import files, and the traps that have already cost time. Use for ANY live-org change — library, users, groups, territories, taxonomy — and for diagnosing the "Postgres queries hang forever" wedged-session failure. Never tell the user writes are impossible; script them against the Rails endpoints.
---

# SuperCat MCP access — verified capability map

Verified 2026-08-17 by reading the configs and server source directly. Re-verify if
the MCP config changes.

## Short version

**Every SuperCat MCP tool is read-only — but writes ARE possible, just not via MCP.**

- **Reads** → `supercat-postgres-vpn` (`execute_sql`, SELECT only)
- **Writes** → **Admin Console HTTP automation** over HTTPS, logged in as
  `Kylor_Johnson` with the credentials in `~/.supercat/mcp-credentials.json`
- **Product/taxonomy changes** → regenerate the CSV and import
- **Verification after a write** → back to Postgres

Do not tell the user writes are impossible. They are not. There is simply no MCP
tool for them — you script them against the Rails app's own endpoints (below).

## The servers

### `supercat-postgres-vpn` — active, read-only

```json
"supercat-postgres-vpn": {
  "command": "npx",
  "args": ["-y", "mcp-remote",
           "https://mcp-postgres-tools.tools.supercatsolutions.com/sse"]
}
```

A thin `mcp-remote` proxy to a **remote** MCP server. Tools are defined server-side:

`execute_sql` (read-only) · `explain_query` · `list_objects` · `list_schemas` ·
`get_object_details` · `get_top_queries` · `analyze_db_health` ·
`analyze_query_indexes` · `analyze_workload_indexes`

Read-only is the **remote server's** contract. No local config edit changes it.
Cursor used the identical endpoint — this never behaved differently there.

### `supercat-cs-tools` — RETIRED, and was also read-only

```json
"supercat-cs-tools": {
  "command": "node",
  "args": ["/Users/kylorjohnson/supercat-code/supercat_server/bin/mcp-server"]
}
```

Present in `~/.cursor/mcp.json`, absent from Claude Code. Reads
`~/.supercat/mcp-credentials.json` (`{username, password, api_base}`) and calls the
Rails MCP API over HTTP Basic auth.

**All 27 tools are `get_*`, `search_data`, or `analyze_*`.** The one `POST` in the
source is how `search_data` sends its request body — not a write operation.

`SuperCat 4.0/CLAUDE.md` says: *"Never use supercat-cs-tools (retired)."* Use
`supercat-postgres-vpn` or `bigquery-admin` instead.

## THE WRITE PATH — Admin Console automation over HTTPS

`~/.supercat/mcp-credentials.json` holds `{username, password, api_base}` —
username `Kylor_Johnson`. Those are the **SuperCat login**, usable both for the
retired Rails MCP API and for an Admin Console session. This is how Library edits
have been done before.

Log in, then drive the app's real endpoints. Because these go through the Rails
controllers, `force_org_users_synch!` fires and `acts_as_list` keeps positions
correct — which raw SQL would not.

```
POST   /supercat/sessions                        username, password, authenticity_token
POST   /<org>/shared_resources                   resource_type=directory|link|file
DELETE /<org>/shared_resources/:id
PATCH  /<org>/shared_resources/:id
POST   /<org>/shared_resources/move_to_directory      entry_id, directory_id, ids[]
POST   /<org>/shared_resources/update_entry_positions
POST   /<org>/shared_resources/reorder_directories
PATCH  /<org>/user_types/:id                     user-group auth
```

Permitted `shared_resource` params (`shared_resources_controller.rb:201`):
`parent_id, value, label, shareable, interaction_mode, user_type_ids[]`
- **directory** → `value` is the folder name (directories have no `label`)
- **link** → `value` is the URL, `label` is the display name
- **file** → multipart `the_file` + `label`

Every page requires a Rails `authenticity_token` scraped from a prior GET.

**Working reference implementation:**
`SuperCat_Simple_Final/02_Implementation/Legrand/Build/rebuild_library.py`
— dry-run by default, `--go` to apply, one `--step` at a time.

Use Postgres afterward to verify.

## Fixing "Postgres queries hang forever"

Symptom: queries return fast early in a session, then stall — 120s backgrounding,
then a 1800s idle-timeout failure.

**Diagnose first — this is usually NOT the VPN:**

```bash
curl -s -o /dev/null -w "HTTP %{http_code} connect=%{time_connect}s\n" \
  --max-time 12 https://mcp-postgres-tools.tools.supercatsolutions.com/sse
```

`HTTP 200` with a fast connect = host is up; the SSE stream stays open, so hitting
`--max-time` is expected and fine.

- **Host reachable + queries hang** → the `mcp-remote` proxy session is wedged.
  **Restart Claude Code, or reconnect via `/mcp`.** Nothing to fix in config.
- **Connect fails / times out** → genuine VPN or host problem.

For long silent runs, `CLAUDE_CODE_MCP_TOOL_IDLE_TIMEOUT` (ms) raises the global
idle limit; a per-server `"timeout"` in MCP settings does it for one server only.

## Even with DB write access, do not write to these tables

Independent of permissions — direct SQL bypasses Rails and corrupts state:

| Table | Why raw SQL breaks it |
|---|---|
| `shared_resources` | `shared_resources_controller.rb:79` calls `force_org_users_synch!` on save — that is what pushes Library changes to reps' iPads. Skipping it leaves the DB correct and devices stale. Also `acts_as_list` manages `position` scoped to `(organization_id, parent_id)`; hand-set positions corrupt ordering. |
| `user_types` | `*_auth` fields are `'a'`/`'n'`/`'c'` (All/None/Selected). Setting `'c'` without populating the join tables silently hides everything from that group. |
| `products` / `taxonomies` | Owned by the importer. Hand-edits make the build non-reproducible — this already happened on Legrand (`COL1`–`COL10` + a `Hideable` column injected post-generation). |

## What to do instead

| Task | Correct route |
|---|---|
| Create/delete/move Library items | Admin Console → Library |
| User-group Library or price-level auth | Admin Console → User Groups |
| Territory codes on users | Admin Console → Users |
| Product/taxonomy changes | Regenerate the CSV → import → verify in Tools → Admin Reports → File Import Status |
| Anything read-only | `supercat-postgres-vpn` (or `bigquery-admin` for warehouse data) |

Blue-link timestamp in File Import Status = the import had problems; click it for
line numbers.

---

# Working in a live client org — general playbook

The Library was the first case; the pattern generalizes to any Admin-managed entity.
Verified end to end on Legrand (`leg`) 2026-08-17/18: 5 deletes, 24 directory creates,
110 moves, 28 renames, 3 relocations, 16 file uploads, 3 link creates — zero rollbacks.

## The pattern

1. **Read first, from the DB.** Establish current state with `execute_sql` before
   touching anything. Counts, IDs, current values.
2. **Write through the app, never the DB.** Log in and drive the real Admin endpoints
   so callbacks and list-position management run.
3. **Script it as a reviewed artifact with a data-only plan block** at the top. Never
   an ad-hoc inline heredoc that mutates production — the permission classifier
   blocks those, correctly.
4. **Dry-run by default.** Nothing mutates without an explicit `--go`.
5. **One `--step` at a time**, with a cheap verification between steps.
6. **Verify current state immediately before writing.** On Legrand, six users' territory
   codes turned out to be already correct — checking first avoided six pointless writes.
7. **Idempotent steps.** Skip items already in the target state so a re-run is safe.
8. **Guard destructive steps.** The `cleanup` step only deleted a directory if it was
   both a known legacy folder AND had zero children.

## Entity → endpoint map (routes verified in config/routes.rb)

| Entity | Endpoints | Notes |
|---|---|---|
| Library items | `POST/PATCH/DELETE /<org>/shared_resources[/:id]`, `POST .../move_to_directory` | `move_to_directory` wants `moved_child_ids[]`, `parent_id`, `ids[]` — where `ids` is the destination's full ordering *including* the moved item |
| User territories | `PATCH /<org>/org_users/:id` | `territory_codes` is a **top-level** comma-joined param, NOT nested under `org_user[]` |
| User groups | `PATCH /<org>/user_types/:id` | `*_auth` fields are `'a'`/`'n'`/`'c'` = All/None/Selected |
| Categories | `/<org>/categories` | |
| Collections | `/<org>/trade_names/:id/collections` | scoped per trade name — the same collection name gets a separate code per brand |
| Products / taxonomy | **CSV import only** | never hand-edit; regenerate from the build script |

Login: `POST /supercat/sessions` with `username`, `password`, `authenticity_token`.
Every mutating request needs an `authenticity_token` scraped from a prior GET.

## Traps that cost real time on Legrand

- **`.with_defaults(user_type_ids: [])`** on `shared_resource_params`: a label-only
  PATCH will wipe per-item user-group assignments unless you re-read and resubmit them.
- **Stubbed steps that only print.** Three steps (`links`, `upload`, `territories`)
  printed success without calling the API. Always verify the resulting state, never
  trust the log line.
- **Attribute order in form HTML** is `value=` then `name=` — regexes assuming the
  reverse silently match nothing, which then looks like "no existing value."
- **HTML entities in labels** — `Catalogs &amp; Brochures` breaks exact-match lookups.
  Unescape before comparing.
- **Orphaned `mcp-remote` processes survive Cmd+Q.** A wedged Postgres session persists
  across an app restart; find and kill the stale PIDs (`ps aux | grep mcp-remote`).
- **Verify a claim before stating it.** A regenerated products.csv silently blanked
  `ImageFileName` on 19 products that had live images; a diff against the last
  known-good file caught it. Diff generated output against the file that produced the
  current live state, every time.

## Carry-forward rule for regenerated import files

If the live file contains values the generator cannot derive (Legrand: `Hideable`,
plus `ImageFileName` for images uploaded after the last build), preserve the last
known-good file and carry those columns forward by key. Otherwise regeneration
silently destroys data. Then diff: the only differences should be the ones intended.

## Reference implementation

`SuperCat_Simple_Final/02_Implementation/Legrand/Build/rebuild_library.py`
