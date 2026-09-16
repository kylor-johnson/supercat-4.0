# Wave 4.1 — Authoring Prompt for `_root/08_quality_bar.md`

> **For paste into a fresh Cursor agent chat as the first message.** Do not modify before pasting.
> **Drafted**: 2026-05-22 by planning agent (post Wave-3 operator-stamping pass)
> **Output target**: `Pricing Migration/_root/08_quality_bar.md` (replace stub contents)
> **Estimated authored length**: 350–550 lines (the QA layer is dense — it indexes every rule across `_root/01`–`_root/07`)
> **Dependency**: All of `_root/01`–`_root/07` authored and reviewed (complete as of 2026-05-22). Final fresh-agent prompt in Stage 2; `_root/00_manifest.md` follows from the planning agent.

---

## You are a fresh agent

You have no prior context about the SuperCat Pricing Migration. That is **load-bearing** for this prompt. `_root/08_quality_bar.md` is the canonical pre-send checklist for every per-account brief produced by the system. It is also the audit checklist for QA-only sessions that re-review already-drafted briefs.

Your job is to **build the single send-checklist** that every brief must pass. The rules being checked are owned by `_root/01`–`_root/07`. **Your doc does NOT own the rules. Your doc owns the checks against them.** A check looks like: "Verify X; owning rule is `_root/04 §Y`; how to verify is Z; severity is blocker / warning."

You will not invent new rules. You will not loosen, summarize, or "improve" any existing rule. You will index every rule that exists across `_root/01`–`_root/07` and write a check for each rule that is verifiable at draft time, send time, or audit time. Where the archived handoff or template-test material describes a check that the new `_root/` set already enforces, you cross-reference and consolidate (one check per rule, never two).

The cost of a missing check is a brief that ships with a drift the system was built to prevent. The cost of a duplicate check is a checklist that contradicts itself when one of the duplicates gets edited and the other doesn't. Both failure modes are unacceptable.

---

## Step 1: Required reading (in this exact order)

