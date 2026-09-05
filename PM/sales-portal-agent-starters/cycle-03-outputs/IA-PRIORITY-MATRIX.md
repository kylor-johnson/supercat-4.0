# IA PRIORITY MATRIX — Bet F (v0)

**Date:** 2026-07-24 · **Phase:** 2 shape pack · **Isolation:** ON · **Does not unlock Bet A GO**
**Source of truth:** `PERSONA-RESEARCH-v0.md` §2–4, §6 · Companion: `PERSONA-ONE-PAGERS.md`, `DEMO-SURFACE-CONTRACT.md`
**Reading law:** this matrix is the **ordering law** Bet B reads for each surface's lead answer; the fail-closed rules (§B) are what Bet B / Bet E must honor. It is **not** a new Bet A AC and does **not** unlock GO.

**Legend:** **MUST** = above the fold / lead answer for that persona · **nice** = secondary / follow-up · **HIDE** = suppressed by default (may be a granted privilege). Client-facing labels = `COPY-AUDIT`; capability IDs in parentheses for eng only.

---

## A. Persona × surface matrix

Surfaces in canonical nav order (`DEMO-SURFACE-CONTRACT` §1). **What's broken = teaching only** — non-shipping surface, never a persona default (row at bottom).

| Surface (primary question) | Sales rep | CEO/Owner (Owner/VP) | Admin / sales ops |
|---|---|---|---|
| **Dashboard** — org chrome + KPIs | **HIDE** as landing (org-wide chrome; not the rep's book) · nice once territory-honest | **nice** — org glance; not the reconciling answer | **nice** — sanity glance; not the config home |
| **Customers** — "how much did these customers buy in the range?" | **MUST** *(recommended default home — HYPOTHESIS)*; only my territory's customers; export = screen | nice — whole-org rollup as a follow-up | nice — reconciliation check (export = screen) |
| **Orders** — confirmed vs open quotes | **MUST** — confirmed vs quote split on my book | nice — team backlog glance; backlog ≠ sales | nice — verify quotes never counted as sales |
| **Invoices** — "what did we invoice under these filters?" | **MUST** — invoiced total that moves with my territory + dates (EBR-40) | nice — org invoiced total (Reports/Intelligence is the owner home) | **MUST** (reconciliation) — export matches the screen (EBR-91) |
| **Reports** — Sales Summary = invoiced net | nice — same spine, my scope | **MUST** (secondary owner home) — invoiced net summary (C1 spine) | **MUST** — the reconciliation surface; export = total |
| **Intelligence** — invoiced sales (C1) + accounts fading (S1) + team strip | nice — accounts fading for my accounts | **MUST** *(recommended default home)* — C1 + S1 + team activity | nice — read-only; not ops's job to tune |
| **Settings hub** (Bet E) — enablement / access / display / export | **HIDE** — reps don't configure | nice — read enablement state; not the owner's daily job | **MUST** *(recommended default home)* — enablement tree + who-sees-what; client vs SuperCat gates |
| **What's broken** *(teaching only — non-shipping)* | teaching | teaching | teaching |

**Default-home summary (HYPOTHESIS — pending customer A/B, research §9.2):**
- **Sales rep → Customers** (Invoices close runner-up; freeze as *recommended pending feedback*).
- **CEO/Owner → Intelligence** (Reports secondary).
- **Admin/ops → Settings hub** (Reports/Invoices for the reconciliation half).

**Cross-persona reading:** the same surface serves two personas by *what's shown first + what's gated* — e.g., Customers leads with "only your territory's customers" for a rep but rolls up whole-org for an owner **only where `access_all_customer_sales_totals` is granted** (Rule R1). This is role-aware defaults, not a forked UI (research §6 domain read).

---

## B. Five fail-closed rules (AC-grade)

Promoted from `PERSONA-RESEARCH-v0` §6 to given/when/then so **Bet B** (answer-first shell) and **Bet E** (control plane) honor them. These constrain *what a shared surface may show*; they add **no new Bet A AC** and do not unlock GO. Each cites the standing AC it inherits.

### R1 — Assigned-book default (territory fail-closed)
*Contradiction: "only my accounts" (rep) vs "whole org" (owner) over one god-view sidebar.*

| # | Given | When | Then |
|---|---|---|---|
| R1.1 | Portal-enabled rep with assigned territories, **not** granted all-customer totals | Opens Customers / Invoices / Dashboard (any surface with a total) | Surface leads with the **assigned book only**; total = `SUM(net_amount)` for that scope — never whole-org |
| R1.2 | Same rep with **empty / zero** territory keys, not granted all-customer totals | Opens any scoped surface | **Fail-closed:** empty book + clear empty-state — **never** full org [`FILTER-TRUTH-AC` A1.4] |
| R1.3 | Owner/VP or user-type **explicitly granted** `access_all_customer_sales_totals` | Opens same surface | Whole-org rollup is allowed as that persona's lead — a **granted privilege**, not a default [`SETTINGS` AC-E2 #7; control-plane A.5] |
| R1.4 | Org with empty `territories` master (32/55 today) | Uses territory filter | No promise of named rollups; must still not silently show whole org to unterritoried reps [`FILTER-TRUTH-AC` A1.5; F11] |

### R2 — Suppress named rep→revenue below Tier 2
*Contradiction: "who are my top reps?" (owner) vs orgs that cannot name reps (Tier 0/1).*

| # | Given | When | Then |
|---|---|---|---|
| R2.1 | Org where `REP_IDENTITY_TIER` < 2 (12 Tier-0 orgs impossible) | Any persona opens Intelligence / team strip | **Suppress** named rep→revenue (RS-01); team strip shows **activity / behavior only** [Capability #27; `INSIGHT-IR-v1-AC` AC-3] |
| R2.2 | Any org, v1 default | Intelligence renders | RS-01 named-rep-revenue is **never the v1 default lead**, even at Tier 2 [`INSIGHT-IR-v1-AC` AC-3] |
| R2.3 | Some reps unmapped in an otherwise-attributable org | Team view renders | **Never silently drop** unmapped reps — show the gap honestly, don't fabricate attribution [F9] |

### R3 — Revenue definitions visible-but-locked
*Contradiction: client admin wants to tune portal math vs reconciliation must hold.*

| # | Given | When | Then |
|---|---|---|---|
| R3.1 | Client org-admin opens Revenue definitions (Settings) | Views the six metric-law settings | All render **visible, read-only, 🔒** [`SETTINGS` AC-E3.1] |
| R3.2 | Same admin | Attempts to mutate any row | UI refuses; copy: changes require **SuperCat + INSIGHT** [`SETTINGS` AC-E3.2] |
| R3.3 | SuperCat operator after INSIGHT sign-off | Changes a definition | Audit log records who/when/old/new [`SETTINGS` AC-E3.3] |

### R4 — Client vs SuperCat gates (permission tier)
*Contradiction: client admin vs SuperCat superadmin levers in one hub.*

| # | Given | When | Then |
|---|---|---|---|
| R4.1 | Client org-admin opens Settings hub | Views sections | Sees Enablement / Territory & data access (synch, totals) / Display / Reports & export as **editable**; SuperCat-only levers hidden or disabled [`SETTINGS` AC-E2] |
| R4.2 | Client org-admin | Reaches Territory match mode / `force_portal_display` / Experiments | Controls are **hidden / read-only** — superadmin only [`SETTINGS` AC-E4.2/E5] |
| R4.3 | Bet A filter honesty **not** shipped | Hub shows Territory match mode | Copy must **not** claim invoice-list / dashboard territory filters are fixed [`SETTINGS` AC-E4.4] |

### R5 — STRONG single-feed caveat (never FULL)
*Contradiction: "complete picture of the business" (owner) vs single-feed truth.*

| # | Given | When | Then |
|---|---|---|---|
| R5.1 | Any surface labels a number *sales / invoiced* | Rendered for any persona | Value = `SUM(portal_invoices.net_amount)`, RTD-clamped, $5M cap; **confidence ceiling STRONG**, never FULL [`FILTER-TRUTH-AC` A4; Capability §4] |
| R5.2 | Owner topline (C1) rendered | Intelligence / Reports | Carries a plain single-feed provenance line; **no completeness / margin / AR** claim [Capability §4/§5, F8] |
| R5.3 | Gross-only org | Returns figure would show | Show "returns not represented" — **never "$0 returns"** [Capability #24] |

---

## C. What this matrix is not

- **Not** a nav fork or a forked role-based product — it is the *ordering + gating* law over one shared surface (research §6).
- **Not** a new Bet A AC; **not** a GO unlock. Bet A validation (Track 1) unlocks GO.
- **Not** a Dashboard redesign; Dashboard stays as-is, just not the rep's landing.
- **Not** a build spec for an Admin Console feature-usage report (see `SURFACE-PLACEMENT.md`).
- Default homes are **HYPOTHESIS** pending customer A/B (research §9.2, §9.7).

---

*Phase 2 priority matrix. Fail-closed rules inherit standing ACs; no new metrics, no margin, no RS-01 lead. Isolation ON. Does not unlock Bet A GO.*
