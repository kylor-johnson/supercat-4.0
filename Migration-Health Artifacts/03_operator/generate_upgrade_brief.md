# Operator Prompt — Generate Migration or Expansion Brief

**Purpose:** Generate a client-facing brief + internal prep sheet for a single account using the current template system.
**Output:** Two files — (1) `02_briefs/generated/[org_shortname]_[brief-type]_[date].md` (client-facing), (2) `02_briefs/generated/[org_shortname]_prep-sheet_[date].md` (internal)
**Who runs this:** Fresh agent in a new Cursor chat session. No prior context required.
**Estimated time:** 20–35 minutes per brief (includes Health V3 read, contract gate, and optional on-demand data queries).

---

## How to Use This Prompt

1. Open a new Cursor chat (Agent mode)
2. Paste the prompt below, replacing the two variables at the top
3. Let the agent run
4. Review the output — check all operator instruction blocks and confirm placeholders are filled
5. Remove all internal routing notes before sending to the client

---

## The Prompt (copy everything below this line)

---

You are generating a client-facing pricing brief for a SuperCat customer. This brief will be delivered by the CEO or CSM in a reactive context — when a client pushes back on a pricing change, or when a migration conversation creates an opening for an upgrade discussion.

**Inputs:**
- `org_shortname`: {{ORG_SHORTNAME}}
- `brief_type`: {{BRIEF_TYPE}}  ← must be exactly one of: "format_a", "format_b", "format_c_t1t2", "format_c_t2t3"

**Design principles that must hold throughout the brief:**
1. State the price change plainly and early — never bury it
2. Lead with the correction mechanic (why the number is changing)
3. Remove all behavioral usage data from the client-facing body — no health scores, login counts, activity tables, or feature adoption metrics
4. Retain pricing mechanics — before/after math, rate tables, peer price ranges, user charge calculations
5. Separate normalization (Job 1) from expansion (Job 2) — never conflate in the same document
6. Include "why now" — one sentence: this is a 2026 standardization across the full install base
7. Include "what doesn't change" — workflow, access, integrations, data are unchanged
8. On Format B (significant delta >10%): the close must be a specific CEO call commitment, not a passive handoff
9. Acknowledge early-adopter tenure directly for accounts that signed before 2016
10. Format C expansion briefs are only generated after confirmed migration acceptance — verify this before proceeding

---

### Step 1: Confirm routing

Read the routing table at:
`SuperCat 4.0/Migration-Health Artifacts/01_routing/migration_wave_routing.csv`

Find the row for `{{ORG_SHORTNAME}}`. Confirm:
- `migration_brief_type` is not `none` (already migrated accounts need no brief)
- For Format C briefs: `expansion_brief_type` matches the requested brief type AND is not `hold`
- `flags` column — if any flags exist, STOP and report them. Do not generate a brief for a flagged account without human review.

If checks fail, stop and explain why. Do not proceed.

---

### Step 1b: Read Health V3 data

Find the account's latest Health V3 scorecard:
`SuperCat 4.0/Health V3/runs/[LATEST_RUN_DATE]/[ORG_SLUG]_scorecard.md`

If no scorecard exists for this account, note "No Health V3 run on file" and proceed with available routing data only — the prep sheet Health V3 Snapshot section will be partially blank.

Extract and record:
- Composite score and health band
- All four dimension scores: Engagement, Adoption, Value Delivery, Operational Health
- Dimension narratives (one sentence each, for prep sheet)
- Support fire flag (YES/NO)
- Behavioral floor override flag (YES/NO)
- Ghost account flag (YES/NO)
- Health trend direction and score delta from prior run

These values populate the internal routing note headers and the prep sheet Health V3 Snapshot section. **They do not appear in the client-facing brief body.**

---

### Step 1c: Contract status gate

Before calculating the effective date, confirm the account's contract structure.

Check available contract information (routing CSV, notes, or Finance records):
- Monthly or annual contract?
- Has the initial term ended?
- What is the next renewal date?

