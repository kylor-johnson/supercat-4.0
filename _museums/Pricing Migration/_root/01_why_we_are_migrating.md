# 01 — Why We Are Migrating

> **Last updated**: 2026-05-22
> **Owner**: CEO
> **Primary sources**: `_reference/2026-05-20__execution_plan_v3.3.md` §I, §IV, §IX; foundation `03_how_we_make_money.md` (inlined excerpts in this doc — see §2 and §4)
> **What this doc owns**: The migration thesis. The 5 structural problems being solved. The 4 operating principles (empathetic in communication / fast on notice / firm on architecture / artifacts over meetings). The success metrics (ACV uplift; ≤6 logo churn; ≤$3K/mo MRR churn). The definition of "done." The inlined foundation/exec-plan excerpts that operators and agents need without leaving this folder.
> **What this doc DOES NOT own**: Voice/tone (`_root/04`); driver framing (`_root/05`); segment/format mapping (`_root/02` + `_root/06`); data fields (`_root/07`); quality checks (`_root/08`).

---

## 1. The thesis

Years of custom deals, one-off discounts, and grandfathered rates have spread the book from **56% below book to 42% above book** for equivalent value. That is not a handful of exceptions — it is the structural norm. The 2026 refresh exists to convert that asymmetry into a system. The migration's purpose is threefold: **establish a defensible price card** that scales with how customers actually use the product; **correct legacy inequity systematically**, account by account, rather than tolerating it as the cost of growth; and **preserve the relationships that justify the embedded position** SuperCat occupies in each customer's workflow. This is internal copy. It does not hedge. It does not promise pricing won't move again. It states the case so every downstream artifact can speak from a shared spine.

---

## 2. The five structural problems being solved

These five problems are the operative diagnosis. They are stamped in foundation/03 (decision D-000a, 2026-01-28) and inlined here so any agent or operator working in this folder has them without leaving the migration directory.

1. **Per-user value metric is poorly executed.** The metric is right — value scales with selling teams — but the 25-user included base doesn't map to actual usage patterns, there is no volume incentive (the 26th user costs the same as the 200th), and arrears billing creates unpredictable customer bills.

2. **Per-module pricing has no expansion gravity.** Every module is $295–$395 with no tier logic, no bundle pricing, and no aspirational upgrade path. Expansion is event-driven (a customer needs a feature) rather than aspiration-driven (a customer wants the next tier).

3. **Legacy pricing creates structural inequity.** Years of grandfathered rates and one-off discounts have spread the book from **56% below book to 42% above book** for equivalent value. This is not a handful of exceptions — it is the structural norm. Custom iPad bases as low as $350 (vs. $725 book), discounted user rates ($15–$22 vs. $25 book), bundled or free modules, and up to 100 provided users (vs. 25 standard) are all in active accounts today.

4. **Implementation fees are front-loaded and disconnected from data readiness.** Fixed upfront fees apply regardless of whether a customer's data is pristine or requires extensive cleaning. Simple implementations subsidize complex ones; SuperCat almost certainly undercharges data-heavy implementations.

5. **Support is unmonetized and uniform.** No tiered SLAs, no premium pathway. High-touch accounts consume disproportionate CS resources with no revenue offset.

The migration is the operational response to these five problems. The remaining sections of this doc describe what "response" means.

---

## 3. The four operating principles

The following four principles are quoted verbatim from `_reference/2026-05-20__execution_plan_v3.3.md` §I. Every voice rule in `_root/04`, every driver framing in `_root/05`, and every format choice in `_root/06` traces back to one of these four. Inlining them here makes that traceability legible.

1. **Empathetic in communication, fast on notice, firm on architecture.** Flexible on timing, billing mechanics, user cleanup, and multi-brand consolidation. Not flexible on recreating bespoke legacy pricing.

2. **Migration starts when compliant written notice is received.** The 60-day window is simultaneously legal requirement, customer adjustment period, and commercial transition. Every day without notice is a day of delayed revenue.

