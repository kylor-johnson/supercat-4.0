# Client-review HTML brief — Sales Analytics (cycle-04)

**Date:** 2026-07-24 · **Cycle:** 04 · **Isolation:** ON (this file specifies; it does not build)
**Companion:** `PRODUCT-BAR-AUDIT.md` (same folder) — the receipts this brief responds to
**Governs:** any HTML artifact placed in front of a paying customer or a prospect
**Does not govern:** `sales-portal-internal-demo.html` and `sales-portal-persona-ia-demo.html`, which stay internal and keep their teaching surfaces

**Authorizes nothing.** No Rails, no Jira, no GO. Building the artifact this brief describes requires Kylor to say so in that chat.

---

## 1. What a client review is for

A demo shows a client what we built. A **review** finds out where our acceptance criteria are wrong while it is still cheap to change them.

That difference sets everything below. The artifact is not a sales asset and not a progress report — it is an instrument for producing **AC deltas**. If a session ends with the client impressed and no AC changed, the session failed. If it ends with the client unconvinced and three ACs rewritten, it succeeded.

Position in the program (`05e` north star):

```
Bet A ships → prod → verified
        ↓
Client-grade artifact built to this brief
        ↓
Review sessions → AC deltas
        ↓
EBR→SERV packaged for CTO
```

---

## 2. Entry gate — true before a client sits down

Non-negotiable. Any unchecked box means the session is not scheduled.

- [ ] **Bet A verified in prod** on the review org — including `A1.2` (dashboard path on a dash-enabled user), currently open at `FILTER-TRUTH-AC.md:97`
- [ ] **SERV-2196 ship-to over-grant** either fixed or the review org confirmed zero-exposure. `sarreid` is 99.8% multi-territory and is disqualified as a territory-scoping review org until this is honest
- [ ] **One stamped dataset** generated and reconciling (§3)
- [ ] **Zero in-artifact disclaimers** — nothing on screen explains that part of the screen is not real (§5)
- [ ] **Masking verified** — no real ERP keys, no second client's data, no staff names (§6)
- [ ] **Every visible figure sourceable in under 30 seconds** by whoever runs the session

The last one is the practical test of all the others. If a client points at a number and asks "where does that come from," and the answer takes a minute or arrives as a hedge, the artifact was not ready.

---

## 3. The single-dataset rule

This is the core of the brief, because `PRODUCT-BAR-AUDIT.md` §3 traces every reconciliation failure to the same cause: three files holding hand-typed numbers.

**Rule: heroes are computed, never written.**

The artifact loads exactly one dataset — atomic rows, not pre-totalled summaries — and every figure on every surface is a function over those rows, evaluated in the page.

| Layer | Requirement |
|---|---|
| **Source** | One org, one `report_through_date`, generated from stamped SQL (`IR-v1-QUERIES.md` pattern). No figure enters the file by hand |
| **Grain** | Invoice-level, or month × customer × territory aggregates — fine enough that every hero in scope is derivable. Never store a total that is also displayed |
| **Derivation** | `SUM(net_amount)`, RTD-clamped, $5M single-row cap, `customer_bill_to_number` grain — one function, called by Dashboard, Invoices, Customers, and Reports alike |
| **Consequence** | Reports Monthly sums to Reports Summary *structurally*. `LT-RPT.2` parity stops being something we check and becomes something that cannot break |
| **Provenance** | Dataset header carries `{confidence, feed_completeness, total_business_source, report_through_date}` per `INSIGHT-IR-v1-AC` AC-5, rendered once as a plain line — not a badge on every tile |

This also de-risks the Rails build. The dataset shape is the read-model in `ENG-HANDOFF` §E.2 — so the review artifact becomes a working specification of the contract rather than a throwaway.

**Regeneration, not editing.** When numbers need to change, the dataset is regenerated from SQL. Nobody opens the HTML to adjust a figure. The moment that happens once, drift returns.

---

## 4. Rebuild or start new — recommendation

**Start new: `design-system/app/sales-portal-client-review-v1.html`. Leave both existing demos alone.**

Reasoning:

- The internal demo's value *is* the teaching surfaces. "What's broken," the Broken|Fixed switch, and the bug simulators explain the filter problem to internal audiences better than any document. Stripping them produces a worse internal asset and a still-compromised client one.
- The fork already failed once. `sales-portal-persona-ia-demo.html` is a ~220-line fork of the internal demo and has inherited its Reports contradiction. A third hand-maintained fork guarantees a third set of divergent numbers.
- A clean file can be built dataset-first (§3). Retrofitting the rule into 2,787 lines of literals means touching nearly every figure anyway.