**Effective date rules:**
- Monthly contract: effective date = delivery date + 60 days (minimum written notice)
- Annual contract: effective date = no later than 90 days before the next renewal date
- If contract structure is UNKNOWN: flag as "Contract status unconfirmed — do not send until Finance confirms." Do not calculate an effective date.

Record the earliest enforceable effective date and the notice recipient (contract signatory). Both go in the prep sheet Contract Status section and the Format B routing note header. **Do not proceed to generate a Format B brief if contract status is unknown.**

---

### Step 2: Pull account pricing data

Read the migration table at:
`Downloads/2026-05-13__migration_table__v6.csv`

Find the row for `{{ORG_SHORTNAME}}`. Extract:
- `current_mrr`, `new_total_mrr`, `delta_mrr`, `delta_pct`
- `migration_driver` (determines which "Why the Number Is Changing" block to use)
- `assigned_tier`, `current_stack`
- `risk_label`

Also note the account's `health_band` and `health_score` from the routing CSV — internal routing note only, not the client-facing body.

---

### Step 2b: Pull account intelligence data (for prep sheet and Format C)

This step populates the prep sheet usage metrics and, for Format C briefs, the client-facing intelligence signals.

**Check for an existing IP2.0 run first:**
Look for a file at: `SuperCat 4.0/Insightful Product 2.0/runs/[ORG_SLUG]/` — if a recent run exists (within 60 days), read it and extract the relevant metrics directly.

**If no IP2.0 run exists, run on-demand queries using MCP tools:**

First, confirm the org_id by name:
```sql
SELECT id, name FROM organizations WHERE name ILIKE '%[ORG_NAME]%' LIMIT 5;
```

Use `user-supercat-postgres-vpn` for:

**Active rep count (last 90 days):**
```sql
SELECT COUNT(DISTINCT ou.user_id) AS active_reps_90d
FROM org_users ou
JOIN login_events le ON le.user_id = ou.user_id AND le.organization_id = [ORG_ID]
WHERE ou.organization_id = [ORG_ID]
  AND le.created_at > NOW() - INTERVAL '90 days';
```
If `login_events` does not exist, check `user_sessions` with `organization_id` column instead.

**Buyer count — three-layer definition (IMPORTANT: do not use raw `customers` table count alone):**
```sql
SELECT
  COUNT(*) AS total_customers_loaded,
  COUNT(DISTINCT o.customer_num) FILTER (WHERE o.is_submitted = true AND o.created_at > NOW() - INTERVAL '12 months') AS active_buyers_12mo,
  COUNT(DISTINCT o.customer_num) FILTER (WHERE o.is_submitted = true AND o.created_at < NOW() - INTERVAL '12 months') AS ever_ordered_pre_12mo
FROM customers c
LEFT JOIN orders o ON o.customer_num = c.code AND o.organization_id = [ORG_ID]
WHERE c.organization_id = [ORG_ID];
```
Derive: `dormant_buyers` = customers who have ever ordered but not in last 12 months = `ever_ordered_pre_12mo` minus those who also appear in `active_buyers_12mo`. For the brief, report all three: total loaded, active last 12mo, and dormant (ordered historically, silent 12mo+). Do NOT use total loaded as the sole buyer count — it includes accounts that have never transacted.

**Trailing annual orders:**
```sql
SELECT COUNT(*) AS orders_trailing_12mo
FROM orders
WHERE organization_id = [ORG_ID]
  AND is_submitted = true
  AND created_at > NOW() - INTERVAL '12 months';
```

**B2B Cart and mobile site status:**
```sql
SELECT id, url_key, enable_online_catalog, enable_online_ordering, enable_sales_portal
FROM mobile_sites
WHERE organization_id = [ORG_ID];
```
If no rows returned: no mobile site configured (iPad-only). Note this explicitly.

Use `user-bigquery-vpn` for:
- Trailing annual GMV estimate (if available in BigQuery cache)
- Portal session count (if Clicky/analytics data is in BigQuery)

