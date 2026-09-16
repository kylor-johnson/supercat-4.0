---
id: PER-03
title: VP Sales / sales ops (manager folds here)
version: 0.1
status: draft
date: 2026-08-25
owner: Kylor Johnson
axis: persona
population: 2365 internal admin records; 377 iPad-active, 141 eOL-active (Postgres, 2026-08-25)
primary_surface: Sales Portal + Admin Console
depends_on: [PER-00]
jobs: [JTBD-031, JTBD-032, JTBD-033, JTBD-034, JTBD-035]
---

# PER-03 — VP Sales / sales ops

> **2026-09-15 — login seat, not the persona set.** Maps to **PG-HQ** in [`00-PERSONA-GROUPS.md`](00-PERSONA-GROUPS.md). JTBD-0xx IDs below are retired; use `JOB-HQ-*` in [`analytics/jtbd-register.md`](analytics/jtbd-register.md).

**Behavioural definition.** Owns the selling system rather than a book. Decides who sees what, keeps
the numbers reconcilable, and answers for team performance upward. Combines the Owner/VP seat from
`PERSONA-ONE-PAGERS.md` Persona 2 with the ops half of Persona 3 — one person in most of our
clients, given a median of ~37–44 employees `[OBSERVED: Lens 1]`.

**Manager folds here** as an oversight-scoped variant — a permission tier, not a separate context.

**Documented trust failures** (both inherited, both real): **config opacity** — access rules hidden
across *134 toggles / 39 YAML flags / 6 layers* with no admin surface [F10]; and **reconciliation** —
export ≠ displayed total [EBR-91], which makes this persona the one who fields "the CSV doesn't
match" and rebuilds it by hand.

**Ranked jobs.** 5.

---

## JTBD-031 — Get one topline I can defend *(rank 1)*

**Job.** When I report upward, I want a total that reconciles to the ledger, so I'm not defending a
number I can't source.

**Decision it changes.** What gets reported to the owner/board, and whether the product is trusted
as the system of record for performance.

**Trigger / cadence.** Monthly close; weekly in-season.

**Primary metric.** **Invoiced net for the period, org-wide.** *Secondary:* prior-year comparison;
open order backlog.

**Data inputs.**

| Input | Source system | Exists today? |
|---|---|---|
| Invoiced net, line-derived | `portal_invoices` | **Partial — 38/109 orgs** |
| Prior-year same period | `portal_invoices` | Depends on feed depth |
| Backlog (order + invoice line calc) | `orders` + `portal_invoices` | Yes — spec §6.2 |

**Varies by segment?** **DOES NOT DIFFER.**

**Current state.** **Served, with a hard honesty ceiling.** The Dashboard invoiced KPI exists — but
spec §4.5 warns *"Dashboard is a summary surface, not a promise that every panel uses one measure"*;
Top Customers and Top Products use **ordered** amount while the invoice KPI uses **invoiced**, and
*"do not necessarily reconcile."* Every topline must carry the single-feed caveat: **STRONG, never
FULL**. No "your total business is $X, complete."

⚠️ **Anatomy/spec conflict bites here.** This is the one persona both documents agree the Portal
serves. Where they disagree is whether it serves *only* this persona — which decides whether rep
scoping is a first-class Portal concern or an iPad concern. **Unresolved.**

---

## JTBD-032 — Know the team is actually using the system *(rank 2)*

**Job.** When I assess whether the investment is working, I want to see who is logging in and writing
orders, so I intervene on adoption before renewal.

**Decision it changes.** Who gets coached, and whether seats are renewed or cut.

**Trigger / cadence.** Monthly.

**Primary metric.** **Count of reps active in the last 30 days against seats licensed.**
*Secondary:* orders written per active rep; days since last sync per rep.

**Data inputs.**

| Input | Source system | Exists today? |
|---|---|---|
| `last_ipad_login_at`, `last_ecat_online_login_at` | `org_users` | **Yes** |
| Orders per user | `orders` | Yes |
| Seats licensed | subscription plan | Yes |
| `enable_rep_activity` | `organizations` | **Yes but enabled for only 7 of 257 orgs** `[MEASURED]` |