**Consequence to accept:** three portal HTML files with three purposes — internal teaching (`internal-demo`), IA illustration (`persona-ia-demo`), client review (`client-review-v1`). Only the third is governed by this brief. The first two must never be sent to a client, and the persona demo specifically must not appear in the §8 sessions (`PRODUCT-BAR-AUDIT.md` §7.3).

---

## 5. Surfaces in scope for review v1

Four surfaces done completely beats seven done illustratively.

| Surface | In v1? | Why |
|---|---|---|
| **Dashboard** | **In** — as landing | It is the production default; the client will expect it. Its invoiced KPI must reconcile to Invoices and Reports. Not a probe target — it is org chrome, not the reconciling answer |
| **Invoices** | **In** — the proof surface | Bet A's home. Hero total moves with territory and date; export matches it. This is what the review is actually testing |
| **Customers** | **In** | Selected-range sales hero recomputing with date range (`LT-CUST.1`), fail-closed territory behaviour (`A1.4`) |
| **Reports → Summary** | **In** | Cheapest possible demonstration of `LT-RPT.2` parity once §3 holds |
| **Intelligence** | **Out — v2** | Gated on `C4` (cci + kll re-stamp, ❌ at `SPEC-GAP-CHECKLIST.md:59`). Showing C1/S1 before grade orgs are re-stamped repeats the exact error in `PRODUCT-BAR-AUDIT.md` §3 |
| **Settings hub** | **Out** | No GO. `AC-E4.4` forbids hub copy implying filter truth is fixed; safest compliance is absence |
| **What's broken** | **Out — permanently** | Non-shipping teaching surface (`DEMO-SURFACE-CONTRACT.md:20`). Never client-facing under any framing |
| **Persona switcher** | **Out** | Pre-loads the answer to `IA-RECOMMENDATION` §3.3 and renders `HIDE · not for you` at a paying user |

Reports → Product Details and Monthly may appear as tabs if and only if they derive from the same dataset. If they cannot, they are omitted rather than approximated.

---

## 6. No-gos (hard list)

Each traced to a receipt in the current demos so there is no ambiguity about what is being excluded.

| No-go | Receipt it comes from |
|---|---|
| Teaching surfaces in nav | `internal-demo:1158` `What's broken`; cross-link `:1231` |
| Bug simulators of any kind | `:1383`, `:1566` `Simulate today's filter bug`; `:1953–1954` Broken/Fixed |
| Wave badges, Delete buttons, flag names, ticket IDs | `:1870–1929`; static tree naming `enable_sales_portal` at `:1871–1877` |
| Org switcher exposing another client | `:1107–1113` (Sarreid ↔ Currey) |
| Staff names or internal identity | `:1165` `Kylor Johnson`; title `:6` `Internal Demo` |
| Contradictory live/mock chrome | `:1184` `Live · read-only` beside `:1186` `Cycle 03 · mockup-only` |
| Real ERP account or rep keys | `:1415–1417` `29925 / 32162 / 31098`; `cycle03-mockup:236–240` |
| Any on-screen disclaimer | `:1856`, `:1921`, `:1978` — the pattern itself, not these instances |
| Illustrative figures presented as answers | `cycle03-mockup:202` hero contradicting its own footnote at `:315` |
| Persona rank labels | `persona-ia-demo:2536–2586` `HIDE · not for you` |

**The disclaimer test.** If the artifact needs a label explaining that something on it isn't real, that something is removed instead. There is no acceptable phrasing.

---

## 7. Data and masking rules

**Whose data.** Show a client **their own**, live-stamped. It is the most persuasive version and it has no confidentiality problem. `wwjc` is the recommended pilot — it is the Bet A verify org, so the review can show a filter that now tells the truth on data the client recognises.

For prospects and for any session where the client's own feed is unavailable, generate a **masked composite** from the same pipeline. Never repurpose one client's stamped dataset for another client's session.

**Masking.** Applied at dataset generation, never in the HTML.

- Company names → deterministic pseudonyms, stable across sessions so a returning client sees consistent accounts
- Account keys → synthetic identifiers in a reserved range that cannot collide with real bill-to numbers
- Rep codes → synthetic, and never mapped back to a named person below `REP_IDENTITY_TIER` 2 (`R2.1`)
- The real → synthetic map lives outside `design-system/` and is not committed alongside the artifact

