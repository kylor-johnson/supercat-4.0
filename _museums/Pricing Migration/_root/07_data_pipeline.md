# 07 — Data Pipeline

> **What this doc owns**: Source-of-truth hierarchy across the four data inputs. Canonical Python loaders (one definitive copy for v6.2 CSV; one for HTML model cross-check). Postgres MCP queries (`org_id` resolution; user/login activity; eCat order/GMV activity). Fallback rules when a live source fails. Naming conventions for brief and delivery-email output files. The canonical field list every brief's internal routing block must contain. File-path index of every input the pipeline reads and every output it writes.
>
> **What this doc DOES NOT own**: How to render data in copy (`_root/04` voice; `_root/05` driver framing). Which fields gate which content (`_root/08` quality bar). The mapping from `comm_action` to format folder (`_root/06`). Segment definitions and counts (`_root/02`). The actual data values — those live in the CSVs.
>
> **Last updated**: 2026-05-26 (**CL-028 RESOLVED at §4.5 source** — Stage 4.2 sca v2 cohort iter 3 audit 2026-05-26 surfaced rule-vs-operationalization drift between §4.5 prose "(or the dollar discrepancy exceeds $60/month)" parenthetical and `_meta/v6_2_reconciliation_log.md` line 21 AND-discipline methodology. Operator-stamped `resolve_now_AND_canonical` 2026-05-26: §4.5 prose tightened from ambiguous "(or …)" parenthetical to explicit "AND the dollar discrepancy exceeds $60/month"; closing parenthetical added documenting the resolution; sweep result unchanged at 37 flagged. Prior 2026-05-26 entry: Wave 6 batch — §7.5 added: per-format delivery-email routing-block subset matrix codified across all 5 Stage 3 templates [Format A, Format B, CEO Letter, Good-News Notice, entity-packet parent-letter cover email]; CL-022 inferred-subset state CLOSED at rule layer; prior Stage 3 delivery-email templates' `CL-022 note` blockquotes retained as template-scaffolding audit-trail of the pre-§7.5 inference pattern. Prior 2026-05-26 entry: Stage 4.1 lpf production proof closeout — §4.5 Resolution discipline paragraph appended (CL-025 RESOLVED at source). Prior: 2026-05-22.)
> **Owner**: CEO
> **Primary sources**: archived `format-a-notices/_fresh-agent-prompt.md`, `format-b-notices/_fresh-agent-prompt.md`, `ceo-letter-notices/_fresh-agent-prompt.md` STEPs 1, 1.5, 1b (explicitly-directed extraction per `_root/CONTRACTS.md` §4); archived `_handoff-prompt.md` §Data Pipeline + §File Paths; `_master-account-data-v6.2.csv` (header + sample rows); `migration_comm_tiers_2026-05-19.csv` (header + sample rows); `_reference/migration_revenue_model_2026-05-14.html` (top-of-file only, per Wave 2.3 prompt §7); for §7.5 — the 5 Stage 3 delivery-email templates (`format-a-notices/_delivery-email-template.md`, `format-b-notices/_delivery-email-template.md`, `ceo-letter-notices/_delivery-email-template.md`, `good-news-notices/_delivery-email-template.md`, `entity-packets/_parent-letter-delivery-email-template.md`) Section 2 routing blocks (operator-approved across Stage 3.1 → 3.5 review passes 2026-05-26 — `_root/09_changelog.md`).

---

## §1. Source-of-truth hierarchy

Four data sources feed every per-account brief. They resolve in this order when two disagree:

1. **`_master-account-data-v6.2.csv`** — authoritative roster. Owns every per-account number (`current_mrr`, `new_total_mrr`, `delta_mrr`, `delta_pct`, `migration_driver`, `secondary_drivers`, health scores, `support_fire`, `composite_narrative`, all pricing-breakdown fields). **If a number lives in v6.2 CSV, this is the number used.**

2. **Postgres (via MCP `user-supercat-postgres-vpn`)** — live operational data. Owns dynamic metrics the v6.2 CSV does not carry: `active_org_users`, `logged_in_90d`, `total_logins_90d`, `ltm_orders`, `ltm_gmv`, `ltm_customers_served`. Queried per-account at draft time, never batch-loaded.

3. **`_reference/migration_revenue_model_2026-05-14.html`** — cross-check only. Used to validate that v6.2 CSV math (delta calculations, new MRR derivations) ties out. **When the HTML model and v6.2 CSV disagree on any number, v6.2 CSV wins.** The disagreement is logged in `_root/09_changelog.md` as a pending reconciliation. The HTML model uses abbreviated keys (`cm`, `nm`, `dm`, `dp`, `t`, `d`, `tb`, `iu`, `eu`, `uc`, `hs`, `hb`, `c`, `mc`, `dt`, `cy`, `oid`, `s`); these are not interchangeable with v6.2 CSV column names — see §2.

4. **`migration_comm_tiers_2026-05-19.csv`** — routing source. Authoritative for `comm_action` (which format a customer gets). Known errata listed in `_root/02` §7; where the routing CSV and the corrected list disagree, the corrected list wins.

**No number used in a brief comes from any source other than these four.** If a drafter cannot find a number in any of the four, the drafter **STOPS** and asks the operator per `_root/CONTRACTS.md` §2. They do not estimate. They do not extrapolate.

---

## §2. The v6.2 CSV — column-by-column field guide

The CSV file at `_master-account-data-v6.2.csv` opens with one blank line (all commas), then a header row, then one data row per account. The Python loader in §3 skips the blank line and treats the second line as headers.

The primary key is **`ord_id`** (3–6 character org shortname, e.g. `kal`, `cci`, `shl`). It is the join key into Postgres (`organizations.shortname`) and the HTML model (`oid`).

| Column | Type | Meaning | Used in | Notes |
|---|---|---|---|---|
| `company` | string | Account display name | Brief title, lede, delivery email subject | Source-of-truth for the human-readable name; never construct from `ord_id` |
| `parent_entity` | string | Parent corporate entity | Routing block; entity-gating decisions (`_root/02` §entity-rule) | Blank for standalone accounts |
| `billing_entity` | string | Entity that receives the invoice | Routing block; delivery routing | When non-blank and ≠ `company`, route notice to `billing_entity` contact (see `shl` → Progressive Lighting) |
| `paying_entity` | string | Entity legally paying | Routing block | Usually equals `billing_entity` |
| `ord_id` | string | Org shortname; primary key | Every join (Postgres `organizations.shortname`, HTML model `oid`), file naming | Lowercase; matches Postgres exactly |
| `cohort_year` | int | Year account first onboarded | Routing block `Cohort`; tenure-paragraph gating in lede (`_root/04`) | Pre-2016 = early adopter; tenure acknowledgment required per `_root/04` §lede |
| `deal_type` | string | `Monthly`, `Annual`, or `2026` | Routing block; effective-date guardrail | `Annual` accounts use 90-day notice window per archived handoff §Format Routing |
| `current_mrr` | int (USD) | Pre-migration monthly MRR | "Before" total in pricing table; lede dollar | Before-row totals must equal this exactly |
| `current_platform_mrr` | int (USD) | Pre-migration platform-base component | "Before: platform base" row | Component of `current_mrr` |
| `current_user_mrr` | int (USD) | Pre-migration user-charge component | "Before: user charge" row | Component of `current_mrr`; for Format B, use `implied_billed_excess = ROUND(current_user_mrr ÷ current_user_rate)` for the table per archived Format B STEP 4 |
| `current_user_rate` | int (USD) | Pre-migration per-user rate | "Before: user detail" row | Often legacy below-book rate (e.g. $15 vs $25 book) |
| `current_provided_users` | int | Pre-migration included-user count | "Before: user detail" row; included-user-reduction comparison | When `new_included_users` < this, included-user-reduction rule applies (`_root/05`) |
| `trailing_avg_users` | int | Trailing 12-month avg active users | Narrative ("your team averages around X users") | Never expressed as ratio of provisioned users in client copy (`_root/04` §lede-stat-guardrail) |
| `active_users` | int | Current active user count snapshot | Internal cross-check only | Not surfaced in client copy |
| `current_stack` | string | Legacy stack description, e.g. `iPad` | Internal context | Not surfaced in client copy |
| `current_sites` | int | Site count | Internal context | Rarely used |
| `discount_drivers` | string (free text) | Notes on legacy discount structure | Routing block context; informs `migration_driver` selection | Multi-line free text |
| `angies_notes` | string (free text) | CEO/exec context notes | Routing block context; `special_arrangement` CEO-awareness override per archived Format B STEP 4 | Multi-line; first 200 chars surfaced in pipeline debug print |
| `assigned_tier` | string | New tier label (e.g. `T1 — Catalog Essentials`) | Internal cross-check vs. HTML model `t` | Cross-check field |
| `tier_base` | int (USD) | New platform-base monthly rate | "After: platform base" row | Cross-check against HTML model `tb`; CSV wins on conflict |
| `included_users` | int | New included-user count for tier | "After: included users" row | Cross-check against HTML model `iu`; CSV wins |
| `modeled_users` | int | Modeled user count for the new structure | Internal cross-check | Not surfaced in client copy |
| `excess_users` | int | New excess-user count | "After: user charge" row math | Cross-check against HTML model `eu`; CSV wins |
| `user_charge` | int (USD) | New user-charge component | "After: user charge" row | Cross-check against HTML model `uc`; CSV wins |
| `brands` | int | Brand count | Internal | Rarely surfaced |
| `additional_brand_charge` | int (USD) | Multi-brand add-on charge | Pricing table component when non-zero | Currently 0 for nearly all accounts |
| `addon_charge` | int (USD) | Other add-on charges (e.g. CPQ) | Pricing table component when non-zero | See `am`/Alfonso Marina for CPQ-folded example |
| `new_total_mrr` | int (USD) | Post-migration monthly MRR | "After" total in pricing table; lede dollar | After-row totals must equal this exactly. Cross-check against HTML model `nm`; CSV wins |
| `assumptions` | string (free text) | Modeling notes | Internal | Not surfaced |
| `delta_mrr` | int (USD, signed) | `new_total_mrr − current_mrr` | Lede ("a change of $[DELTA]/month"); routing block | Cross-check against HTML model `dm`; CSV wins |
| `delta_pct` | float (signed) | Percent change | Routing block `Delta`; format-routing decisions (`_root/06`) | Cross-check against HTML model `dp`; CSV wins. **Never lead client copy with this** (non-negotiable in archived prompts) |
| `risk_label` | string | Risk band label | Routing block `Risk label` | Format A briefs surface this; Format B/CEO Letter use `health_band` instead |
| `migration_driver` | string | **Primary driver — authoritative** | Routing block; "Why the Number Is Changing" template-block selection (`_root/05`) | Allowed values per `_root/05` driver taxonomy. **Always use this field, never HTML model `d`** |
| `secondary_drivers` | string (pipe-separated) | Secondary drivers | Supporting context within primary driver block (`_root/05`); never a separate section | When `included_user_reduction` appears as primary OR secondary, alternate "unchanged" line applies per archived non-negotiables |
| `migration_status` | string | Workflow status (`already_migrated`, `pending`, etc.) | Pipeline gating (skip `already_migrated`) | Filter at load time |
| `migration_confidence` | string | `confident`, `value_led`, `careful` | Routing block; informs CEO-pre-call gating | `careful` accounts may require additional review |
| `health_score` | float | Composite health 0–100 | Routing block `Health: [SCORE]` | **Never in client-facing copy** (non-negotiable #5) |
| `health_band` | string | `Thriving`, `Healthy`, `Watch`, `At Risk`, `Critical`, `Unscored` | Routing block `Health: — [BAND]`; lede-tone modulation per archived voice rules | **Never in client-facing copy** |
| `engagement_score` | float | E dimension 0–100 | Routing block `Engagement` | **Never in client-facing copy** |
| `adoption_score` | float | A dimension 0–100 | Routing block `Adoption` | **Never in client-facing copy** |
| `value_delivery_score` | float | VD dimension 0–100 | Routing block `Value Delivery` | **Never in client-facing copy** |
| `operational_health_score` | float | OH dimension 0–100 | Routing block `Ops Health` | **Never in client-facing copy** |
| `composite_narrative` | string (free text) | Health-narrative paragraph | Lede tone anchor; **Postgres fallback substitute** when live queries fail (§5) | Multi-line; quoted with surrounding double-quotes in the CSV |
| `ghost_account` | bool (`TRUE`/`FALSE`) | Ghost-account flag (placeholder / inactive / test) | Pipeline gating — **SKIP when TRUE** (operator decision 2026-05-22) | Currently `FALSE` for nearly all rows; the loader in §3 enforces the skip |
| `support_fire` | bool (`TRUE`/`FALSE`) | Active support escalation flag | Routing block `Support fire`; ⚠️ flag rendering per archived STEP 1b | Draft anyway; flag in routing block + delivery email; operator decides send timing |
| `support_fire_days_open` | int | Days the escalation has been open | Routing block ⚠️ line ("[N] days open") | Only meaningful when `support_fire = TRUE` |
| `bundle_config_mismatch` | bool | Bundle/config drift flag | Internal pipeline flag | Rarely surfaced; if `TRUE`, escalate per operator |
| `migration_segment` | string | Segment label per `_root/02` | Routing block context; segment cross-reference | Aligns with `_root/02` segment definitions |
| `notice_cohort` | string | Notice batch label | Routing block `Wave` | Drives sequencing |
| `notice_deadline` | string | Notice send deadline | Routing block context | Free text; informs sequencing |
| `messaging_headline` | string | Pre-computed messaging headline | Reference for drafter; not used verbatim | Sanity-check only |
| `artifact_type` | string | Artifact type (e.g. `Notice`, `CEO Letter`) | Cross-check against routing CSV `comm_action` | When in conflict, defer to routing CSV per `_root/06` |
| `delivery_owner` | string | Who sends (e.g. `Kylor`, `CS team`) | Operational routing | Not surfaced in client copy |

**Total columns**: 53 named columns (the CSV header line begins with a leading comma; that empty first column is the row-index slot and carries no data — the loader in §3 ignores it via `csv.DictReader`).

**Field-name discipline**: when a downstream doc, template, or draft references a column, it must use the verbatim column name in this table. If a `_root/` doc references a field name that is not present here, that is either a stale reference or a data gap — flag it to the operator per `_root/CONTRACTS.md` §2.

---

## §3. Loading the v6.2 CSV (canonical Python pattern)

The three archived fresh-agent prompts use a functionally identical loader; the canonical version is:

```python
import csv
import io

V62_PATH = (
    "/Users/kylorjohnson/Library/Mobile Documents/"
    "com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/"
    "_master-account-data-v6.2.csv"
)

with open(V62_PATH, newline="", encoding="utf-8-sig") as f:
    content = f.read()

# The CSV opens with one blank header-padding line (all commas).
# Skip it; the real header row is the second line.
lines = content.split("\n")
master = {
    r["ord_id"].strip(): r
    for r in csv.DictReader(io.StringIO("\n".join(lines[1:])))
    if r.get("ord_id", "").strip()
    and r.get("ghost_account", "").strip().upper() != "TRUE"
}
```

**Operator notes:**
- `master[ord_id]` returns a `dict` keyed by the column names in §2. All values are strings; cast to `int`/`float` at the call site as needed.
- The `utf-8-sig` encoding strips a BOM if present. Do not remove it.
- The leading blank line in the CSV is intentional spacing; do not edit the source file to remove it without coordinating with the v6.2 CSV maintainer.
- To slice for one account: `master.get(ord_id)`. If the result is `None` or empty: **STOP**. The account is not in the authoritative roster. Do not infer; ask the operator. (Note: `master.get(ord_id) is None` may indicate either a missing account OR a `ghost_account = TRUE` row that the loader filtered. The drafter checks `ord_id` against the raw CSV to disambiguate.)
- The `migration_status` field gates pipeline inclusion. Rows with `migration_status = "already_migrated"` are not eligible for migration notices — skip them at the call site.
- The `ghost_account = TRUE` filter is enforced in the loader above (operator decision 2026-05-22) — these are placeholder / inactive / test rows that should never receive a migration notice. Currently zero pending accounts carry this flag; the loader is defensive against future re-introduction.
- **The CSV is one-row-per-account as of 2026-05-22** (cleanup performed under operator decision, see `_root/09_changelog.md`). The loader's dict-comprehension pattern is keep-last-wins by `ord_id` — defensive against future re-introduction of duplicate rows. Drafters do not need to think about dedupe; the loader handles it.

**Anti-drift note**: this is the one definitive loader for v6.2 CSV. The three archived per-format prompts each carried a near-copy of the same code with format-specific `print` statements appended for debug output. The print statements are debug, not loader logic; they do not belong in this section.

---

## §3.5. Loading the HTML model (canonical Python pattern, cross-check only)

The HTML model lives at `_reference/migration_revenue_model_2026-05-14.html`. The model's per-account array is embedded as a `const A = [...]` JavaScript literal inside a `<script>` block. The canonical loader extracts the array via regex:

```python
import json
import re

HTML_MODEL_PATH = (
    "/Users/kylorjohnson/Library/Mobile Documents/"
    "com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/"
    "_reference/migration_revenue_model_2026-05-14.html"
)

with open(HTML_MODEL_PATH, "r") as f:
    html = f.read()

match = re.search(r"const A = (\[.*?\]);", html, re.DOTALL)
model = {a["oid"]: a for a in json.loads(match.group(1))}
```

**Operator notes:**
- `model[oid]` returns a `dict` keyed by HTML-model abbreviations: `cm` (current MRR), `nm` (new MRR), `dm` (delta MRR), `dp` (delta pct), `t` (tier), `d` (driver), `mc` (migration confidence), `dt` (deal type), `cy` (cohort year), `iu` (included users), `eu` (excess users), `uc` (user charge), `tb` (tier base), `hs` (health score), `hb` (health band), `c` (company), `s` (stack), `oid` (org id). Do **not** treat these as authoritative — they are cross-check only per §1.
- If `re.search` returns `None`, the HTML file's structure has changed. **STOP** and ask the operator; do not attempt to repair.

**Path divergence flag**: the three archived fresh-agent prompts and the archived handoff all load the HTML model from `~/Downloads/migration_revenue_model_2026-05-14 (2).html`. That path violates the current `AGENTS.md` rule against reading `~/Downloads/`. The canonical path moving forward is `_reference/migration_revenue_model_2026-05-14.html` (already mirrored into the folder per Stage 1.1). The `~/Downloads/` references in archived material are bugs — they are not authoritative and must not be propagated.

---

## §4. Postgres MCP queries

All queries below run through MCP server `user-supercat-postgres-vpn`. Queries are reproduced **verbatim** from archived format-a/format-b/ceo-letter `_fresh-agent-prompt.md` STEP 1.5. Do not edit. Any rewrite risks the live query failing or returning different data.

### §4.1 — `org_id` resolution (from `ord_id` shortname)

- **Purpose**: resolve the human-readable org shortname (`ord_id` from v6.2 CSV; also called `shortname` in Postgres) to the numeric `id` used by every other Postgres query.
- **MCP call signature**: `user-supercat-postgres-vpn` query tool; argument is the SQL string with `:org_shortname` (or inline-substituted `'{{ORG_SHORTNAME}}'`) replaced by the v6.2 CSV `ord_id` value.
- **Query SQL**:

  ```sql
  SELECT id AS org_id, shortname, name
  FROM organizations
  WHERE shortname = '{{ORG_SHORTNAME}}';
  ```

- **Expected return shape**: one row — `org_id` (int), `shortname` (string), `name` (string). Capture `org_id` for §4.2 and §4.3.
- **Fallback if empty/error**: see §5 — Postgres org_id resolution failure.

### §4.2 — User and login activity

- **Purpose**: pull current provisioned-user count and 90-day login activity for the org.
- **MCP call signature**: same as §4.1, with `{{ORG_ID}}` replaced by the integer returned by §4.1.
- **Query SQL**:

  ```sql
  SELECT
    (SELECT COUNT(*) FROM org_users
     WHERE organization_id = {{ORG_ID}} AND disabled = false) AS active_org_users,
    (SELECT COUNT(DISTINCT user_id) FROM login_events
     WHERE organization_id = {{ORG_ID}}
       AND created_at > NOW() - INTERVAL '90 days') AS logged_in_90d,
    (SELECT COUNT(*) FROM login_events
     WHERE organization_id = {{ORG_ID}}
       AND created_at > NOW() - INTERVAL '90 days') AS total_logins_90d;
  ```

- **Expected return shape**: one row — `active_org_users` (int), `logged_in_90d` (int), `total_logins_90d` (int).
- **Rendering constraint**: `active_org_users` and `logged_in_90d` are loaded into the routing block, but **never expressed as a provisioned-vs.-active ratio in client copy**. That guardrail is owned by `_root/04` §lede-stat-guardrail; the pipeline's job is to capture both fields and log them in the routing block (§7), and to surface only `total_logins_90d` (and tenure / output metrics) in the lede.
- **Fallback if empty/error**: see §5 — Postgres user/login query failure.

### §4.3 — Order and GMV activity (LTM eCat orders)

- **Purpose**: pull last-twelve-month eCat order count, GMV, and distinct-customer-served count.
- **MCP call signature**: same as §4.2.
- **Query SQL**:

  ```sql
  SELECT
    COUNT(*) AS ltm_orders,
    ROUND(SUM(total)::numeric, 2) AS ltm_gmv,
    COUNT(DISTINCT customer_num) AS ltm_customers_served
  FROM orders
  WHERE organization_id = {{ORG_ID}}
    AND is_submitted = true
    AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
    AND created_at > NOW() - INTERVAL '12 months'
    AND customer_num IS NOT NULL;
  ```

- **Expected return shape**: one row — `ltm_orders` (int), `ltm_gmv` (numeric, 2dp), `ltm_customers_served` (int).
- **Rendering constraint**: the `orders` table is **eCat-submitted orders only**. In client copy these are called "eCat orders" — never "your total orders" or anything that frames the count as total business volume. Cross-channel framing (`portal_orders`) requires the phrase "total business across all channels" and is owned by `_root/04`. The pipeline does not query `portal_orders` for migration notices.
- **Fallback if empty/error**: see §5 — Postgres order/GMV query failure.

### §4.4 — Derived metrics (computed from §4.3 + v6.2 CSV)

These are not Postgres queries; they are derived at draft time and live in the routing block when applicable.

- `cost_per_order = ROUND((new_total_mrr × 12) / ltm_orders, 2)` — annual subscription per eCat order.
- `annual_subscription = new_total_mrr × 12`
- `delta_per_order = ROUND((delta_mrr × 12) / ltm_orders, 2)` — annual delta per eCat order.

**Whether to surface these in client copy** (and at what thresholds) is owned by `_root/04` §4.8 (Value anchor: per-order cost + delta-per-order reframe), not this doc. The pipeline computes and stores them; the format-specific brief logic decides whether to render. Per `_root/04` §4.8 (operator decision 2026-05-22 — see `_root/09_changelog.md` Wave 1 entry), the canonical inclusion gate is `cost_per_order < $200` across all formats; the archived Format B template's stale `$35` threshold is tracked for Stage 3 cleanup as `CL-002` in `_meta/stage3_cleanup.md`.

### §4.5 — Before-state user-billing reconciliation (derived from v6.2 CSV only)

- `implied_billed_excess = ROUND(current_user_mrr ÷ current_user_rate)`
- `narrative_excess = trailing_avg_users − current_provided_users`

If `|implied_billed_excess − narrative_excess| > 3` **AND** the dollar discrepancy exceeds $60/month, the routing block must carry a `⚠️ USER BILLING RECONCILIATION NEEDED` line. Both thresholds must trip jointly per the operationalized methodology in `_meta/v6_2_reconciliation_log.md` (sweep run 2026-05-26; 37 of 107 pending accounts flagged under this AND-discipline). The pipeline's job is to compute both numbers and surface the discrepancy; the rule for *what to do* with the discrepancy (which number drives the table row vs. the narrative) is owned by `_root/05` / `_root/08`.

(CL-028 RESOLVED 2026-05-26 at source — pre-CL-028 prose used "(or the dollar discrepancy exceeds $60/month)" as a parenthetical clarification, which could be read as either synonym or disjunction. The operationalized methodology in `_meta/v6_2_reconciliation_log.md` line 21 + the Stage 4.1 lpf cohort sweep + every Stage 4 per-account session to date all apply the AND-discipline. CL-028 tightens the prose to match the methodology. Surfaced by Stage 4.2 sca v2 cohort iter 3 audit 2026-05-26 — sca's gap pattern (gap_users +7 / gap_dollars $0) would have flagged under strict OR-reading despite drafter pre-flight + tracker showing not-flagged; the AND-reading is canonical.)

**Resolution discipline (operator-stamped 2026-05-26, Stage 4.1 `lpf` production proof finding)**: when the reconciliation flag fires, the brief's After-row math is NOT re-versioned. Per `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` Appendix B, v6.2 modeled values are canonical for After-row math (see `_root/05 §2.1.5`); the gap between billing-implied enabled count and v6.2 `modeled_users` is closed via INTERNAL SuperCat ops cleanup pre-`[EFFECTIVE_DATE]` (disable phantom enabled accounts in the customer's environment so billing-side enabled aligns with `modeled_users` by the effective date). Per-account ops cleanup tasks are tracked at `_meta/v6_2_reconciliation_log.md` (37 flagged accounts pre-populated from the cohort-wide sweep run 2026-05-26 against v6.2 + billing math). The `⚠️ USER BILLING RECONCILIATION NEEDED` line in the routing block (§7) is the pre-send trigger for the ops cleanup task; it does NOT block brief approval. **Client copy NEVER mentions "unused users," "phantom accounts," or any user-cleanup language** (per `_root/04 §3` audience-discipline; the ops cleanup is a SuperCat-side workstream, not a customer conversation topic). For accounts where v6.2 modeled cannot be operationally reconciled by `[EFFECTIVE_DATE]`, the operator escalates per `_root/CONTRACTS.md §2` and may re-version v6.2 `modeled_users` to the operationally-correct value (which then re-routes the account per `_root/06` 6-step flow).

The cohort-wide sweep run at the discipline stamp surfaced 37 of 107 pending accounts with material reconciliation gaps (35%) and 33 of 107 with format-routing flips under an enabled-canonical override (31%) — confirming that the reconciliation gap is a systemic v6.2 modeling characteristic, not a per-account edge case. The discipline above is the cohort-wide standing rule; per-account exceptions land in `_meta/v6_2_reconciliation_log.md` with operator stamp.

---

## §5. Fallback rules

When a live data source fails or returns empty, the pipeline does not improvise. Each failure mode has a single prescribed response.

| Failure mode | Fallback | Logged where |
|---|---|---|
| Postgres `org_id` resolution returns empty (§4.1) | Use `composite_narrative` from v6.2 CSV in place of all operational stats. Suppress every Postgres-derived field in the routing block; render only the tenure/relationship lede. | Routing block (`Postgres live data: UNAVAILABLE — fell back to composite_narrative`) + `_root/09_changelog.md` |
| Postgres `org_id` resolution errors (timeout, connection) | Same as above. | Same as above. |
| Postgres user/login query (§4.2) returns empty | Suppress any lede stat sentence built on `total_logins_90d` / `active_org_users`. Fall back to tenure + named-platform-surface language per `_root/04` §lede-stat-guardrail. | Routing block (note which sub-field is empty) |
| Postgres order/GMV query (§4.3) returns empty (`ltm_orders = 0`) | Omit any "eCat orders" / "customers served" sentence in the lede. Omit the value anchor section (§4.4). Do not flag in client copy; the routing block carries the note. | Routing block (`ltm_orders = 0 — value anchor omitted`) |
| Postgres order/GMV query errors | Same as the empty case. | Same. |
| HTML model and v6.2 CSV disagree on any number | Use the v6.2 CSV value. Log the disagreement (account, field, both values). | `_root/09_changelog.md` (cross-check disagreement entry) |
| v6.2 CSV missing a required field for an account | **STOP**. Ask the operator. Do not infer. Do not pull the missing value from any other source. | Operator escalation per `_root/CONTRACTS.md` §2 |
| `support_fire = TRUE` on the account | Not a failure mode. Draft the brief and delivery email in full. Add the ⚠️ line to the routing block per §7. Add the ⚠️ note to the delivery email's operator notes. Nothing about the support issue appears in client-facing copy. Operator decides send timing. | Routing block + delivery email operator notes |
| Account row exists but `migration_status = "already_migrated"` | Skip the account. Do not draft a migration notice. | Pipeline filter at load time (§3) |
| Account row exists but `ghost_account = TRUE` | Skip the account. Placeholder / inactive / test row; never receives a migration notice. | Pipeline filter at load time (§3) — loader excludes the row from `master[]` entirely |

**Discipline**: a fallback is not the same as a workaround. The fallbacks above are the complete set; a drafter who encounters a failure mode not in the table stops and asks the operator. Inventing a new fallback is the §2 drift vector.

---

## §6. Naming conventions for output files

Two output files per account: a brief and a delivery email.

**File-name pattern**:

| File | Pattern | Example |
|---|---|---|
| Brief | `<ord_id>__<account-slug>__brief.md` | `kal__kalco-allegri-crystal__brief.md` |
| Delivery email | `<ord_id>__<account-slug>__delivery-email.md` | `kal__kalco-allegri-crystal__delivery-email.md` |

**Components**:
- `<ord_id>` — verbatim from v6.2 CSV `ord_id` column. Lowercase. Never reformatted (no leading zeros, no padding).
- `<account-slug>` — lowercase, hyphen-separated, derived from `company`. Slashes (`/`) become hyphens. Ampersands (`&`) drop or become `-and-`. Punctuation drops. Multi-brand entities concatenate brand names with hyphens (e.g. `Kalco Lighting / Allegri Crystal` → `kalco-allegri-crystal`).
- `__` (double underscore) — segment separator. Single-underscores inside `<ord_id>` or `<account-slug>` are reserved for future use; do not introduce them today.
- `brief.md` / `delivery-email.md` — segment-type suffix. Always lowercase, always `.md`.

**Versioned re-runs**: when a brief is regenerated because a rule changed in a `_root/` doc that affects its content, append `__v2`, `__v3`, etc., before the `.md` extension:

- `kal__kalco-allegri-crystal__brief__v2.md`
- `kal__kalco-allegri-crystal__delivery-email__v2.md`

A `__v2` is required whenever a re-run is triggered by an upstream rule change (in `_root/03`, `_root/04`, `_root/05`, `_root/06`, `_root/07`, or `_root/08`) that propagates into the brief's content per `_root/CONTRACTS.md` §3 step 5. The unversioned and `__v2` files coexist in the same folder until the unversioned file is retired by the operator.

**Output-file location**:

| Format | Folder |
|---|---|
| Format A — 60-Day Notice (≤10% delta) | `Pricing Migration/format-a-notices/` |
| Format B — Notice + Meeting (>10% delta, <$400) | `Pricing Migration/format-b-notices/` |
| CEO Letter + Call Commitment ($400–$599) | `Pricing Migration/ceo-letter-notices/` |
| Good-News Notice (decrease) | `Pricing Migration/good-news-notices/` |
| CEO Pre-Call → Format B (≥$600) | `Pricing Migration/format-b-notices/` (with CEO awareness flag — see §7) |

The mapping from `comm_action` value to folder is owned by `_root/06`; the table above reflects the post-refactor folder layout for pipeline orientation only.

---

## §7. The required "internal routing block"

Every brief begins with a Markdown blockquote labeled the **internal routing note**. The block is the trust artifact — it tells a reviewer (or a future agent) exactly which data the brief was built from. The block is stripped before sending to the client.

The block is a **contract**. Every brief contains every general field below in order; format-specific fields appear conditionally per the matrix at the end of this section.

### Canonical field list (general — every brief)

```markdown
> **Internal routing note** (remove before sending):
> Brief type: <BRIEF_TYPE> | <FORMAT_LABEL>
> Account: [ACCOUNT_NAME] | Tier: [T1/T2/T3] | Wave: [WAVE]
> Migration driver: [DRIVER] | Health: [SCORE] — [BAND] | Risk label: [RISK]
> Engagement: [E] | Adoption: [A] | Value Delivery: [VD] | Ops Health: [OH]
> Support fire: [YES/NO] | Behavioral floor applied: [YES/NO]
> Delta: [DELTA_PCT] (+$[DELTA_MRR]/month)
> Cohort: [YEAR]
> Contract: [MONTHLY/ANNUAL] | Renewal date: [DATE or UNKNOWN]
> Earliest enforceable effective date: [DATE]
> Comm_action: [COMM_ACTION from routing CSV]
> Postgres live data (<YYYY-MM-DD>): active_org_users=[N] | logged_in_90d=[N] | total_logins_90d=[N] | ltm_orders=[N] | ltm_gmv=$[N] | ltm_customers_served=[N]
> CEO awareness required before send: [YES/NO]
```

### Conditional fields (add when the condition holds)

| Field | Condition |
|---|---|
| `> **⚠️ SUPPORT FIRE: [N] days open. Production-ready. Operator decides send timing.**` | `support_fire = TRUE`. Insert immediately after the `Support fire` row. |
| `> CEO call commitment date: [SPECIFIC DATE — within 5 business days of send]` | Format = CEO Letter (or any tier with CEO Letter component). |
| `> CEO name for sign-off: [CEO FIRST + LAST NAME]` | Format = CEO Letter. |
| `> ⚠️ CEO PRE-CALL REQUIRED — arrangement was negotiated by [NAME]. Do not send at CSM level before CEO confirms.` | `migration_driver = special_arrangement` AND `angies_notes` / `discount_drivers` reference a named executive as originator. |
| `> ⚠️ USER BILLING RECONCILIATION NEEDED — billed amount implies [M] excess users ($Y/month) but stated trailing average implies [N] excess users ($X/month). Confirm before sending.` | §4.5 discrepancy threshold tripped. |
| `> Expansion eligible: [YES/NO] — [NOTE]` | Format A only (carried over from archived Format A v2 sample). |
| `> Billing entity: [NAME] — notice routes to billing contact` | `billing_entity` is non-blank AND ≠ `company`. |
| `> Tenure acknowledgment required: YES — [YEARS] years (cohort [YEAR])` | `cohort_year ≤ 2016` (early adopter). |
| `> Watch health flag: [YES/NO] — escalate to CSM if YES` | Good-News Notice format only. |

### Per-format matrix

| Field | Format A | Format B | CEO Letter | Good-News |
|---|---|---|---|---|
| General fields (Brief type → Postgres live data) | required | required | required | required* |
| `CEO awareness required before send` | NO (always) | NO for Notice+Meeting; YES for CEO Pre-Call | YES (always) | NO (always) |
| `CEO call commitment date` | n/a | n/a | required | n/a |
| `CEO name for sign-off` | n/a | n/a | required | n/a |
| `Expansion eligible` | required | n/a | n/a | required |
| `Watch health flag` | n/a | n/a | n/a | required |

\* Good-News Notice substitutes `Current MRR / New MRR / Delta (negative)` lines for the `Delta:` row, and omits the Postgres live-data line (live data is not used in price-decrease notices).

### Rule

Every brief's routing block contains every general field. A field that genuinely does not apply renders as `n/a` or the empty string — never as a deleted line. The block is *the* §3-step-5 propagation hook: when an upstream rule changes, the routing block tells the rerunner exactly which data the prior draft used.

---

## §7.5. The required "internal routing block" — delivery-email subset per format

Every delivery email begins with the same kind of Markdown blockquote as the brief — a drafter-facing **internal routing note**, stripped before sending. The delivery-email routing block is a **deliberately slim subset** of the brief's full routing block per §7: it carries only the fields that matter at delivery time (account identity, dollar-change snapshot, effective-date, attachment pointer, format-specific awareness/call/commitment flags, applicable conditionals), not the full Postgres live-data line, behavioral-floor row, or per-driver detail that lives in the brief's routing block.

This section is the canonical per-format matrix for the delivery-email subset. It codifies the convention applied uniformly across all 5 Stage 3 delivery-email templates (Format A, Format B, CEO Letter, Good-News Notice, entity-packet parent-letter cover email). The convention was operator-approved across Stage 3.1 → 3.5 review passes (2026-05-26 — see `_root/09_changelog.md` Stage 3.1 through Stage 3.5 prep entries) and Stage 3.1–3.5 templates each carried a `CL-022 note` blockquote in their Section 2 acknowledging the inferred-subset state pending this rule-layer codification (Wave 6 batch — `_meta/stage3_cleanup.md` CL-022). With §7.5 landed, the inferred-subset state is closed: each delivery-email template's Section 2 now references this matrix as canonical, and the `CL-022 note` blockquotes carried by the 5 templates are template-scaffolding annotations of the rule-layer history (they are not re-introduced as ongoing inference; they document the pre-§7.5 inference pattern for audit-trail purposes only).

### Per-format delivery-email routing-block field list

The matrix below names every field carried in each format's delivery-email routing block, in order, with applicability and conditional logic. Fields are read top-to-bottom in each column; a field that genuinely does not apply for a given format renders as `n/a` only when the format-row says `required` with an `n/a-when` condition, or is omitted from the format's block when the format-row says `n/a`. The format-column entries are: **required** (always emitted), **n/a** (never emitted for this format), **conditional** (emitted only when the named condition holds — refer to the conditional-rows table below).

| Field | Format A | Format B | CEO Letter | Good-News Notice | Entity-packet (parent-letter cover email) |
|---|---|---|---|---|---|
| `Brief type: <FORMAT_LABEL> \| Delivery email` | required | required | required | required | required |
| `Account: [NAME] \| Tier: [T1/T2/T3] \| Wave: [WAVE]` | required | required | required (+ `ord_id` row per CEO Letter convention) | required | n/a (replaced by entity-level identity rows) |
| `Entity name: [ENTITY_NAME] \| Entity type: [rollup \| standalone_multi_org] \| Brands count: [N]` | n/a | n/a | n/a | n/a | required |
| `Member accounts: [BRAND_A \| BRAND_B \| …]` | n/a | n/a | n/a | n/a | required |
| `Member ord_ids: [ORD_ID_A \| ORD_ID_B \| …]` | n/a | n/a | n/a | n/a | required |
| `Migration driver: [DRIVER] \| Health: [SCORE] — [BAND]` | required | required | required | required | n/a (per-child territory; lives in per-child routing blocks) |
| `Current MRR: $[CURRENT_MRR] \| New MRR: $[NEW_MRR] \| Delta: +$[DELTA]/month ([DELTA_PCT])` | required | required | required | required (substitutes `Delta: –$[DELTA]/month` decrease form per §7 footnote) | required (substitutes entity-level form: `Current entity MRR: $[CURRENT_ENTITY_MRR] \| New entity MRR: $[DEFAULT_MRR] \| Delta: +$[DEFAULT_DELTA]/month (+[DEFAULT_DELTA_PCT]%)` — `default_*` only per `_root/04 §4.15.5`; `consolidated_*` is INTERNAL-ONLY, never in customer copy) |
| `consolidated_mrr: $[N] \| consolidated_delta: +$[N]/month \| consolidation_saving: $[N]/month` | n/a | n/a | n/a | n/a | required as **INTERNAL-ONLY** row per `_root/04 §4.15.5` (lives in the routing block which is removed before sending; never in customer copy) |
| `Cohort: [YEAR] \| Contract: [MONTHLY/ANNUAL] \| Renewal date: [DATE or UNKNOWN]` | required | required | required | required | n/a (cohort/contract data lives per child) |
| `Notice cohort: [June \| Post-Migration]` | n/a | n/a | n/a | n/a | required (drives timing context per `_root/02 §5` + `_root/06 §1.6`; sourced from Master Entity tab `notice_cohort` column) |
| `Earliest enforceable effective date: [EFFECTIVE_DATE]` | required | required | required | required | required (entity-level reference; per-child effective dates carry through to per-child notices independently) |
| `Parent-letter send date (Day 0): [DATE]` | n/a | n/a | n/a | n/a | required |
| `Per-child notices send window (Day 1–Day 2): [DATE] – [DATE]` | n/a | n/a | n/a | n/a | required |
| `Attachment: [ord_id]__[company-slug]__brief.md` (per §6 naming) | required | required | required | required | required (substitutes parent-letter form: `[entity-slug]__parent-letter.md` per §6 Stage 4 production naming convention) |
| `Comm_action: <VALUE>` (from routing CSV per `_root/06 §5`) | required (`Format A — 60-Day Notice`; or `(after CSM touchpoint)` / `(after renewal-date confirm)` per `_root/06 §5.5` `post_hold_action` variants) | required (`Format B — Notice + Meeting Offer` OR `CEO Pre-Call → Format B`; or `post_hold_action` variants per `_root/06 §5.5`) | required (`CEO Letter + Call Commitment`; or `post_hold_action` variants per `_root/06 §5.5`) | required (`Good-News Notice`; or `Good-News Notice (after CSM touchpoint)` / `Good-News Notice (after renewal-date confirm)` per `_root/06 §5.5`) | required (`entity_packet_parent_letter` per `_root/06 §1.6` two-stage routing pattern) |
| `Delivery owner: [CEO \| Kylor]` — drives voice fork per `_root/04 §4.15.1`; sourced from Master Entity tab `delivery_owner` column | n/a | n/a | n/a | n/a | required |
| `CEO awareness required before send: <VALUE>` | required (`NO (always)`) | required (`NO` for standard Notice + Meeting Offer; `YES` for `CEO Pre-Call → Format B`) | required (`YES (always)`) | required (`NO (always)`) | required (`YES (always)` per `_root/06 §1.6` operator stamp 2026-05-26 — CEO authors CEO-delivered fork; CEO reviews and approves Kylor-delivered fork before Kylor sends) |
| `CEO call commitment date: [SPECIFIC DATE — within 5 business days of send]` | n/a | n/a | required (3-location parity contract: this date MUST match the brief's Section 3o close text AND the brief's Section 2 routing block per `_root/04 §4.12`) | n/a | required for CEO-delivered fork only (3-location parity contract: this date MUST match the parent letter's Section 3g close text AND the parent letter's Section 2 routing block per `_root/04 §4.15.6` + `_root/04 §4.12`); renders `n/a for Kylor-delivered fork` |
| `CEO name for sign-off: [CEO FIRST + LAST NAME]` | n/a | n/a | required | n/a | required for CEO-delivered fork only; renders `n/a for Kylor-delivered fork` |
| `Support fire cleared: [YES/NO]` | n/a | n/a | required (CEO-Letter-specific standing field per `_root/04 §3` row on support-issue context — the support fire flag must clear, or the CEO must explicitly accept proceeding with it open, before send; this is a stronger gate than the `⚠️ SUPPORT FIRE` conditional row in the table below because the cleared/not-cleared disposition is itself a CEO-Letter pre-send blocker; operator-stamped 2026-05-26 at Stage 4 prep Source-fix Session B landing on matrix-template parity resolution) | n/a | n/a |
| `Expansion eligible: [YES/NO]` | required (if YES, queue Format C only after confirmed positive signal per `_root/04 §2.6`) | n/a (Format B's meeting offer is not a discovery call per `_root/04 §2.6`) | n/a (CEO Letter's call commitment is not a discovery call) | required (if YES, queue Format C only after confirmed positive signal per `_root/04 §2.6`; never combined with the Good-News email) | n/a (entity-level expansion is not modeled at v6.2; per-child expansion eligibility lives in per-child routing blocks) |
| `Watch health flag: [YES/NO]` | n/a | n/a | n/a | required (Good-News-specific gate per `_root/06 §4.2` Watch-band carve-out; if YES: DO NOT send the Good-News email — escalate to CSM for health check-in first) | n/a (per-child Watch / At-Risk / Critical handling is per-child territory per `_root/06 §4.2`) |
| `Postgres live data (<YYYY-MM-DD>): active_org_users=[N] \| logged_in_90d=[N] \| total_logins_90d=[N] \| ltm_orders=[N] \| ltm_gmv=$[N] \| ltm_customers_served=[N]` | **OMITTED** at delivery-email level (the full Postgres live-data line is carried in the brief's routing block per §7; the delivery email's slim subset does not re-emit it — the brief is attached, and the brief's block is the trust artifact for live data) | **OMITTED** (same rationale as Format A) | **OMITTED** (same rationale as Format A) | **OMITTED** per §7 footnote — Good-News Notice does not use Postgres live data in the brief either (price-decrease notices do not surface live operational metrics; mirrors `_root/04 §4.12` Good News close register — "math, not a favor"); the line is absent at both brief and delivery-email level | **OMITTED** — entity-packet emails draw from Master Entity tab + Master Account tab joined via `member_ord_ids` ↔ `ord_id`; per-child Postgres data lives in per-child routing blocks per Stage 3.1 / 3.2 / 3.3 conventions, not the parent-letter delivery email |

### Conditional rows (per-format applicability)

Same conditional-fields convention as the brief per §7 above, with delivery-email-specific scope: each conditional row is added immediately after the field it modifies in the format's block when the condition fires. The matrix below names which conditional rows fire in which formats.

| Conditional row (template-condensed; full text in the format's delivery-email Section 2) | Format A | Format B | CEO Letter | Good-News Notice | Entity-packet |
|---|---|---|---|---|---|
| `> **⚠️ SUPPORT FIRE: [N] days open. Production-ready. Operator decides send timing.**` (CEO Letter substitutes "Operator decides send timing (CEO decides for CEO Letter)"; entity-packet substitutes "[N] days open across [CHILD_BRAND]") | when `support_fire = TRUE` | when `support_fire = TRUE` | when `support_fire = TRUE` (stronger gate per `_root/04 §3` row; CEO must accept or clear before send) | when `support_fire = TRUE` | when ANY member brand carries `support_fire = TRUE` (stronger gate at entity-packet level because a slip on any per-child notice past the 48-hour window is a credibility failure per `_root/04 §4.15.6`) |
| `> ⚠️ CEO PRE-CALL CONFIRMED — [CEO_NAME] called [CONTACT_NAME] on [PRE_CALL_DATE]. Email reflects that conversation.` | n/a | when `comm_action = "CEO Pre-Call → Format B"` (drafter confirms the CEO call happened BEFORE send; if not, escalate per `_root/CONTRACTS.md §2`) | n/a | n/a | n/a |
| `> ⚠️ CEO PRE-CALL REQUIRED — arrangement was negotiated by [NAME]. Do not send at CSM level before CEO confirms.` | when `migration_driver = special_arrangement` AND `angies_notes` / `discount_drivers` reference a named executive as originator | when same condition holds | when same condition holds (CEO confirms arrangement history with Finance before call commitment per `_root/05 §2.8.6`) | n/a (Good-News scope is decrease-side; `special_arrangement` does not surface in Good-News routing) | when ANY member brand meets the condition (mirrors the parent letter's flag; CEO must confirm context before parent letter goes out) |
| `> ⚠️ USER BILLING RECONCILIATION NEEDED — billed amount implies [M] excess users ($Y/month) but stated trailing average implies [N] excess users ($X/month). Confirm before sending.` | n/a (per Stage 3.1 template scope — reconciliation flag carried at brief level only) | n/a (per Stage 3.2 template scope) | when `_root/07 §4.5` discrepancy threshold tripped (mirrors brief's routing-block flag) | n/a (Good-News scope is decrease-side; the reconciliation flag is increase-side per `_root/07 §4.5`) | when `_root/07 §4.5` discrepancy threshold tripped on any member brand (mirrors parent letter's flag) |
| `> Billing entity: [NAME] — notice routes to billing contact` | when `billing_entity` is non-blank AND ≠ `company` | when same condition holds | when same condition holds | when same condition holds | when entity-level `billing_entity` is non-blank AND ≠ `company` (parent letter routes to entity billing contact; per-child notices route to per-child billing contacts independently) |
| `> Tenure acknowledgment required: YES — [YEARS] years (cohort [YEAR])` (CEO Letter variant: `> Tenure acknowledgment in email: YES — [YEARS] years (cohort [COHORT_YEAR])`; entity-packet variant: `> Tenure acknowledgment in cover email: YES — earliest member cohort = [YEAR] ([N] years)`) | n/a at delivery-email level (Format A tenure acknowledgment lives in the brief, not the delivery email) | n/a at delivery-email level | when `cohort_year ≤ 2016` (CEO Letter delivery email adds a one-sentence tenure acknowledgment per `_root/04 §4.7`) | informational only at delivery-email level when `cohort_year ≤ 2016`; Good News does NOT carry the `_root/04 §4.7` early-adopter tenure paragraph in either the brief or the email per the warm low-touch register at `_root/04 §4.12` Good News close | when earliest member brand's `cohort_year ≤ 2016`; relationship-historicity integrates into Paragraph 1 per `_root/04 §4.15.2` (not a separate sentence) |
| `> Mixed-segment annotation: YES — [SEGMENT_LABELS]` | n/a | n/a | n/a | n/a | when `mixed_segment` is populated; informational only at the email level (the `_root/04 §4.15.3` deal-type heterogeneity acknowledgment lives in the parent letter, not the cover email) |

### Per-format omissions and substitutions (delivery-email-specific)

- **Format A** — same lean subset as the brief minus Postgres live-data, behavioral-floor row, dimension scores, and per-driver detail; `Expansion eligible` is the Format-A-specific add. (CL-022 inferred-subset state CLOSED 2026-05-26 with §7.5 landed; pre-§7.5 inference history preserved in the template's Section 2 `CL-022 note` for audit trail.)
- **Format B** — same as Format A minus `Expansion eligible`; adds `Comm_action: [Format B — Notice + Meeting Offer / CEO Pre-Call → Format B]` and conditional `CEO awareness required before send: YES` when `comm_action = "CEO Pre-Call → Format B"`; adds the `CEO PRE-CALL CONFIRMED` conditional row.
- **CEO Letter** — adds `ord_id` to the Account row (per Stage 3.3 template convention — full per-account identity at CEO Letter precision); adds three CEO-Letter-specific fields: `CEO awareness confirmed before send: YES` (always), `CEO call commitment date: [SPECIFIC DATE]` (3-location parity contract), `CEO name for sign-off`; adds `Support fire cleared: [YES/NO]` (CEO-Letter-specific gate per `_root/04 §3` row); adds the `Tenure acknowledgment in email` conditional row when `cohort_year ≤ 2016` (CEO Letter is the only delivery-email format that carries the tenure acknowledgment in the email body itself per `_root/04 §4.7`).
- **Good-News Notice** — substitutes `Current MRR / New MRR / Delta (negative)` for the standard `Delta:` row per §7 footnote; **OMITS the Postgres live-data line** at both brief and delivery-email level (the omission is a property of the format per `_root/06 §1` and `_root/04 §4.12` Good News close register, not a delivery-email-only thinning); adds `Expansion eligible: required` AND `Watch health flag: required` (Good-News-specific fields — the Watch flag is the Good-News-specific gate per `_root/06 §4.2`); does NOT carry `CEO call commitment date` / `CEO name for sign-off` (those are CEO Letter only); does NOT carry Format B's `Comm_action = "CEO Pre-Call → Format B"` value (Good News is decrease-side only per `_root/06 §3` row 1).
- **Entity-packet (parent-letter cover email)** — fundamentally different routing-block shape because the artifact is entity-scoped, not account-scoped: replaces per-account identity rows (Account / Tier / Wave) with entity-level identity rows (Entity name / Entity type / Brands count / Member accounts / Member ord_ids); replaces per-account dollar lines with entity-level dollar lines drawn from Master Entity tab `default_*` columns (NEVER `consolidated_*` in customer copy per `_root/04 §4.15.5`); adds the **INTERNAL-ONLY** `consolidated_mrr` / `consolidated_delta` / `consolidation_saving` row (lives in the routing block which is removed before sending; never in customer copy under any rendering); adds `Notice cohort`, `Parent-letter send date (Day 0)`, `Per-child notices send window (Day 1–Day 2)`, `Delivery owner: [CEO | Kylor]` (drives voice fork per `_root/04 §4.15.1`); substitutes parent-letter attachment naming per `_root/07 §6` Stage 4 production convention; OMITS `Migration driver / Health` rows (per-child territory per `_root/04 §4.15.4`); OMITS `Cohort / Contract / Renewal date` (per-child territory); OMITS `Expansion eligible` (entity-level expansion not modeled at v6.2); OMITS `Watch health flag` (per-child territory); OMITS Postgres live-data (Master-Entity-tab sourced); renders `CEO call commitment date` and `CEO name for sign-off` conditionally per `delivery_owner` fork (required for CEO-delivered fork; `n/a for Kylor-delivered fork`); the Kylor-delivered fork's commitment is a 48-hour window per `_root/04 §4.15.6`, not a specific calendar date.

### Rule

Every delivery-email's routing block contains every field marked `required` for its format in the matrix above, in order. Conditional rows fire only when their condition holds, and are placed immediately after the field they modify. A field that genuinely does not apply renders as `n/a` only when the matrix row says `required` with an `n/a-when` condition (the Kylor-delivered fork's CEO-call-commitment-date and CEO-name-for-sign-off rows are the canonical examples); a field that does not apply to the format at all is OMITTED from the block (`n/a` in the matrix column). The block is stripped before sending — same as §7 — and is the §3-step-5 propagation hook at the delivery-email layer: when an upstream rule changes (a §6 dispatch, a `_root/04 §4.15.X` voice rule, a §2 column rename), the delivery-email's routing block tells the rerunner exactly which data the prior send used.

Pre-§7.5, each Stage 3 delivery-email template carried a `CL-022 note` in its Section 2 acknowledging the inferred-subset state and naming this matrix as the canonical future home. With §7.5 landed (Wave 6 batch — 2026-05-26), the inferred-subset state is CLOSED: each delivery-email template's Section 2 now references §7.5 as canonical. The pre-§7.5 `CL-022 note` blockquotes in each template remain in place as template-scaffolding audit-trail of the rule-layer history (they are not re-introduced as ongoing inference; they document how the matrix landed). Future delivery-email templates inherit §7.5 directly without restating the matrix.

---

## §8. File-path index

Every file the pipeline reads or writes.

| File | Role | R/W | Location |
|---|---|---|---|
| `_master-account-data-v6.2.csv` | Authoritative account roster (§2) | Read | `Pricing Migration/` |
| `migration_comm_tiers_2026-05-19.csv` | Routing data (`comm_action` per account) | Read | `Pricing Migration/` |
| `_reference/migration_revenue_model_2026-05-14.html` | Math cross-check only (§3.5) | Read | `Pricing Migration/_reference/` |
| Postgres `organizations` table (via MCP `user-supercat-postgres-vpn`) | `org_id` resolution (§4.1) | Read | Remote DB |
| Postgres `org_users` table (via MCP) | Provisioned-user count (§4.2) | Read | Remote DB |
| Postgres `login_events` table (via MCP) | 90-day login activity (§4.2) | Read | Remote DB |
| Postgres `orders` table (via MCP) | LTM eCat orders + GMV (§4.3) | Read | Remote DB |
| `format-a-notices/<ord_id>__<slug>__brief.md` | Format A brief output | Write | `Pricing Migration/format-a-notices/` |
| `format-a-notices/<ord_id>__<slug>__delivery-email.md` | Format A delivery-email output | Write | `Pricing Migration/format-a-notices/` |
| `format-b-notices/<ord_id>__<slug>__brief.md` | Format B brief output | Write | `Pricing Migration/format-b-notices/` |
| `format-b-notices/<ord_id>__<slug>__delivery-email.md` | Format B delivery-email output | Write | `Pricing Migration/format-b-notices/` |
| `ceo-letter-notices/<ord_id>__<slug>__brief.md` | CEO Letter brief output | Write | `Pricing Migration/ceo-letter-notices/` |
| `ceo-letter-notices/<ord_id>__<slug>__delivery-email.md` | CEO Letter delivery-email output | Write | `Pricing Migration/ceo-letter-notices/` |
| `good-news-notices/<ord_id>__<slug>__brief.md` | Good-News Notice output | Write | `Pricing Migration/good-news-notices/` |
| `good-news-notices/<ord_id>__<slug>__delivery-email.md` | Good-News Notice delivery-email output | Write | `Pricing Migration/good-news-notices/` |
| `_root/09_changelog.md` | Rolling log; receives cross-check disagreements (§5) and rule-change entries | Append-write | `Pricing Migration/_root/` |

**Path discipline**: every input above lives inside `Pricing Migration/`. No pipeline path resolves outside the folder. Archived references to `~/Downloads/migration_revenue_model_2026-05-14 (2).html` are stale (see §3.5) — they are not authoritative under the current `AGENTS.md`.

---

## §9. What this doc does NOT own

- **Voice and tone of the content rendered from these fields** → `_root/04_communication_posture.md`.
- **Per-driver narrative content (the prose that the fields feed into)** → `_root/05_driver_taxonomy.md`.
- **Which `comm_action` value maps to which format folder** → `_root/06_format_routing.md`.
- **Segment definitions, account counts, entity-gating rules, and routing errata** → `_root/02_who_is_being_migrated.md`.
- **What "Thriving" / "Healthy" / "Watch" / "At Risk" mean and what tone modulation each implies** → `_root/04`.
- **Quality gates** → `_root/08_quality_bar.md`. **Conformance-block format** → `_root/00_manifest.md §5`.
- **The actual per-account data values** — those are in the CSVs themselves. This doc is the *map* to the data, not the data.

---

*Cross-references: `_root/CONTRACTS.md` (anti-archive rule §4 — archived prompts were read for this doc under explicit Wave 2.3 authorization; this is the only legitimate path per CONTRACTS §4); `_root/00_manifest.md` (required-reading order); `_root/09_changelog.md` (cross-check disagreement log, fallback-event log).*
