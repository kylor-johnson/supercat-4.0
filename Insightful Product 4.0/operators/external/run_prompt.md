# Insightful 4.0 — Run Prompt (External)

> **Purpose.** Produce a ship-ready HTML intelligence report for any org. Follow
> every step in order. Do not skip steps, reorder, or interpret the spec — the
> pipeline encodes it.

---

## Step 1 — Resolve client

Resolve the org shortname to an `organization_id`.

```sql
SELECT id, shortname, name FROM organizations WHERE shortname = '{shortname}';
```

Execute via MCP `user-supercat-postgres-vpn` → `execute_sql`.

Record:
- `{org}` = shortname (e.g. `cci`)
- `{org_id}` = id (e.g. `4`)
- `{Org_Display}` = human display name for output filename (e.g. `Currey_Company`)

---

## Step 2 — Check / populate cache

Verify `pipeline/cache/{org}/{date}/` exists and contains populated CSVs.

```bash
ls pipeline/cache/{org}/{date}/
```

If missing or empty, populate:

```bash
.venv-renderer/bin/python -m pipeline.populate_cache --org {org} --date {date}
```

**If Postgres env vars are not set locally** (no `DATABASE_URL` / `PG*` vars), populate via MCP:

1. Run each query from `pipeline/config.py` `QUERIES_ALL` via MCP `user-supercat-postgres-vpn` → `execute_sql`
2. Import results using `pipeline.cache.import_from_dicts()`

---

## Step 3 — Run pipeline

Produce the DRAFT markdown:

```bash
.venv-renderer/bin/python -m pipeline.run_report --org {org} --date {date} [--cohort-validation] [--no-narrative]
```

### Flag decision tree

| Condition | Flag |
|---|---|
| No ratified profile at `profiles/{org}.md` | Add `--cohort-validation` |
| `ANTHROPIC_API_KEY` not set in environment | Add `--no-narrative` |
| Both conditions | Add both flags |
| Ratified profile exists AND API key set | No flags needed |

### Expected output

- `outputs/{org}_DRAFT_{date}.md`
- If `--cohort-validation` fired the inline-draft path: `profiles/{org}.draft.md`

---

## Step 4 — Verify smoke_check

The CLI reports PASS or FAIL at the end of Step 3.

- **PASS** → proceed to Step 5.
- **FAIL** → read the listed issues. Fix the **template** (in `pipeline/templates/`), not the output file. Re-run Step 3.

Do not hand-edit the output markdown. The draft IS the output — if it's wrong, the template or signal logic is wrong.

---

## Step 5 — Render to HTML

### Standard run (ratified profile exists)

```bash
.venv-renderer/bin/python -m report_render.html_renderer \
    --md outputs/{org}_DRAFT_{date}.md \
    --profile profiles/{org}.md \
    --out outputs/{Org_Display}_CEO_intelligence_report_{date}.html
```

### Cohort-validation run (no ratified profile)

```bash
.venv-renderer/bin/python -m report_render.html_renderer \
    --md outputs/{org}_DRAFT_{date}.md \
    --profile profiles/{org}.draft.md \
    --out outputs/{Org_Display}_CEO_intelligence_report_{date}.html
```

---

## Step 6 — Run Step-10 audit

```bash
.venv-renderer/bin/python -m report_render.step10_check \
    --html outputs/{Org_Display}_CEO_intelligence_report_{date}.html \
    --md outputs/{org}_DRAFT_{date}.md
```

This runs checks [4], [8], [9], [11], [12] from the Step-10 ledger.

---

## Step 7 — Report result

| Outcome | Meaning | Action |
|---|---|---|
| **PASS** | All checks green | HTML is ship-ready. Done. |
| **PATCHED** | Minor issues auto-fixed by renderer | Note inherited §P violations from source MD. Ship. |
| **DEFECT** | Specific remediation needed | Name which template or signal rule to fix. Do NOT "rewrite the section." Re-run from Step 3 after fixing. |

---

## Constraints

- Do NOT spawn section agents.
- Do NOT write prose, interpret the spec, or re-author editorial content.
- Do NOT load the full canon into context (the pipeline code encodes it).
- Do NOT surgically edit the output markdown — fix templates if wrong.
- Do NOT reference frozen folders (`Insightful Product 2.0` or `3.0`).
- All file paths are relative to `Insightful Product 4.0/`.
