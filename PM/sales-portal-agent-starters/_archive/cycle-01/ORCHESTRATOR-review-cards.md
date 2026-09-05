# ORCHESTRATOR — Session Brief + Review Cards (Cycle 01)

**Date:** 2026-07-16
**Role:** Betting-table chair / domain referee / synthesis auditor / lane traffic controller / quality gate.
Loaded: `00-PROGRAM-SPINE.md`, `00a-DOCTRINE-shapeup-ddd-affinity.md`, `00b-PRODUCT-HANDOFF-analytics.md`.

---

# Session Brief — 2026-07-16

## Isolation
**ON.** No `supercat-code` writes occurred. All lane outputs are markdown + one mockup-only HTML. Lift only on Kylor's verbatim `ISOLATION OFF — GO on <ticket-or-path>`.

## Lane status (hill)
- **Lane 0 Trust:** downhill — SERV-2178/2196/2395 diagnosed with file:line + live evidence; ready to implement on GO.
- **Lane 1 UX:** downhill (first pass) — answer-first wireframe on App kit, grounded in live sarreid/cci; awaiting customer feedback.
- **Lane 2 Computational:** downhill (spec) — True Topline + Concentration spec + AC + reproducible SQL; prototype figures live.
- **Lane 3 Inferential:** **PARKED** (EBR-772).

## Open bets
| Bet | Appetite | Status | Blocker |
|---|---|---|---|
| A — Territory & filter truth | Small (1-2w) | Diagnosed; implement on GO | Isolation |
| B — Design overlay wireframes | Small | Wireframe v1 done; needs feedback | Feedback session |
| C — Computational report v1 | Big | Spec + AC + live prototype | Bet on next cycle |
| D — Agentic (EBR-772) | — | PARKED | WIP rule + isolation |

## What to run next
1. **02-FIX (Agent), on GO** — implement SERV-2178 first (fail-closed leakage). One ticket per chat.
2. **03-UX (Agent)** — run the customer feedback session using the wireframe + question list; update AC. Parallel-OK with FIX (different lanes).
3. **04-INSIGHT (Agent)** — harden the read model (report_through_date clamp) for next-cycle Bet C. Parallel-OK (shares the two heroes).

## Do not run
- Any Rails implementation while isolation ON.
- EBR-772 / talk-to-data "just to explore."
- Two FIX tickets in one chat.