**Record whatever data is available.** If a query fails or returns null, note "Not available" rather than leaving a blank. These metrics populate:
1. The prep sheet Health V3 Snapshot usage metrics table
2. The internal routing note header in Format C (use all three buyer count layers)
3. The "What's Not Working Right Now" section in Format C T1→T2 — use the three-layer buyer framing: total loaded, active ordering (12mo), dormant. Do NOT use total loaded count as a standalone "buyers per rep" ratio.
4. The conditional preview in Format C T2→T3 (if Engagement ≥ 60 AND Value Delivery ≥ 60)

---

### Step 3: Populate the templates

**3a — Client-facing brief**

Read the appropriate template:

| brief_type input | Template file |
|---|---|
| `format_a` | `SuperCat 4.0/Migration-Health Artifacts/02_briefs/templates/format_a_normalization_near_flat.md` |
| `format_b` | `SuperCat 4.0/Migration-Health Artifacts/02_briefs/templates/format_b_normalization_significant_delta.md` |
| `format_c_t1t2` | `SuperCat 4.0/Migration-Health Artifacts/02_briefs/templates/format_c_expansion_upgrade.md` (use Subtype A section, delete Subtype B) |
| `format_c_t2t3` | `SuperCat 4.0/Migration-Health Artifacts/02_briefs/templates/format_c_expansion_upgrade.md` (use Subtype B section, delete Subtype A) |

Replace every `[PLACEHOLDER]` with actual data. Follow all operator instructions embedded in the template. For conditional blocks (e.g., "FOR T3 ACCOUNTS — add this sentence"), evaluate and apply based on the account's tier — do not leave the instruction text in the output.

---

**Lede and "What You've Built" population (Format A and Format B only):**

Both Format A and Format B templates contain a LEDE BLOCK and, for Format A, a "What You've Built" section. These are the most important sections for accounts in Thriving or Healthy health bands — they open the brief with the client's own platform success story before landing the price change.

**Health band gate (evaluate from Step 1b):**
- **Thriving or Healthy:** Write the lede. It replaces the standalone price change sentence. For Format A, also write the "What You've Built" section.
- **Watch, At Risk, or Critical:** Delete the lede block and the "What You've Built" section entirely. Start the document with the standalone price change sentence. Do not attempt a lede with incomplete data or a generic placeholder.

**Fallback rule — data completeness:**
If active rep count, login volume (last 90 days), and tenure are not all confirmed from Step 2b data, **skip the lede entirely** regardless of health band. Begin with the standalone price change sentence. Do not write a lede with estimated numbers, ranges, or "approximately" language. A missing-data lede is worse than no lede.

**How to write the lede:**

*Quality bar:* Model it on the original pilot outputs at:
- `SuperCat 4.0/Migration-Health Artifacts/02_briefs/generated/bcf_braxton-culler_value-justification_2026-05-14.html`
- `SuperCat 4.0/Migration-Health Artifacts/02_briefs/generated/sarreid_value-justification_2026-05-14.html`

These are the gold standard. The lede should feel like a gift of intelligence — the client's own activity mirrored back to them — not like a performance review.

*Framing rules:*
1. Frame all stats as what the client has built, never as what SuperCat measured. Use "you've built," "your team," "your reps" — not "our data shows" or "health scoring indicates."
2. Do not use the words "health," "score," "band," "Thriving," "Healthy," or any assessment language. Those belong in the internal routing note only.
3. Pick the 2–3 most impressive and client-recognizable numbers — active reps vs. total, login volume, tenure, GMV or order volume, feature adoption highlight. Do not list everything — choose the most compelling.
4. End the lede paragraph by embedding the price change: "Your monthly invoice is moving from **$[CURRENT_MRR]** to **$[NEW_MRR]** — a **$[DELTA] change** — and this document explains exactly why." (Format A). For Format B: "Your monthly subscription is moving from **$[CURRENT_MRR]** to **$[NEW_MRR]** — an increase of **$[DELTA]/month ([DELTA_PCT])** — and this letter explains exactly why."

