---
name: ecat-admin-write
description: Apply a change to a live SuperCat org through the Admin Console's own Rails endpoints as a logged-in user — Library files and folders, mobile site / portal splash images, collections and taxonomies, user-group authorization, item ordering. Use whenever the ask is to CHANGE an org rather than report on it ("upload this logo", "add these files to the Library", "rename/reorder/remove that folder", "the reps' iPads aren't seeing it"). The read-only Postgres MCP does NOT block these writes and is not a reason to decline — app-layer writes are the correct path, not a workaround. Credentials are already on disk; never ask the user for them.
---

# eCat Admin Write (consultant-only)

Answers one question for one org:

> **How do I actually apply this change so it reaches the reps?**

## 0. Read this before reaching for SQL, and before saying a write is impossible

Changes go through the Rails controllers **as a logged-in user**, because the controllers
fire callbacks the database does not:

- `SharedResourcesController` calls `force_org_users_synch!` on create/update/destroy. That
  is the thing that pushes a Library change to reps' iPads. A direct SQL `UPDATE` skips it
  and leaves every device stale — the change is in the database and invisible in the field.
- Positional models use `acts_as_list`. Writing rows directly corrupts `position` for every
  sibling.

So the read-only `supercat-postgres-vpn` MCP is **not an obstacle being worked around.** It
is the read half of a correct split:

| Need | Use |
|---|---|
| Find out what is wrong / verify what changed | `supercat-postgres-vpn` (SELECT) |
| Change it | this skill (Rails controllers) |

`ecat-postgres-audit` and `ecat-config-check` are read-only *by design, for auditing*. Their
read-only framing is not a statement that org changes are impossible. Do not tell the user a
change cannot be made because Postgres is read-only — that conflates the two halves.

## 1. Credentials — never ask for them

Username and password live at `~/.supercat/mcp-credentials.json` (mode 0600), read by
`credentials()` in `supercat_admin.py`.

- **Never** prompt the user for a password.
- **Never** accept one pasted into chat. If one is pasted anyway, do not write it to a file,
  and tell the user to rotate it — a chat transcript is a disclosure.
- **Never** inline a secret into a command line or an inline env var: it lands in shell
  history and is visible in the process table to every other user on the machine. Read from
  the file inside the script instead.

## 2. The client

Use `supercat_admin.py` (next to this file). Do not hand-roll a fourth copy of the login
dance — three already exist under `Legrand/Build/` and have started to drift.

```python
import sys
sys.path.insert(0, os.path.expanduser("~/.claude/skills/ecat-admin-write"))
from supercat_admin import Admin

adm = Admin("leg", dry_run=not args.go).login()
res = adm.post("/shared_resources", {...})
print(res.explain())
```

Auth sequence, handled by `.login()`: GET `/supercat/sessions/new` → scrape
`authenticity_token` → POST `/supercat/sessions` → cookie held in the session jar. A fresh
CSRF token is scraped per mutating request.

## 3. Two response traps

Both are already-paid-for lessons. They are the reason a write can look successful and not be.

### 3.1 A failed login returns HTTP 200

`raise_for_status()` will not catch it — you get the login page back with a 200. Detect by
landing URL and flash text:

```python
if "sessions/new" in r.url or "Invalid" in r.text[:4000]:
```

### 3.2 With `allow_redirects=True`, the status is the *landing page's*, not the write's

A `200` frequently means "the index page rendered fine", while the PATCH itself was a 302 you
never saw. `#update` redirects to the index only when `save` returned true; on failure it
re-renders `:edit`. **Success is proven by the redirect target, not the status code.**
`WriteResult.ok` in the client encodes this: `status < 400` **and** the landing URL does not
end in `/edit` or `/new`.

## 4. Strong params silently wipe omitted fields

`shared_resource_params` applies `.with_defaults(user_type_ids: [])`. A PATCH that sends only
`label` therefore **clears every user-group assignment on that row.**

The general rule: **on a PATCH, re-submit the fields you intend to keep**, not just the one
you are changing. Read the edit form first and echo back the current values. Two live
examples of this being handled correctly:

- `rename()` in `rebuild_library.py` re-reads `/shared_resources/:id/edit` and re-submits the
  checked `user_type_ids[]`.
- The `fal` splash-image upload re-submitted `mobile_site[logo_url]` unchanged.

## 5. Route inventory

