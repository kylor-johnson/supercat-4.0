# 08 — Quality Bar

> **What this doc owns**: The single pre-send checklist for every per-account brief produced by the system. One QB-NNN check per rule in `_root/01`–`_root/07` that is verifiable at draft time, send time, or audit time. The standard anatomy every check uses. The severity discipline (blocker / warning / audit-only). The drift-control, routing, data-pipeline, voice / content, math, audit-only, and cross-doc check sections. The catalogue of checks carried forward from the archived `_handoff-prompt.md` §Quality Bar and the archived `_template-test-prompt.md`, mapped to their current owning `_root/` rule.
>
> **What this doc DOES NOT own**: The rules being checked (they live in `_root/01`–`_root/07`). The actual draft outputs (those are per-account artifacts in the format folders). How to fix a failing check (the fix lives in the doc that owns the rule; the drafter escalates per `_root/CONTRACTS.md §2`). Stage 3 template-level checks (those land when Stage 3 rebuilds the templates; this doc indexes the rule layer only).
>
> **Last updated**: 2026-05-26 (Wave 6 batch — Section 10 added: 12 entity-packet program QB-NNN checks [QB-127 through QB-138] codified from EP-* identifiers in `entity-packets/_parent-letter-template.md` Section 4 + `entity-packets/_parent-letter-delivery-email-template.md` Section 4; owning-rule layer is `_root/04 §4.15` + `_root/06 §1.6`; prior Section 10 renumbered to Section 11; Stage 3.5 deferred item #5 RESOLVED at rule layer; prior entity-packet template EP-* lists retained as template-scaffolding audit-trail of the pre-§10 inference pattern. Prior: 2026-05-22.)
> **Owner**: CEO
> **Primary sources**: `_root/01`–`_root/07` (the rule layer being checked); `_root/CONTRACTS.md` (the drift-control contract); archived `_handoff-prompt.md` §Quality Bar + archived `_template-test-prompt.md` (read under explicit Wave 4.1 authorization per `_root/CONTRACTS.md §4` for historical-check extraction); for Section 10 — the 2 entity-packet templates (`entity-packets/_parent-letter-template.md` + `entity-packets/_parent-letter-delivery-email-template.md`) Section 4 EP-* identifier lists (operator-approved at Stage 3.5 review pass 2026-05-26 — `_root/09_changelog.md`), backed by `_root/04 §4.15.1`–`§4.15.6` (parent-letter voice register, operator-stamped 2026-05-26) and `_root/06 §1.6` (entity-packet routing pattern + 14-entity scope + Ferguson Enterprises exception, operator-stamped 2026-05-26).
> **Supersedes**: the archived `_handoff-prompt.md` §Quality Bar + the archived `_template-test-prompt.md`. After this doc lands, no other Quality Bar / QA checklist exists in the system.

---

## Section 1 — Purpose, audience, and how this checklist is exercised

This doc is the single pre-send checklist for every per-account brief produced by the migration communications system. There is no other QA checklist; the archived `_handoff-prompt.md §Quality Bar` and the archived `_template-test-prompt.md` are superseded.

The checklist is exercised in three modes. (a) The Stage 4 per-account drafting agent runs every check whose **applies-to** field covers the brief's format, before posting its conformance block. (b) The planning agent or operator runs the same checks during pre-send review. (c) A dedicated QA-only fresh-agent session iterates this doc against an already-drafted brief when re-auditing is requested. The three modes use the same checks; only the timing differs.

A failing check is a tripwire. The drafter does not improvise a fix — the drafter **escalates per `_root/CONTRACTS.md §2`** and names the failing check and the relevant owning rule. The resolution is an operator decision: either the brief is corrected to clear the check, or the rule the check enforces is revised per `_root/CONTRACTS.md §3` and the check is updated to match.

A missing check is also a tripwire. If a drafter believes a rule exists in `_root/01`–`_root/07` but no check here covers it, the drafter flags the gap in its conformance block. The operator adds the missing check via the `_root/CONTRACTS.md §3` rule-change protocol (the missing check is a `_root/08` edit; the rule it would have enforced lives in the owning `_root/` doc). The drafter does not invent a check on the fly.

A duplicate check is the inverse failure mode. Every rule lives in exactly one `_root/` doc per `_root/CONTRACTS.md §5`, and every check lives exactly once in this doc. A check that rephrases another check under a new ID is drift — when one of the duplicates is later edited and the other is not, the checklist begins contradicting itself silently. Auditors who find a duplicate flag it for consolidation.

---

## Section 2 — Anatomy of a check

Every check in §3–§9 uses this exact form:

```
- **QB-NNN** — One-sentence statement of what to verify.
  - **Owning rule**: `_root/XX §N.M` (the canonical source — never restated here)
  - **How to verify**: <manual / grep pattern / regex / cross-reference / data-pipeline output>
  - **Severity**: blocker | warning | audit-only
  - **Applies to**: <Format A | Format B | CEO Letter | Good News | entity packet | all formats>
```

The `QB-NNN` IDs are zero-padded sequence numbers, assigned in document order. **IDs are stable.** Once assigned, an ID is never reused — if a check is removed in a future revision the ID is retired, not recycled.

Severity is binary at draft time:

- **blocker** — do not send. A failing blocker is escalated to the operator per `_root/CONTRACTS.md §2`; the brief is not delivered until the check clears or the underlying rule is revised.
- **warning** — operator review required before send. A failing warning surfaces an account-specific judgment call (e.g. value-anchor inclusion in a borderline case) that the operator stamps; the brief is not sent without that stamp.
- **audit-only** — post-send sweep. The check cannot run before send (e.g. a customer-reply analysis); it produces a learning signal that feeds back into the rule layer.

The **owning rule** field is a pointer only. This doc never restates the rule text. If the reader needs to know what the rule says, they follow the pointer to the owning `_root/` doc. Restating rules here would duplicate them out of their owning doc, which is the drift `_root/CONTRACTS.md §5` was written to prevent.

---

## Section 3 — Drift-control checks (apply to every fresh-agent session, not just briefs)

These checks fire before the drafter touches brief content. They confirm the session itself is in conformance with `AGENTS.md` and `_root/CONTRACTS.md`. A failure here invalidates everything that follows.

- **QB-001** — The agent's first chat response in the session echoes every `_root/` doc title plus the current "Last updated" date for each.
  - **Owning rule**: `_root/CONTRACTS.md §2` (manifest-echo contract)
  - **How to verify**: Read the first message of the session; cross-reference the echoed dates against each doc's header block.
  - **Severity**: blocker
  - **Applies to**: all formats (and every non-brief session)

- **QB-002** — The agent's final chat response contains a conformance block in the canonical format defined by `_root/00_manifest.md §5`.
  - **Owning rule**: `_root/CONTRACTS.md §verifying-conformance` step 3; canonical format owned by `_root/00_manifest.md §5` (stamped 2026-05-22 at Stage 5; Stage 1–4 sessions used per-prompt format specifications).
  - **How to verify**: Read the final message; confirm the block is delimited and contains the required sections (files read, archive reads, files not read, counts, gaps, conflicts, open questions).
  - **Severity**: blocker
  - **Applies to**: all formats (and every non-brief session)

- **QB-003** — The conformance block's files-read list enumerates every `_root/` doc plus every other file the session opened, each with its last-updated date or filesystem mtime.
  - **Owning rule**: `_root/CONTRACTS.md §verifying-conformance` step 1 + step 3
  - **How to verify**: Cross-reference the conformance block's files-read list against the session's actual tool-call history; confirm date / mtime stamps.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-004** — No file under `_archive/**` was read in the session unless the active prompt explicitly authorized that specific archive read.
  - **Owning rule**: `_root/CONTRACTS.md §4` (anti-archive rule + explicit-extraction exception)
  - **How to verify**: Cross-reference the conformance block's "explicitly-authorized archive reads" list against the session's actual reads; any archive read outside that list is a failure.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-005** — No file under `~/Downloads/**` was read in the session.
  - **Owning rule**: `AGENTS.md` hard rules
  - **How to verify**: Scan the session's tool-call history for `~/Downloads/` paths; cross-reference against the routing CSV's `migration_revenue_model_2026-05-14.html` reference (the canonical path is `_reference/migration_revenue_model_2026-05-14.html` per `_root/07 §3.5`).
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-006** — No `_meta/**` file was opened except a single operator-directed prompt file (the Wave-N authoring prompt or a similarly-named directive).
  - **Owning rule**: `AGENTS.md` hard rules
  - **How to verify**: Cross-reference the session's `_meta/` reads against the operator's directive; folder browsing is a failure.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-007** — No rule owned by another `_root/` doc is restated in the brief, the conformance block, or any output artifact; references are by `_root/XX §N.M` pointer only.
  - **Owning rule**: `_root/CONTRACTS.md §5` (path-reference contract)
  - **How to verify**: Grep the output artifacts for distinctive rule-fragment strings (e.g. "every account we work with," "platform has grown considerably," "below the midpoint" prescribed-vocabulary phrases) and confirm each appears in client copy only where the owning `_root/` doc directs verbatim insertion — never as a restated rule.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-008** — No rule appears in the brief that is not traceable to a source in `_root/01`–`_root/07` (or to a `_root/09_changelog.md`-logged edit).
  - **Owning rule**: `_root/CONTRACTS.md §2` (no improvisation)
  - **How to verify**: For each substantive sentence in the brief that asserts a rule-like claim, locate the owning `_root/` doc section; flag any that cannot be traced.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-009** — The conformance block contains an "Open questions for operator" section; an empty list ("none") is acceptable, an absent section is not.
  - **Owning rule**: `_root/CONTRACTS.md §2` (agent contract: stop and ask)
  - **How to verify**: Read the conformance block; confirm the section is present.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-010** — If the drafter encountered a situation no `_root/` doc covers, the drafter stopped and asked per `_root/CONTRACTS.md §2` rather than inferring a rule from templates, prior drafts, or "what feels consistent."
  - **Owning rule**: `_root/CONTRACTS.md §2` (no improvisation)
  - **How to verify**: Inspect the open-questions list (QB-009) and the drafter's reasoning trail; any improvised rule that should have been escalated is a failure.
  - **Severity**: blocker
  - **Applies to**: all formats

---

## Section 4 — Routing checks (against `_root/02` + `_root/06` + `_root/07`)

These checks confirm the drafter is producing the right brief for the right account. They fire before the drafter touches body content.

- **QB-011** — The brief's `ord_id` resolves to exactly one row in `_master-account-data-v6.2.csv`; the row is not filtered (`ghost_account ≠ TRUE` AND `migration_status ≠ 'already_migrated'`).
  - **Owning rule**: `_root/07 §3` (loader filter) + `_root/02 §8` (109 / 107 / 2 reconciliation)
  - **How to verify**: Run the canonical loader from `_root/07 §3`; confirm `master.get(ord_id)` returns a non-None row.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-012** — The brief's segment matches `migration_segment` from v6.2 for the account's `ord_id`.
  - **Owning rule**: `_root/02 §1` (8 migration segments)
  - **How to verify**: Read v6.2 `migration_segment`; cross-reference the routing-block "Wave" / segment field.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-013** — The brief's format derives from the 6-step routing-decision flow (status → decrease → entity → annual → health → delta-tier); the drafter did not select the format by other means.
  - **Owning rule**: `_root/06 §2` (routing-decision flow) + `_root/06 §3` (delta-tier dispatch)
  - **How to verify**: Walk the 6 steps against the account's v6.2 row; the first step that fires determines the routing decision and must match the brief's format.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-014** — The brief's format agrees with the routing CSV's `comm_action` value after applying the 5 errata in `_root/02 §7` / `_root/06 §6`.
  - **Owning rule**: `_root/06 §5` (`comm_action` vocabulary) + `_root/06 §6` (errata mirror)
  - **How to verify**: Read `migration_comm_tiers_2026-05-19.csv` for the `ord_id`; apply the errata if applicable; compare to the brief's format.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-015** — For any of the 5 errata `ord_id`s (`rac`, `wac`, `sbl`, `big`, `kl`), the corrected value from `_root/02 §7` is used — not the routing-CSV value.
  - **Owning rule**: `_root/02 §7` (canonical errata list)
  - **How to verify**: Match `ord_id` against the §7 table; if matched, confirm the routing decision uses the corrected value column, not the routing-CSV value column.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-016** — If the routing CSV row has `comm_action = HOLD`, the drafter consulted the row's `post_hold_action` column and is producing the named eventual-format brief, OR is explicitly deferring per the `hold_condition`.
  - **Owning rule**: `_root/06 §5` HOLD entry + `_root/06 §5.5` (`hold_condition`, `post_hold_action`, `flags`, `nuances`)
  - **How to verify**: Read the routing CSV row's `hold_condition` and `post_hold_action`; confirm the brief's format matches `post_hold_action` (or that the brief is intentionally deferred and not drafted).
  - **Severity**: blocker
  - **Applies to**: all formats (post-hold draft)

- **QB-017** — If `health_band = 'Critical'`, the drafter consulted `post_hold_action` directly; the drafter did NOT default either to Reading A (defer + draft post-stabilization) or to the separate-intervention path.
  - **Owning rule**: `_root/06 §4.2` Critical-band paragraph + `_root/02 §4` Critical-band per-account exception (both operator-stamped 2026-05-22)
  - **How to verify**: Read the routing CSV row's `post_hold_action`; confirm the brief's existence (or non-existence, if `NOT migration — separate health intervention program`) matches that value.
  - **Severity**: blocker
  - **Applies to**: all formats (Critical-band accounts only)

- **QB-018** — For an account near the Δ_pct / Δ_mrr boundary (Δ ≈ $75–$80 with Δ_pct ≈ 10–12%, OR Δ ≈ $600–$700 with Δ_pct ≈ 8–10%), the higher-touch format is selected per the operator-stamped precedence rule.
  - **Owning rule**: `_root/06 §3` Δ_pct vs Δ_mrr precedence (operator-stamped 2026-05-22)
  - **How to verify**: Compute Δ_pct and Δ_mrr from v6.2; if the two metrics dispatch to different formats per `_root/06 §3` table, confirm the higher-touch format was selected.
  - **Severity**: blocker
  - **Applies to**: Format A / Format B / CEO Pre-Call → Format B (boundary cases)

- **QB-019** — If `parent_entity` is non-empty AND `parent_entity ≠ company`, the drafter does NOT produce a standalone child brief; the child folds into the entity packet.
  - **Owning rule**: `_root/02 §3` (entity overlay) + `_root/06 §4.1` (entity overlay format consequence)
  - **How to verify**: Read v6.2 `parent_entity` for the `ord_id`; if the entity-overlay trigger fires, confirm no standalone brief was drafted for that child.
  - **Severity**: blocker
  - **Applies to**: all formats (entity-child accounts)

- **QB-020** — If `deal_type = 'Annual'`, the brief routes off the renewal calendar with a ≥90-day notice window and the routing-block `notice_cohort` is `Renewal-Based`.
  - **Owning rule**: `_root/02 §5` (annual overlay) + `_root/06 §4.3` (annual overlay format consequence)
  - **How to verify**: Read v6.2 `deal_type` and `notice_cohort`; confirm both routing-block fields match the §5 / §4.3 prescribed values; confirm the brief's effective-date math respects 90-day window.
  - **Severity**: blocker
  - **Applies to**: all formats (Annual accounts)

- **QB-021** — A Good-News-eligible account (`delta_mrr < 0`) that is also Watch / At Risk / Critical does NOT receive a Good News brief; it routes through CSM health check-in first.
  - **Owning rule**: `_root/06 §4.2` (Format-A-vs-Good-News interaction)
  - **How to verify**: For any draft in `good-news-notices/`, confirm `health_band ∉ {Watch, At Risk, Critical}`; if it is, the brief should not exist.
  - **Severity**: blocker
  - **Applies to**: Good News

- **QB-022** — An At-Risk account (`health_band = 'At Risk'`) does not receive a migration notice in the June or July cohorts; it is in `notice_cohort = 'Post-Migration'` and the brief is held until the override resolves.
  - **Owning rule**: `_root/06 §4.2` At-Risk handling (Reading A, operator-stamped 2026-05-22)
  - **How to verify**: Cross-reference `health_band` against `notice_cohort` for any in-flight brief; an At-Risk account in June or July cohort is a failure.
  - **Severity**: blocker
  - **Applies to**: all formats (At-Risk accounts)

- **QB-023** — If `value_delivery_score < 40` OR `health_band ∈ {Watch, At Risk, Critical}`, the account is in the Strategic segment with notice deferred until CEO-led stabilization (or, for Critical, per `post_hold_action`).
  - **Owning rule**: `_root/02 §4` (health-override triggers) + `_root/06 §4.2` (health-override format consequence)
  - **How to verify**: Read v6.2 `value_delivery_score` and `health_band`; confirm `migration_segment = 'Strategic'` (with Critical-band exception per QB-017); confirm the brief is not in an active cohort prematurely.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-024** — The brief and its companion delivery email are written to the correct per-format output folder.
  - **Owning rule**: `_root/07 §6` (output-file location, canonical owner) — mirrored in `_root/06 §7`
  - **How to verify**: Cross-reference the brief's format against the §6 mapping; Format A → `format-a-notices/`, Format B → `format-b-notices/`, CEO Letter → `ceo-letter-notices/`, Good News → `good-news-notices/`.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-025** — A CEO Pre-Call → Format B brief is written to `format-b-notices/` with `CEO awareness required before send: YES` in the routing block.
  - **Owning rule**: `_root/06 §1` (CEO Pre-Call → Format B routing pattern) + `_root/07 §7` (per-format routing-block matrix)
  - **How to verify**: For any Format B brief whose routing-block `Comm_action` is `CEO Pre-Call → Format B`, confirm the routing block's `CEO awareness required before send` row is `YES`.
  - **Severity**: blocker
  - **Applies to**: Format B (CEO Pre-Call variant)

- **QB-026** — If the routing CSV's `post_hold_action` names `CEO-Led Entity Pre-Engagement → Coordinated Notices`, the CEO has designed the parent program and run the parent conversation before any child notice is drafted.
  - **Owning rule**: `_root/06 §1` (CEO-Led Entity Pre-Engagement → Coordinated Notices pattern; 5 accounts across HVLG / WAC Group / Coleto Brands)
  - **How to verify**: For any child brief whose `post_hold_action` matches, confirm via operator stamp that the parent engagement has occurred; child briefs predate parent engagement is a failure.
  - **Severity**: blocker
  - **Applies to**: entity packet (HVLG, WAC Group, Coleto Brands)

- **QB-027** — The 6-step routing-decision flow was evaluated in the prescribed order (status → decrease → entity → annual → health → delta-tier); an earlier-firing step pre-empts every later one.
  - **Owning rule**: `_root/06 §2` (order of evaluation)
  - **How to verify**: Trace the routing decision for the account through the 6 steps in order; the first step that fires must equal the brief's effective routing path.
  - **Severity**: blocker
  - **Applies to**: all formats

---

## Section 5 — Data-pipeline checks (against `_root/07`)

These checks confirm the drafter used the canonical data pipeline rather than improvising.

- **QB-028** — The v6.2 CSV was loaded with the canonical pattern in `_root/07 §3`; the loader's `ghost_account = TRUE` and `migration_status = 'already_migrated'` filters were active.
  - **Owning rule**: `_root/07 §3` (canonical loader)
  - **How to verify**: Inspect the loader code used; confirm `utf-8-sig`, blank-first-line skip, `ord_id` key, and the two filters.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-029** — Where the HTML model and v6.2 disagree on any number, the v6.2 value is used; the disagreement is logged in the routing block (or in `_root/09_changelog.md` if material).
  - **Owning rule**: `_root/07 §1` (source-of-truth hierarchy) + `_root/07 §3.5` (HTML model is cross-check only)
  - **How to verify**: Spot-check the brief's headline numbers (`current_mrr`, `new_total_mrr`, `delta_mrr`, `delta_pct`) against the HTML model's abbreviated equivalents (`cm`, `nm`, `dm`, `dp`); confirm v6.2 wins on any discrepancy.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-030** — The three Postgres MCP queries (`§4.1` org_id resolution, `§4.2` user / login activity, `§4.3` order / GMV activity) were used verbatim from `_root/07 §4`; no SQL was rewritten.
  - **Owning rule**: `_root/07 §4.1`, `§4.2`, `§4.3`
  - **How to verify**: Inspect the queries issued in the session; compare to the verbatim SQL in the owning sections.
  - **Severity**: blocker
  - **Applies to**: Format A / Format B / CEO Letter (Good News omits per `_root/07 §7` matrix)

- **QB-031** — Derived metrics (`cost_per_order`, `annual_subscription`, `delta_per_order`) were computed from `_root/07 §4.4` formulas using v6.2 + Postgres inputs, not lifted from prose.
  - **Owning rule**: `_root/07 §4.4` (derived metrics)
  - **How to verify**: Re-compute from v6.2 `new_total_mrr` / `delta_mrr` and Postgres `ltm_orders`; cross-check against the routing-block values.
  - **Severity**: blocker
  - **Applies to**: Format A / Format B / CEO Letter (when value-anchor section qualifies per `_root/04 §4.8`)

- **QB-032** — The before-state user-billing reconciliation (`implied_billed_excess` vs `narrative_excess`) was computed; if the discrepancy threshold is tripped, the routing block carries the `⚠️ USER BILLING RECONCILIATION NEEDED` line.
  - **Owning rule**: `_root/07 §4.5` (before-state reconciliation) + `_root/07 §7` conditional-fields table
  - **How to verify**: Re-compute both values; if `|implied_billed_excess − narrative_excess| > 3` OR the dollar discrepancy > $60/month, confirm the ⚠️ line is present.
  - **Severity**: blocker
  - **Applies to**: Format A / Format B / CEO Letter

- **QB-033** — When a Postgres query failed or returned empty, the prescribed fallback in the `_root/07 §5` table was applied (not an improvised one); the routing block notes the failure.
  - **Owning rule**: `_root/07 §5` (fallback rules)
  - **How to verify**: Cross-reference any "Postgres live data: UNAVAILABLE" / per-field-empty notes in the routing block against the §5 fallback row; confirm the brief substituted the prescribed alternative (e.g. `composite_narrative` substitution, omitted value-anchor section, suppressed lede stat).
  - **Severity**: blocker
  - **Applies to**: all formats (when a fallback fires)

- **QB-034** — The output filename matches the convention `<ord_id>__<account-slug>__brief.md` / `__delivery-email.md`; `ord_id` is lowercase verbatim from v6.2; the slug is lowercase, hyphen-separated.
  - **Owning rule**: `_root/07 §6` (file-name pattern)
  - **How to verify**: Inspect the saved filenames against the §6 pattern.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-035** — A re-run triggered by an upstream `_root/` rule change uses `__v2` / `__v3` versioning per `_root/07 §6` + `_root/CONTRACTS.md §3` step 5; the unversioned and versioned files coexist until the operator retires the prior file.
  - **Owning rule**: `_root/07 §6` (versioned re-runs) + `_root/CONTRACTS.md §3` step 5 (propagation)
  - **How to verify**: For any re-drafted brief, confirm the `__v2+` suffix is present; cross-reference against the changelog entry that triggered the re-run.
  - **Severity**: blocker
  - **Applies to**: all formats (re-runs only)

- **QB-036** — Every brief opens with the internal routing-note blockquote containing every general field in the `_root/07 §7` canonical field list, in order; absent fields render as `n/a` or empty, never as a deleted line.
  - **Owning rule**: `_root/07 §7` (required internal routing block; canonical field list)
  - **How to verify**: Confirm each required line is present (Brief type, Account / Tier / Wave, Migration driver / Health / Risk, Engagement / Adoption / VD / OH, Support fire / Behavioral floor, Delta, Cohort, Contract / Renewal, Earliest enforceable effective date, Comm_action, Postgres live data line, CEO awareness flag).
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-037** — The per-format conditional routing-block fields are rendered exactly when the `_root/07 §7` matrix prescribes (Format A: `Expansion eligible` required; CEO Letter: `CEO call commitment date` + `CEO name for sign-off` required; Good News: `Watch health flag` + before/after MRR substitution for the `Delta:` row + Postgres live-data line omitted).
  - **Owning rule**: `_root/07 §7` (per-format conditional-fields matrix)
  - **How to verify**: Cross-reference the brief's routing block against the §7 matrix for its format.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-038** — No path under `~/Downloads/` is referenced in any output artifact or pipeline code; the HTML model loads from `_reference/migration_revenue_model_2026-05-14.html` per `_root/07 §3.5` / §8.
  - **Owning rule**: `_root/07 §3.5` (path-divergence flag) + `_root/07 §8` (file-path index) + `AGENTS.md` hard rules
  - **How to verify**: Grep the brief, the delivery email, and any logged code for `~/Downloads/`; any hit is a failure.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-039** — The Postgres live-data line in the routing block carries `active_org_users`, `logged_in_90d`, `total_logins_90d`, `ltm_orders`, `ltm_gmv`, `ltm_customers_served` (or the prescribed fallback note); the dated stamp is the actual query date.
  - **Owning rule**: `_root/07 §4.2` + `§4.3` + `§7` (Postgres live-data line)
  - **How to verify**: Inspect the routing block's `Postgres live data` line; confirm all six fields are populated or flagged per the §5 fallback.
  - **Severity**: blocker
  - **Applies to**: Format A / Format B / CEO Letter

---

## Section 6 — Voice / content checks (against `_root/03` + `_root/04` + `_root/05`)

This is the largest section. Checks are grouped by owning subsection: §2 non-negotiables, §3 forbidden phrases, §4 named voice rules, `_root/05` driver content, `_root/03` product/pricing language. A check appears under the owning section only; cross-references appear as parentheticals.

### §6.1 Against `_root/04 §2` (the 14 non-negotiables)

The §2 non-negotiables that point to a §4 named-voice-rule subsection are checked under §6.3 (avoiding duplication). The §2 entries below are the standalone non-negotiables that have no §4 counterpart.

- **QB-040** — The lede leads with the dollar amount and effective date; the percentage, if present, appears later in the same sentence or in the summary table.
  - **Owning rule**: `_root/04 §2.1`
  - **How to verify**: Inspect the lede paragraph; confirm the first dollar / date precedes any percentage figure.
  - **Severity**: blocker
  - **Applies to**: Format A / Format B / CEO Letter

- **QB-041** — The phrase "we're adjusting your pricing" (and minor variants) appears nowhere in the brief.
  - **Owning rule**: `_root/04 §2.2`
  - **How to verify**: Grep the brief for `adjust(ing)? your pricing`.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-042** — No apology for the change, the legacy structure, or the prior invoice appears anywhere in the brief.
  - **Owning rule**: `_root/04 §2.3` (and the `_root/04 §3` row on apology for prior pricing)
  - **How to verify**: Grep the brief for apology vocabulary (`sorry`, `apologize`, `regret`, `unfortunately the prior`, etc.); inspect the lede and the "How This Compares" framing.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-043** — No health-band name (`Thriving`, `Healthy`, `Watch`, `At Risk`, `Critical`) and no dimension score (`Engagement: N`, `Adoption: N`, `Value Delivery: N`, `Operational Health: N`) appears in client-facing copy.
  - **Owning rule**: `_root/04 §2.5` (and the `_root/04 §3` rows on health-band names and dimension scores)
  - **How to verify**: Grep the brief body (excluding the internal routing block, which is removed before send) for the five band names and the four score labels; any hit is a failure.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-044** — No expansion / upgrade language (Format C content, next-tier feature names, "at the next tier you'd also get") appears in a migration brief; migration first, expansion only after a confirmed positive signal.
  - **Owning rule**: `_root/04 §2.6` (and the `_root/04 §3` row on expansion-tier feature names)
  - **How to verify**: Grep the brief for expansion-tier triggers (`next tier`, `upgrade to`, `also get`, `Format C`); inspect the close for upsell residue.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-045** — The universality claim uses "every account we work with" / "all accounts we work with" without hedge; no "most," "many," or "broader install base."
  - **Owning rule**: `_root/04 §2.7` (and the `_root/04 §3` rows on hedging the universality claim and on "install base")
  - **How to verify**: Grep the brief for the prescribed phrase; grep for forbidden hedges (`most accounts`, `many accounts`, `broader install base`, `install base`).
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-046** — The "What's Coming in 2026" verbatim block from `_root/03 §3` is present in the brief, character-for-character; the operator-note line at the bottom is removed before send.
  - **Owning rule**: `_root/04 §2.9` (every brief includes the section verbatim) + `_root/03 §3` (verbatim source; operator decision 2026-05-22 coverage rule extends to all 4 formats)
  - **How to verify**: Diff the brief's "What's Coming in 2026" section against the `_root/03 §3` verbatim block; confirm the trailing `*[Operator note — remove before sending: …]*` line is absent in the sent version.
  - **Severity**: blocker
  - **Applies to**: Format A / Format B / CEO Letter / Good News (per Q4 operator decision 2026-05-22)

- **QB-047** — The internal routing-note blockquote at the top of every brief is removed from the version delivered to the client.
  - **Owning rule**: `_root/04 §2.14` (most-common drift event named as a non-negotiable)
  - **How to verify**: Inspect the delivered artifact; the `> **Internal routing note**` blockquote must be absent.
  - **Severity**: blocker
  - **Applies to**: all formats

### §6.2 Against `_root/04 §3` (the 27-row forbidden-phrase table)

One check per row that detects the literal phrase pattern. Forbidden-phrase rows whose underlying rule is fully covered by a §2 non-negotiable check (rows 14, 20, 21, 22, 23, 24, 25) are checked here at the literal-phrase layer; the §2 check verifies the structural / behavioral rule. The two layers are complementary, not duplicative.

- **QB-048** — The phrase "trailing 12-month average" does not appear in client-facing copy.
  - **Owning rule**: `_root/04 §3` row "trailing 12-month average"
  - **How to verify**: Grep client copy for `trailing 12-month average`.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-049** — The phrase "install base" does not appear in client-facing copy.
  - **Owning rule**: `_root/04 §3` row "install base"
  - **How to verify**: Grep client copy for `install base`.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-050** — The phrase "full-stack commercial operating system" does not appear in client-facing copy.
  - **Owning rule**: `_root/04 §3` row "full-stack commercial operating system"
  - **How to verify**: Grep client copy for the literal string.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-051** — The phrase "five connected surfaces" does not appear in client-facing copy.
  - **Owning rule**: `_root/04 §3` row "five connected surfaces"
  - **How to verify**: Grep client copy for the literal string.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-052** — Percentile notation (`p25`, `p75`, `75th percentile`, `interquartile`) does not appear in client-facing copy.
  - **Owning rule**: `_root/04 §3` row "p25, p75, 75th percentile, interquartile"
  - **How to verify**: Grep client copy for the four patterns (case-insensitive).
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-053** — Tier codes `T1`, `T2`, `T3` appear only inside tables; running prose uses the tier name (`Catalog Essentials`, `Commerce Professional`, `Commerce Enterprise`).
  - **Owning rule**: `_root/04 §3` row on tier codes in running prose
  - **How to verify**: Inspect running prose for `\bT[123]\b` outside table syntax; substitute the tier name where the code appears in narrative sentences.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-054** — No competitor pricing reference (named or unnamed) appears in client-facing copy; specifically no "equivalent platforms range from $X–$Y," "comparable solutions cost roughly $X," or any external-category dollar range.
  - **Owning rule**: `_root/04 §3` row on competitor pricing references (operator-stamped universal prohibition 2026-05-22)
  - **How to verify**: Grep client copy for `equivalent platforms`, `comparable solutions`, `competitor`, and dollar-range patterns positioned against an external category (e.g. `$3,000.{0,3}\$3,500`).
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-055** — The phrase "rate card" does not appear in client-facing copy.
  - **Owning rule**: `_root/04 §3` row on "rate card"
  - **How to verify**: Grep client copy for `rate card`.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-056** — The phrase "as part of this refresh" does not appear in client-facing copy unless inside the CEO Letter's verbatim driver blocks (where "refresh" is the canonical CEO-Letter phrasing per `_root/05`).
  - **Owning rule**: `_root/04 §3` row on "as part of this refresh"
  - **How to verify**: Grep client copy for `as part of this refresh`; cross-reference any hit against the CEO Letter verbatim blocks in `_root/05` (where the phrase is permitted character-for-character).
  - **Severity**: blocker
  - **Applies to**: Format A / Format B / Good News (CEO Letter has permitted verbatim usage)

- **QB-057** — The legacy sentence "SuperCat is standardizing its pricing... first time we've applied a consistent commercial structure..." does not appear; replaced by the consolidated 2026 sentence ("In 2026, we're moving every account to one clear pricing structure — here's exactly what that means for you").
  - **Owning rule**: `_root/04 §3` row on the consolidated 2026 sentence
  - **How to verify**: Grep client copy for the legacy fragment; cross-reference the consolidated 2026 sentence is present where the lede framing calls for it.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-058** — The legacy "Your rate at signing predates the current rate card and we're bringing it in line with the standard structure" sentence does not appear; replaced by the §4.1 tenure-aware variants.
  - **Owning rule**: `_root/04 §3` row on "Your rate at signing predates the current rate card"
  - **How to verify**: Grep client copy for `predates the current rate card`; confirm the §4.1 tenure-aware variant is used instead (per QB-077).
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-059** — The sentence "There are no account-specific adjustments in how [ACCOUNT_NAME]'s number was calculated" does not appear anywhere in any brief.
  - **Owning rule**: `_root/04 §3` row on "no account-specific adjustments" (CL-001 cleanup item)
  - **How to verify**: Grep client copy for `no account-specific adjustments`; any hit is a failure.
  - **Severity**: blocker
  - **Applies to**: all formats (especially CEO Letter and the `da` exemplar pattern)

- **QB-060** — Provisioned-vs.-active user ratio framing (`[X of Y] users logged in`, `X out of Y users`) does not appear in client-facing copy.
  - **Owning rule**: `_root/04 §3` row on provisioned-vs.-active ratio (also enforces §4.2 lede guardrail and §2.8 non-negotiable; archived template-test CHECK 7)
  - **How to verify**: Grep client copy for `\b\d+ of \d+ users\b` and `\bout of \d+ users\b` patterns.
  - **Severity**: blocker
  - **Applies to**: Format A / Format B / CEO Letter

- **QB-061** — Per-order subscription cost ("That works out to $X/order…") does not appear in the lede paragraph; per-order math is reserved for the "What This Works Out To" section per §4.8.
  - **Owning rule**: `_root/04 §3` row on per-order subscription cost in the lede
  - **How to verify**: Inspect the lede paragraph; grep for `per order`, `per-order`, `$\d+/order` patterns and confirm they appear (if at all) only in the "What This Works Out To" section.
  - **Severity**: blocker
  - **Applies to**: Format A / Format B / CEO Letter

- **QB-062** — The lede does not lead with a percentage figure (e.g. "a 60.7% change…"); dollar amount and effective date come first per §2.1 + §4.4.
  - **Owning rule**: `_root/04 §3` row on leading with a percentage (operationally non-negotiable via §2.1)
  - **How to verify**: Inspect the lede's first sentence; confirm a dollar / date precedes any percentage. This is the literal-phrase mirror of QB-040.
  - **Severity**: blocker
  - **Applies to**: Format A / Format B / CEO Letter

- **QB-063** — Minimizing language ("modest," "small," "minor" change) does not appear in client-facing copy.
  - **Owning rule**: `_root/04 §3` row on minimizing language
  - **How to verify**: Grep client copy for `modest`, `small change`, `minor change`, `minor adjustment`.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-064** — Favor framing ("gift," "reward for loyalty," "thank you for being a customer") does not appear in any Good News notice; the mechanic is stated plainly.
  - **Owning rule**: `_root/04 §3` row on gift / reward / favor framing
  - **How to verify**: Grep the Good News brief for `gift`, `reward`, `thank you for being`.
  - **Severity**: blocker
  - **Applies to**: Good News

- **QB-065** — No apology for prior pricing ("we're sorry the legacy structure was…") appears in client-facing copy.
  - **Owning rule**: `_root/04 §3` row on apology for prior pricing (operationally non-negotiable via §2.3)
  - **How to verify**: Grep client copy for `sorry the legacy`, `regret`, `apologize for`, `should have updated`. Literal-phrase mirror of QB-042.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-066** — The account's total ERP-side order volume is not used as a lede stat; order counts in the lede are scoped to "orders submitted through SuperCat" or "eCat orders."
  - **Owning rule**: `_root/04 §3` row on total ERP-side order volume as a lede stat
  - **How to verify**: Inspect the lede's order-count sentence (if any); confirm it includes `eCat`, `through SuperCat`, or `submitted through eCat`.
  - **Severity**: blocker
  - **Applies to**: Format A / Format B / CEO Letter

- **QB-067** — No support-issue context ("we've been working through your support issue") appears in client-facing copy; the support fire is flagged in the internal routing block only.
  - **Owning rule**: `_root/04 §3` row on support-issue context in client copy
  - **How to verify**: Grep client copy for `support issue`, `support escalation`, `working through your`, `ticket`; cross-reference against `support_fire = TRUE` rows where the ⚠️ flag should appear in the (removed-before-send) routing block.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-068** — Health-band names (`Thriving`, `Healthy`, `Watch`, `At Risk`, `Critical`) do not appear in client copy.
  - **Owning rule**: `_root/04 §3` row on health-band names (operationally non-negotiable via §2.5)
  - **How to verify**: Grep client copy for the five band strings (word-bounded). Literal-phrase mirror of QB-043 for the band-name half.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-069** — Dimension scores (`Engagement: N`, `Adoption: N`, `Value Delivery: N`, `Operational Health: N`) do not appear in client copy.
  - **Owning rule**: `_root/04 §3` row on dimension scores (operationally non-negotiable via §2.5)
  - **How to verify**: Grep client copy for `Engagement:\s*\d`, `Adoption:\s*\d`, `Value Delivery:\s*\d`, `Operational Health:\s*\d` patterns. Literal-phrase mirror of QB-043 for the dimension-score half.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-070** — Expansion-tier feature names ("at the next tier you'd also get…") do not appear in any migration brief.
  - **Owning rule**: `_root/04 §3` row on expansion-tier feature names (operationally non-negotiable via §2.6)
  - **How to verify**: Grep client copy for `at the next tier`, `next tier`, `upgrade tier`, `also get`; cross-reference QB-044.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-071** — Peer-range dollar values (e.g. "Commerce Professional ranges from $1,295–$1,589") do not appear in any client-facing copy; peer dollar values stay INTERNAL-ONLY across all four formats.
  - **Owning rule**: `_root/04 §3` row on peer-range dollar values (operator decision 2026-05-22 — universal prohibition; supersedes prior Format-A-allowed pattern) + `_root/04 §4.11`
  - **How to verify**: Grep client copy for `\$[\d,]+\s*[–-]\s*\$[\d,]+` dollar-range patterns; for any hit, confirm it is not a peer-range comparison (it may be a per-tier rate-card single value).
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-072** — Hedged universality phrasing ("most accounts," "many accounts," "across the broader install base") does not appear in client copy.
  - **Owning rule**: `_root/04 §3` row on hedging the universality claim (operationally non-negotiable via §2.7)
  - **How to verify**: Grep client copy for `most accounts`, `many accounts`, `broader install base`, `across the broader`. Literal-phrase mirror of QB-045.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-073** — The word "transition" describing the customer's side of the move ("as you transition to the new pricing") does not appear; "going forward" / "effective [DATE]" is used instead. Exception: narrow administrative usage inside the `annual_discount_retirement` block is permitted per `_root/05 §2.7`.
  - **Owning rule**: `_root/04 §3` row on "transition" (with the ADR administrative-context exception)
  - **How to verify**: Grep client copy for `transition`; cross-reference any hit against the ADR block context per `_root/05 §2.7.2`/`§2.7.3` (which contain the permitted phrase "we'll document that as part of this transition").
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-074** — Unpublished premium SKU names (Sales Intelligence, Insights Layer, Premium Support, Commerce add-on) do not appear in client-facing copy; they are response-only per `_root/03 §6`.
  - **Owning rule**: `_root/04 §3` row spirit + `_root/03 §6` "never in proactive comms" rule + `_root/06 §5.5` `flags` vocabulary `INSIGHTS-LAYER`
  - **How to verify**: Grep client copy for `Sales Intelligence` (proactive), `Insights Layer`, `Premium Support`, `Commerce add-on`.
  - **Severity**: blocker
  - **Applies to**: all formats

### §6.3 Against `_root/04 §4` (the 14 named voice rules)

One check per subsection. The §2 non-negotiables that point here (§2.4, §2.8, §2.10, §2.11, §2.12, §2.13) are enforced through these checks; cross-references appear inline.

- **QB-075** — The lede names the relationship before it delivers the number; at least one account-specific stat (sessions, active users, surfaces in use, scoped order count, tenure year) appears in the lede; tenure-aware variant matches the cohort year band.
  - **Owning rule**: `_root/04 §4.1`
  - **How to verify**: Inspect the lede paragraph; confirm one relationship sentence precedes the dollar sentence; confirm at least one stat is present; confirm the tenure phrase matches `cohort_year` from v6.2.
  - **Severity**: blocker
  - **Applies to**: Format A / Format B / CEO Letter (suppressed for Watch / At Risk / Critical per §4.13 — see QB-087)

- **QB-076** — The lede uses unambiguous platform metrics (tenure, active users, session volume, surfaces in use); no provisioned-vs.-active ratio; no per-order subscription cost; any order count is scoped to "eCat orders" or "orders submitted through SuperCat."
  - **Owning rule**: `_root/04 §4.2` (operationally non-negotiable via §2.8) — also enforced by QB-060, QB-061, QB-066 at the literal-phrase layer; this check is the structural-rule layer
  - **How to verify**: Inspect the lede stat selection; cross-reference against the §4.2 illustrative pair (follows / violates).
  - **Severity**: blocker
  - **Applies to**: Format A / Format B / CEO Letter

- **QB-077** — Where the "How This Compares" section uses "above the midpoint," the user-count clause is present and names the team size explicitly while confirming the platform base is at the tier standard.
  - **Owning rule**: `_root/04 §4.3` (operationally non-negotiable via §2.12; archived template-test CHECK 5)
  - **How to verify**: Compute `NEW_MRR − midpoint` against the §4.3 threshold table; if `NEW_MRR > midpoint + $75`, confirm the position label is "above the midpoint" AND the user-count clause is present.
  - **Severity**: blocker
  - **Applies to**: Format A / Format B / CEO Letter

- **QB-078** — Where `delta_pct > 30%`, the lede directly acknowledges the annual dollar impact using the §4.4 verbatim form (CEO Letter: "That's $[DELTA × 12]/year — a real budget line…"; Format B: monthly-and-annual in the same sentence).
  - **Owning rule**: `_root/04 §4.4` (operationally non-negotiable via §2.11; archived template-test CHECK 8; archived handoff Quality Bar "Delta >30% → lede names the annual dollar impact")
  - **How to verify**: Read `delta_pct` from v6.2; if > 30%, inspect the lede for the verbatim sentence with the correct annual figure.
  - **Severity**: blocker
  - **Applies to**: Format B / CEO Letter (delta > 30% accounts)

- **QB-079** — The closing-summary "only thing changing" sentence is present verbatim; the IUR variant is used when `included_user_reduction` is primary or any secondary, the default form when not.
  - **Owning rule**: `_root/04 §4.5` (operationally non-negotiable via §2.4 + §2.13; archived template-test CHECK 4; archived handoff Quality Bar "`included_user_reduction` accounts → alternate closing line")
  - **How to verify**: Read `migration_driver` and `secondary_drivers` from v6.2; confirm the §4.5 verbatim sentence appears character-for-character in the correct variant.
  - **Severity**: blocker
  - **Applies to**: Format A / Format B / CEO Letter

- **QB-080** — When `new_tier_base > current_platform_mrr`, the platform-base-grown sentence ("The platform has grown considerably since [YEAR] — more surfaces, more capability, the infrastructure behind it. The rate now reflects what the platform is today.") appears verbatim with the correct cohort year token.
  - **Owning rule**: `_root/04 §4.6` (operationally non-negotiable via §2.10; archived handoff Quality Bar "Platform base increase (any driver) → base repricing justification sentence present")
  - **How to verify**: Read v6.2 `tier_base` and `current_platform_mrr` (and `current_mrr` as the broader gate); if base increases, grep the brief for the §4.6 verbatim sentence with `[YEAR]` substituted from `cohort_year`.
  - **Severity**: blocker
  - **Applies to**: Format A / Format B / CEO Letter (any driver where base increases)

- **QB-081** — For accounts with `cohort_year ≤ 2015`, the named-year tenure paragraph appears in or immediately after the lede in the Format-B or CEO-Letter verbatim form; for the CEO Letter, the paragraph ends with the call commitment.
  - **Owning rule**: `_root/04 §4.7`
  - **How to verify**: Read `cohort_year` from v6.2; if ≤ 2015, grep the brief for the named-year tenure language and the "fundamentally different product" framing.
  - **Severity**: blocker
  - **Applies to**: Format B / CEO Letter (early-adopter cohorts)

- **QB-082** — The value-anchor section "What This Works Out To" is included iff `ltm_orders > 0` AND `cost_per_order < $200`; the second sentence (delta-per-order reframe) is appended iff `delta_per_order < $50`; otherwise the second sentence is omitted; if `ltm_orders = 0` OR `cost_per_order ≥ $200`, the entire section is omitted.
  - **Owning rule**: `_root/04 §4.8` (operator-stamped $200 threshold 2026-05-22; archived template-test CHECK 6; archived handoff Quality Bar "Value anchor: include if `ltm_orders > 0` and `cost_per_order < $200`")
  - **How to verify**: Compute `cost_per_order` and `delta_per_order` per `_root/07 §4.4`; cross-reference inclusion gates against the brief.
  - **Severity**: blocker
  - **Applies to**: Format A / Format B / CEO Letter

- **QB-083** — Immediately after the pricing table in any URN block AND any IUR block, the verbatim billing-basis footnote ("*User billing is based on enabled accounts in your SuperCat environment — the user figures above reflect your current enabled count.*") appears before the next `---` separator.
  - **Owning rule**: `_root/04 §4.9` (operationally non-negotiable via §2.13; archived template-test CHECK 2 + CHECK 3)
  - **How to verify**: For URN-primary or IUR-primary briefs (and URN-with-IUR-secondary briefs), grep the brief for the verbatim sentence directly after the pricing table.
  - **Severity**: blocker
  - **Applies to**: Format B / CEO Letter (URN or IUR present)

- **QB-084** — When the URN block applies AND `Before platform base ≠ After platform base`, the platform-base conditional sentence (Format B form or CEO Letter form per §4.10) is present.
  - **Owning rule**: `_root/04 §4.10` (archived template-test CHECK 1)
  - **How to verify**: For URN-primary briefs, compute `Before platform base` (= `current_platform_mrr`) vs `After platform base` (= `tier_base`); if they differ, grep the URN block for the prescribed sentence.
  - **Severity**: blocker
  - **Applies to**: Format B / CEO Letter (URN with base move)

- **QB-085** — The "How This Compares" section uses only the prescribed plain-English position vocabulary ("at the base rate" / "below the midpoint" / "near the midpoint" / "above the midpoint"); no peer-range dollar values appear in client copy.
  - **Owning rule**: `_root/04 §4.11` (peer-range universal prohibition operator-stamped 2026-05-22)
  - **How to verify**: Inspect the "How This Compares" section; confirm one of the four prescribed phrases is used and no peer-range dollar values appear. Cross-reference QB-071.
  - **Severity**: blocker
  - **Applies to**: Format A / Format B / CEO Letter

- **QB-086** — The format-specific close text is verbatim per §4.12 (Format A passive offer; Format B active meeting offer; CEO Letter specific call-commitment date within 5 business days of send; Good News no-ask close). The formal-notice line appears immediately after every non-Good-News close.
  - **Owning rule**: `_root/04 §4.12`
  - **How to verify**: Diff the close paragraph against the §4.12 verbatim block for the matching format; for the CEO Letter, confirm the call date is a real calendar date within 5 business days of send (not "soon" or "in the coming days") and matches the routing block's `CEO call commitment date` field.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-087** — For accounts where `health_band ∈ {Watch, At Risk, Critical}` OR `value_delivery_score < 40`, the relationship-stats lede and "What You've Built" section are suppressed; the brief opens with the §4.13 verbatim standalone dollar-change sentence. For the CEO Letter, the call commitment immediately follows the dollar change.
  - **Owning rule**: `_root/04 §4.13`
  - **How to verify**: Read v6.2 `health_band` and `value_delivery_score`; if either trigger fires, inspect the lede for the §4.13 standalone sentence form and the absence of the relationship-stats lede.
  - **Severity**: blocker
  - **Applies to**: Format A / Format B / CEO Letter (Watch / At Risk / Critical or VD<40)

- **QB-088** — For accounts where `migration_driver = platform_discount_correction`, the §4.14 verbatim sentence ("Your rate reflects a discount applied at signing that's being retired as part of this change.") replaces the default "rate at signing" sentence in the lede framing block.
  - **Owning rule**: `_root/04 §4.14`
  - **How to verify**: Read v6.2 `migration_driver`; if `platform_discount_correction`, grep the lede framing for the §4.14 verbatim substitution and confirm the default tenure-aware "rate was set in [YEAR]" sentence is absent.
  - **Severity**: blocker
  - **Applies to**: Format A / Format B / CEO Letter (PDC accounts)

### §6.4 Against `_root/05` (driver content)

These checks verify the per-driver "Why the Number Is Changing" block is used verbatim from `_root/05` and that conditional sub-blocks fire correctly.

- **QB-089** — The primary-driver "Why the Number Is Changing" block in the brief matches the verbatim block in `_root/05 §2.X` (or §3.X for decrease-side drivers) for the brief's format, character-for-character — no paraphrasing, no reordering, no synonym substitution.
  - **Owning rule**: `_root/05 §2` + `_root/05 §3` (verbatim driver-prose blocks)
  - **How to verify**: Look up `migration_driver` in v6.2; identify the matching §2.N / §3.N subsection for the brief's format; diff the brief block against the source.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-090** — Every bracketed placeholder (`[YEAR]`, `[LEGACY_USER_RATE]`, `[NEW_INCLUDED]`, `[TIER]`, `[TRAILING_AVG]`, etc.) in the driver block is filled with a value sourced from v6.2 or the canonical Postgres queries — no unsubstituted `[BRACKET]` text remains in client copy.
  - **Owning rule**: `_root/05 §1.2` (primary driver authoritative; substitute from v6.2) + `_root/07 §2` (column meanings)
  - **How to verify**: Grep client copy for `\[[A-Z_]+\]` patterns; any hit is an unsubstituted placeholder.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-091** — Conditional sub-blocks (`[IF excess users remain]`, `[IF trailing avg users ≤ new included base]`, `[IF secondary driver = …]`, `[REQUIRED when Before platform base ≠ After platform base]`) are rendered iff the condition holds for the account, per the §2 driver-subsection conditional logic.
  - **Owning rule**: `_root/05 §2.1.6`, `§2.2.6`, `§2.3.6`, `§2.4.6`, `§2.5.6`, `§2.6.6`, `§2.7.6`, `§2.8.6`
  - **How to verify**: For each `[IF ...]` marker in the matching driver block, compute the condition from v6.2; confirm the sub-block is rendered iff the condition is TRUE.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-092** — Secondary-driver weaving follows the §4 matrix for the account's primary + secondary combination; the integration is woven into the primary block as supporting context, never a separate section.
  - **Owning rule**: `_root/05 §1.3` (no separate "Secondary Drivers" section) + `_root/05 §4` (secondary-driver weaving matrix)
  - **How to verify**: Read `secondary_drivers` from v6.2; locate the matching row in `_root/05 §4`; confirm the prescribed integration (sub-block or per-account narrative) is present and no separate "Secondary Drivers" heading exists.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-093** — For Format B and CEO Letter briefs where the primary + secondary combination is `multi_org_retirement | included_user_reduction` (6 accounts), the IUR integration follows the §4 matrix; per CL-016 (operator-stamped 2026-05-22, IUR-only scope), the new Stage 3 templates will carry an explicit IUR sub-block — until Stage 3 lands, the drafter integrates per-account narratively per the §4 matrix's "no templated sub-block" note.
  - **Owning rule**: `_root/05 §2.6.7` + `_root/05 §4` matrix + CL-016 operator-stamp
  - **How to verify**: For any MOR-primary + IUR-secondary brief, confirm IUR-variant close (per QB-079) AND billing-basis footnote (per QB-083) are present; confirm the IUR move is integrated narratively within the MOR block, not as a separate section.
  - **Severity**: blocker
  - **Applies to**: Format B / CEO Letter (MOR + IUR accounts)

- **QB-094** — For Format B and CEO Letter briefs where the primary + secondary combination is `multi_org_retirement | user_rate_normalization` (2 accounts), the URN integration follows the §4 matrix per-account narrative pattern.
  - **Owning rule**: `_root/05 §2.6.7` + `_root/05 §4` matrix
  - **How to verify**: For any MOR-primary + URN-secondary brief, confirm the URN move is integrated narratively within the MOR block (a sentence such as "Your per-user rate is also moving from $[LEGACY_USER_RATE]/user to the current graduated standard"); confirm billing-basis footnote is present if URN integration produces a user-charge change.
  - **Severity**: blocker
  - **Applies to**: Format B / CEO Letter (MOR + URN accounts)

- **QB-095** — Format A briefs do NOT improvise content for drivers the format does not carry templated prose for (`tier_base_increase` per `_root/05 §2.3.4`, `included_user_reduction` per `§2.4.4`, `annual_discount_retirement` per `§2.7.4`); the drafter escalates per `_root/CONTRACTS.md §2` rather than back-filling from Format B.
  - **Owning rule**: `_root/05 §2.3.4`, `§2.4.4`, `§2.7.4` (Format A does not carry the block) + `_root/CONTRACTS.md §2` (no improvisation)
  - **How to verify**: For any Format A brief, read `migration_driver`; if it is one of the three flagged drivers AND the brief contains substantive driver prose, confirm the operator stamped a deviation (otherwise a failure).
  - **Severity**: blocker
  - **Applies to**: Format A

- **QB-096** — Where v6.2 `migration_driver` and the HTML model's `d` field disagree, the v6.2 value is used (per `_root/05 §1.2`).
  - **Owning rule**: `_root/05 §1.2` + `_root/07 §1` source-of-truth hierarchy
  - **How to verify**: Compare v6.2 `migration_driver` against HTML model `d` for the account; the brief block must match v6.2.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-097** — No brief is drafted for accounts where `migration_driver = 'already_migrated'` or `migration_status = 'already_migrated'` (the `tcs` / `drf` anomaly is filtered at the loader).
  - **Owning rule**: `_root/05 §1.4` + `_root/07 §3` (loader filter)
  - **How to verify**: Grep brief output folders for `tcs__` or `drf__` filenames; any hit is a failure.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-098** — Decrease-side drivers (`module_compression`, `user_count_variance`, `rate_architecture`) frame the decrease as a mechanic, not a favor; the Good News close from `_root/04 §4.12` is used.
  - **Owning rule**: `_root/05 §3.1.5`, `§3.2.4`, `§3.3.4` (voice posture note) + `_root/04 §4.12` (Good News close)
  - **How to verify**: For Good News briefs, confirm the decrease is explained as a mechanic (consolidation, recalibration, recalculation) and the verbatim close from `_root/04 §4.12` is present.
  - **Severity**: blocker
  - **Applies to**: Good News

### §6.5 Against `_root/03` (product / pricing language)

- **QB-099** — The "What You're Getting at $[X]/month" tier block matches the canonical T1 / T2 / T3 verbatim block in `_root/03 §1` character-for-character; the `[NEW_INCLUDED]` placeholder is substituted from v6.2 `included_users`.
  - **Owning rule**: `_root/03 §1` (verbatim T1 / T2 / T3 blocks)
  - **How to verify**: Read v6.2 `assigned_tier`; diff the brief's tier block against the matching `_root/03 §1` subsection (T1 / T2 / T3).
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-100** — The user-rate ladder in client copy uses the bands **1–10 / 11–25 / 26–50 / 51+** at **$25 / $22 / $20 / $18**; the foundation/03 D-004b bands (1–25 / 26–50 / 51–100 / 101+) are NOT used.
  - **Owning rule**: `_root/03 §2 Block A` (canonical customer-facing ladder; foundation D-004b stale stamp tracked as CL-007)
  - **How to verify**: Grep the brief for the four band labels; any appearance of `1–25`, `26–50` as a *first* band, `51–100`, or `101+` is a failure.
  - **Severity**: blocker
  - **Applies to**: all formats (when the ladder renders — URN / IUR / TBI / ABTS drivers)

- **QB-101** — Unpublished premium SKUs (Sales Intelligence add-on, Insights Layer, Premium Support, Commerce add-on) are not named anywhere in client-facing copy.
  - **Owning rule**: `_root/03 §6` ("never in proactive comms")
  - **How to verify**: Grep client copy for the four SKU names (cross-references QB-074).
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-102** — INTERNAL-only sections (peer ranges per `_root/03 §5`; unpublished premium SKU prices per `§6`; competitive-positioning tables per `§5`) are stripped before send; they appear only in the internal routing block / prep sheet.
  - **Owning rule**: `_root/03 §5` + `_root/03 §6` (INTERNAL tags) + `_root/04 §1` (internal-vs.-client boundary)
  - **How to verify**: Inspect the brief; confirm peer-range dollar tables (T1 $774 / $1,200 / $1,629; T2 $1,295 / $1,440 / $1,589; T3 $2,295 / $2,585 / $2,875) and the AmpTab / Pepperi comparison table are absent from client copy. Cross-reference QB-071.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-103** — The Implementation-fee table (`_root/03 §4` Essentials / Guided / Comprehensive) does not appear in any migration brief unless the operator explicitly authorizes its inclusion for a re-implementation conversation.
  - **Owning rule**: `_root/03 §4` (recommendation: implementation-fee table is reference-only for migration comms)
  - **How to verify**: Grep client copy for `Essentials.{0,80}Guided.{0,80}Comprehensive` patterns or the dollar values `$2,500` / `$5,000` in an implementation context.
  - **Severity**: warning
  - **Applies to**: all formats

---

## Section 7 — Math / numeric reconciliation checks (against `_root/02` + `_root/07`)

- **QB-104** — The pricing table's "Before" total matches `current_mrr` from v6.2 exactly; the "After" total matches `new_total_mrr` exactly.
  - **Owning rule**: `_root/07 §2` (column meanings; Before total = `current_mrr`; After total = `new_total_mrr`) + archived handoff Quality Bar "Math balances: Before total = `current_mrr`, After total = `new_mrr` exactly"
  - **How to verify**: Sum the brief's pricing-table "Before" column rows; compare to v6.2 `current_mrr`. Repeat for "After" vs `new_total_mrr`.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-105** — The brief's stated Δ MRR equals `new_total_mrr − current_mrr` within ±$1 rounding; this matches v6.2 `delta_mrr`.
  - **Owning rule**: `_root/07 §2` (`delta_mrr` cross-check against `new_total_mrr − current_mrr`)
  - **How to verify**: Re-compute `new_total_mrr − current_mrr` from v6.2; compare to brief Δ figure and to v6.2 `delta_mrr`.
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-106** — When the brief asserts an annual dollar figure (per QB-078 for delta > 30%), the figure equals `delta_mrr × 12` within ±$1 rounding.
  - **Owning rule**: `_root/04 §4.4` (annual figure derivation) + `_root/07 §2` (`delta_mrr`)
  - **How to verify**: Multiply v6.2 `delta_mrr` by 12; compare to the brief's annual figure.
  - **Severity**: blocker
  - **Applies to**: Format B / CEO Letter (delta > 30%)

- **QB-107** — The brief's new tier base matches v6.2 `tier_base`, and the new included-user count matches `included_users`, for the assigned tier in `_root/03 §1`.
  - **Owning rule**: `_root/03 §1` (T1 / T2 / T3 headline prices and included users) + `_root/07 §2`
  - **How to verify**: Compare v6.2 `tier_base` and `included_users` against the brief's "After" rows and the T1 / T2 / T3 standards ($749 / 10; $1,295 / 15; $2,295 / 40).
  - **Severity**: blocker
  - **Applies to**: all formats

- **QB-108** — At a Δ-tier boundary ($80, $400, $600), the format-selection check (QB-013, QB-018) reconciles with the operator-stamped precedence rule.
  - **Owning rule**: `_root/06 §3` Δ-tier dispatch + precedence rule (operator-stamped 2026-05-22)
  - **How to verify**: For any Δ within ±$20 of a tier boundary, re-evaluate the §3 dispatch table and the §3 precedence rule; confirm the brief's format matches the higher-touch outcome.
  - **Severity**: blocker
  - **Applies to**: Format A / Format B / CEO Letter / CEO Pre-Call → Format B (boundary accounts)

- **QB-109** — v6.2 contains exactly 109 unique `ord_id` rows (107 `migration_pending` + 2 `already_migrated`); segment counts roll up to the `_root/02 §1` totals; aggregate Δ MRR = +$32,652.60/mo (= exec plan v3.3 §I +$32,653/mo within rounding).
  - **Owning rule**: `_root/02 §8` (109 / 107 / 2 reconciliation)
  - **How to verify**: Re-run the canonical loader; count distinct `ord_id`s by `migration_status`; sum `delta_mrr` over `migration_pending` rows. Audit-only check at the dataset level.
  - **Severity**: audit-only
  - **Applies to**: all formats (dataset integrity)

- **QB-110** — The pre-send `implied_billed_excess = ROUND(current_user_mrr / current_user_rate)` and `narrative_excess = trailing_avg_users − current_provided_users` reconcile within ±3 users (or the dollar discrepancy is ≤ $60/month); else the routing block carries the ⚠️ reconciliation flag per `_root/07 §4.5`.
  - **Owning rule**: `_root/07 §4.5` (before-state reconciliation)
  - **How to verify**: Re-compute both numbers from v6.2; compare to the brief's pricing-table excess-users row; cross-reference QB-032.
  - **Severity**: blocker
  - **Applies to**: Format A / Format B / CEO Letter

- **QB-111** — When `support_fire = TRUE`, the routing block carries the `⚠️ SUPPORT FIRE: [N] days open. Production-ready. Operator decides send timing.` line; the brief is drafted in full; client-facing copy contains no reference to the support issue.
  - **Owning rule**: `_root/07 §5` (`support_fire = TRUE` handling — not a failure mode) + `_root/07 §7` (conditional routing-block field) + archived handoff Quality Bar "`support_fire = TRUE` → ⚠️ flag in routing block, NOT skipped"
  - **How to verify**: Read v6.2 `support_fire` and `support_fire_days_open`; confirm the routing-block ⚠️ line if TRUE; cross-reference QB-067 for client-copy absence.
  - **Severity**: blocker
  - **Applies to**: all formats (when support_fire = TRUE)

---

## Section 8 — Audit-only checks (post-send sweep)

These cannot run before send. They produce learning signals that feed back into the rule layer.

- **QB-112** — Customer-reply analysis: if the customer's reply names a forbidden phrase from `_root/04 §3` as a friction point, the operator considers whether to broaden or refine the §3 row.
  - **Owning rule**: `_root/04 §3` (forbidden-phrase row evolution) + `_root/CONTRACTS.md §3` (rule-change protocol)
  - **How to verify**: After send + reply, read the customer reply; flag any §3-row mention; escalate per `_root/CONTRACTS.md §3`.
  - **Severity**: audit-only
  - **Applies to**: all formats

- **QB-113** — The 60-day countdown from send date to the brief's effective date is logged on the operator calendar; the effective date matches the routing block's `Earliest enforceable effective date` field.
  - **Owning rule**: `_root/01 §3` operating principle 2 ("Migration starts when compliant written notice is received") + `_root/06 §3` (60-day notice architecture)
  - **How to verify**: Cross-reference send date + 60 days against the routing-block effective date and against the operator calendar.
  - **Severity**: audit-only
  - **Applies to**: Format A / Format B / CEO Letter

- **QB-114** — For CEO Letter and CEO Pre-Call → Format B briefs, the call-commitment date (within 5 business days of send per `_root/04 §4.12`) is on the CEO calendar and the call was actually placed by that date.
  - **Owning rule**: `_root/04 §4.12` (CEO Letter close "I'll call you personally by [SPECIFIC DATE]")
  - **How to verify**: Cross-reference the routing-block `CEO call commitment date` against the CEO calendar; confirm the call landed.
  - **Severity**: audit-only
  - **Applies to**: CEO Letter / Format B (CEO Pre-Call variant)

- **QB-115** — For Annual briefs, the renewal date is captured in the cohort tracker; the notice was sent ≥90 days before that date.
  - **Owning rule**: `_root/02 §5` (annual overlay) + `_root/06 §4.3` (annual overlay timing)
  - **How to verify**: Cross-reference v6.2 `notice_cohort = 'Renewal-Based'` rows; confirm the renewal date is logged; confirm the send-to-renewal interval ≥ 90 days.
  - **Severity**: audit-only
  - **Applies to**: all formats (Annual accounts)

- **QB-116** — All 107 `migration_pending` accounts have either a sent notice or a stamped operator decision to defer (per `_root/01 §4` definition of done).
  - **Owning rule**: `_root/01 §4` (definition of done)
  - **How to verify**: Roll up the per-account state across `format-a-notices/`, `format-b-notices/`, `ceo-letter-notices/`, `good-news-notices/`, entity packets, and the operator's defer log; confirm 107 distinct `ord_id`s are accounted for.
  - **Severity**: audit-only
  - **Applies to**: all formats (dataset-level)

- **QB-117** — Migration-induced logo churn does not exceed 6 accounts; migration-induced MRR churn does not exceed $3,000/mo.
  - **Owning rule**: `_root/01 §4` (success metrics guardrails)
  - **How to verify**: Track customer-departure decisions tagged "migration-induced" against the two caps.
  - **Severity**: audit-only
  - **Applies to**: all formats (dataset-level)

- **QB-118** — Entity-conversation feedback is synthesized and applied to Executive and Pre-Engagement (July cohort) artifacts before those cohorts launch.
  - **Owning rule**: `_root/01 §4` (Entity-conversation feedback synthesized before July cohort launch)
  - **How to verify**: Audit the entity-pilot feedback log; confirm the synthesis output is reflected in updated July cohort drafts.
  - **Severity**: audit-only
  - **Applies to**: entity packet → Executive / Pre-Engagement

---

## Section 9 — Cross-doc drift checks (run rarely; high signal)

These detect drift across `_root/` docs themselves. Run periodically by the operator, or after any `_root/09_changelog.md` entry.

- **QB-119** — No `_root/` doc restates a rule owned by another `_root/` doc; references are by `_root/XX §N.M` pointer only.
  - **Owning rule**: `_root/CONTRACTS.md §5` (path-reference contract)
  - **How to verify**: Grep across `_root/` for distinctive rule-fragment strings (e.g. "every account we work with," "The platform has grown considerably since [YEAR]," "Across [ltm_orders] eCat orders last year"); each fragment should appear in exactly one owning doc.
  - **Severity**: warning
  - **Applies to**: dataset-level (rule layer)

- **QB-120** — The 5 errata in `_root/02 §7` and `_root/06 §6` are character-for-character identical (rac / wac / sbl / big / kl rows).
  - **Owning rule**: `_root/02 §7` (canonical owner) + `_root/06 §6` (self-sufficient mirror)
  - **How to verify**: Diff the two tables.
  - **Severity**: blocker
  - **Applies to**: dataset-level (rule layer)

- **QB-121** — The `comm_action` vocabulary in `_root/06 §5` (7 distinct values + their row counts) matches the distinct values + row counts in `migration_comm_tiers_2026-05-19.csv`.
  - **Owning rule**: `_root/06 §5`
  - **How to verify**: `awk`/grep distinct `comm_action` values from the CSV with counts; compare to the §5 table.
  - **Severity**: blocker
  - **Applies to**: dataset-level (rule layer)

- **QB-122** — The 53-column v6.2 field guide in `_root/07 §2` matches the v6.2 CSV header row (each column name present in §2; no extras; no missing).
  - **Owning rule**: `_root/07 §2`
  - **How to verify**: Extract the CSV header row; diff against the §2 table column names.
  - **Severity**: blocker
  - **Applies to**: dataset-level (rule layer)

- **QB-123** — The "What's Coming in 2026" verbatim block in `_root/03 §3` matches the block as it appears in every brief that is required to carry it (per QB-046); the trailing operator-note line is stripped from each sent version.
  - **Owning rule**: `_root/03 §3` + `_root/04 §2.9`
  - **How to verify**: Diff `_root/03 §3` against the section as rendered in every in-flight brief (Stage-3 dependency once templates exist).
  - **Severity**: warning
  - **Applies to**: dataset-level (Stage 3 template build + Stage 4 drafts)

- **QB-124** — Every `_root/09_changelog.md` entry corresponding to a rule change includes the `_root/CONTRACTS.md §3` propagation steps: edit owning doc, log entry, bump `Last updated`, bump `_root/00_manifest.md`, identify and re-run affected drafts.
  - **Owning rule**: `_root/CONTRACTS.md §3` (rule-change protocol)
  - **How to verify**: For each post-bootstrapping changelog entry, confirm the affected doc's `Last updated` date matches; confirm the manifest is bumped (post-Stage-5); confirm any affected per-account draft has a `__vN+` re-run.
  - **Severity**: warning
  - **Applies to**: dataset-level (rule-change history)

- **QB-125** — `_root/00_manifest.md` (post-Stage-5) lists every `_root/` doc with a `Last updated` date that matches the doc's header block; any mismatch is a §3-propagation failure.
  - **Owning rule**: `_root/CONTRACTS.md §3` step 4 (manifest bump)
  - **How to verify**: Diff the manifest's per-doc dates against each doc's header.
  - **Severity**: blocker
  - **Applies to**: dataset-level (manifest existence required — Stage 5)

- **QB-126** — The driver counts in `_root/05 §1.1` (37 URN + 17 PDC + 12 TBI + 11 IUR + 10 ABTS + 6 MOR + 2 ADR + 1 SA = 96 increase-side; plus 8 MC + 2 UCV + 1 RA = 11 decrease-side; plus 2 `already_migrated` = 109 total) reconcile to v6.2 exactly. The corrected ground-truth counts were stamped 2026-05-22 in the Wave 4 changelog entry (operator-stamped via planning-agent v6.2 audit; superseded the pre-Wave-4 narrative of "101 of 107 increase-side" + "4 module_compression accounts" + "7 decrease accounts").
  - **Owning rule**: `_root/05 §1.1`
  - **How to verify**: `python3 -c "import csv; f=open('_master-account-data-v6.2.csv'); next(f); from collections import Counter; print(Counter(r['migration_driver'].strip() for r in csv.DictReader(f) if r['migration_status'].strip()=='migration_pending'))"` (skips the leading-blank sentinel row; restricts to `migration_pending`); diff distinct values + counts against the §1.1 tables.
  - **Severity**: blocker
  - **Applies to**: dataset-level (rule layer)

---

## Section 10 — Entity-packet program checks (against `_root/04 §4.15` + `_root/06 §1.6`)

These checks fire on the entity-packet program scope per `_root/06 §1.6` — the canonical 13-entity Stage 3.5 template scope (12 increase-side rollup + 1 standalone_multi_org). They are paired blockers: each check applies to either the entity-packet parent letter (`entity-packets/_parent-letter-template.md`), the entity-packet parent-letter cover email (`entity-packets/_parent-letter-delivery-email-template.md`), or both. The `Applies to:` field names the artifact precisely; per-child notices in the entity-packet program are out of scope for §10 — per-child notices route to their natural standalone-format templates per `_root/06 §2`–`§3` and are checked by the §3–§9 QB-NNN catalog as standalone Format A / Format B / CEO Letter / Good-News artifacts.

Pre-§10, each entity-packet template carried an EP-* identifier list in its Section 4 ("Entity-packet-specific blockers — inferred per `_root/04 §4.15.1`–`§4.15.6`; flag in conformance block") flagging the inferred-check state pending this rule-layer codification (Wave 6 batch — `_meta/stage3_cleanup.md` Stage 3.5 deferred item #5). With §10 landed, the inferred-check state is CLOSED: each EP-* identifier in the entity-packet templates is now backed by a canonical QB-NNN below, and the template Section 4 EP-* lists become template-scaffolding audit-trail of the pre-§10 inference pattern (they are not re-introduced as ongoing inference; they document how the checks landed). Future entity-packet drafts inherit §10 directly.

The §10 checks reference `_root/04 §4.15` (the 6-sub-section parent-letter voice register, operator-stamped 2026-05-26 at Stage 3.5 prep) and `_root/06 §1.6` (the entity-packet routing pattern + 14-entity scope + Ferguson Enterprises exception, operator-stamped 2026-05-26 at Stage 3.5 prep) as the owning rule layer. The strict-placeholder precedent operator-stamped 2026-05-26 applies in full: §10 indexes the rule; it does not restate it.

- **QB-127** — The entity-packet parent letter renders exactly ONE voice fork (CEO-delivered OR Kylor-delivered) per Master Entity tab `delivery_owner` value at draft time, and that fork is consistent across Section 3b greeting, Section 3g close, and Section 3h signature (no mixed-fork rendering).
  - **Owning rule**: `_root/04 §4.15.1` (voice fork CEO-delivered + Kylor-delivered HoCS variants + cross-format CSM-role note)
  - **How to verify**: Open the rendered parent letter; confirm Section 3b uses `Dear [RECIPIENT_FIRST_NAME],` (CEO-delivered) OR `Hi [RECIPIENT_FIRST_NAME],` (Kylor-delivered); confirm Section 3g close matches the same fork's blockquote per `_root/04 §4.15.6`; confirm Section 3h signature matches (CEO's name + `CEO, SuperCat` for CEO-delivered; `Kylor Johnson, Head of Customer Success, SuperCat` for Kylor-delivered); cross-reference the rendered fork against the Master Entity tab `delivery_owner` column value for the entity.
  - **Severity**: blocker
  - **Applies to**: entity packet (parent letter)

- **QB-128** — The entity-packet parent-letter cover email renders exactly ONE voice fork, and that fork MIRRORS the parent letter's fork. Greeting, close, and signature in the cover email use the same fork as the parent letter's Section 3b greeting + Section 3g close + Section 3h signature.
  - **Owning rule**: `_root/04 §4.15.1` (voice fork CEO-delivered + Kylor-delivered HoCS variants + cross-format CSM-role note)
  - **How to verify**: Open the rendered cover email and the rendered parent letter side-by-side; confirm both render the same `delivery_owner` fork at greeting, close, and signature. A mismatched fork between cover email and parent letter is a CEO-Letter-level credibility failure per the cross-format §4.15.1 contract.
  - **Severity**: blocker
  - **Applies to**: entity packet (parent-letter cover email)

- **QB-129** — Neither the entity-packet parent letter nor the cover email carries per-brand mechanics: no per-child driver block ("Why the Number Is Changing"), no per-child pricing table, no per-child tier feature list ("What You're Getting at $X"), no per-child value-anchor section ("What This Works Out To"), no per-child call commitment (Format A passive offer / Format B meeting offer / CEO Letter specific-date call / Good News no-ask close), no per-child "What's Coming in 2026" verbatim block from `_root/03 §3`, no per-child "How This Compares" position sentence per `_root/04 §4.11`, no per-child operations-unchanged sentence per `_root/04 §4.5`, and no per-child consolidated 2026 framing sentence per `_root/04 §3` (or `§3.1` for Good News children).
  - **Owning rule**: `_root/04 §4.15.4` (per-brand mechanics restraint)
  - **How to verify**: Grep the rendered parent letter and cover email for distinctive per-driver content fragments (e.g. "Why the Number Is Changing," "What You're Getting at $," "What This Works Out To," "What's Coming in 2026," "How This Compares," "Your workflow, your team's access," "the consolidated 2026 framing sentence" from `_root/04 §3` / `§3.1`, `_root/04 §4.12` Format A passive close, `_root/04 §4.12` Format B meeting offer, `_root/04 §4.12` CEO Letter specific-date call, `_root/04 §4.12` Good News no-ask close); each fragment should be absent from both artifacts. The per-brand narrative threading list in parent letter Section 3d uses Master Entity tab `entity_messaging_headline` snippets only (one bullet per brand, no per-brand pricing detail or driver mechanic) — confirm the list adheres to the §4.15.4 restraint.
  - **Severity**: blocker
  - **Applies to**: entity packet (parent letter + parent-letter cover email)

- **QB-130** — Neither the entity-packet parent letter nor the cover email mentions `consolidated_delta`, `consolidation_saving`, "consolidation savings opportunity," "rolling everything into one rate," or any soft pointer to the consolidated scenario in customer copy. The dollar number in parent letter Section 3f and in cover email Paragraph 1 uses `default_delta` / `default_mrr` / `default_delta_pct` from the Master Entity tab only; the `consolidated_*` columns appear ONLY in the Section 2 routing block (which is removed before sending) and in CSM/CEO post-send conversation tooling.
  - **Owning rule**: `_root/04 §4.15.5` (default-only pricing posture + terminology constraint distinguishing legacy `multi_org_retirement` migration mechanic from the new `consolidation_saving` sense of "consolidation")
  - **How to verify**: Grep the customer-facing body of the parent letter and cover email (excluding Section 2 routing block, which is removed before sending) for `consolidated_delta`, `consolidation_saving`, `consolidation savings`, `consolidated`, `rolling everything`, `into one rate`; each should be absent from customer copy. Confirm the 4-row entity-level summary table in parent letter Section 3f uses `default_mrr` / `default_delta` / `default_delta_pct` only; the table does NOT add a consolidated-scenario row or a consolidation-savings row. The per-brand narrative threading list in Section 3d may surface a child's `multi_org_retirement` migration mechanic via that brand's `entity_messaging_headline` snippet (legacy multi-org discount retiring) — that "consolidation" is the migration mechanic per `_root/05 §2.6`, distinct from the new `consolidation_saving` sense per `_root/04 §4.15.5` terminology constraint; consult §4.15.5 if the wording feels ambiguous.
  - **Severity**: blocker
  - **Applies to**: entity packet (parent letter + parent-letter cover email)

- **QB-131** — The entity-packet parent letter's Section 2 routing block records Day 0 (parent-letter send date) AND the Day 1–Day 2 per-child notice send window. Every member brand's per-child notice has a confirmed send slot within Day 1–Day 2 of Day 0 BEFORE the parent letter ships. If any child's notice cannot ship within 48 hours of Day 0, the parent letter is held — slipping the parent letter is preferable to slipping the 48-hour per-child window.
  - **Owning rule**: `_root/04 §4.15.6` (routing pointer to per-child notices + 48-hour timing paragraph)
  - **How to verify**: Open the parent letter's Section 2 routing block; confirm both `Parent-letter send date (Day 0): [DATE]` and `Per-child notices send window (Day 1–Day 2): [DATE] – [DATE]` rows are populated with non-placeholder values. Cross-reference against the CS scheduling queue / CRM send calendar for every member brand; confirm each per-child notice has a confirmed send slot within the Day 1–Day 2 window. If any child's notice is not queued, escalate per `_root/CONTRACTS.md §2` BEFORE Day 0 send.
  - **Severity**: blocker
  - **Applies to**: entity packet (parent letter)

- **QB-132** — The entity-packet cover email's Paragraph 2 signals the 48-hour per-child notice cadence per `_root/04 §4.15.6` BEFORE the voice-fork close in Paragraph 3. The recipient must know per-brand notices are coming within 48 hours so the program reads as coordination, not as silence between the parent letter (Day 0) and the per-child notices (Day 1–Day 2).
  - **Owning rule**: `_root/04 §4.15.6` (routing pointer to per-child notices + 48-hour timing paragraph)
  - **How to verify**: Read the cover email body; confirm Paragraph 2 carries an explicit 48-hour signal ("each brand's specific pricing will follow in a separate note within 48 hours" register, or equivalent calibration) AND that the signal lands BEFORE Paragraph 3's voice-fork close. The signal must be structural (timing + format-of-delivery), not substantive (no preview of per-child mechanics per `_root/04 §4.15.4` per-brand mechanics restraint).
  - **Severity**: blocker
  - **Applies to**: entity packet (parent-letter cover email)

- **QB-133** — The entity-packet parent letter's Section 3c lede paragraph names every member brand from the Master Entity tab `member_accounts` column. No abbreviated "and family" / "and others" / "and related brands" hand-wave that omits brand names.
  - **Owning rule**: `_root/04 §4.15.2` (multi-brand portfolio acknowledgment — required content: every member brand named)
  - **How to verify**: Cross-reference the natural-language brand list rendered in Section 3c against the Master Entity tab `member_accounts` column value (pipe-separated source) for the entity; every brand name in `member_accounts` must appear in Section 3c. Grep the rendered Section 3c for "and family," "and others," "and the rest," "and related brands"; each should be absent.
  - **Severity**: blocker
  - **Applies to**: entity packet (parent letter)

- **QB-134** — The entity-packet cover email's Paragraph 1 + Paragraph 2 substitute dollar / date / brand-count tokens from Master Entity tab (`brands` / `default_delta` / `default_delta_pct` / `member_accounts` columns) at the entity level only. The cover email does NOT enumerate every member brand by name — that is the parent letter's job at Section 3c per `_root/04 §4.15.2`; the cover email signals the portfolio at the entity level only.
  - **Owning rule**: `_root/04 §4.15.2` (multi-brand portfolio acknowledgment — entity-level scope in the cover email vs. parent-letter Section 3c enumeration scope)
  - **How to verify**: Read the cover email body; confirm Paragraph 1 references `[ENTITY_NAME]` (entity-level name from Master Entity tab) and `[N]` brand count from Master Entity tab `brands` column without enumerating each member brand by name; confirm Paragraph 2 references `[N]` brand count without enumeration. Brand-by-name enumeration in the cover email is per-child territory leakage; the email signals the portfolio at the entity level only.
  - **Severity**: blocker
  - **Applies to**: entity packet (parent-letter cover email)

- **QB-135** — For Kylor-delivered fork entity packets, both the parent letter's Section 3h signature and the cover email's signature use `Kylor Johnson, Head of Customer Success, SuperCat` — NOT the generic `CSM` role marker. Replies route directly to Kylor, with no CSM hand-off; SuperCat's CSM support role does NOT handle migration conversations.
  - **Owning rule**: `_root/04 §4.15.1` (cross-format CSM-role note — HoCS as the signature title for migration-program communications across all 5 Stage 3 templates)
  - **How to verify**: For any entity whose Master Entity tab `delivery_owner = Kylor`, open the rendered parent letter and cover email; confirm both signatures use `Kylor Johnson, Head of Customer Success, SuperCat` verbatim. Grep both artifacts for `CSM` (uppercase or `Customer Success Manager`); each should be absent from the Kylor-delivered fork signature line. Confirm reply-routing in CRM / mail-config is set to Kylor's address with no CSM hand-off rule.
  - **Severity**: blocker
  - **Applies to**: entity packet (parent letter + parent-letter cover email — Kylor-delivered fork only)

- **QB-136** — For CEO-delivered fork entity packets only: the specific calendar date in the parent letter's Section 3g close text MATCHES the date in the parent letter's Section 2 routing block (CEO call commitment date row) MATCHES the date in the cover email's Section 2 routing block (CEO call commitment date row). Three-location parity is required; any drift between the three is a CEO-Letter-level credibility failure (the call must actually happen by that date per `_root/04 §4.12` convention inherited via `_root/04 §4.15.6`).
  - **Owning rule**: `_root/04 §4.15.6` CEO-delivered close (inherits the specific-calendar-date convention from `_root/04 §4.12` CEO Letter close)
  - **How to verify**: For any entity whose Master Entity tab `delivery_owner = CEO`, open the rendered parent letter and cover email; extract the specific calendar date from (a) parent letter Section 3g close text, (b) parent letter Section 2 routing block `CEO call commitment date` row, (c) cover email Section 2 routing block `CEO call commitment date` row; confirm all three dates are identical. Confirm the date is a specific calendar date within 5 business days of Day 0 send — NEVER "soon," "in the coming days," "shortly," or any other vague-timing variant. Cross-reference against the CEO's calendar to confirm the call is on the calendar before send.
  - **Severity**: blocker
  - **Applies to**: entity packet (parent letter + parent-letter cover email — CEO-delivered fork only)

- **QB-137** — Ferguson Enterprises is NOT drafted from the entity-packet templates per the `_root/06 §1.6` mixed-direction exception paragraph. If the routing CSV inadvertently routes Ferguson to entity-packet, escalate per `_root/CONTRACTS.md §2`; a Ferguson coordinated wrapper is authored ad-hoc at Stage 4 if the operator judges it necessary, not from this template.
  - **Owning rule**: `_root/06 §1.6` (14-entity routing pattern enumeration + Ferguson Enterprises mixed-direction exception paragraph)
  - **How to verify**: Confirm Ferguson Enterprises is excluded from the Stage 3.5 template scope per `_root/06 §1.6`: scan the routing CSV / Master Entity tab for the Ferguson row; confirm any per-child dispatch routes `mlg` to its natural increase-side format per `_root/06 §2`–`§3` and `ml` to Good News per `_root/06 §3` row 1; confirm no entity-packet parent letter is queued for Ferguson. If the routing CSV emits `entity_packet_parent_letter` for Ferguson, the routing has drifted from `_root/06 §1.6` — escalate per `_root/CONTRACTS.md §2`; do not draft from the entity-packet template.
  - **Severity**: blocker
  - **Applies to**: entity packet (parent letter + parent-letter cover email — routing-gate)

- **QB-138** — The entity-packet parent letter and the cover email are PARITY-MATCHED at draft time across (a) fork choice (greeting + close + signature use the same `delivery_owner` value), (b) entity-level dollar values (`default_mrr` / `default_delta` / `default_delta_pct` from Master Entity tab — matched between parent letter Section 3f and cover email Paragraph 1), (c) brand count (`brands` column from Master Entity tab — matched between parent letter Section 3c + cover email Paragraph 1 + cover email Paragraph 2), (d) effective date (entity-level `effective_date` reference — matched between parent letter Section 2 + parent letter Section 3c lede + parent letter Section 3f table + parent letter Section 3g formal-notice line + cover email Section 2 + cover email Paragraph 1 + cover email Paragraph 4 formal-notice line), and (e) for CEO-delivered fork only, the specific calendar date in the parent letter Section 3g close + parent letter Section 2 routing block + cover email Section 2 routing block (the QB-136 3-location date parity is a sub-case of this parity contract).
  - **Owning rule**: `_root/04 §4.15` (the 6-sub-section parent-letter voice register; parity is a structural property of the parent-letter + cover-email coordinated pair sent at Day 0 per `_root/04 §4.15.6` two-stage sequencing)
  - **How to verify**: Open the rendered parent letter and cover email side-by-side; check each of the five parity dimensions (a)–(e) named above. Any drift at any dimension is a credibility failure — the email and parent letter are sent as a coordinated pair at Day 0; mismatched values between them signal the entity-packet program was authored carelessly. For CEO-delivered fork the specific-date parity is a 3-location parity (parent-letter close text + parent-letter routing block + cover-email routing block — QB-136); for all forks the other four parity dimensions are 2-location-plus (entity-name / dollar / brand-count / effective-date appear in both artifacts and must match).
  - **Severity**: blocker
  - **Applies to**: entity packet (parent letter + parent-letter cover email)

---

## Section 11 — What this doc does NOT own (closing reminder)

`_root/08` indexes checks against the rule layer. It does not own:

- **The rules being checked.** They live in `_root/01`–`_root/07`. A drafter who needs the rule text follows the pointer in the owning-rule field, never reads it from here.
- **The actual draft outputs.** Per-account briefs live in the four format folders (`format-a-notices/`, `format-b-notices/`, `ceo-letter-notices/`, `good-news-notices/`) plus the future entity-packet folder (Stage 3 CL-014). This doc never carries example draft text.
- **How to fix a failing check.** The fix lives in the doc that owns the rule. The drafter does not improvise; the drafter escalates per `_root/CONTRACTS.md §2`. The operator decides whether to revise the brief or revise the rule.
- **Stage 3 template-level checks.** Once Stage 3 rebuilds the per-format brief templates, an additional `_root/08`-style template-test layer may be added. Until templates exist, the present checklist indexes the rule layer only.
- **The conformance-block format itself.** Originally reserved for this doc per `_root/CONTRACTS.md §verifying-conformance` step 3, the canonical conformance-block format was migrated to `_root/00_manifest.md §5` at Stage 5 (2026-05-22) — the manifest is the first doc every fresh agent reads, and the format is metadata about how every session ends, not a per-brief check. This doc's QB-002 / QB-003 enforce the format; the manifest defines it.

---

*Cross-references: `_root/CONTRACTS.md` §2 (agent contract — every QB-NNN here is the operational expression of "stop and ask rather than improvise"), §3 (rule-change protocol — every check change follows this protocol), §4 (anti-archive rule — handoff and template-test reads were the only authorized historical-check extractions for this doc), §5 (path-reference contract — every owning-rule field is a pointer, never a restatement); `_root/09_changelog.md` (the rule-change history that backs every check's owning rule).*
