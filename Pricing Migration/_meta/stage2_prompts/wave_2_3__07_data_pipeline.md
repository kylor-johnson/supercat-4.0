# Wave 2.3 — Authoring Prompt for `_root/07_data_pipeline.md`

> **For paste into a fresh Cursor agent chat as the first message.** Do not modify before pasting.
> **Drafted**: 2026-05-22 by planning agent
> **Output target**: `Pricing Migration/_root/07_data_pipeline.md` (replace stub contents)
> **Estimated authored length**: 300–500 lines
> **Dependency**: Independent. Can be authored after Wave 1 produces `_root/01` + `_root/CONTRACTS.md`. Best paired with Wave 2.1 (the segment doc references the pipeline doc, and vice versa).

---

## You are a fresh agent

You have no prior context about the SuperCat Pricing Migration. Your job is to author **one file** — `Pricing Migration/_root/07_data_pipeline.md` — using only the materials this prompt directs you to.

This is a TECHNICAL doc. Its audience is a drafter (human or agent) who needs to load account data, run live database queries, handle missing data gracefully, and write output files with consistent naming. Your job is to consolidate the mechanics — currently scattered across 3+ archived fresh-agent prompts and the handoff doc — into one definitive specification.

You will not improvise. If anything is unclear, stop and ask the operator. **Do not invent column names, query syntax, or fallback rules.**

---

## Step 1: Required reading (in this exact order)

Read each file completely. Echo each file path + last-updated date in your first chat response.

### Folder orientation (mandatory)
1. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/AGENTS.md`
2. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/00_README.md`
3. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/CONTRACTS.md`
4. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/07_data_pipeline.md` (the stub — read the "owns / does not own" boundary)

### Primary content sources — the data itself

5. **The authoritative account dataset** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_master-account-data-v6.2.csv`. Read header row in full + ~10 data rows. Identify every column. Categorize each: identity (e.g. `baseitemcode`, `account_name`), pricing (e.g. `current_mrr`, `new_mrr`, `delta_dollar`, `delta_pct`, `migration_driver`), health (e.g. `e_score`, `a_score`, `vd_score`, `oh_score`, `health_band`), flags (e.g. `support_fire`, `entity_parent`, `contract_type`), narrative (e.g. `composite_narrative` if present), and any others.

6. **The routing CSV** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/migration_comm_tiers_2026-05-19.csv`. Read header + ~10 rows. Identify fields.

7. **The HTML revenue model (for cross-check)** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_reference/migration_revenue_model_2026-05-14.html`. You do NOT need to read this in full. Read the top ~50 lines to understand the structure. The role of this file in the pipeline is **cross-check only**: when the v6.2 CSV and the HTML model disagree on a number (e.g. delta, new MRR), the v6.2 CSV wins. State that hierarchy.

### Primary content sources — the pipeline mechanics (explicitly authorized archive reads)

You ARE permitted to read these specific archive files for technical-procedure extraction. This is an explicit per-prompt override of the anti-archive rule per `_root/CONTRACTS.md` §4.

8. **Format A fresh-agent prompt** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/format-a-notices/_fresh-agent-prompt.md`. Read in full. Pay special attention to:
   - STEP 1 (loading v6.2 CSV — the Python pattern)
   - STEP 1.5 (loading the HTML model for cross-check)
   - STEP 1b (Postgres MCP queries — org_id resolution, user/login stats, order/GMV stats)
   - The fallback rules (when Postgres returns empty / errors)
   - The output-file naming conventions

9. **Format B fresh-agent prompt** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/format-b-notices/_fresh-agent-prompt.md`. Read the same steps. Where Format B's pipeline differs from Format A's, note the difference — most likely a different query or fallback for the higher-delta scenario.

10. **CEO Letter fresh-agent prompt** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/ceo-letter-notices/_fresh-agent-prompt.md`. Same.