## Decisions needed from Kylor (max 3)
1. Confirm Bet A = Small batch and FIX+UX run in parallel this cycle (PROGRAM's flagged calls).
2. Single-account-risk threshold: default `top1_share >= 20%` OK, or set per-org?
3. Concentration list: mask customer names by default, or real names for internal comps?

---

# Review Card — FIX diagnosis (`FIX-diagnosis-territory-datefilter.md`)

## Verdict
PASS-WITH-FIXES

## Isolation check
Did they touch/apply Rails? **N** — diagnosis + proposed patches as markdown only. Isolation intact.

## Shape Up check
- [x] Problem is a baseline story (reps see all/none customers; range doesn't move totals)
- [x] Appetite implied (Bet A Small) — restated in PROGRAM
- [x] Elements at fix-proposal level, smallest-surface
- [x] Rabbit holes called out (layout coupling, shared partials, ETL lag)
- [x] No-gos listed (no reface/new metrics/LLM)
- [x] Not a grab-bag

## DDD check
- [x] Ubiquitous language correct (bill-to vs ship-to territory; warehouse projection vs live `territory_codes`)
- [x] Bounded context named (Portal Reporting / warehouse ACL, not catalog)
- [x] Metric spine correct (reconciles to invoiced net_amount)
- [x] ACL called out (warehouse bridges vs live OrgUser column; ETL as the ACL)

## Affinity / evidence check
- [x] Claims cite Jira + code file:line + KLL doc + live queries — not vibes
- [x] Mechanism sentences (empty-territory leakage; dual-path over-grant; substring gate)
- [x] Contradictions/edge cases called out (may_access_all_customer_sales_totals?; case-mismatch)

## Lane / WIP check
- [x] Stays Lane 0; no Lane 3 jump; parallel-safe with UX/INSIGHT

## Required fixes (owner = 02-FIX at implementation)
1. Split into one ticket per FIX chat when isolation lifts (starter rule) — file bundles 3 for PROGRAM convenience.
2. For SERV-2178 fail-closed change, confirm behavior for user types with `may_access_all_customer_sales_totals?` before flipping.
3. Verify SERV-2196 ship-to case-fix requires re-ETL to backfill bridges.

## Promote?
Ready for betting table / GO decision. Not yet implemented.

---

# Review Card — UX wireframe (`UX-brief-and-wireframe.md` + `sales-portal-cycle01-mockup.html`)

## Verdict
PASS

## Isolation check
Did they touch/apply Rails? **N** — mockup written to `design-system/app/` (allowed target), no `supercat_server`.

## Shape Up check
- [x] Problem baseline (classic portal dated; needs answer-first before Rails)
- [x] Appetite (Bet B Small)
- [x] Elements at fat-marker fidelity, answer-first, two heroes only
- [x] Rabbit holes (feature-flag/layout coupling; depends on filter correctness)
- [x] No-gos listed
- [x] Not a grab-bag ("Portal 2.0")

## DDD check
- [x] Ubiquitous language matches spine (invoiced topline; concentration at billing-entity grain)
- [x] Bounded context named (Sales Portal reporting, not catalog)
- [x] Metric spine correct (invoiced net_amount; provenance chip in UI)
- [x] ACL called out ("invoiced ledger, not warehouse dashboard rollup")

## Affinity / evidence check
- [x] Every figure traces to a live query (sarreid $16.03M / top1 30.0%; cci $71.14M / 6.1%)
- [x] Mechanism naming (single-account risk with the $4.8M exposure + cliff to #2)

## Craft check (UX)
- [x] Real density (sarreid/cci-shaped), not empty Tremor shell
- [x] App kit language (real `ds/tokens` + `.kc`/`.kdt`/`.kb`, `.kshell`), not marketing editorial
- [x] One job per view; answer-first for each hero; single crimson accent reserved for risk

## Lane / WIP check
- [x] Lane 1; no Omni-explore invented while trust is broken; shares heroes with INSIGHT

## Required fixes (owner = 03-UX)
1. Run the actual customer feedback session (questions provided) before treating as final.
2. Freeze overlay AC until PROGRAM/Orchestrator confirms the two heroes post-feedback.
3. Add an empty/low-confidence state (what shows when `Q-ECON-00 = NONE` or territory empty).

## Promote?
Ready for customer feedback. Internal-only until then.

---

# Review Card — INSIGHT spec (`INSIGHT-spec-topline-concentration.md`)

## Verdict
PASS

## Isolation check
Did they touch/apply Rails or Insightful pipeline code? **N** — spec + AC + read-only SQL only.

## Shape Up check
- [x] Problem baseline (owners/reps need heroes without Excel; portal doesn't surface them)
- [x] Appetite (Bet C Big)
- [x] Elements listed (two heroes, read model, provenance stamps)
- [x] Rabbit holes (warehouse vs invoiced ACL; rep-identity gating; bad-date clamp)
- [x] No-gos listed (Lane 3, margin/COGS, %-off-list leakage, attribution rate)

## DDD check
- [x] Metric spine correct: `SUM(portal_invoices.net_amount)`, clamped LTM, STRONG ceiling, $5M cap
- [x] Bounded context named (invoiced spine as computation authority; portal = presentation)
- [x] ACL called out (one spine, two presentations; label which spine the portal shows)
- [x] Customer grain correct (billing entity; parent roll-up suppressed)

## Affinity / evidence check
- [x] Reproducible SQL returns the cited live figures for sarreid + cci
- [x] Opposite-shape test pair (concentrated vs diversified) proves it reads real org shape

## Lane / WIP check
- [x] Computational only; EBR-772 explicitly parked; hard gaps (margin/AR) suppressed not guessed
- [x] Does not assume broken filters are fine — calls the Lane 0 dependency

## Required fixes (owner = 04-INSIGHT)
1. Switch prototype from `CURRENT_DATE`-anchored window to the `report_through_date` clamp before build.
2. Gate SERV-2388 per-rep on rep-identity Tier 2; ship `rep_number`-grain fallback for Tier 0/1 orgs.
3. Add `Q-ECON-00` preflight stamp emission to the read model contract.

## Promote?
Ready for the betting table as the Bet C pitch basis. Prototype figures internal-only (masked).

---

# Park decision — Bet D / EBR-772 (Lane 3)

**PARKED — no-go this cycle.** Rationale (WIP hard rule + spine §5 bet D):
- Talk-to-data / agentic anomaly layer is explicitly **downstream of a trusted computational surface**. Lane 0 trust (Bet A) is not yet even implemented, and Bet C is spec-stage.
- The spine's metric law makes an LLM layer premature: attribution/capture-rate claims require `FEED_COMPLETENESS = CORROBORATED`, which a single invoice feed never provides (STRONG ceiling). An NL layer on top of un-trusted totals would confidently narrate wrong numbers.
- **Revive criteria:** only after (1) Bet C ships and reconciles to invoiced truth on a live org, and (2) a feedback session validates the two heroes. Until then, no "just explore EBR-772" chats.

---

# Spine diff proposal (apply only on Kylor's `UPDATE SPINE`)
- **Bet A:** appetite resolved TBD -> **Small batch**; diagnosis complete (link `cycle-01-outputs/FIX-diagnosis-territory-datefilter.md`).
- **Bet B:** wireframe v1 delivered (`design-system/app/sales-portal-cycle01-mockup.html`); status uphill -> downhill pending feedback.
- **Bet C:** spec + AC + live prototype delivered; ready to bet next cycle.
- **New finding candidate F8:** "Concentration is org-specific and material — sarreid top-1 = 30.0% of invoiced (single-account risk) vs cci 6.1% (diversified); the report must read real org shape." Evidence: live 2026-07-16 (`portal_invoices`, orgs 1/161).
- **Jira note:** SERV-2382 absorbed into Hero 1; SERV-2388 gated on rep Tier 2; SERV-2425/2403/EBR-629 deferred; EBR-7 answered by net semantics (margin is a hard gap).