3. **Architecture-forward. Don't hide behind "standardization."** Standardization is true — but it's not why a customer accepts a price increase. They accept it because SuperCat is embedded in their workflow and replacement costs more than normalization. Lead with what the customer gets. Never lead with the percentage.

4. **Artifacts over meetings.** With a 2-person CS team (CEO + Kylor), bespoke communication artifacts are the primary vehicle for substance delivery. Meetings are reserved for entity parents and Strategic accounts. A data-rich value justification delivered alongside notice communicates more substance than a 20-minute call — and scales.

### How these show up in communications

Each principle has one concrete consequence in the comms system, owned in detail by the docs named in parentheses. Empathetic in communication: the per-customer brief is the artifact, not a generic email blast — composition rules live in `_root/04`. Fast on notice: every communication artifact is engineered to clear the 60-day clock as soon as it is paired with the notice — the routing that enforces this lives in `_root/06`. Architecture-forward: drivers are framed in terms of what the new architecture delivers, not in terms of percentage change — the driver taxonomy lives in `_root/05`. Artifacts over meetings: format selection routes the largest segments to artifact-led delivery and reserves meetings for Entity parents and Strategic accounts — the routing logic lives in `_root/06`.

---

## 4. Success metrics and the definition of "done"

The migration has one primary metric, two guardrails, and a small set of operational thresholds. They are pulled from `_reference/2026-05-20__execution_plan_v3.3.md` §IX and from the stamped foundation decision D-000b.

- **Primary metric — ACV uplift.** ACV (Average Contract Value) is the success metric for the refresh, stamped in foundation/03 as decision D-000b (2026-01-28). The migration model targets +$32,653/mo in MRR uplift across the migration-pending book; the realized fraction of that target is the operative number.
- **Migration-induced logo churn cap**: ≤6 accounts.
- **Migration-induced MRR churn cap**: ≤$3,000/mo.
- **Entity-conversation feedback synthesized before July cohort launch.** Entity conversations are the high-fidelity validation of the comm system; their feedback must be synthesized and applied to Executive and Pre-Engagement artifacts before those go out.
- **Strategic account resolution.** Each Strategic account is either migrated, on an approved transition path, or has its churn documented as intentional. None left in indefinite limbo.
- **Annual-account notice timing**: 100% of in-horizon renewals noticed ≥90 days before renewal date.

Two further numbers — **gross retention** and **win rate** — are watched but not formally instrumented. Per foundation/03 (D-000b), they are check-engine lights. If accounts churn citing pricing, pause and reassess pacing. If new-business close rates deteriorate, the issue is messaging or calibration, not architecture.

### Definition of "done"

The migration is complete when the 107-account migration-pending book is on the new price card (or has been intentionally churned within the caps above), the per-account corrections to the v6.2 dataset have been incorporated into the canonical record, and the June, July, and Deferred cohorts have all executed their last comm action per `migration_comm_tiers_2026-05-19.csv`. "Done" is not a date; it is the state in which every account in the book has either accepted the new architecture, exited it deliberately, or sits on a stamped, time-bounded transition path under CEO authority.

---

## 5. What "communication" means inside this migration

This section establishes the philosophical position that the rest of the `_root/` stack operationalizes. The four points below are the position; the operational rules live where they are owned.

- **Every comm artifact is a per-account artifact.** There is no blast. The artifact is engineered to that customer's pricing, drivers, health, and tenure. The migration is the moment SuperCat earns the right to its embedded position by communicating with intent and craft, not the moment it merely informs.
- **Voice is always opening-relationship-before-price, never the inverse.** Tone is professional, declarative, empathetic on impact, firm on architecture — not friendly-personal, not legalistic-cold.
- **The artifact is the case.** A data-rich value justification, paired with the notice, is the substance the customer evaluates. Meetings are reserved for the segments where they add information the artifact cannot carry alone.
- **The 60-day notice window is non-negotiable architecture; the framing inside the window is fully flexible per-customer.** The clock is a contract; the words inside it are a craft decision per account.

How that philosophy becomes operational rules lives in `_root/04` (voice), `_root/05` (drivers), `_root/06` (format routing), and `_root/08` (quality bar).