11. **The handoff prompt** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/_handoff-prompt.md`. Read §"Data Pipeline — Three Sources for Every Brief" (around lines 89–136) and §"File Paths" (around lines 60–88).

### Do NOT read

- The full HTML model (item 7) — top of file is enough.
- Other `_root/` stubs beyond items 1–4 — your scope is `_root/07`.
- Any archived brief or template — content concerns are not pipeline concerns.

---

## Step 2: What you are authoring

`_root/07_data_pipeline.md` is the **technical specification** for how any drafter (human or agent) loads, queries, validates, and writes data for a per-account brief. The doc is dense and procedural; clarity beats brevity. Future drafters reference this doc by section number.

Author the doc as the following sections in this order:

### Section 1 — Source-of-truth hierarchy

A short, declarative subsection (~100 words) stating the resolution order when two data sources disagree:

1. **`_master-account-data-v6.2.csv`** — the authoritative roster for any per-account number (current MRR, new MRR, delta, driver, health scores, flags). If a number lives in v6.2 CSV, this is the number used.
2. **Postgres (via MCP) — live database** — the authoritative source for *current operational* data (user count, login activity, recent orders, GMV). The v6.2 CSV does NOT carry these dynamic metrics; Postgres does. State that Postgres is queried per-account at draft time, NOT batch-loaded.
3. **`migration_revenue_model_2026-05-14.html`** — the **cross-check** source. Used to validate that the math in v6.2 CSV (delta calculations, new MRR derivations) ties out. When the HTML model and v6.2 CSV disagree on a number, v6.2 CSV wins; the disagreement is logged in `_root/09_changelog.md` as a pending reconciliation.
4. **`migration_comm_tiers_2026-05-19.csv`** — the routing source. Authoritative for `comm_action` (which format a customer gets), with 5 known errata listed in `_root/02` §7. Where the routing CSV and the corrected list disagree, the corrected list wins.

State explicitly: **no number used in a brief should come from any source other than these four**. If a drafter cannot find a number in any of the four, the drafter STOPS and asks the operator. They do not estimate. They do not extrapolate.

### Section 2 — The v6.2 CSV: column-by-column field guide

A table: **Column** | **Type** | **Meaning** | **Used in** | **Notes**.

Populate from the v6.2 CSV's actual header row (item 5 above). Every column appears in this table. For each:
- **Meaning**: what the field represents (e.g. "current monthly MRR in USD as of 2026-05-XX baseline").
- **Used in**: which sections of which artifacts the field shows up in (e.g. "Format A lede dollar amount; Format B 'Before/After' table"). Where uncertain, write "[TBD — verify against templates]" and flag in the conformance block.
- **Notes**: gotchas (e.g. "this column is blank for entity-parent accounts; use child-account aggregate instead").

This is the doc a drafter reads when they need to know "what does `vd_score` mean and where do I use it?" Be comprehensive.

### Section 3 — Loading the v6.2 CSV (Python pattern, single definitive copy)

A fenced code block containing the Python pattern for loading v6.2 CSV that the archived fresh-agent prompts use. Extract from Format A prompt STEP 1 (item 8). If Format B and CEO Letter use different patterns, reconcile to a single canonical pattern and flag any meaningful differences.

```python
# Single definitive loader — extracted from archived format-a/format-b/ceo-letter STEP 1
# [Author the actual Python here — pandas, csv reader, whatever the archived prompts use]
```

Add operator notes around the code: which columns to filter by, how to slice for a single account by `baseitemcode`, what to do if the account isn't found.

### Section 4 — Postgres MCP queries

A subsection per query type. The archived fresh-agent prompts use Postgres MCP for live operational data. Extract every query referenced. For each:
- **Purpose** (e.g. "resolve org_id from baseitemcode")
- **MCP call signature** (e.g. server + tool name + arguments shape)
- **Query SQL** (verbatim from the archived prompts)
- **Expected return shape** (rows, columns)
- **Fallback if the query returns empty or errors** (e.g. "use `composite_narrative` from v6.2 CSV as substitute, log the fallback in the brief's internal routing block")

Required query subsections (extract names from archived prompts; these are the names I expect based on planning context, verify against actual archived content):

- **§4.1 — `org_id` resolution** (from `baseitemcode` to the live `org_id` in Postgres)
- **§4.2 — User and login activity** (active users in last N days, login frequency)
- **§4.3 — Order activity and GMV** (recent orders submitted through SuperCat, GMV totals)

If the archived prompts contain queries I haven't named here, ADD them as additional subsections (§4.4, §4.5, etc.) — do not omit.

### Section 5 — Fallback rules

A consolidated rules table for when the live data sources fail or return empty:

| Failure mode | Fallback | Logged where |
|---|---|---|
| Postgres `org_id` resolution returns empty | Use `composite_narrative` field from v6.2 CSV in place of operational stats | Brief's internal routing block + `_root/09_changelog.md` |
| Postgres user/login query returns empty | Suppress the lede stat sentence; use tenure + named-platform-surface fallback per `_root/04` §4.2 lede-stat-guardrail | Brief's internal routing block |
| Postgres order/GMV query returns empty | [...] | [...] |
| HTML model and v6.2 CSV disagree on a number | Use v6.2 CSV value; log the disagreement | `_root/09_changelog.md` |
| v6.2 CSV missing a required field for an account | STOP. Ask the operator. Do not infer. | Operator escalation |

Populate the table fully from archived-prompt fallback rules. Add any rules implied by archived briefs (e.g. if a brief shows "tenure stat fallback" without a user-count stat, the rule that produced that pattern belongs here).

### Section 6 — Naming conventions for output files

Source: extract from `_current-state.md` and the archived fresh-agent prompts.

The naming pattern (confirm against archives) appears to be:
- Brief: `<account_short_code>__<account_long_name>__brief.md` (e.g. `kal__kalco-allegri-crystal__brief.md`)
- Versioned re-runs: append `__v2`, `__v3` (e.g. `kal__kalco-allegri-crystal__brief__v2.md`)
- Delivery email: `<account_short_code>__<account_long_name>__delivery-email.md`
- Versioned delivery emails: same `__v2` pattern

State the pattern. Define what triggers a `__v2` (any rule change in `_root/04` / `_root/05` / `_root/03` that affects the brief's content → re-run produces `__v2`).

Output-file location:
- Format A briefs: `format-a-notices/<file>.md`
- Format B briefs: `format-b-notices/<file>.md`
- CEO Letter briefs: `ceo-letter-notices/<file>.md`
- Good News briefs: `good-news-notices/<file>.md`

### Section 7 — The required "internal routing block"

Every brief begins with an internal routing block (a Markdown blockquote that gets stripped before send). The block lists the data fields the drafter relied on. The field list is a *contract* — every brief's internal routing block contains the same fields in the same order.

Extract the canonical field list from the archived Format A / Format B / CEO Letter templates' "Internal routing note" blockquotes (visible at the top of each `_brief-template.md`). Reconcile any differences across the three formats (some fields are CEO-letter-specific, e.g. CEO call-commitment date; flag these as format-conditional fields).

Render as:

```markdown
> **Internal routing note** (remove before sending):
> Brief type: <BRIEF_TYPE> | <FORMAT>
> Account: [ACCOUNT_NAME] | Tier: [TIER] | Wave: [WAVE]
> Migration driver: [DRIVER] | Health: [SCORE] — [BAND] | Risk label: [RISK]
> Engagement: [E_SCORE] | Adoption: [A_SCORE] | Value Delivery: [VD_SCORE] | Ops Health: [OH_SCORE]
> Support fire: [YES/NO] | Behavioral floor applied: [YES/NO]
> [...format-specific fields...]
```

State: every brief's internal routing block must contain every general field listed here, plus the format-specific fields appropriate to its format. The block is the **trust artifact** — it tells a reviewer (or future agent) which data the brief was built from.

### Section 8 — File-path index

A clean Markdown table of every file the data pipeline touches:

| File | Role | Read / Write | Where it lives |
|---|---|---|---|
| `_master-account-data-v6.2.csv` | Authoritative account roster | Read | `Pricing Migration/` |
| `migration_comm_tiers_2026-05-19.csv` | Routing data | Read | `Pricing Migration/` |
| `_reference/migration_revenue_model_2026-05-14.html` | Math cross-check | Read | `Pricing Migration/_reference/` |
| Postgres (via MCP `user-supercat-postgres-vpn`) | Live operational data | Read | Remote DB |
| `format-a-notices/<account>__brief.md` | Format A brief output | Write | `Pricing Migration/format-a-notices/` |
| ... | ... | ... | ... |

Populate every input and every output. Use absolute paths where ambiguity is possible; use relative-to-`Pricing Migration/` paths where it's cleaner.

### Section 9 — What this doc does NOT own

- **Voice / tone of the content rendered from these fields** → `_root/04`
- **Per-driver narrative content (the prose) that the fields feed into** → `_root/05`
- **Which routing CSV value maps to which format folder** → `_root/06`
- **Segment definitions and account counts** → `_root/02`
- **The actual data values** — those are in the CSVs themselves; this doc is the *map* to the data, not the data

### Header block

Match the pattern:
- `> **Last updated**: 2026-05-22`
- `> **Owner**: CEO`
- `> **Primary sources**: archived format-a/format-b/ceo-letter `_fresh-agent-prompt.md` STEPs 1, 1.5, 1b (explicitly-directed extraction per `_root/CONTRACTS.md` §4); archived `_handoff-prompt.md` §Data Pipeline + §File Paths; `_master-account-data-v6.2.csv`; `migration_comm_tiers_2026-05-19.csv`; `_reference/migration_revenue_model_2026-05-14.html` (top-of-file only)`
- `> **What this doc owns** / `> **What this doc DOES NOT own**` — populate