Read it all before writing. Echo each file path + last-updated date (from each file's header block where present) in the conformance block of your final reply.

### Folder orientation (mandatory — echo in conformance block)

1. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/AGENTS.md`
2. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/00_README.md`
3. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/CONTRACTS.md`
4. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/08_quality_bar.md` (the stub you're replacing)
5. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/09_changelog.md` (read every entry — the changelog tells you which rules have been stamped, revised, or operator-overridden; that history matters when you cite an owning rule)

### Already-authored root docs — read in FULL (these are the rules you will index)

6. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/01_why_we_are_migrating.md` — the WHY layer. Few mechanical checks here (mostly principle-level), but the "definition of done" in §4 produces audit-level checks (e.g. "All 107 pending accounts have a sent notice or a stamped operator decision to defer").
7. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/02_who_is_being_migrated.md` — segments, $200 / $400 / $600 ownership boundary, entity overlay, health overrides (incl. Critical-band per-account exception stamped 2026-05-22), annual overlay, June / July / Deferred cohorts, the 5 routing-CSV errata, 109 / 107 / 2 reconciliation.
8. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/03_what_we_sell.md` — T1 / T2 / T3 verbatim "What You're Getting at $X" blocks, user-rate ladder, "What's Coming in 2026" verbatim block (now in ALL 4 brief formats per operator decision Q4), implementation-fee tiers, INTERNAL-only sections.
9. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/04_communication_posture.md` — **the highest-rule-density doc in the system**: 14 non-negotiables (§2), 27-row forbidden-phrase table (§3), 14 named voice rules (§4.1–§4.14), driver-voice orientation (§5). Most of your checklist is going to land here. Read every row of §3 and every subsection of §4 carefully — each one is a potential check.
10. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/05_driver_taxonomy.md` — 11 `migration_driver` values, verbatim driver-prose blocks per format, conditional sub-blocks, secondary-driver weaving matrix, anomaly handling (`already_migrated`). The "verbatim block used (not paraphrased)" check originates here.
11. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/06_format_routing.md` — 4 brief formats + 2 routing patterns, 6-step routing-decision flow, delta-tier dispatch table with operator-stamped Δ_pct vs Δ_mrr precedence rule (2026-05-22), 3 overrides incl. operator-stamped At-Risk Reading A and operator-stamped Critical-band per-account-judgment rule, `comm_action` vocabulary + 4 companion CSV columns (`hold_condition`, `post_hold_action`, `flags`, `nuances`) per §5.5, the 5 errata mirror.
12. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_root/07_data_pipeline.md` — source-of-truth hierarchy, 53-column field guide, canonical loaders, 3 verbatim Postgres MCP queries, 9-row fallback table, file-naming convention, canonical routing-block field-list matrix per format, file-path index.

### CSVs (header + spot-check rows; do NOT paste row data into the authored doc)

13. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_master-account-data-v6.2.csv` — verify 109 rows (107 `migration_pending` + 2 `already_migrated`) per `_root/02 §8`. Header row only into your reading; you'll cite columns by name in the checklist.
14. `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/migration_comm_tiers_2026-05-19.csv` — verify the 7 distinct `comm_action` values + the 4 companion columns documented in `_root/06 §5` and §5.5.

### Primary content sources — the pre-refactor archive (this prompt EXPLICITLY AUTHORIZES reading these despite the general anti-archive rule in `_root/CONTRACTS.md §4`)

15. **Archived handoff §Quality Bar** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/_handoff-prompt.md`. Read **only**:
    - §"Quality Bar" (search the doc for the heading) — the per-draft check list the prior system used
    - §"CHECK"-prefixed lines wherever they appear in the handoff (typically inside the §Quality Bar block but a few are scattered elsewhere)
    Do not read the rest of the handoff — voice rules belong to `_root/04`, driver content belongs to `_root/05`, routing belongs to `_root/06`, pipeline belongs to `_root/07`. If a Quality Bar item is already enforced as a stronger / clearer rule in one of those owning docs, your check cites the owning doc, NOT the handoff (the handoff is archived).

16. **Archived template-test prompt** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/_template-test-prompt.md`. Read in full — this is the pre-refactor pre-send QA prompt. Every check it asserts that survives translation to the new `_root/` rule set becomes a check in your doc. Any check it asserts that is now obsolete (because the rule it was checking has been deleted or changed) is silently dropped — flag the dropped check in your conformance block.

17. **Archived current-state notes** — `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/_archive/2026-05-22__pre-refactor/_current-state.md`. Read **only**:
    - Any "drift event" / "what went wrong" callout (these tell you which historical drifts the new checklist must prevent)
    - Any "internal routing-note left in published brief" reference (this is one of the existing non-negotiables in `_root/04 §2`; you'll want a hard check)

### Do NOT read

- The bodies of any archived brief template (Format A / Format B / CEO Letter / Good News brief-template `.md` files) — the rules they encode now live in `_root/03`, `_root/04`, `_root/05`. Reading the templates here is scope creep and may pull stale wording into your checks.
- Any per-account exemplar brief (kal, kii, ih, da, pf) — exemplars are not the rule; the rule is what `_root/03`–`_root/06` say.
- `~/Downloads/**` or anything outside `Pricing Migration/` and `Migration-Health Artifacts/`.
- Other `_root/` stubs (`00_manifest.md`) — stub-only; planning agent authors it after you.

---

## Step 2: Authoritative context the planning agent has already verified

You do not re-verify these — use as fact:

- **Rule layer is fully operator-stamped as of 2026-05-22.** All 4 Wave-3 operator decisions (FLAG-1 Δ-precedence, FLAG-2 At-Risk Reading A, Critical-band per-account judgment, multi_org+IUR sub-block extension) are recorded in the 2026-05-22 Wave 3 operator-stamping changelog entry. No "planning-agent default" language exists in any rule doc; if you find some, flag it.
- **Account count: 109 unique v6.2 `ord_id`s — 107 `migration_pending` + 2 `already_migrated`** (CopperSmith `tcs`, Dorell Fabrics `drf`).
- **The 7 distinct `comm_action` values in the routing CSV** are: `Format A — 60-Day Notice` (15), `Format B — Notice + Meeting Offer` (19), `CEO Letter + Call Commitment` (9), `CEO Pre-Call → Format B` (9), `Good-News Notice` (4), `Already Migrated` (2), `HOLD` (51). Total = 109. Documented in `_root/06 §5`.
- **The 5 routing-CSV errata** (canonical in `_root/02 §7`; mirrored in `_root/06 §6`): `rac`, `wac`, `sbl`, `big`, `kl` — corrected values override the CSV until cleanup item `CL-000` lands.
- **No per-account brief currently exists** (all archived). Your checklist will be exercised first against Stage 4 per-account drafts, not against any current artifact.
- **Stage 3 cleanup items live in `_meta/stage3_cleanup.md`** — you do not read that file (it's `_meta/`, not `_root/`); checks against Stage 3 template content are out of scope until Stage 3 rebuilds the templates. Your checks index the rule docs (`_root/01`–`_root/07`), not the templates yet.

---

## Step 3: What you are authoring

`_root/08_quality_bar.md` is the single send-checklist for every per-account brief produced by the system. Author the doc as the following sections, in this order:

### Section 1 — Purpose, audience, and how this checklist is exercised

A short opening section (3–5 short paragraphs) covering:

- What this doc is: the single pre-send checklist for every per-account brief.
- Who exercises it: (a) the Stage 4 per-account drafting agent, before posting its conformance block; (b) the planning agent / operator, during pre-send review; (c) a dedicated QA-only fresh-agent session, when re-auditing an already-drafted brief.
- The rule for failed checks: a drafter who hits a failing check **escalates per `_root/CONTRACTS.md §2`**, never improvises a fix. The check is the trip wire; the resolution is operator decision.
- The rule for missing checks: if a drafter believes a rule exists but no check covers it, the drafter flags via the conformance block; the operator adds the missing check via the `_root/CONTRACTS.md §3` rule-change protocol.
- The rule for duplicate checks: every rule appears in exactly one `_root/` doc; every check appears exactly once in `_root/08`. A duplicate is drift.

### Section 2 — Anatomy of a check

State the standard form every check in §3–§7 uses:

```
- **CHECK ID** — One-sentence statement of what to verify.
  - **Owning rule**: `_root/XX §N.M` (the canonical source — never restated here)
  - **How to verify**: <manual / grep pattern / regex / cross-reference / data-pipeline output>
  - **Severity**: blocker (do not send) | warning (operator review required) | audit-only (post-send sweep)
  - **Applies to**: <Format A | Format B | CEO Letter | Good News | entity packet | all formats>
```

The check ID convention: `QB-NNN` where NNN is a zero-padded sequence number, assigned in document order. Once assigned, IDs are stable — IDs are never reused even if a check is later removed.

### Section 3 — Drift-control checks (apply to every fresh-agent session, not just briefs)

These are the checks that prevent the agent from drifting outside its lane. They run before the drafter touches the brief content itself.

Cover at minimum:

- Manifest echoed in the agent's first chat response (per `_root/CONTRACTS.md §2`).
- Conformance block present in the agent's final chat response (per `_root/CONTRACTS.md §2`).
- Files-read list complete with last-updated dates (per `_root/CONTRACTS.md §2`).
- No `_archive/**` read unless explicitly per-prompt authorized (per `_root/CONTRACTS.md §4`).
- No `~/Downloads/**` read ever (per `AGENTS.md` hard rules).
- No rule restated from another `_root/` doc (per `_root/CONTRACTS.md` — every rule lives in exactly one doc).
- No invention of a rule the source did not state (per `_root/CONTRACTS.md §2`).
- Open-questions list present (per `_root/CONTRACTS.md §2`) — empty list is acceptable, missing section is not.

Each check carries its own QB-NNN ID, severity, and the standard anatomy.

### Section 4 — Routing checks (against `_root/02` + `_root/06` + `_root/07`)

Pre-draft checks that confirm the drafter is producing the right brief for the right account. Cover at minimum:

- Account exists in v6.2 (`ord_id` resolves to one row; not `ghost_account = TRUE`; not `migration_status = 'already_migrated'`).
- Segment matches what v6.2 says (`migration_segment` column).
- Format matches what `_root/06 §3` delta-tier dispatch + `_root/06 §4` overrides produce (the format is not arbitrarily selected by the drafter — it derives from the data).
- `comm_action` value in routing CSV agrees with the derived format (after applying the 5 errata per `_root/02 §7` / `_root/06 §6`).
- For HOLD rows, the drafter has consulted `post_hold_action` (per `_root/06 §5.5`) and is producing the eventual-format brief OR explicitly deferring per the HOLD condition.
- For Critical-band rows (`health_band = 'Critical'`), the drafter has consulted `post_hold_action` directly — no default presumption either way (per `_root/06 §4.2` Critical-band-handling paragraph + `_root/02 §4` Critical-band per-account exception paragraph, both operator-stamped 2026-05-22).
- For Δ_mrr / Δ_pct boundary cases, the operator-stamped "higher-touch format wins" precedence rule is applied (per `_root/06 §3` precedence stamp 2026-05-22).
- Entity-children route via the parent's entity packet (per `_root/02 §3` + `_root/06 §4.1`) — drafter does not produce a standalone child brief.
- Annual accounts (`deal_type = 'Annual'`) use the 90-day notice window (per `_root/02 §5` + `_root/06 §4.3`), not the 60-day window.
- Output writes to the correct format folder per `_root/07 §6`.
- CEO Pre-Call brief writes to `format-b-notices/` with `CEO awareness required before send: YES` in the routing block per `_root/07 §7`.

### Section 5 — Data-pipeline checks (against `_root/07`)

Checks that confirm the drafter used the canonical data pipeline rather than improvising. Cover at minimum:

- Drafter loaded v6.2 with the canonical loader pattern (per `_root/07 §3`); the loader's filter for `ghost_account = TRUE` and `migration_status = 'already_migrated'` was active.
- The 3 verbatim Postgres MCP queries from `_root/07 §4.1`–§4.3 were used as-is; no improvised query variations.
- Derived metrics (`cost_per_order`, `annual_subscription`, `delta_per_order`) per `_root/07 §4.4` were computed from the canonical inputs, not from prose.
- The before-state user-billing reconciliation per `_root/07 §4.5` was performed.
- Where Postgres or v6.2 returned a fallback condition per `_root/07 §5`, the prescribed fallback was applied (not a different one).
- Routing-block field list per `_root/07 §7` matches the format's column requirements.
- Filename follows the convention in `_root/07 §6` (incl. versioned re-run `__v2` / `__v3` per the canonical pattern).

### Section 6 — Voice / content checks (against `_root/03` + `_root/04` + `_root/05`)

The largest section. Build by walking through each doc methodically. Cover at minimum (and enumerate ALL, not just these illustrations):

**Against `_root/04 §2` (the 14 non-negotiables)** — one check per non-negotiable. Examples (illustrative; you produce the full list):

- Internal routing-note blockquote is removed before send (`_root/04 §2.X`).
- Brief uses the operations-unchanged sentence (default OR IUR variant, per the IF condition in `_root/04 §4.5`).
- Brief uses the format-specific close text verbatim per `_root/04 §4.12`.

**Against `_root/04 §3` (the 27-row forbidden-phrase table)** — one check per row that detects the phrase pattern in the draft. Use a literal-string or simple-regex pattern where possible; cite the row's "what to write instead" reference for the resolution. Examples:

- No "no account-specific adjustments" sentence appears (`_root/04 §3 row N`).
- No peer dollar range in client copy (`_root/04 §3 row M`, operator-stamped 2026-05-22).
- No "equivalent platforms $3,000–$3,500" or any unnamed-competitor pricing comparison (`_root/04 §3 row K`, operator-stamped 2026-05-22).
- No "comprehensive" / "five connected surfaces" / similar marketing register (`_root/04 §3`).

**Against `_root/04 §4` (the 14 named voice rules)** — one check per subsection. Examples:

- Tenure-aware "rate was set in [YEAR]" variant matches the cohort year per `_root/04 §4.1`.
- Value-anchor section included iff `cost_per_order < $200` per `_root/04 §4.8` (operator-stamped 2026-05-22).
- Watch-band lede override applied iff `health_band ∈ {Watch, At Risk, Critical}` per `_root/04 §4.13` — relationship-stats lede suppressed, brief opens with standalone dollar-change sentence (per `_root/04 §4.13`).
- Discount-correction lede substitution applied iff `migration_driver = platform_discount_correction` per `_root/04 §4.14`.

**Against `_root/05` (driver content)** — checks that the driver-prose block is used verbatim:

- Primary-driver "Why the Number Is Changing" block is verbatim from `_root/05 §N` for the format (no paraphrasing, no reordering, no synonym substitution).
- All bracketed placeholders in the driver block are filled correctly.
- Conditional sub-blocks (`[IF excess users remain]`, `[IF tier_change]`, etc.) are rendered iff the condition holds for the account.
- Secondary-driver weaving follows the matrix in `_root/05 §4`; multi_org + IUR uses the (Stage-3-pending) extended sub-block per CL-016; multi_org + URN uses per-account narrative integration per the kii / da exemplar pattern.
- Format A briefs that the format does NOT carry templated prose for (`tier_base_increase`, `included_user_reduction`, `annual_discount_retirement` per `_root/05 §2.3.4`, `§2.4.4`, `§2.7.4`) trigger an escalation, not improvised content.

**Against `_root/03` (product / pricing language)** — checks that the customer-facing tier and product language is verbatim:

- "What You're Getting at $X" block matches the canonical T1/T2/T3 block in `_root/03 §2` Block A character-for-character.
- "What's Coming in 2026" verbatim block from `_root/03 §3` is present in ALL 4 brief formats including Good News per operator decision Q4 (2026-05-22).
- User-rate ladder (1–10 / 11–25 / 26–50 / 51+ at $25/$22/$20/$18) matches `_root/03 §2` Block A; foundation/03 D-004b ladder bands are NOT used (the foundation stamp is stale per CL-007 until reconciled).
- Unpublished premium SKUs (Sales Intelligence / Insights Layer per `_root/03 §6`) are NOT named in client copy.
- INTERNAL-only sections (peer ranges per `_root/03 §5`; unpublished premium SKU pricing per `_root/03 §6`) are stripped from anything that ships.

### Section 7 — Math / numeric reconciliation checks (against `_root/02` + `_root/07`)

- Δ MRR in the brief = (new MRR) − (current MRR) from v6.2; matches v6.2's `delta_mrr` column within rounding.
- Annual delta = Δ MRR × 12; if the brief asserts the annual figure (per `_root/04 §4.4` for high-delta accounts), the multiplication is correct.
- New tier-base and new user-included count match the assigned tier per `_root/03 §1`–§2.
- For Format A or Format B briefs at or near the Δ-tier boundaries ($80, $400, $600), the format-selection check (§4) reconciles with the precedence rule (`_root/06 §3` operator-stamped 2026-05-22).
- v6.2 row counts: 109 unique `ord_id`s = 107 `migration_pending` + 2 `already_migrated` (`_root/02 §8`).

### Section 8 — Audit-only checks (post-send sweep)

A short section listing checks that can only run after the brief has been sent (not pre-send blockers):

- Customer-reply analysis: did the customer's reply name a forbidden phrase as a friction point? (If yes, escalate to `_root/04` for a possible new forbidden-phrase row.)
- 60-day countdown to effective date is on calendar.
- For CEO Letter / CEO Pre-Call → Format B briefs: the call commitment date (within 5 business days per `_root/04 §4.12`) is on the CEO calendar.
- For Annual briefs: the renewal date is correctly captured in the cohort tracker per `_root/02 §5` + `_root/06 §4.3`.

### Section 9 — Cross-doc drift checks (run rarely; high signal)

The checks that detect drift across `_root/` docs themselves (separate from the brief-level checks above). Run by the operator periodically, or after any `_root/09_changelog.md` entry. Examples:

- No `_root/` doc restates a rule owned by another `_root/` doc (grep for known rule-fragment strings across the rule layer).
- The 5 errata in `_root/02 §7` and `_root/06 §6` are character-for-character identical.
- The `comm_action` vocabulary in `_root/06 §5` matches the distinct values in `migration_comm_tiers_2026-05-19.csv`.
- The 53-column v6.2 field list in `_root/07 §2` matches the CSV header row.
- The "What's Coming in 2026" verbatim block in `_root/03 §3` is referenced by every brief template (Stage-3 dependency once templates exist).

### Section 10 — What this doc does NOT own (closing reminder)

A short closing section listing what `_root/08` does NOT own:

- The rules being checked (they live in `_root/01`–`_root/07`).
- The actual draft outputs (those are per-account artifacts in the format folders).
- How to fix a failing check (the fix lives in the doc that owns the rule; the drafter escalates per `_root/CONTRACTS.md §2`).
- Stage 3 template-level checks (those land when Stage 3 rebuilds the templates; this doc indexes the rule layer only).

### Header block (match the pattern in other root docs)

```
# 08 — Quality Bar

> **What this doc owns**: <populate from your final section list>
>
> **What this doc DOES NOT own**: <populate>
>
> **Last updated**: 2026-05-22
> **Owner**: CEO
> **Primary sources**: `_root/01`–`_root/07` (the rule layer being checked); `_root/CONTRACTS.md` (the drift-control contract); archived `_handoff-prompt.md` §Quality Bar + archived `_template-test-prompt.md` (read under explicit Wave 4.1 authorization per `_root/CONTRACTS.md §4` for historical-check extraction)
> **Supersedes**: the archived `_handoff-prompt.md` §Quality Bar + the archived `_template-test-prompt.md`. After this doc lands, no other Quality Bar / QA checklist exists in the system.
```

---

## Step 4: Anti-drift discipline

- **Every rule lives in exactly one `_root/` doc; every check lives exactly once here.** A check that duplicates another check (or rephrases the same rule under a new ID) is drift.
- **A check NEVER restates the rule.** Cite the owning `_root/XX §N` and let the reader follow the link. If the brief drafter needs the rule text to evaluate the check, they read the owning doc.
- **Severity is binary at draft time**: blocker means do not send; warning means operator decision before send. Audit-only checks run AFTER send and do not gate sending.
- **If a Quality Bar item from the archived handoff is now obsolete (the rule was removed from `_root/04`), drop the check silently and flag the drop in your conformance block** — do NOT include obsolete checks.
- **If a Quality Bar item from the archived handoff is now STRONGER in `_root/04` (e.g. the peer-dollar prohibition was broadened 2026-05-22), cite the current rule, not the historical one.**
- **The 4 operator-stamped Wave-3 decisions (2026-05-22) are binding**: any check that contradicts FLAG-1, FLAG-2, Critical-band per-account judgment, or CL-016 IUR-extension scope is a drift bug; flag it.
- **Asking is cheap. Inventing is the drift vector.** If a rule in `_root/01`–`_root/07` is ambiguous and you cannot write a verifiable check, flag — do not write a vague check.

---

## Step 5: Voice and format constraints

- Register: operator-facing, declarative, no marketing language. Same register as `_root/02`, `_root/04`, `_root/06`, `_root/07`.
- Use clean Markdown structure: `##` for the 10 sections, `###` for groupings inside §3–§7 (e.g. "Against `_root/04 §2`", "Against `_root/04 §3`"). Use the bullet-list anatomy from §2 for every check.
- Stable, sequential `QB-NNN` IDs. Once assigned, the ID is permanent — even if a check is removed in a future revision, the ID is retired, never reused.
- Numbered lists ONLY where the order matters (the routing-decision flow in §4 references `_root/06 §2`'s 6-step order, for example).
- No emoji. No "Importantly" / "Critically" — severity is the operational signal of importance.

---

## Step 6: Output

Replace the entire current contents of `Pricing Migration/_root/08_quality_bar.md` with the authored document.

Then, in your chat reply (NOT in the file), produce this conformance block:

```
─── Conformance Block ─────────────────────────────────────────
Authored: _root/08_quality_bar.md (replaced stub)

Files read (with last-updated date / mtime):
- <enumerate every file path from Step 1 + last-updated date>

Explicitly-authorized archive reads:
- <list the archived sections you read under Wave 4.1 §1 items 15–17 authorization>

Files NOT read:
- <enumerate per Step 1 "Do NOT read" + any others>

Total checks authored: <count of QB-NNN entries across §3–§9>
Breakdown by section:
- §3 Drift-control checks: <count>
- §4 Routing checks: <count>
- §5 Data-pipeline checks: <count>
- §6 Voice / content checks: <count>
  - Against _root/04 §2 (non-negotiables): <count>
  - Against _root/04 §3 (forbidden phrases): <count>
  - Against _root/04 §4 (named voice rules): <count>
  - Against _root/05 (driver content): <count>
  - Against _root/03 (product/pricing language): <count>
- §7 Math / numeric reconciliation checks: <count>
- §8 Audit-only checks: <count>
- §9 Cross-doc drift checks: <count>

Severity distribution:
- Blockers: <count>
- Warnings: <count>
- Audit-only: <count>

Checks from archived handoff §Quality Bar / archived _template-test-prompt that I CARRIED FORWARD: <list IDs and the new QB-NNN they map to>
Checks from archived sources that I DROPPED (rule no longer exists or has been superseded): <list with rationale, e.g. "handoff Check 'X' dropped because the rule it checked was removed from _root/04 in the Wave 1 authoring per _root/09_changelog.md 2026-05-22 entry">
Checks from archived sources that I STRENGTHENED (the new _root/ rule is stricter than the archived check): <list with rationale>

Gaps surfaced (a rule in _root/01–_root/07 with NO check I could write, OR a check the archived material asserted with NO supporting rule in _root/):
- <list, or "none">

Conflicts between source materials (and my chosen resolution):
- <list, or "none">

Open questions for operator:
- <list, or "none">
─────────────────────────────────────────────────────────────
```

Then **STOP**. Do not edit any other file. The operator will paste your output back to the planning agent for review before the planning agent authors `_root/00_manifest.md` (Stage 5).

---

## Step 7: If something is missing or contradictory

- A rule in `_root/01`–`_root/07` that you cannot translate into a verifiable check → flag with the §-pointer and your best attempt; the operator decides whether to refine the rule or accept an audit-only check.
- A check in the archived handoff or `_template-test-prompt.md` that references a rule that no longer exists in `_root/04` (or wherever) → drop the check; document the drop in the conformance block.
- A check in the archived materials that is now stricter under operator-stamped `_root/04` (e.g. peer dollars formerly Format-B-only, now stripped from all formats per Wave 1 review 2026-05-22) → use the stricter form; cite the current rule.
- Two `_root/` docs that appear to say different things → flag the conflict in the conformance block; do NOT pick one. (The 4 Wave-3 operator-stamped decisions and the `_root/02 §4` Critical-band paragraph were specifically added to prevent this.)
- A rule that lives in archived materials but was never lifted into `_root/` (i.e. the rule is dead) → do NOT write a check for it; flag the dead rule in the conformance block.

**Asking is cheap. Inventing is the drift vector.**
