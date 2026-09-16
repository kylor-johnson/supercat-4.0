# Wave 2.1 — Authoring Prompt for `_root/02_who_is_being_migrated.md`

> **For paste into a fresh Cursor agent chat as the first message.** Do not modify before pasting.
> **Drafted**: 2026-05-22 by planning agent
> **Output target**: `Pricing Migration/_root/02_who_is_being_migrated.md` (replace stub contents)
> **Estimated authored length**: 250–400 lines
> **Dependency**: Independent of `_root/04`. Can be authored after Wave 1 has produced `_root/01` and `_root/CONTRACTS.md`. Best paired with Wave 2.3 (`07_data_pipeline.md`) — the segments authored here will be referenced by the pipeline doc, and the pipeline doc will reference the data-source-of-truth rules established here.

---

## You are a fresh agent

You have no prior context about the SuperCat Pricing Migration. Your independence makes your output trustworthy. Your job is to author **one file** — `Pricing Migration/_root/02_who_is_being_migrated.md` — using only the materials this prompt directs you to.

You will not improvise. If anything is unclear, stop and ask the operator.

---

## Step 1: Required reading (in this exact order)

Read each file completely. Echo each file path + last-updated date in your first chat response.

### Folder orientation (mandatory)
1. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/AGENTS.md`
2. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/00_README.md`
3. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/CONTRACTS.md`
4. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/02_who_is_being_migrated.md` (the stub — read the "owns / does not own" boundary)
5. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/01_why_we_are_migrating.md` (the WHY doc; read so your WHO doc doesn't restate any of its content)

### Primary content sources (mandatory — these are the data foundations)

6. **The execution plan, v3.3** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_reference/2026-05-20__execution_plan_v3.3.md`. **Read these sections in full**: §II (Segment definitions and account counts), §IV (June/July/Deferred cohort assignment + timing), §VI (Health-modifier rules and overrides), and the §"What Changed v2 → v3.3" table for context on why the current 8-segment vocabulary exists.

7. **The authoritative account dataset** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_master-account-data-v6.2.csv`. Open and read at least the header row and the first ~10 data rows. **Cite the columns by name** when authoring — every field reference in your output should match a literal column in the v6.2 CSV. Do not invent fields. Do not paraphrase column names.

8. **The routing CSV** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/migration_comm_tiers_2026-05-19.csv`. Read header row + first ~10 data rows. The routing CSV's `comm_action` and segment columns feed into format mapping (which lives in `_root/06`, not here). You read it to understand the link between segment and routing — your doc owns the segment definitions; `_root/06` owns the routing logic.

### Do NOT read

- `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/**` — per `_root/CONTRACTS.md` §4. The segment vocabulary in the archive is older and superseded by exec plan v3.3.
- The other `_root/` stubs (04, 05, 06, 07, 08) — they are being authored in parallel. Your scope is `_root/02`.

---

## Step 2: What you are authoring

`_root/02_who_is_being_migrated.md` is the **roster doc**. Anyone asking "which accounts are getting which kind of migration treatment, and why?" reads this doc. It answers at the segment level — not at the per-account level. Per-account specifics live in the v6.2 CSV, which this doc points to as the source of truth.

The doc owns exactly the following content. Author each as its own section in this order:

### Section 1 — The 8 migration segments

A table with: **Segment name** | **Definition** | **Account count** | **Avg / median delta** | **Owner (CS / CEO / CEO+CS)** | **Notes**.

Source: exec plan v3.3 §II. The 8 segments as named there. Preserve their exact names — do not rename or "improve." Account counts are as of the v3.3 plan; if v6.2 CSV reveals a more recent count for any segment, prefer the CSV and add a note ("v6.2 CSV reports N; v3.3 plan reported M — using CSV as source of truth per `_root/07` hierarchy").

End the section with: "The 8-segment vocabulary is the authoritative way to talk about *what kind of customer is being migrated*. The 4-format vocabulary (Format A / Format B / CEO Letter / Good News) — which is *how a customer gets communicated to* — is the routing layer and lives in `_root/06`."

### Section 2 — The ownership boundary ($200 / $400 / $600)