Verified against `config/routes.rb` and `rebuild_library.py`. Routes are scoped under
`/:organization_shortname`. Rails receives PATCH/DELETE as a POST carrying `_method` in the
body — the client does this for you.

| Method | Route | Purpose |
|---|---|---|
| POST | `/supercat/sessions` | login (not org-scoped) |
| POST | `/<org>/shared_resources` | create — `resource_type=directory\|link\|file` |
| DELETE | `/<org>/shared_resources/:id` | destroy |
| POST | `/<org>/shared_resources/move_to_directory` | reparent |
| POST | `/<org>/shared_resources/update_entry_positions` | reorder |
| PATCH | `/<org>/user_types/:id` | user-group authorization |
| PATCH | `/<org>/mobile_sites/:id` | mobile site, incl. splash image (multipart) |
| POST/PATCH/DELETE | `/<org>/trade_names/:tid/collections[/:id]` | collections / taxonomy |

Permitted `shared_resource` params (`shared_resources_controller.rb:201`): `parent_id`,
`value`, `label`, `shareable`, `interaction_mode`, `user_type_ids[]`.

- `directory` → `value` is the folder name
- `link` → `value` is the URL, `label` is the display name
- `file` → multipart `the_file` + `label`

`move_to_directory` takes `moved_child_ids[]`, `parent_id`, and `ids[]` — where `ids[]` is the
destination's **full ordering including the moved entry**, because the model sets
`position = ids.index(entry.id) + 1`. Send a partial list and you scramble the folder.

## 6. Blast radius

**Creates, updates and uploads run without stopping.** Dry-run, execute, verify, report. No
confirmation prompts, no credential requests, no debate about read-only Postgres.

**Bulk deletes and bulk moves stop.** At `BULK_THRESHOLD` (3) rows or more, `adm.destructive()`
requires a snapshot taken this run *and* an explicit `confirmed=True`. It prints the target
list and exits otherwise.

This is not general caution — it is scoped to one shape of operation. A prior session moved 55
items and deleted 13 directories from a live client Library in one run. It came out clean
*because* that session chose to snapshot first (`library_snapshot_pre_merge_2026-08-31.txt`);
nothing required it. Now something does.

Always dump current state before a destructive step:

```python
adm.snapshot("library", adm.get_text("/shared_resources"))
adm.destructive(doomed_ids, confirmed=args.confirm)
```

## 7. Verification is mandatory

`WriteResult.ok` means Rails accepted the form. It does not mean the column holds what you
intended. After every write:

1. **SELECT the row** through `supercat-postgres-vpn` and print before/after —
   `Admin.verify_sql(table, row_id, org_id)`.
2. **Pull the `log_change!` row** — `Admin.audit_sql(...)`. The controller writes it on
   success, so it is server-side proof independent of anything the script says about itself.
   Confirm the `change_logs` table and column names against the schema the first time.
3. For file uploads, fetch the resulting asset URL and check `content-type` and byte count
   against the source.

Report the before/after table. "HTTP 200" is not a result.

## 8. Script conventions

Every write script follows the shape already established under `Legrand/Build/`:

- **Dry-run is the default.** Nothing mutates without `--go`.
- `--only <key>` / `--step <name>` to run one item at a time and check Admin between steps.
- **Idempotent** — skip an item already present rather than creating a duplicate.
- The plan is **data at the top of the file**, separate from execution.
- Order a batch smallest-first so any size ceiling shows up cheaply.
- Print the resolved URL and params for each call, executed or not.

## 9. Where this sits

| Task | Skill |
|---|---|
| What is wrong with this org's config? | `ecat-config-check` |
| What is the org's data/import state? | `ecat-postgres-audit` |
| **Apply the fix** | **this skill** |
| What `mobile_sites` / portal settings mean | `ecat-online` |
| Catalog data changes (products, customers, pricing) | the import pipeline — `ecat-core-files`, not this skill |

**Catalog data goes through imports, not here.** Products, customers, inventory and stories
are CSV + SFTP + the scheduled importer (`ecat-core-files`, `ecat-images-ftp`). This skill is
for configuration and content the Admin Console owns.

## 10. Attribution

These writes authenticate as a real named user, so they land in `change_logs` indistinguishable
from manual work. If a change may later be questioned by the client, say in the handoff that it
was applied programmatically and name the snapshot file.
