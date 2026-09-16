---
id: PROD-GAPS
title: Data-work backlog — split by owner
version: 0.1
status: draft
date: 2026-08-25
owner: Kylor Johnson
depends_on: [JTBD-REG, PROD-MAP]
---

# Data-work backlog

> **2026-09-15.** Job IDs in this backlog (JTBD-0xx) refer to the retired Aug 25 seat register. The live jobs are `JOB-*` in [`../analytics/jtbd-register.md`](../analytics/jtbd-register.md). The split below (we build it vs client must send it) still holds — especially the invoice feed for 71 orgs, which still blocks commercial-truth jobs.

**Two lists, because they have different owners.** List A is engineering work we control. List B is
client data we can only ask for. Conflating them has been making the roadmap look more tractable
than it is.

---

## A. WE BUILD IT — fields we could add, surfaces we could ship

| # | Gap | Jobs unblocked | Size | Note |
|---|---|---|---|---|
| A1 | **Product launch date / "new" flag** | JTBD-054 | **S** | One nullable date on `products`. Everything else in that job is already computable. Highest ratio of value to effort in this list |
| A2 | **Inventory snapshot age exposed to the UI** | JTBD-084, and every offline staleness rule in surface-mapping §5.3 | **S** | The import timestamp exists; it is simply never surfaced. Buyers are shown availability with no indication of how old it is |
| A3 | **Catalog completeness aggregation** | JTBD-053 | **S** | No new fields — images, prices and taxonomy all exist. Pure aggregation. Cheapest genuinely new job in the register |
| A4 | **Rep-activity surface ungated** | JTBD-032, JTBD-063 | **S** | `enable_rep_activity` is on for **7 of 257 orgs** `[MEASURED]`. Data exists; the switch is off |
| A5 | **Import failure alerting (push, not pull)** | JTBD-034 | **S** | File Import Status must be visited today. Note the trap: an `Error` row silently suppresses deletion of omitted records — a failure that looks like success |
| A6 | **Export/UI reconciliation** (EBR-91) | JTBD-035, and trust for all Portal jobs | **S** | Defect fix, not a build. Gates owner trust in everything downstream |
| A7 | **Order-failure reason codes** | JTBD-044 | **M** | Without it the job's metric cannot be computed at all, only inferred from support tickets |
| A8 | **Per-account baseline / seasonality store** | JTBD-014, JTBD-062 | **M** | Needed to define "fading" against an account's own history. SEG-01's lumpy project buying breaks a naive rule — the window must be account-aware |
| A9 | **View-as / scoped preview** | JTBD-024, JTBD-033 | **M** | Also the authority question in PER-02: should an external principal preview a manufacturer's user? |
| A10 | **Settings/enablement aggregation** | JTBD-033 | **M** | 134 toggles / 39 YAML flags / 6 layers [F10]. Aggregation, not new data |
| A11 | **`RepNumber` as a multi-value structure** | JTBD-012, JTBD-021, JTBD-022 | **L** | Spec §7.5: comma-separated rep numbers *"not reliably represented by the current scalar warehouse model."* EBR-180 / SERV-2178 |
| A12 | **Agency entity + migration** | all of PER-02 (021–024) | **L** | Spec'd in surface-mapping §4. The migration over **11,873 free-text `company_name` values** is the cost, not the schema |
| A13 | **Option-selection capture, normalised** | JTBD-052 | **L** | Capture varies by org today. Only matters where CPQ is deployed — **16 orgs** — but CPQ depth is the named competitive differentiator |
| A14 | **Inventory history retention** | JTBD-051 (sell-through) | **L** | Inventory is a snapshot replaced on every import. Any trend job needs retention that does not exist |

**Shape of list A: 6 × S, 4 × M, 4 × L.** The six S items are disproportionately valuable — A3, A4
and A6 in particular need no new data at all, only aggregation, a config flip, and a defect fix.

---

## B. CLIENT MUST SEND IT — gated on client data, no surface work fixes it

### B1. The invoice feed — the single biggest constraint in the register

**Present for 38 of 109 roster orgs** `[OBSERVED: stamped v4.0 §1.1]`. It degrades **13 of 31
jobs** — more than every engineering gap in list A combined.

**We cannot build our way out of this.** It is the client's ERP data, sent to us or not.

#### What the 13 jobs degrade *to* — the distinction that decides shippability

Asked directly, because it determines whether these ship to non-feed orgs or not:

**Group 1 — degrade to a usable order-based view (7 jobs). SHIPPABLE with a label.**

| JTBD | Without the feed | Shippable? |
|---|---|---|
| JTBD-011 know my book | Ordered value instead of invoiced net | **Yes**, labelled `ECAT_ONLY` |
| JTBD-014 account gone quiet | Order recency and order-value trend | **Yes** — decline detection works on orders |
| JTBD-041 CS account history | Orders only; invoice half missing | **Yes** — already how non-feed orgs use it |
| JTBD-051 what's selling | Ordered units by item | **Yes**, labelled |
| JTBD-062 accounts slipping | Order-based decline | **Yes**, labelled |
| JTBD-082 buyer order/invoice history | Orders only | **Yes** — already live |
| JTBD-086 buyer own performance | Ordered value trend | **Yes**, labelled |