A short subsection (~100 words) explaining the dollar-delta thresholds that determine who owns the comm:
- Delta ≤ $200/month: CS-owned (Format A)
- Delta > $200/month and ≤ $600/month: CS-owned but escalated (Format B)
- Delta > $600/month: CEO-owned (CEO Letter)
- Exceptions: entity overlay, health overrides — flagged separately in this doc and detailed in `_root/06`

State the rule. State the rationale (CEO bandwidth is the constraint; the dollar threshold is how we triage). Do not state the routing CSV's exact `comm_action` values here — those live in `_root/06`.

### Section 3 — The entity overlay rule

A short subsection. Source: exec plan v3.3 §II + §IV. Entity parents (accounts that represent a group of related accounts) receive a single coordinated treatment — even if any individual entity-child would route differently. State the rule: identify entity parents from the `entity_parent` flag in v6.2 CSV; the parent's treatment supersedes individual children's; the CEO is involved in entity-parent conversations. List the count of entity parents from v6.2.

### Section 4 — Health overrides (VD<40, Watch, At Risk, Critical)

A short subsection. Source: exec plan v3.3 §VI + the inline health-band logic visible in the archived templates (which is the operationalization of this rule).

State:
- Health is computed as a composite of Engagement, Adoption, Value Delivery, Ops Health (the four sub-scores in v6.2 CSV).
- A Value Delivery score <40 forces a "Watch" or worse band regardless of the composite.
- Watch / At Risk / Critical health bands trigger an *override* in two places: (a) the voice (the lede block changes — see `_root/04` §health-band-overrides for the voice rule); (b) the routing (the format selection may be downgraded to ensure CEO involvement — see `_root/06`).

This section owns the *health-band-triggers-override* rule. It does not own the voice override itself (that's `_root/04`) and does not own the routing override itself (that's `_root/06`) — it owns the *trigger*.

### Section 5 — Annual overlay

A short subsection. Source: exec plan v3.3 §IV. Accounts on annual contracts have a ≥90-day notice requirement before renewal. State the rule. State the consequence: annual accounts may be routed to a *deferred* cohort if the standard cohort timing would violate the 90-day window. Identify the `contract_type` field in v6.2 CSV that flags annual.

### Section 6 — Cohort assignment (June / July / Deferred)

A table: **Cohort** | **Send window** | **Earliest enforceable effective date** | **Account count** | **Segments included**.

Source: exec plan v3.3 §IV. Populate the table from §IV's cohort definitions. Cross-check with v6.2 CSV's `cohort` column (or equivalent — name the actual column). If counts disagree between v3.3 plan and v6.2 CSV, prefer the CSV and note the difference.

Note: the 60-day notice window is structural (regulatory / contractual). The cohort timing flows from the notice window + the annual overlay + the strategic ordering of which segments go first. The cohort assignment IS rule-bound; it is not an operator preference.

### Section 7 — The five known routing-CSV errata

A short subsection. Source: the archived `_handoff-prompt.md` §"Data Corrections" listed five specific routing-CSV errata that were caught during drafting. These corrections must persist into the refactored system.

You ARE permitted to read `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/_handoff-prompt.md` §"Data Corrections (routing CSV was wrong on these)" for this specific extraction. This is an explicit per-prompt override of the anti-archive rule per `_root/CONTRACTS.md` §4 (the "explicitly directed read" exception).

Render the 5 errata as a list: **Account** | **CSV value** | **Corrected value** | **Reason**.

End with: "These corrections are not yet baked into the routing CSV itself. Until they are, every routing decision must cross-check against this list. The corrections also live in `_root/06_format_routing.md` (the routing doc owns the routing decision; this doc owns the errata so the segment-roster is canonical)."

### Section 8 — Pointer to the per-account roster (with the 107/109/locked-pricing reconciliation)