**Varies by segment?** **DOES NOT DIFFER.**

**Current state.** **Data exists; the surface almost never does.** `enable_rep_activity` is on for
**7 orgs**. This is a cheap, high-value job that is gated off almost everywhere — the clearest
quick win in this register.

**Honesty gate.** Low SuperCat-submitted volume is **not** proof of failed adoption — *"selling
instrument ≠ order consummation"*. Narrate activity, not implied failure.

---

## JTBD-033 — Answer "why can't this user see their book" *(rank 3)*

**Job.** When a rep says the numbers are wrong or the portal is off, I want to see what governs their
access, so I fix it without filing a SuperCat ticket.

**Decision it changes.** Whether the fix takes minutes in-house or days through support.

**Trigger / cadence.** Reactive; continuous during onboarding and market season.

**Primary metric.** **Access issues resolved in-house without a SuperCat ticket.** *Secondary:*
median time-to-resolution.

**Data inputs.** Territory assignment; `customer_synching` (962 All / 645 Associated / 327 None);
`access_all_customer_sales_totals`; user type permissions; the org/feature gates. All exist —
**scattered across 134 toggles, 39 YAML flags, 6 layers, with no single admin surface** [F10].

**Varies by segment?** **DOES NOT DIFFER.**

**Current state.** **Not served.** This is the Settings-hub enablement decision tree (Bet E, AC-E1).
The data is all present; what is missing is one place to read it.

---

## JTBD-034 — Know the nightly data actually landed *(rank 4)*

**Job.** When imports run overnight, I want to know if something failed, so I find out before a rep
or a dealer does.

**Decision it changes.** Whether the day starts with a fix or with a complaint.

**Trigger / cadence.** Daily, morning.

**Primary metric.** **Count of import jobs that failed or partially failed in the last 24 hours.**
*Secondary:* rows rejected per file; hours since last successful inventory import.

**Data inputs.** Import event/status records — exist, surfaced via Admin Console **File Import
Status**. Warehouse ETL delay is documented (spec §5.3).

**Varies by segment?** **YES — SEG-04.** Volume Distribution runs **median 4,498 products and
median order count 5,759** `[MEASURED]`; import volume and failure blast radius are materially
larger, and a partial failure is correspondingly harder to spot by eye.

**Current state.** **Served reactively, not proactively.** File Import Status must be *visited*;
nothing pushes. Note: a blue-link timestamp means problems, and an `Error` row silently suppresses
deletion of omitted records — a failure mode that looks like success.

**This is the job that absorbs the dropped IT/integrations persona.** It is the only
analytics-shaped integration job, and it belongs to whoever fields the consequence.

---

## JTBD-035 — Make the export match the screen *(rank 5)*

**Job.** When I export for a board pack or a rep, I want the file to equal what was on screen for the
same filters, so I'm not reconciling two versions of our own data.

**Decision it changes.** Whether the product's output is usable directly — or whether every number
gets rebuilt in Excel, which then becomes the real system of record.

**Trigger / cadence.** Monthly close; ad hoc.

**Primary metric.** **Export-to-UI reconciliation rate at identical filters (target 100%).**
*Secondary:* count of exports followed by a manual correction.

**Data inputs.** Same query behind both paths — spec §12 defines the CSV export contract.

**Varies by segment?** **DOES NOT DIFFER.**

**Current state.** **Served badly — EBR-91.** Export/period drift is documented and compounds the
territory failure in JTBD-012. This is a correctness defect more than a new build.

---

## Jobs considered and cut

| Candidate | Why cut |
|---|---|
| "Forecast next quarter" | No forecast primitive exists, and building one on a feed present for 38/109 orgs would inherit PARTIAL confidence at best. Would produce a confident-looking number the data cannot support |
| "See margin by rep or account" | **Schema-absent.** No COGS. Suppress, never estimate |
| "Track AR / who owes us" | Billed ≠ collected (principle 5). Invoiced data cannot imply collection, DSO, or AR health |
| "Run a custom report builder" | The Portal is *"not a generic BI builder"* `[OBSERVED: spec §3]`. Users work in business objects. A builder would be a different product |
