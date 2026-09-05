# Sales Portal — Decision Brief: Bet A (Filter Truth)

> **The ask:** Approve starting **Bet A — Filter Truth** with locked, validated scope.
>
> **Keep:** EBR-40 + EBR-91 (+ EBR-212 paired) · **Park:** EBR-87 · **Close:** EBR-7 (doctrine)
>
> **GO phrase:** `ISOLATION OFF — GO on EBR-40`
>
> This approves pouring the trust foundation first. It is **not** approval of Intelligence, the Settings hub, an LLM layer, a Dashboard redesign, or the broader roadmap.

| | |
| --- | --- |
| **Owner** | Kylor |
| **Date** | 2026-07-20 · **Updated** 2026-07-21 |
| **Status** | Mockup only · Isolation ON · **validation complete** · nothing shipped |
| **Purpose** | GO decision on validated scope — not a UI demo |

---

## Response to leadership feedback (2026-07-20)

Content and sequence were right — trust before Intelligence. Three asks from the CTO are now closed as follows:

### 1. Define / verify assumptions (old EBRs still real?)

| Ticket | Still open in Jira? | Still valid in production? | Disposition |
| --- | --- | --- | --- |
| **EBR-40** | Yes (Triaging) | **Yes** | **Keep** core GO |
| **EBR-212** | Yes (In Progress, stalled) | **Partial** (same mechanism; wwjc multi-terr reps lack dashboard) | **Keep paired** with 40 |
| **EBR-91** | Yes (Triaging; ticket underdefined) | **Yes — period drift** | **Keep** + rewrite AC |
| **EBR-87** | Yes (Triaging) | **No as universal** | **Park** |
| **EBR-7** | Yes (Prod Council Denied 2022) | Doctrine already answered by `net_amount` | **Close, don’t rebuild** |

**Method:** production Postgres + live Rails code (2026-07-21). Steps to reproduce live in `BUG-VALIDATION-PACK.md`. Optional 5‑min UI: log in as `cmallon` → Invoices → Current YTD → select `105:1 Gigi Lane` → confirm ~710 invoices / ~$777k.

**EBR-40 proof (wwjc trust flagship):** `cmallon` YTD bill-to book **1,404 / $1.46M** → T1 `105:1 Gigi Lane` **710 / $777k**. Kalco 2021 Ferguson/`0016` URLs are stale (bill-to is `0999` today). Ship-to bridge case bug still in code.

### 2. “Quotes appearing as sales/orders” (CTO skepticism)

**Parked from Bet A GO.** Live quote statuses only on `cci` (`Q`) and `ril` (`Quote`); both already exclude those from backlog via org config. Kalco has **zero** quote portal orders today. Invoiced “sales” is `portal_invoices.net_amount` — quotes don’t land there. Metric-law copy stays (“quotes ≠ sales”); no dedicated build. Optional CS follow-up only if Orders-list UX confuses `cci`/`ril` — not a universal customer issue.

### 3. Visuals are distractors / separate IA track

Agreed. Dashboard / Intelligence / Settings mocks are **off the default path** for this decision. Persona identification + information-architecture priority + customer A/B of content/grouping/aggregation/annotation is a **separate Track 2** (`IA-PERSONA-TRACK.md`) — it does **not** unlock this GO.

---

## Prereads & documents

### Public URLs (optional only)

| Demo | URL | Use |
| --- | --- | --- |
| **Bet A pitch demo** | https://supercat-sales-portal-demos.pages.dev/app/sales-portal-bet-a-pitch-demo | Optional click-through — Invoices first |
| **Internal demo** (full Cycle 03) | https://supercat-sales-portal-demos.pages.dev/app/sales-portal-internal-demo | **Off default path** — program preview only |

### Spec pack (disk)