---

## Step 3: Anti-drift discipline

- **There is one Python loader.** If the three archived fresh-agent prompts contain three slightly-different loaders, you author ONE canonical version and the discrepancies go in your conformance block as `_root/09_changelog.md` candidates.
- **Postgres queries are verbatim.** Copy SQL character-for-character from the archived prompts. Any "improvement" risks the live query failing or returning different data.
- **Field names are verbatim from v6.2 CSV.** If you reference a column, it must literally exist in the CSV header.

---

## Step 4: Voice and format constraints

- Register: technical / operator-facing. Procedural prose. Fenced code blocks for Python and SQL. Tables for column guides, fallback rules, file index.
- Where a Postgres query has parameters, mark them clearly (e.g. `WHERE org_id = :org_id` and document `:org_id` as the parameter).
- No emojis. No exhortation.

---

## Step 5: Output

Replace the entire current contents of `Pricing Migration/_root/07_data_pipeline.md` with the authored document.

Then, in your chat reply (NOT in the file), produce this conformance block:

```
─── Conformance Block ─────────────────────────────────────────
Authored: _root/07_data_pipeline.md (replaced stub)
Files read: <enumerate items 1–11 with last-updated dates>
Explicitly-authorized archive reads: 3 archived fresh-agent prompts + archived handoff §Data Pipeline + §File Paths (per Step 1 items 8–11)
Files NOT read: archived briefs/templates (content concerns); other root-doc stubs
v6.2 CSV columns documented: <count> (header has <count> columns total — should match)
Postgres queries documented: <count> + names (e.g. "§4.1 org_id resolution, §4.2 user/login, §4.3 orders/GMV, ...")
Fallback rules consolidated: <count>
Differences between Format A / B / CEO Letter pipelines (and chosen canonical): <list, or "none">
v6.2 columns referenced by other root docs but not present in CSV: <list, or "none">
Postgres queries referenced by archived prompts but missing from this doc: <list, or "none — all extracted">
Open questions for operator: <list, or "none">
─────────────────────────────────────────────────────────────
```

Then **STOP**. The operator will paste your output back for review.

---

## Step 6: If something is missing

If a Postgres query in the archived prompts is incomplete (missing parameters, ambiguous return shape), stop and ask the operator. Pipeline correctness depends on queries being executable as-stated.

If a field referenced by an archived prompt or template is missing from v6.2 CSV, flag it explicitly. It is either a stale reference (the field was removed) or a data gap (the field should exist but doesn't). Both require operator input.