**Metric law, restated because the artifact must obey it:** sales / invoiced = `SUM(portal_invoices.net_amount)`, RTD-clamped, $5M cap, confidence ceiling **STRONG** and never FULL; quotes ≠ sales; backlog ≠ sales; export = UI; gross-only orgs show "returns not represented," never "$0 returns."

---

## 8. Session design

Recruiting frame, seats, and the five persona probes are specified in `PRODUCT-BAR-AUDIT.md` §7 — that study closes `IA-RECOMMENDATION-v0.md` §3. This section covers only how a session is run.

**Room.** The client (one Owner/VP and one lead rep, separately where possible), Kylor, and no one else. A second SuperCat attendee turns exploration into a presentation.

**Shape — 45 minutes:**

| Phase | Time | What happens |
|---|---|---|
| Cold open | 5 min | Artifact on screen at the landing surface. No walkthrough. *"It's Monday morning. Show me what you'd check."* |
| Follow the client | 20 min | They navigate. We answer questions and otherwise stay quiet. Every hesitation is data |
| Break the number | 10 min | Explicitly invite it: *"Try to catch it lying."* Change territory, change dates, export, add up a column |
| Probes | 10 min | Only the `PRODUCT-BAR-AUDIT.md` §7 questions that the session did not answer on its own |

**Never do:** explain a surface before they touch it; ask "do you like this"; show a roadmap; promise a date; open the internal demo to illustrate a point.

---

## 9. Pass / fail

**A session passes when all three hold:**

1. The client tried to break a number — territory, date range, export, or arithmetic — and could not.
2. At least one AC changed as a result. Zero deltas means we learned nothing or the client was too polite.
3. The client named, unprompted, which surface they would open on Monday.

**Failure signals — stop and fix before the next session:**

- We talked more than they did
- Any question was answered with "that part is illustrative"
- A number was challenged and could not be sourced within 30 seconds
- The client asked what a control does and the honest answer was "nothing yet"
- Two surfaces disagreed in front of them

The last one is fatal and means §3 was not actually implemented.

---

## 10. Feedback → AC

Deltas are only useful if they land somewhere specific.

| Step | Rule |
|---|---|
| Capture | Every delta written against a **named AC ID** (`LT-INV.2`, `A1.4`, `AC-3`…). Feedback that maps to no AC goes to a parking list, not into a pack |
| Threshold | Change an AC when **≥2 of 4 orgs** independently produce the same delta. One org is an anecdote — `sarreid` and `cci` differ structurally enough that n=1 misleads |
| Sequence | Update AC after all sessions, not between them. Rewriting mid-study contaminates the remaining sessions |
| Frozen | `FILTER-TRUTH-AC.md` body is not rewritten by review feedback — Bet A is built and verified against it. Deltas touching Bet A become new tickets |
| Output | One `AC-DELTAS-client-review.md` in this folder, then `SERV-DRAFTS-post-a.md` — paste-ready bodies for Kylor, never Jira writes |

---

## 11. Pre-schedule checklist

- [ ] `sales-portal-client-review-v1.html` exists and loads one dataset (§3)
- [ ] Reports Monthly sums to Reports Summary — verified by arithmetic, not by eye
- [ ] Dashboard KPI = Invoices hero = Reports total for the same scope
- [ ] Export equals the on-screen hero on Invoices and on Customers
- [ ] Territory change moves both hero and rows; empty territory keys fail closed to an empty book (`A1.4`)
- [ ] Every no-go in §6 confirmed absent — grep for `Wave`, `Delete`, `Simulate`, `broken`, `illustrative`, `mockup`, `masked`
- [ ] Masking map applied and stored outside the artifact
- [ ] Session runner can source every visible figure in under 30 seconds

---

## 12. Non-authorizations

- Does **not** authorize building the artifact — Kylor asks for that explicitly
- Does **not** modify `FILTER-TRUTH-AC.md`, the Bet A TRD, or SERV-2447 / 2448 / 2449
- Does **not** unlock any `ISOLATION OFF — GO`
- Does **not** edit the internal or persona demos
- Does **not** authorize Jira writes of any kind
- Does **not** open Intelligence, Settings, or the Admin Console Feature Usage project

---

*Cycle-04 client-review bar. Specification only. The artifact is built when Kylor says so, dataset-first, in a new file.*