*Format A — "What You've Built" section (H2):*
After the lede paragraph, write 3–4 data point sentences as a short section under `## What You've Built on SuperCat`. Each sentence states one fact. Use only confirmed numbers from Step 2b. If a stat is unavailable, omit it — do not pad with estimates. Delete the section entirely if fewer than 2 confirmed data points are available.

*Format B — no "What You've Built" H2:*
The CEO letter is personal and relational. Stats go inline in the lede paragraph only — no separate section heading. The early-adopter acknowledgment paragraph ("You've been with us since [YEAR]...") follows the lede naturally; do not add a section break between them.

---

**Critical checks before saving the client-facing brief:**
- No `[PLACEHOLDER]` text remains (unfilled placeholders block sending)
- No instruction block text remains (all `**[FOR X ACCOUNTS...]**` conditional flags must be evaluated and either applied or deleted)
- The lede block gate was evaluated: either a written lede or the standalone price change sentence — never both, never neither
- No behavioral usage data in the client-facing body framed as assessment language (lede stats are the client's own output, not SuperCat health data)
- The close matches the brief type: Format A = CS contact follow-up; Format B = CEO personal call commitment with specific date; Format C = CSM named with action
- Format B close includes the formal notice sentence with the confirmed effective date
- For Format C T2→T3: the conditional preview section is only included if Engagement ≥ 60 AND Value Delivery ≥ 60 — delete it otherwise

**Save to:**
`SuperCat 4.0/Migration-Health Artifacts/02_briefs/generated/{{ORG_SHORTNAME}}_{{BRIEF_TYPE}}_[date].md`

---

**3b — Internal prep sheet**

Always generate the prep sheet alongside Format B briefs. Generate it for Format A and Format C when expansion is eligible or when the account is in Watch band or above.

Read the template at:
`SuperCat 4.0/Migration-Health Artifacts/02_briefs/templates/internal_ceo_cs_prep_sheet.md`

Populate using all data gathered in Steps 1–2b:
- Account Snapshot: from migration table and routing CSV
- Contract Status: from Step 1c
- Health V3 Snapshot: from Step 1b (dimension scores, narratives, flags, usage metrics)
- Migration Driver: plain-language explanation of the specific rate correction
- Likely Objections: use the standard blocks; add account-specific context in brackets where relevant
- Concession Hierarchy: fill "Available here?" column and 25% guardrail check before the call
- Churn Risk: use health band + trend + support fire flag from Step 1b
- Expansion Notes: only if expansion_eligible = YES

**Save to:**
`SuperCat 4.0/Migration-Health Artifacts/02_briefs/generated/{{ORG_SHORTNAME}}_prep-sheet_[date].md`

---

### Step 4: Report back

After saving both files, summarize:
1. All placeholders successfully filled (or list any that remain and why)
2. Which "Why the Number Is Changing" driver block was used
3. Health V3 data found — composite score, band, and whether any flags were set
4. Contract status confirmed — earliest enforceable effective date used
5. IP2.0 run status — existing run used vs. on-demand queries run
6. Any operator checks that flagged an issue (flags in routing CSV, contract unknown, behavioral floor, etc.)
7. Whether the brief is ready to send or needs review
8. File paths of both saved outputs

---

## Peer Price Anchors (reference — do not look these up, use as-is)

| Tier | p25 | p75 |
|---|---|---|
| T1 (Catalog Essentials) | $774/mo | $1,629/mo |
| T2 (Commerce Professional) | $1,295/mo | $1,589/mo |
| T3 (Commerce Enterprise) | $2,295/mo | $2,875/mo |

---

## Sample Accounts (for testing)

**Format A pilot — `bcf` (Braxton Culler, T3, Thriving, +0.6%)**
**Format B pilot — `sarreid` (Sarreid Ltd., T3, Thriving, +33.1%)**
**Format C T1→T2 pilot — `mh` (Magnussen Home, T1, Thriving, +7.9% migration confirmed)**