A short closing section. The per-account roster is in `_master-account-data-v6.2.csv`. State this. Name the key columns the roster carries (`baseitemcode`, `account_name`, `tier`, `migration_driver`, `delta_dollar`, `delta_pct`, `health_score`, `health_band`, `entity_parent`, `contract_type`, `cohort`, etc. — verify these match the actual CSV header before authoring; if they don't, USE THE ACTUAL COLUMN NAMES from the CSV). Point readers to `_root/07_data_pipeline.md` for how to load and use the CSV.

**Reconciliation required (carried over from Wave 1.2 review):** The exec plan v3.3 §I states **109 accounts mapped** with corrected economics, but **107 migration-pending** in the cohort total (June 55 + July 16 + Deferred 36 = 107). The foundation excerpt (foundation 2 / 03_how_we_make_money.md §"How the migration works") separately names a **5-account locked-pricing / in-implementation cohort** as "exceptions in the migration plan, not part of the default motion." Resolve and state explicitly in this section:
  - How many accounts are in v6.2 CSV total?
  - How many are migration-pending (the 107)?
  - What are the 2 non-pending accounts (109 − 107)? Are they the 5-account locked-pricing cohort (in which case the foundation count is stale), a subset of it, or unrelated?
  - Cite v6.2 CSV as the source of truth for the answer. If v6.2 cannot answer cleanly (e.g. no `migration_status` flag), flag the gap in the conformance block — the operator may need to add a column.

This reconciliation is the authoritative count for the entire system. `_root/01` §4 ("Definition of done") references the 107-pending count and points here for the full reconciliation. Get this right; downstream docs trust it.

### Header block

Match the pattern in other root-doc stubs:
- `> **Last updated**: 2026-05-22`
- `> **Owner**: CEO`
- `> **Primary sources**: `_reference/2026-05-20__execution_plan_v3.3.md` §II + §IV + §VI; `_master-account-data-v6.2.csv`; `migration_comm_tiers_2026-05-19.csv`; archived `_handoff-prompt.md` §Data Corrections (explicitly-directed extraction per `_root/CONTRACTS.md` §4)`
- `> **What this doc owns** / `> **What this doc DOES NOT own**` — populate from the stub's existing values plus what you actually authored

---

## Step 3: What this doc does NOT contain

- **No format mapping** (segment → Format A/B/CEO Letter/Good News). That belongs to `_root/06`.
- **No driver framing.** Drivers are referenced (the v6.2 CSV has a `migration_driver` field) but the per-driver content lives in `_root/05`.
- **No voice/tone differences by health band.** The HEALTH BAND triggers an override here; the override's content lives in `_root/04`.
- **No data-loading mechanics.** "Run this Python to filter v6.2 by cohort" belongs to `_root/07`.
- **No per-account exceptions.** The 109-account roster IS exceptions; this doc points to the CSV.

If you find yourself writing toward any of those topics, remove and reference the owning doc.

---

## Step 4: Voice and format constraints

- Register: operator-facing, declarative. Same register as `01_why_we_are_migrating.md` and `AGENTS.md`.
- Tables: use Markdown tables for the 8-segment listing, the cohort listing, the errata listing. Tables make the data scannable.
- No emojis.
- When a field name from the CSV appears in prose, render it as `` `column_name` `` (backticks) so the reference is greppable.

---

## Step 5: Output

Replace the entire current contents of `Pricing Migration/_root/02_who_is_being_migrated.md` with the authored document.

Then, in your chat reply (NOT in the file), produce this conformance block:

```
─── Conformance Block ─────────────────────────────────────────
Authored: _root/02_who_is_being_migrated.md (replaced stub)
Files read:
  - <enumerate items 1–8 from Step 1 with last-updated dates>
Explicitly-authorized archive read: Pricing Migration/_archive/.../_handoff-prompt.md §Data Corrections (per Section 7 of this prompt)
Files NOT read: every other archive file, every other root-doc stub
Segments authored: <count, should be 8>
Cohorts authored: <count, should be 3 — June / July / Deferred — confirm against exec plan §IV>
Errata authored: <count, should be 5>
CSV columns referenced — and verified to exist in v6.2: <list>
CSV columns referenced but NOT found in v6.2: <list, or "none" — if non-empty, this is a gap requiring operator input>
Account count from v6.2 (total active): <number>
Discrepancies between v3.3 plan and v6.2 CSV (account counts, segment names, etc.): <list with my chosen resolution per source-of-truth hierarchy, or "none">
Open questions for operator: <list, or "none">
─────────────────────────────────────────────────────────────
```

Then **STOP**. The operator will paste your output back for review before the next wave begins.

---

## Step 6: If something is missing

If a section the prompt asks you to author cannot be supported by the named sources, stop and ask. Most common gap: a CSV column the prompt references doesn't exist or is named differently. State which column you expected and which columns you actually found.
