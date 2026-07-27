# Handoff: run this week's onboarding Phase Progression assessment (current: v3.5)

**To:** the next agent (fresh session)
**From:** the prior agent (which built v3.1)
**Date:** 2026-06-05
**Operator:** Kylor Johnson (CEO, SuperCat Solutions)

---

## Why you're here

The prior session built v3.1 of the onboarding Phase Progression Framework and an audit that justifies every change vs v3.0. The framework is conceptually ready but has never been run end-to-end. Your job is the first real run — produce this week's dated assessment file and surface any ambiguities the framework spec doesn't already resolve.

You were chosen for this because the prior agent has 5 hours of accumulated context that biases interpretation. A fresh agent reading only the framework + this handoff will catch spec gaps the prior agent has already filled in subconsciously. Push back if anything is ambiguous — that feedback is the most valuable thing you can produce besides the output file itself.

---

## What is in scope (read these, in order)

1. **The framework you're executing — the canonical spec:**

   The framework lives in 4 coordinated files. Together they are the SOURCE OF TRUTH. Read all four end-to-end before running a single query.

   1. `SuperCat 4.0/onboarding-models/Phase_Progression_Framework.md` (current version) — thin index: version header, "what this is," "what changed," file layout, change log. Treat its version header as the source of truth for which version you're running.
   2. `SuperCat 4.0/onboarding-models/Phase_Anchors.md` — auto-cohort SQL, `client_domains[]` resolution, Sources table, the 7 phase definitions (Anchor + Done-when + per-phase health + Common ambiguity), and the Integration Workstream (parallel).
   3. `SuperCat 4.0/onboarding-models/Flags_and_Signals.md` — Hard rules (no metric without a tool call, verifiable-quote rule, etc.) and the 6-section ambiguity flag taxonomy (Sections A–F).
   4. `SuperCat 4.0/onboarding-models/Output_Contract.md` — phase-assignment algorithm, per-client output structure, cohort-level output, deliberate non-goals, and run-mechanics summary.

2. **eCat ground truth (so you understand what the import files mean):**
   `~/Downloads/llms.txt` — the data spec for products / customers / inventory / stories / options / matrix_options. Required reading to interpret import_events YAML correctly.

3. **Audit rationale (skim only — context for why v3.1 looks the way it does):**
   `SuperCat 4.0/onboarding-models/Phase_Progression_Framework_AUDIT.md`

   You do not need to verify the audit's claims — they're already applied to v3.1. Skim Section 2 (per-phase findings) only if a phase anchor in the framework looks surprising; the audit explains why each one is shaped the way it is.

## What is OUT of scope — DO NOT read or invoke

- **`SuperCat 4.0/onboarding-models/_archive/`** — everything in here is superseded. Includes:
  - `_archive/Phase_Progression_Framework_v3.0_baseline.md` — the pre-audit baseline; v3.1 is canonical and v3.0 has anchor clauses that have been corrected.
  - `_archive/v2_stage_gated_2026-06-05/` — the OLD 11-stage system (`Stage_Gated_Data_Collection.md`, `Validation_Layer_Fathom_HelpScout.md`, `Output_Format.md`, old `RUN_PROMPT.md`, old `README.md`). Different framework entirely. Do not read.
  - `_archive/baseline_pre-bq-migration_2026-06-03/`, `_archive/superseded_versions/` — older snapshots, ignore.
- **`SuperCat 4.0/.cursor/skills/ecat-onboarding-orchestrator/`** — misguided per the audit; do not invoke.
- **`~/Downloads/index (1).html`** (admin training HTML) — referenced in the framework's Phase 6 rationale; you do not need to read it to run the framework.

If anything in `_archive/` tempts you (e.g. the old SQL queries look more detailed), resist. v3.1's queries are the corrected ones; the old ones have known bugs (LIMIT-trap on batched IN-clauses, `external_rep` contamination, etc.).

---

## Tools you have