**The mandatory label**, inherited verbatim: eCat is *"directionally unreliable as a size proxy —
it ran **0.22–3.10×** the invoiced truth across the brand_to_customer cohort (usually understating
2–4.5×)"*, and channel posture must be carried: `ALL_CHANNEL` → lead with invoiced net;
`ECAT_ONLY` → absolute eCat dollars only, **never** presented as the account's business.

**Group 2 — degrade to nothing. NOT SHIPPABLE without the feed (6 jobs).**

| JTBD | Why it fails outright |
|---|---|
| JTBD-015 / JTBD-043 "where is my order" | The answer *is* the invoice. No invoice, no shipped-status truth |
| JTBD-021 / JTBD-023 agency book & renewal value | A renewal argument on eCat volume alone is indefensible in the meeting it is meant to win — 0.22–3.10× error |
| JTBD-031 defensible topline | The job is *"reconciles to the ledger."* Order value does not reconcile to a ledger. Substituting it defeats the job |
| JTBD-061 owner's one true topline | Same, at the highest consequence. **STRONG, never FULL**; with no feed it is not even STRONG |

**The operative rule: where the job is "what really happened commercially," absence of the feed is
fatal. Where the job is "what is the trend / what is moving," orders are a legitimate labelled
proxy.** Seven of thirteen ship; six do not.

#### What to do about it

This reframes a data gap as a **commercial motion**: 71 of 109 roster orgs are running without an
invoice feed and are therefore locked out of six jobs entirely and getting labelled approximations
on seven more. Onboarding an invoice feed is the **highest-leverage single change** available for
those accounts — and it is a conversation, not a sprint.

### B2. Territory master — empty in 32 of 55 orgs [F11]

Degrades **7 jobs** (012, 021, 022, 024, 033, 062, 063). Client-maintained.

**Non-negotiable behaviour:** fail closed. Empty or zero territory keys → show *assigned only*, or
nothing. **Never** fall back to whole-org. This is the documented root trust failure (EBR-40) and
the fastest way to lose a rep permanently.

### B3. ERP ship status / carrier / tracking

Degrades **JTBD-015, JTBD-043**. Not in SuperCat at all, and not on any current integration path.
**Do not build a ship-date promise on data we do not hold** — show what we have with its
provenance, never infer a date.

---

## C. Job exists, data doesn't — kept, not deleted

Six jobs were cut in Phase 2 for absent data. **They are real jobs; the schema is what fails them.**
Recorded here so the absence stays visible.

| Job | Persona(s) | What's missing | Assessment |
|---|---|---|---|
| **Track my commission** | PER-01 rep | Commission rates, splits, payment status. **Nothing in SuperCat** | **The most significant of the six.** Commission is a rep's primary motivator — they are paid on what ships, not what they write. That the system a rep uses every day cannot tell them what they have earned is a finding about the schema, not about the job. Would need ERP payroll integration. **No current path** |
| **See margin / COGS** | PER-01, PER-05, PER-06 | Cost data of any kind | The most-wanted merchandising and exec metric in the industry. **Suppress, never estimate** — an estimated margin is worse than none. Would require client cost data we have no reason to expect |
| **Track AR / cash position** | PER-03, PER-06 | Payment/collection data | Principle 5: billed ≠ collected. Invoiced data must never imply collection, DSO or AR health |
| **Customer satisfaction** | PER-04 | CSAT of any kind | Lives in the helpdesk (HelpScout), not SuperCat. Arguably the right answer is *not* to bring it in |
| **Returns / RMA** | PER-04 | Return records | Systematically empty on gross-only orgs. Prior work bars *"$0 returns"* — must render as "returns not represented" |

**None of these is a roadmap item.** They are recorded so that when someone asks "why can't reps see
their commission," the answer is a documented schema gap with a known cost — not a shrug.

---

## D. Priority — what I would do first

Ordered by value ÷ effort, not by persona:

1. **A6 export/UI reconciliation** (S, defect) — gates trust in every Portal number.
2. **A4 ungate rep activity** (S, config) — 7 of 257 orgs; data already exists.
3. **A3 catalog completeness** (S) — no new fields, real weekly value to PER-05.
4. **A2 inventory snapshot age** (S) — one timestamp; unblocks every staleness rule.
5. **B1 invoice-feed onboarding** (commercial) — the largest constraint in the register, and it is a
   conversation, not a build.
6. **A1 product launch date** (S) — one nullable column unblocks JTBD-054 entirely.
7. **A8 per-account baseline** (M) — unblocks the two "fading account" jobs across rep and owner.

**Deliberately not in the first seven:** A12 agency entity (L, and PER-02 is not servable without
it — see surface-mapping §4), and the JTBD-011 iPad-EC build, which should wait until the
anatomy-vs-spec conflict is settled (surface-mapping §6) because the asymmetry favours resolving
before committing.
