---
id: PER-02
title: Rep agency principal
version: 0.1
status: draft
date: 2026-08-25
owner: Kylor Johnson
axis: persona
population: 617 iPad-active in rep-group-flagged user types across 39 orgs (Postgres, 2026-08-25)
primary_surface: Sales Portal (multi-rep view) — does not exist today
depends_on: [PER-00]
jobs: [JTBD-021, JTBD-022, JTBD-023, JTBD-024]
---

# PER-02 — Rep agency principal

> **2026-09-15 — login seat, not the persona set.** Still unservable (no agency entity). Not a persona group. Canonical set: [`00-PERSONA-GROUPS.md`](00-PERSONA-GROUPS.md). JTBD-0xx IDs below are retired.

**Behavioural definition.** Runs an independent rep agency carrying several manufacturers' lines,
with sub-reps under them. Their unit of concern is **the agency's book across a manufacturer**, not
one territory and not the manufacturer's whole org. They are not employed by the manufacturer, and
the manufacturer is one of several principals they represent.

**Evidence this persona is real** `[MEASURED 2026-08-25]`:

- `user_types.primary_rep_group` is set on **142 of 1,980 user types**, used by **39 orgs**,
  covering **3,821 users**, of whom **617 are iPad-active**.
- Internal (non-buyer) users carry **11,873 distinct `company_name` values** — reps identifying
  their own agency, not the manufacturer.

**The structural problem, stated once because it governs all four jobs.** There is **no agency
entity in the schema**. There is a boolean on a user type and a free-text `company_name` on a user
record. Nothing joins a principal to their sub-reps, and nothing joins one agency across the several
manufacturers it represents. **Every job below is capped by that gap** — see
[`product/data-gaps.md`](product/data-gaps.md).

**Ranked jobs.** 4.

---

## JTBD-021 — See the agency's whole book with one manufacturer *(rank 1)*

**Job.** When I review how my agency is performing for a line I carry, I want the agency's total
across all my sub-reps' territories, so I can manage the relationship as one book.

**Decision it changes.** Whether the agency keeps, grows, or drops the line — and what the principal
argues for at the annual review.

**Trigger / cadence.** Monthly; sharply at contract review and market week.

**Primary metric.** **Agency-total invoiced net for this manufacturer, current period versus prior
year.** *Secondary:* share of the manufacturer's territory coverage the agency holds; sub-rep
contribution split.

**Data inputs.**

| Input | Source system | Exists today? |
|---|---|---|
| Invoiced net by customer by period | `portal_invoices` | **Partial — 38/109 orgs** |
| Sub-rep → principal relationship | — | **DOES NOT EXIST** |
| Agency identity as an entity | — | **DOES NOT EXIST** — only `org_users.company_name` free text |
| Territory → rep assignment | Postgres | Yes, unreliable (32/55 empty) |

**Varies by segment?** **YES — SEG-02.** Premium Trade Brand runs the **highest median territory
count (41)** `[MEASURED]`, so agency-level aggregation matters most there. In a SEG-03 org with a
median of 29 territories and a smaller dealer base, agency ≈ territory and the job collapses into
JTBD-012.

**Current state.** **Not served at all.** Requires the multi-territory rollup that spec §7.5 and
EBR-180 identify as *"a separate, large implementation class"* — comma-separated rep numbers are
*"not reliably represented by the current scalar warehouse model."*

⚠️ **Anatomy/spec conflict bites here.** An agency principal is neither "leadership" nor "a rep."
Whichever way the conflict resolves, this persona sits outside it. **Unresolved.**

---

## JTBD-022 — See which sub-rep is carrying the line and which is not *(rank 2)*

**Job.** When I allocate my agency's effort, I want to see which of my reps are moving this line, so
I coach or reassign.

**Decision it changes.** Territory reassignment and where the principal spends coaching time.

**Trigger / cadence.** Monthly; quarterly at minimum.

**Primary metric.** **Invoiced net per sub-rep, current period.** *Secondary:* active accounts per
sub-rep; accounts with no order in 90 days per sub-rep.

**Data inputs.** Same as JTBD-021, plus per-rep attribution.

⚠️ **Blocked by an identity rule, not just a schema gap.** Named rep→revenue attribution (`RS-01`)
is barred below `REP_IDENTITY_TIER` 2, and unmapped reps must **never be silently dropped** —
dropping them fabricates a leaderboard (principle 6). Where identity is incomplete this job must
**degrade the grain or suppress**, not approximate.

**Varies by segment?** **DOES NOT DIFFER.**

**Current state.** **Not served.** Nothing in production attributes revenue to a named rep for an
external principal.

---

## JTBD-023 — Prove the agency's value at contract renewal *(rank 3)*

**Job.** When my agreement with a manufacturer comes up, I want a defensible record of what my
agency delivered, so the conversation is about evidence rather than impressions.

**Decision it changes.** The commercial terms of the agency agreement — and whether the manufacturer
retains the agency.

**Trigger / cadence.** Annual, plus ad hoc when the relationship is under pressure.

**Primary metric.** **Agency invoiced net, multi-year trend.** *Secondary:* new accounts opened;
territory penetration change.

**Data inputs.**

| Input | Source system | Exists today? |
|---|---|---|
| Multi-year invoiced history | `portal_invoices` | **Partial** — and depth varies by feed start date |
| New-account attribution | — | **DOES NOT EXIST** — no "opened by" on a customer record |
| Agency entity | — | **DOES NOT EXIST** |

**Varies by segment?** **DOES NOT DIFFER.**

**Current state.** **Not served.** Reps build this by hand today, if at all.

**Honest caveat this job must carry:** eCat is *"directionally unreliable as a size proxy — it ran
0.22–3.10× the invoiced truth"* `[OBSERVED: CEO_SYSTEM_CONTEXT]`. An agency-value claim built on
eCat order volume alone would be indefensible in the very meeting it is meant to win.

---

## JTBD-024 — Show a sub-rep exactly what they will see *(rank 4)*

**Job.** When I onboard or troubleshoot a sub-rep, I want to see their scoped view, so I fix access
without filing a ticket.

**Decision it changes.** Whether the principal resolves it themselves or escalates to the
manufacturer's ops team (and from there to SuperCat).

**Trigger / cadence.** On onboarding; reactively when a rep reports a problem.

**Primary metric.** **Access issues resolved by the principal without escalation.** *Secondary:*
time-to-resolution.

**Data inputs.** User → territory assignment; user type permissions; `customer_synching`
(962 All / 645 Associated / 327 None) — all exist; **no impersonation/preview mechanism exists**.

**Varies by segment?** **DOES NOT DIFFER.**

**Current state.** **Not served, and note the authority problem.** This is the "woodshed / what the
rep sees" job that `PERSONA-ONE-PAGERS.md` folded into the manager variant. For an **external**
principal it also raises a question the prior work did not face: should a third party be able to
preview a manufacturer's user's view at all? **Product decision, not a data gap.**

---

## Jobs considered and cut

| Candidate | Why cut |
|---|---|
| "Compare my performance across the manufacturers I carry" | Cross-manufacturer data does not exist in any single SuperCat instance, and building it would mean joining data across clients. **Excluded on principle, not just feasibility** |
| "Manage commission splits between sub-reps" | Commission data is absent from SuperCat entirely |
| "Recruit and onboard new sub-reps" | No decision in the product changes. Belongs to the manufacturer's ops (PER-03) |