| Tool | Server | Use for |
|---|---|---|
| `execute_sql` | `user-supercat-postgres-vpn` | All eCat config + cohort detection. Read-only. VPN required. |
| `query` | `user-bigquery-admin` | Fathom + HelpScout. `SELECT`-only against source tables. VPN required. |

Both require VPN active. The Sources table in `Phase_Anchors.md` lists the exact view/table names. The BigQuery views you'll mostly use:

- `supercat-data-pipeline.onboarding_assessment.fathom_recent_meetings`
- `supercat-data-pipeline.onboarding_assessment.helpscout_tickets`
- `supercat-data-pipeline.mixpanel.events` (if you need order-submitted-event recency)

---

## Your task — execute the current framework end-to-end

### Step 0 — Run date and cohort

1. Run `date -u +%F` to set `$RUN_DATE` (used in the output filename).
2. Execute the **auto-cohort query** verbatim from `Phase_Anchors.md § The cohort — auto-detected`. Confirm it returns exactly 4 onboarding clients (as of 2026-06-05 these were `tcs`, `drf`, `libco`, `pebl` — but check today's result; new clients may have entered the cohort).
3. For each cohort member, resolve `client_domains[]` per `Phase_Anchors.md § Resolving \`client_domains[]\``. The resolution order is:
   1. Manual override in `onboarding-models/overrides.yml` under `client_domains:` (a committed map of shortname → domain list). If the shortname is listed there, use that list verbatim and stop — it is authoritative and overrides every step below.
   2. `organizations.order_email_recipient` domain (when set and not a placeholder)
   3. HubSpot company primary domain (if integrated — may be empty)
   4. **Fallback:** admin `org_users.users.email` domains, EXCLUDING the personal-email-providers list in `Phase_Anchors.md § Resolving \`client_domains[]\``

   **Within a single chosen source, include all of that source's distinct non-personal domains; do NOT merge across sources.** The first non-empty source wins outright. When the chosen source is the step-4 admin-email fallback and it yields ≥2 distinct domains, raise `MULTI_DOMAIN_FALLBACK_UNVERIFIED` (and, if a second legit parent/DBA domain is real, fold it into `overrides.yml § client_domains` so it stops needing verification). Record each client's resolved `client_domains[]` — every Fathom / HelpScout / rep query downstream matches on these.

4. Read `onboarding-models/overrides.yml`. It is a small committed config of human-confirmed facts the live data can't express. It carries:
   - `net_price_only_confirmed:` — shortnames that run single Net-Price-only pricing by design. Any org listed there satisfies the Phase 3 price requirement and must NOT raise `SINGLE_PRICE_LEVEL_UNCONFIRMED` (see `Phase_Anchors.md § Phase 3` Done-when).
   - `integration_status:` — for clients SuperCat owns the integration on (a `Managed Integration` deal line item, per Step 2), the recorded approach/status. A shortname present here suppresses `INTEGRATION_OWNER_UNCLEAR` (it is now tracked); absent → the flag fires for managed clients.
   - `client_domains:` — manual domain overrides consumed in Step 0.3 above.
   - `project_start_date:` — ISO date (`YYYY-MM-DD`) for clients whose account was provisioned well before the real project kickoff. When present, use this date instead of `organizations.created_at` to compute `days_in_onboarding`.

   Integration **ownership** is NOT decided here — that comes from the HubSpot deal line items in Step 2. This file only records the *status* of an owned integration and the by-design/domain facts above.

   > If `overrides.yml` contains a `project_start_date` for this client, use that date (not `organizations.created_at`) to compute `days_in_onboarding`. This handles cases where provisioning significantly preceded the real project kickoff.

### Step 1 — Per-client phase classification

For each client in the cohort, walk Phases 1 → 7 in order, evaluating the Anchor and Done-when clauses verbatim from `Phase_Anchors.md § Phase N` (the per-phase sections also carry per-phase health metrics and Common ambiguity callouts). Use these patterns:

**Postgres metrics:** the v3.0 framework had a useful set of queries in `_archive/v2_stage_gated_2026-06-05/Stage_Gated_Data_Collection.md` — DO NOT read that file, but DO use these primitives, which v3.1 still needs:

```sql
-- Product / image / customer / option counts per client (batched is fine for counts)
SELECT o.shortname,
  (SELECT COUNT(*) FROM products p WHERE p.organization_id = o.id AND p.deleted = false) AS products,
  (SELECT COUNT(*) FROM products p WHERE p.organization_id = o.id AND p.deleted = false AND p.image_exists = true) AS prods_with_img,
  (SELECT COUNT(*) FROM products p WHERE p.organization_id = o.id AND p.deleted = false AND COALESCE(p.hideable, false) = false) AS visible_products,
  (SELECT COUNT(*) FROM customers c WHERE c.organization_id = o.id) AS customers,
  (SELECT COUNT(*) FROM inventories i WHERE i.organization_id = o.id) AS inventory,
  (SELECT COUNT(*) FROM price_levels pl WHERE pl.organization_id = o.id) AS price_levels,
  (SELECT COUNT(*) FROM options opt WHERE opt.organization_id = o.id) AS options,
  (SELECT COUNT(*) FROM option_groups og WHERE og.organization_id = o.id) AS option_groups,
  (SELECT COUNT(*) FROM user_types ut WHERE ut.organization_id = o.id) AS user_types,
  (SELECT COUNT(*) FROM ipad_reports ir WHERE ir.organization_id = o.id) AS ipad_reports,
  (SELECT COUNT(*) FROM orders ord WHERE ord.organization_id = o.id) AS orders,
  o.order_email_recipient, o.send_order_email_on_submit, o.created_at
FROM organizations o WHERE o.shortname IN (...);
```

**Import events (most-recent-per-file-type — v3.5 change):**

Run **one query per file type** (Products, Customers, Options, Option Groups, Inventory, Product Stories). Each returns the single most-recent import event for that file type and org:

```sql
SELECT ie.file_type, ie.created_at, ie.num_warnings, ie.num_errors,
       ie.warning_message, ie.error_message
FROM import_events ie
WHERE ie.organization_id = (SELECT id FROM organizations WHERE shortname = $SHORTNAME)
  AND ie.file_type = 'Products'
ORDER BY ie.created_at DESC
LIMIT 1
```

Repeat for each file type, substituting `'Customers'`, `'Options'`, `'Option Groups'`, `'Inventory'`, `'Product Stories'` in the `ie.file_type =` clause. This is the primary documented approach — it avoids the MCP tool validation failures that both the `CROSS JOIN LATERAL` (v3.2) and `CTE + CROSS JOIN` (v3.4) patterns hit in practice.

> **Known-broken (preserved for reference):** The v3.4 CTE + `CROSS JOIN` query and the earlier v3.2 `CROSS JOIN LATERAL (VALUES ...)` form both failed MCP tool validation on every run that attempted them (2026-06-09, 2026-07-01). The per-file-type correlated subquery pattern above is the one that actually executes cleanly.

**Why per-file-type matters:** in the 2026-06-08 run, DRF's Customers import (04-27) and all non-Products events fell outside the 30 most-recent rows because image-import events dominate the recent history. A naive recency window would report "Products only" and fail the Phase 3 "≥2 core files in 60d" clause → wrong anchor. One query per file type guarantees one row per file type, matching the block-level rule in `Phase_Anchors.md § Phase 3`.

YAML shape is `- - <FileType>` per `Phase_Anchors.md § Phase 2 — Initial Import`. A single row may have multiple file-type blocks. Parse at the **block level** (per `Phase_Anchors.md § Phase 3 — Progress`), not the row level.

**Rep classification (the corrected v3.1 rule, NO client_domains exclusion):**

```sql
SELECT o.shortname, ut.name AS user_type, u.email, ou.is_admin, ou.disabled, ou.last_ipad_login_at,
  CASE
    -- NOTE: This personal-email-providers list must stay in sync with Phase_Anchors.md § Resolving client_domains[]. Edit both or neither.
    WHEN lower(split_part(u.email,'@',2)) IN ('gmail.com','yahoo.com','outlook.com','icloud.com','hotmail.com','me.com','aol.com','fuse.net','proton.me','protonmail.com') THEN 'personal_email'
    -- 'in_house' if domain in client_domains[]; 'external' otherwise — compute per-client in code
    ELSE 'external_or_in_house'
  END AS rep_subtype_raw
FROM org_users ou
JOIN organizations o ON ou.organization_id = o.id
JOIN users u ON ou.user_id = u.id
LEFT JOIN user_types ut ON ou.user_type_id = ut.id
WHERE o.shortname IN (...)
  AND ou.is_admin = false
  AND COALESCE(ut.name, 'DefaultUserGroup') <> 'DefaultUserGroup'
  AND u.email NOT LIKE '%@supercatsolutions.com'
  AND COALESCE(ou.disabled, false) = false;
```

Apply the `in_house` vs `external` split using each client's resolved `client_domains[]` in your output, not in SQL.

**Orders (for Phase 5 health + Phase 7 clause 3):**

```sql
SELECT o.shortname, ord.id, ord.bill_to_company_name, ord.created_at, ord.submit_date,
  ord.is_submitted, u.email AS submitter, ou.is_admin
FROM orders ord
JOIN organizations o ON ord.organization_id = o.id
LEFT JOIN org_users ou ON ord.org_user_id = ou.id
LEFT JOIN users u ON ou.user_id = u.id
WHERE o.shortname IN (...)
ORDER BY o.shortname, ord.created_at DESC;
```

For Phase 7 clause 3 (real customer order in last 90d), apply the **allowlist rule** per `Phase_Anchors.md § Phase 7 — Go-Live (terminal)`: `lower(trim(bill_to_company_name))` must match an existing `customers` row for this org (`lower(trim(customers.company_name))`). A bare mismatch against `organizations.name` is NOT sufficient — see PEBL precedent (v3.2 change). The require-customer-match approach fails safe (an unmatched order under-advances the client and is recoverable next run), unlike the denylist v3.1 originally used.

**Fathom (per client_domains):**

```sql
SELECT meeting_title, meeting_start, duration_minutes, fathom_user,
  external_domains, invitee_emails, section_titles, recording_url, summary
FROM `supercat-data-pipeline.onboarding_assessment.fathom_recent_meetings`
WHERE meeting_start >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
  AND EXISTS (SELECT 1 FROM UNNEST(external_domains) d WHERE d IN ('[client_domain_1]', '...'))
ORDER BY meeting_start DESC;
```

**HelpScout (per client_domains):**

```sql
SELECT ticket_number, ticket_subject, ticket_status, thread_created_at,
  thread_created_by_type, thread_author_email, tags, thread_body
FROM `supercat-data-pipeline.onboarding_assessment.helpscout_tickets`
WHERE primary_customer_domain IN ('[client_domain_1]', '...')
  AND thread_created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
ORDER BY thread_created_at DESC;
```

For Phase 6 qual trigger #4 and Phase 7 clause 4 (Kyla-presence dominance), filter on `thread_author_email LIKE '%@supercatsolutions.com'` in the last 30 days, then compute the ratio of non-`kylor@` authors to total SuperCat authors. The trigger fires when ≥40% are non-Kylor (see `Phase_Anchors.md § Phase 6`).

### Step 2 — Integration workstream (HubSpot deal line items are the source of truth)

Ownership is decided by **what the client bought**, read from the HubSpot deal line items — NOT inferred from meeting keywords. Run this first (BigQuery), matching each org to its HubSpot company by domain:

```sql
WITH co AS (
  SELECT company_id, properties_name AS company, LOWER(properties_domain) AS domain
  FROM `hubspot.company`
  WHERE LOWER(properties_domain) IN ('[client_domain_1]', '...')   -- the cohort's client_domains[]
)
SELECT co.company, d.deal_id, d.properties_dealname AS deal, li.properties_name AS line_item
FROM co
JOIN `hubspot.company_deal` cd ON cd.company_id = co.company_id
JOIN `hubspot.deal` d          ON d.deal_id = cd.deal_id
JOIN `hubspot.line_item_deal` lid ON lid.deal_id = d.deal_id
JOIN `hubspot.line_item` li    ON li.line_item_id = lid.line_item_id
WHERE li.properties_name LIKE '%Managed Integration%'
   OR li.properties_name LIKE '%Certified Pipeline%'
ORDER BY co.company, d.deal_id, li.properties_name;
```

Then classify per `Phase_Anchors.md § Integration Workstream (parallel)`:

- A **`Managed Integration Build` / `Managed Integration Hosting`** line item → Owner = **us**; show the Integration row + block; this is our workstream. Read the recorded status from `overrides.yml § integration_status` for this shortname. If no entry exists there, raise `INTEGRATION_OWNER_UNCLEAR` (managed-but-untracked); if an entry exists, use its `status`/`approach` and do NOT raise the flag.
- A **`Certified Pipeline`** line item → Owner = **them**; emit a single informational line only; do NOT show an open workstream and do NOT raise an integration flag.
- **No integration line item** → self-serve FTP / none → **suppress the Integration row and block entirely.** Do not mention it on the standup.

Multiple deals → highest posture wins (Managed > Certified > none). Enrich `Approach` / `Last activity` from the most recent integration-keyword Fathom/HelpScout (color only — never let it override the line-item ownership). When `overrides.yml § integration_status` has no entry for a managed client, Status = `unset` and `INTEGRATION_OWNER_UNCLEAR` fires.

### Step 3 — Flag emission

For each client, walk all 6 flag sections (A–F) in `Flags_and_Signals.md § Ambiguity flags (the standup agenda)` and emit any flag whose trigger fires. The Hard rules in `Flags_and_Signals.md § Hard rules (non-negotiable)` govern emission discipline (no metric without a tool call; verifiable-quote rule; etc.). Every flag needs a source (Fathom date / HelpScout ticket # / Postgres metric / import-event date) and, where the trigger says "verbatim quote," an actually-retrieved quote — not a paraphrase, not a memory.

When a client has `customers = 0`, inspect the `Customers` row from the import-events query (Step 1) before defaulting to the generic `PHASE_4_VACUOUS_NO_CUSTOMERS`. If the most-recent `Customers` event carries an `:error`/`:fatal` whose message matches a price-code mismatch (regex in `Flags_and_Signals.md § F`, `CUSTOMER_IMPORT_PRICE_CODE_MISMATCH`), raise that specific flag instead — it names the actual cause (file rows reference price codes that aren't Admin price levels) rather than just "no customers yet."

### Step 4 — Assemble the output

Follow `Output_Contract.md § Per-client output structure` and `Output_Contract.md § Cohort-level output (top of file)` exactly. Sort per-client sections by Anchor phase ascending (least far → most far). The phase-assignment algorithm (Anchor / Current / open workstreams / out-of-order narrative) is in `Output_Contract.md § Phase assignment algorithm`.

**`Output_Contract.md § Voice & readability (every run)` is binding.** This is a standup read, not an internal doc. Write plain English; obey the banned-words list; expand acronyms; lead each client with "Phase N of 7" (no readiness %). **Never print an internal flag code anywhere in the client-facing body — not as a title and not in parentheses.** Each flag gets a plain-English title; the title↔code mapping goes in the bottom appendix's flag-reference map (the only place a code may appear). Put run metadata and framework feedback in the bottom appendix per `Output_Contract.md § Appendix`, never at the top. Show the Integration row/block only when SuperCat owns the integration (Step 2).

**Write the result to `SuperCat 4.0/onboarding-models/output/{YYYY-MM-DD}-phase-assessment.md`.** Use the dated filename. This is the canonical output location.

### Step 4b — Emit JSON + render the HTML

The run produces three siblings from the **same computed state**: the `.md` (Step 4, human-readable record), a `.json` (structured data), and a `.html` (rendered report). **HTML is rendered from the JSON by a deterministic generator — the markdown is never parsed to produce HTML.** You author the JSON; the generator does everything mechanical (escaping, asset paths, region cloning) and refuses to write if anything is unresolved.

New Phase-1 surface (all live in `onboarding-models/`; you did NOT see these before). Read only these two — they are the contract; do not re-read the four framework files:

- `phase-assessment.schema.json` — the JSON contract (draft-07): every field, type, enum, required rule. **Authoritative field list.**
- `HTML_Artifact_Contract.md` — the rendering contract (escaping rule, fixed vocabulary, run-wiring section).

Do NOT open or edit `phase-assessment.template.html`, `phase-assessment.css`, `render_phase_assessment.py`, the schema, or the golden pair (`EXAMPLE-2026-06-09-phase-assessment.html` + `EXAMPLE-2026-06-09-phase-assessment.json`). They are fixed infrastructure.

**1. Emit `output/{$RUN_DATE}-phase-assessment.json`** conforming to `phase-assessment.schema.json`. Map your already-computed concepts to fields (this crosswalk is the only authoring detail not already in the schema):

- `report.title` = the md H1 (`"{Month D, YYYY} — Onboarding Phase Assessment"`); `report.source_md` = the md path you just wrote; `report.run_metadata` = the appendix metadata line.
- `agenda.{resolve,discuss,on_track}` = your three standup buckets (the one-bucket-per-client rule from Step 4 still holds). Each item = `lead` (bold lead text **including its terminal punctuation**, e.g. `"Lib and Co. — fix the customer import."`; on-track items are usually just the client name) + `detail_html` (rest of the line, trusted HTML). Set `"urgent": true` on the **single** most urgent resolve item, or on none — **≤1 across the whole report** (the generator enforces this).
- `clients[]` (sort phase-ascending): `short`, `name`, `phase_n` = Anchor, `phase_name` = the fixed label for that step, `next_phase_name` = the phase_n+1 label or `"Live"`, `current_step` = the working-on step (Anchor+1, capped at 7), `product`, `days`, optional `days_qualifier`, `engagement`, `one_thing`, `next_step`, `bottom_line`, and `activity` = `{meetings, support, imports}` (one short line each). Optional `note_html` = the free paragraph the md puts *after* the flags table (a read/caveat or out-of-order observation); use it rather than stuffing that commentary into a flag's `said_html` or `bottom_line`.
- `clients[].integration.mode` = your Step 2 ownership result: `managed` (+`status`, +`what_we_see`), `certified` (+`note`), or `none`. This mirrors the existing "show Integration only when we own it" rule — `managed` → an 8th row, `certified` → one note, `none` → neither.
- `clients[].steps` = **exactly 7** (`no` 1–7, in order), `status` ∈ `done`/`in_progress`/`not_started` (step 7 only `done`/`not_started`), `what_we_see` = one plain sentence. Mirrors "Where they are."
- `clients[].flags` (omit/empty when none): `step` (`"1"`–`"7"`, a span like `"3/4"`, or `Integration`), `issue` = plain title (**never the code**), `code` = internal flag code or `null`, `source`, `said_html` = a verbatim quote wrapped in `<blockquote class="oa-quote">` **or** a plain metric. This carries the verifiable-quote hard rule — quotes stay verbatim. (The on-screen `(CODE)` suffix is the HTML home of the appendix flag-reference map; the code never appears as the title.) **Set `code: null` for confirmed/by-design/suppressed informational rows** — never render a code whose name contradicts its confirmed state (e.g. a confirmed single-net-price row must not show `…_UNCONFIRMED`).
- `appendix.overrides[]` / `appendix.feedback[]` = your bottom-appendix notes, as trusted inline HTML (wrap identifiers/table names in `<code>`).

**Escaping (the one rule that bites):** plain-text fields are authored **raw** — write `Lib & Co`, the generator escapes them; do NOT pre-escape.

> **`_html` field escaping:** Use actual UTF-8 characters for all typographic marks — `'` (curly apostrophe), `"` `"` (curly quotes), `—` (em dash), `→` (arrow), etc. Do NOT use HTML entity names like `&rsquo;` or `&mdash;`. The only escaping needed is literal `&` → `&amp;` when the ampersand is part of prose (e.g., "Lib & Co" → `Lib &amp; Co`). HTML tags in `_html` fields (`<code>`, `<span>`, `<blockquote>`) are trusted and inserted verbatim.

See `HTML_Artifact_Contract.md § Authoring the data`.

**2. Render the HTML** from `onboarding-models/`:

```bash
python3 render_phase_assessment.py output/{$RUN_DATE}-phase-assessment.json
# → writes output/{$RUN_DATE}-phase-assessment.html
```

A **clean exit means the JSON was complete** — the generator's unresolved-token / >1-urgent checks are the guard. If it refuses to write, fix the JSON it points at (do not touch the generator).

> Strip all `<!-- ... -->` comment blocks from the HTML template before writing the final output file. Instructional comments must not appear in the delivered artifact.

### Step 5 — Sanity check before declaring done

- Every cohort member appears in the output (or is explicitly noted as unresolved).
- Every numeric metric came from a tool call; no `❓ QUERY FAILED` left unaddressed.
- Anchor + Current per client are consistent with the phase clauses (re-check Phase 4's `customers > 0` and Phase 7's any-2-of-4 disjunctive specifically).
- **Readability:** no banned internal words in the client-facing body; **no internal flag code anywhere in the body** (codes appear only in the appendix flag-reference map); acronyms expanded; each client leads with "Phase N of 7"; run metadata + framework feedback are in the bottom appendix only.
- **One bucket per client:** in the standup agenda, each client appears under exactly one bucket (Resolve / Discuss / On track) — no client is listed twice; an informational/by-design note alone does not put an on-track client into Discuss.
- **Integration shown only when we own it:** clients with no `Managed Integration` / `Certified Pipeline` line item have NO Integration row or block; `Certified Pipeline` clients get one informational line and no integration flag.
- **Overrides honored:** any org in `overrides.yml § net_price_only_confirmed` does not carry `SINGLE_PRICE_LEVEL_UNCONFIRMED`; any managed-integration org in `overrides.yml § integration_status` does not carry `INTEGRATION_OWNER_UNCLEAR`; any org in `overrides.yml § client_domains` uses that domain list verbatim.
- File written at `SuperCat 4.0/onboarding-models/output/{$RUN_DATE}-phase-assessment.md`.
- **JSON + HTML emitted (Step 4b):** `output/{$RUN_DATE}-phase-assessment.json` validates against the schema and the generator exited clean (wrote the `.html`); the rendered `.html` opens with styling intact. The cohort and per-client cards in the JSON match the md 1:1, sorted phase-ascending, and at most one agenda item is `urgent`.
- **Pipeline not broken:** if you touched anything that affects rendering, `python3 render_phase_assessment.py EXAMPLE-2026-06-09-phase-assessment.json --check EXAMPLE-2026-06-09-phase-assessment.html` still prints `MATCH`. (You should NOT have touched the generator/template/CSS — this is a safety net.)
- If you applied the framework to a non-cohort org (TCD/MALI) for cross-validation, that's optional — only do it if you have time and clearly mark those classifications as outside the cohort.

---

## Known caveats from the v3.0 → v3.1 migration

The prior agent verified these against live data on 2026-06-05. If your run disagrees, that's a signal — either the data changed (legitimately) or the framework has a residual bug (worth flagging). Expected on Jun 5:

| Client | Expected Anchor / Current | Reason |
|---|---|---|
| TCS | Anchor=3, Current=4 | `PHASE_4_VACUOUS_NO_CUSTOMERS` fires — 0 customers blocks Phase 4 anchor's new `customers > 0` clause. |
| DRF | Anchor=2 (**4** if Net-Price-only confirmed manually) | `SINGLE_PRICE_LEVEL_UNCONFIRMED` — only 1 price level (`net`). Phase 3 Done-when requires ≥2 price levels OR explicit Net-Price-only confirmation. Confirming it satisfies Phase 3 AND Phase 4 in one step (389 customers, 100% DPC resolution, 70% images, warning-only products all already hold), so DRF would land at Anchor 4 / Current 5, not Anchor 3. No confirmation override table exists yet, so Anchor=2 is expected today. Flag it; the standup decides. |
| LIBCO | Anchor=3, Current=4 | Same as TCS — 0 customers. Plus `OPTIONS_INTENTIONALLY_EMPTY` (lighting model) and `USER_TYPES_EMPTY` (US Reps + Canadian Reps both empty). |
| PEBL | Anchor=3, Current=4 | Same as TCS — 0 customers. Plus `SELF_TEST_ONLY_ORDERS` (9 orders all `bill_to='Pebl'`) and `RECURRING_WARNINGS_NO_ERROR` (custom-field warnings). |

If you classify a cohort member significantly differently than this (e.g. PEBL at Anchor=5), stop and look hard at the data — either something changed live since Jun 5, or you've misread a framework clause.

TCD and MALI carry `status='active'` and are correctly excluded from the auto-cohort. You should NOT see them in the output unless Kylor explicitly asks for cross-validation.

---

## Output expected from your run

1. **The dated assessment files:** `SuperCat 4.0/onboarding-models/output/{YYYY-MM-DD}-phase-assessment.md` (human-readable record, the content source of truth) plus its two siblings from Step 4b — `.json` (structured data) and `.html` (rendered report). The `.md` is the primary deliverable; the `.json`/`.html` are produced from the same computed state.

2. **A short chat report after writing the file:**
   - The cohort returned by the auto-cohort query.
   - One-line Anchor/Current per client.
   - Any flags fired (count, not contents).
   - **Most important:** any framework clauses you found ambiguous, under-specified, or contradicted by live data. This feedback is what determines whether v3.1 stays as-is or gets another revision pass.

---

## What you should NOT do

- Do NOT edit any of the four framework files (`Phase_Progression_Framework.md`, `Phase_Anchors.md`, `Flags_and_Signals.md`, `Output_Contract.md`). If you find a bug, report it in chat — Kylor decides whether to revise.
- Do NOT edit the rendering infrastructure: `phase-assessment.template.html`, `phase-assessment.css`, `render_phase_assessment.py`, `phase-assessment.schema.json`, or the golden pair (`EXAMPLE-2026-06-09-phase-assessment.html` + `EXAMPLE-2026-06-09-phase-assessment.json`). Your only job for HTML is emitting schema-valid JSON (Step 4b); if the generator refuses to write, fix the JSON, not the generator. If you believe a template/schema change is genuinely needed, report it in chat.
- Do NOT invent SQL beyond what the framework specifies or the primitives above. The framework's queries and the primitives in this handoff are the authoritative set.
- Do NOT skip flags that fire because "the standup will figure it out" — that's the whole point of flags. Every triggered flag belongs in the output.
- Do NOT include orgs outside the auto-cohort (TCD/MALI) unless you mark them clearly as cross-validation classifications outside the formal cohort.
- Do NOT paraphrase quotes. If a Fathom summary or HelpScout body says X, quote X verbatim. If it doesn't say X, don't quote it.

---

## Anti-hallucination rules

See `Flags_and_Signals.md § Hard rules (non-negotiable)`. These rules govern every tool call and every flag emission in this run — read them before you start.

---

## A note on bias

The prior agent has thought about this framework for 5 hours and is invested in v3.1 being right. If your run surfaces a clause that doesn't work in practice — e.g. the Phase 7 disjunctive lets the wrong org through, or the `client_domains[]` resolution returns nothing useful for a specific client — say so. Kylor's standing instruction is "pushback if needed." That applies to your run of the framework, not just to operator interactions.

The single biggest risk in v3.1 is that the framework was verified against the 6 reference orgs the prior agent already knew. A new client whose shape doesn't match those 6 may expose anchor clauses that fail silently. If you see anything like that, flag it.

Good luck.
