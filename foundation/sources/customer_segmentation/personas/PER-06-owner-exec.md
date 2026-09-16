---
id: PER-06
title: Owner / exec
version: 0.1
status: draft
date: 2026-08-25
owner: Kylor Johnson
axis: persona
population: small; overlaps PER-03 in most client orgs
primary_surface: Insightful (deep) + a thin Sales Portal subset
depends_on: [PER-00]
jobs: [JTBD-061, JTBD-062, JTBD-063]
---

# PER-06 — Owner / exec

> **2026-09-15 — login seat, not the persona set.** Maps to **PG-HQ** in [`00-PERSONA-GROUPS.md`](00-PERSONA-GROUPS.md). Account-decline windows **do** differ by selling motion. JTBD-0xx IDs below are retired.

**Behavioural definition.** Owns the business, not the selling system. Consumes conclusions, not
screens. Logs in rarely or never — more often receives the number from someone who did.

**Kept narrowly, and the scope split is inherited, not re-decided.**
`PERSONA-ONE-PAGERS.md` locks it: the portal seat is **Owner/VP Sales consuming a thin C1/S1/team
subset**, and *"the deep CEO factory is Insightful, not the portal."* Whether an owner is a real
portal end-user at all — versus Owner/VP + Ops being the true pair — is their **Open Question §9.3**,
still open. **Not resolved here.**

**Three jobs only.** A persona that logs in rarely does not have six jobs, and inventing more would
be the failure mode this register is meant to avoid.

---

## JTBD-061 — Know the one true topline *(rank 1)*

**Job.** When I want to know how the business is doing, I want one number I can trust, so I'm not
waiting on someone to build it.

**Decision it changes.** Whether the owner acts on the business now or waits for the monthly pack —
and whether an analyst spends days assembling it.

**Trigger / cadence.** Monthly; ad hoc whenever something feels off.

**Primary metric.** **Invoiced net for the period, with a plain provenance line.** *Secondary:*
prior-year comparison; backlog.

**Data inputs.** `portal_invoices` (**38/109 orgs**); prior-year depth varies by feed start.

**Varies by segment?** **DOES NOT DIFFER.**

**Current state.** **Served by Insightful, thinly by the Portal.** Insightful 4.0 already runs CEO
reports off the same tables.

**Binding honesty gate — the one that matters most for this persona.** The topline must carry
**STRONG, never FULL** confidence: a single feed, completeness not independently corroborated. Never
"your total business is $X, complete." An owner acting on a topline that silently claims
completeness it does not have is the highest-consequence failure in this whole register.

⚠️ **Second-order trust dependency, inherited verbatim:** *"three things must be true before
Intelligence is trustworthy: territory scopes the book; export reconciles to UI; quotes never
counted as sales."* Until JTBD-012 and JTBD-035 are fixed, this job is untrustworthy at the root
regardless of how well it is presented.

---

## JTBD-062 — Know which accounts are quietly slipping *(rank 2)*

**Job.** When I look at the business, I want to see which accounts are fading and what they're worth,
so I intervene before it's a hole in the year.

**Decision it changes.** Where the owner personally spends relationship time — usually the highest-
leverage decision they make.

**Trigger / cadence.** Monthly; before market.

**Primary metric.** **Dollar value at risk from accounts in decline.** *Secondary:* count of fading
accounts; who owns each relationship.

**Data inputs.** Invoiced net by customer by period (**partial**); per-account baseline
(**does not exist**); customer → rep ownership (**unreliable, 32/55 orgs empty territory master**).

**Varies by segment?** **YES — SEG-01.** Luxury Specification carries the **highest median customer
count (4,418)** but the lowest median order count of the premium segments — project-driven, lumpy
buying `[MEASURED]`. "Fading" is much harder to define where a customer legitimately orders twice a
year, and a naive decline rule would fire constantly. **The rule needs a segment-aware window here
— one of only four genuine segment variations in the register.**

**Current state.** **Not served in the Portal;** exists as the S1 "accounts fading" concept
(EBR-198) in the Intelligence design.

---

## JTBD-063 — Know whether the sales organisation is working *(rank 3)*

**Job.** When I assess the sales operation, I want to know whether the team is active and covering
the territory, so I know if a problem is the market or us.

**Decision it changes.** Whether the response is hiring, coaching, restructuring territories, or
nothing.

**Trigger / cadence.** Quarterly.

**Primary metric.** **Share of licensed reps active in the last 30 days.** *Secondary:* territories
with no active rep; accounts with no contact in 90 days.

**Data inputs.** `last_ipad_login_at` / `last_ecat_online_login_at` (**yes**); territory coverage
(**unreliable**); `enable_rep_activity` (**7 of 257 orgs**).

**Varies by segment?** **DOES NOT DIFFER.**

**Current state.** **Data exists; surface is gated off almost everywhere.** Same underlying gap as
JTBD-032, viewed from a different altitude.

**Honesty gate.** Absence of SuperCat-submitted volume is **not** evidence of a failing sales team —
*"selling instrument ≠ order consummation."* An owner-facing activity view that implies otherwise
would cause real, wrong personnel decisions.

---

## Jobs considered and cut

| Candidate | Why cut |
|---|---|
| "See margin / profitability" | **Schema-absent.** Explicitly barred: *"anything margin/AR-shaped"* hidden by default |
| "Cash position / AR ageing" | Billed ≠ collected. Not our data |
| "Forecast the year" | Same objection as JTBD-031's cut: no forecast primitive, and PARTIAL-confidence inputs |
| "Compare us to competitors / industry" | Cross-client. Insights Layer under governance, not a client persona job |
| "Named rep leaderboard" | `RS-01` barred below `REP_IDENTITY_TIER` 2; never silently drop unmapped reps. An owner-facing leaderboard on incomplete identity is the most damaging possible version of that error |