| Document | What it covers |
| --- | --- |
| `BUG-VALIDATION-PACK.md` | Filled repro results + rollup |
| `DRAFT-CTO-REPLY-validation.md` | Paste-ready readout reply |
| `CTO-FEEDBACK-2026-07-20.md` | Feedback → actions |
| `TRD-Bet-A-filter-truth.md` | Bet A decision record |
| `FILTER-TRUTH-AC.md` | AC-A1…A4 (A2 rewritten; A3 parked) |
| `IA-PERSONA-TRACK.md` | Track 2 — persona / IA / content A/B (not this GO) |
| `PROGRAM-ROADMAP-cycle03.md` | What comes after Bet A (context) |
| `EBR-AFFINITY-PORTAL.md` | Full EBR routing |

---

## Summary

Reps don’t trust the portal’s numbers, so they rebuild them in Excel. **Bet A** (validated) fixes the foundation:

1. Territory filters limit both the list **and** the totals.
2. Customers selected-range total and export share one period (period drift fixed).

~~3. Quotes never counted as sales (universal build)~~ — **parked** after validation.

Everything else — Intelligence, modern UX, self-serve settings — only pays off once the numbers are trustworthy. **No code until an explicit GO.**

---

## The problem today (validated)

| What a rep does | What breaks | Ticket(s) | Validated |
| --- | --- | --- | --- |
| Picks a territory | Sees the wrong / untrusted book | EBR-40, EBR-212 | **Still real** / partial dash |
| Uses Customers date + export | Spreadsheet period ≠ on-screen | EBR-91 | **Still real** (period drift) |
| Worries quotes inflate “sales” | Not universal; config already handles the two orgs with quotes | EBR-87 | **Parked** |

---

## What Bet A ships

**Appetite:** small, fixed-time batch with variable scope. Trust fix — not a territory data-model rewrite, not a Dashboard redesign.

| Outcome | Detail |
| --- | --- |
| Territory limits list **and** total | Selecting a territory recomputes rows and every total to that book |
| Customers period + export reconcile | Same selected range in UI and CSV (EBR-91 / SERV-2395) |
| One invoiced spine | Every “sales” total = invoiced net |
| Answer-first list tabs | May ride later — **not** the GO proof story (Track 2) |

**Definition of done:** on **wwjc**, territory scopes invoice list + totals; Customers selected-range and export agree; every sales total equals invoiced net.

**Explicitly out of scope for this GO:** multi-territory rewrite (EBR-180) · LLM · Dashboard / Intelligence / Settings as this decision · dedicated EBR-87 build · shipping “What’s broken” as permanent product nav · verifying territory truth on sarreid.

---

## Metric definition (one spine)

> **Revenue / sales / invoiced = SUM of `portal_invoices.net_amount`**, clamped to the report-through date, with a $5M single-row cap and a STRONG confidence ceiling.

| Rule | Detail |
| --- | --- |
| Export / period = UI | EBR-91 (AC rewritten) |
| Quotes ≠ sales | Metric-law copy only — EBR-87 **parked** as build |
| Backlog ≠ sales | Open orders labeled backlog, never sales |
| EBR-7 (discounts) | Already answered by `net_amount` — close, don’t rebuild |

---

## Two tracks (per CTO)

| Track | Focus | Unlocks GO? |
| --- | --- | --- |
| **1 — Trust** | Territory + period/export truth (this brief) | **Yes** |
| **2 — Persona / IA** | Personas → IA priority → customer content A/B | **No** |

---

## Open decisions

1. **GO on Bet A** — phrase `ISOLATION OFF — GO on EBR-40` (scope locked above).
2. **Trust org** — confirm **wwjc** (recommended). Zero-exposure is an *alternate*, not a synonym for wwjc.
3. **Customers date filter** — in this bet (recommended; it *is* the EBR-91 fix) or fast-follow?
4. **Settings Wave 0** — rides with Bet A this cycle, or waits?

---

## Bottom line

Sequence unchanged: **make the numbers trustworthy → make them legible → add Intelligence.**

Assumptions were defined and verified. Quotes-as-sales is not a universal Bet A build. Visuals/Dashboard are not this decision.

**Ask:** Bet A only — `ISOLATION OFF — GO on EBR-40`.
