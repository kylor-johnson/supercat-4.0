# Rep Provenance Map — Tier 1 (Selling-context bones)

> **Inherits from [`provenance_spine.md`](provenance_spine.md).** Gates, tiers, and identity rules are defined there; this map *applies* them to the **rep / selling layer** and names the feeds, confidence, and degrade-vs-suppress behavior per insight. SQL lives in `query_library_v2.md` (Tier 2).
>
> **The one principle that makes this layer different.** **The Rep layer is ERP-optional.** It stands on in-app behavior (`orders`, `login_events`, `org_users`/`users`, Mixpanel) and does **not** require an invoice feed to produce value. Commerce (the ERP) is an **enrichment** that upgrades "activity" → "outcome" — and only when both the invoice feed (Spine §6) *and* the rep-identity match rate (Spine §7.1) permit. Build rep insights so they **degrade to behavior-only**, never go dark, when ERP is absent or rep identity can't be resolved.
>
> **Audience:** sales leadership (VP Sales / National Sales Manager) and, downstream, the rep themselves (Rep Copilot). Lead with the action, method below.
>
> **Empirical basis:** 21-org live Postgres cohort, 2026-06-26 (§ Validation). Live diagnostics labeled `[from-live]`; design figures `[ILLUSTRATIVE]`.

---

## 1. The model in one picture — what we already have vs. what gates the upgrade

```
IN-APP BEHAVIOR (we own it; ERP-optional)                 OUTCOME ENRICHMENT (ERP-gated)
  login_events  ──┐                                          portal_invoices.net_amount
  orders (eCat) ──┼─► REP ACTIVITY & EFFORT  ──[identity ≥80%]──► REP → REVENUE OUTCOME
  org_users/users ┘   (logins, orders written,                   (whose customers invoiced $,
  Mixpanel ───────►   catalogs shared, quote→                     realization by rep, book health)
   (feature depth)    submit cadence, coverage)
                          │                                        ▲
                          └── always reportable ───────────────────┘ only when
                              (behavior-only tier)                   FEED_COMPLETENESS≥STRONG
                                                                     AND rep-identity match ≥80%
```

- **Floor (always on):** logins + orders authored + catalog/asset sharing → effort, cadence, coverage, dormancy. No ERP needed.
- **Ceiling (gated):** rep → invoiced-revenue outcome → only past the identity gate (Spine §7.1) and `FEED_COMPLETENESS` (Spine §6.3).

---

## 2. Feeds inventory — HAVE vs. CLIENT-MUST-ADD

| Feed | Grain | We already HAVE | Client must add | Notes / gate |
|---|---|---|---|---|
| `login_events` | login event (rep, device, ts) | **Yes** — owned, present & fresh for 20/21 orgs `[from-live]` | nothing | Always-available behavior floor. Stale feed = dormant org (mhc last 2026-02-28). |
| `orders` (eCat) | order/quote, with `rep_first_name`/`rep_last_name`/`rep_number`/`org_user_id` | **Yes** — owned; rep identity native here | nothing | Apply eCat-SALE filter (Spine §6.5) for *sales* effort; keep quotes for *activity*. |
| `org_users` / `users` | seat / person | **Yes** — owned | nothing | **Conflates reps + buyers for B2B orgs** (Spine §7.1). Use `last_ipad_login_at IS NOT NULL` or order authorship as the rep-seat proxy, not raw counts. |
| Mixpanel feature usage | event (search, view, share, present) | **HAVE — broad & fresh** (`user-bigquery-admin`, `mixpanel.events` + `*_feature_usage_report`); CORROBORATED 20/21 cohort orgs `[from-live]` | confirm export for net-new orgs | Behavioral *depth* beyond logins — the cohort's richest under-used asset, not sparse. **Mixpanel-coverage gate** (below). Postgres `login_events` is the floor when absent. |
| `portal_invoices` (`net_amount`) | invoice (ERP) | Only if client sends `invoice_data.csv` | **invoice feed** | The outcome enrichment. Gated by Spine §6 + identity §7.1. |
| `portal_orders` (`rep_number`+`rep_name`) | booked order (ERP) | Only if client sends `order_data.csv` | order feed | **Sole bridge from invoice `rep_number` → rep name** (invoices have no name). Coverage drives the identity gate. |

---

## 3. The gates this map adds (on top of the Spine)

### 3.1 Rep-identity match gate (the upgrade gate) — *canonical def in Spine §7.1 (3-tier)*
- **Metric:** first, whether invoice `rep_number` exists at all; then, % of `rep_number`s resolvable to a named rep (via `portal_orders.rep_name`).
- **Three tiers (Spine §7.1, validated 2026-06-26):**
  - **Tier 0 — no ERP rep key** (invoice `rep_number` ≈0%): **ufi, heb, kll, lpf** → **behavior-only; rep→revenue impossible.**
  - **Tier 1 — `rep_number`-only** (date-aligned name bridge <80%, 9 orgs): gh, scw, sc, clm, clli, bri, vic, shl, jyc → **`rep_number` grain, no names.**
  - **Tier 2 — named reachable** (date-aligned name bridge ≥80%, 8 orgs): sarreid, clc, **mhc (⚠ DORMANT)**, cci, wwjc, pf, ril, **bcf (81.8%)** → **named rep→revenue allowed** (still capped by `FEED_COMPLETENESS`). *(Date-aligned bridge re-confirmed 2026-06-29 — `rep_intelligence_layer2_build.md` §2; the un-dated census mis-placed bcf in Tier 1.)*
- **Why it bites `[from-live]`:** 4 orgs have *no* rep key (verified 0% across 120k–251k invoices each), so behavior-only is the default design, not the exception.

### 3.2 Mixpanel-coverage gate
- **Metric:** does BigQuery carry this org's Mixpanel events for the window, with enough volume to be representative?
- **Behavior:** **CORROBORATED** (Mixpanel present) → full feature-depth insights; **LOGINS-ONLY** (no/low Mixpanel) → degrade feature-depth insights to login-based effort/cadence; never fabricate feature engagement from absence.
- **Cohort reality `[from-live]` (2026-06-26):** CORROBORATED for **20/21** orgs — all appear in `mixpanel.events` (29–42 event types) and the feature-usage reports (~40 counters), fresh to 06-25; only **mhc** is LOGINS-ONLY (dormant). The earlier "coverage varies / partial" framing was too cautious: for this cohort the BigQuery ceiling is real and broad.

### 3.3 Active-rep roster gate
- Define the rep population as **iPad-active seats** (`org_users.last_ipad_login_at IS NOT NULL`) ∪ order authors (`orders.org_user_id`), **not** raw `org_users`. Prevents B2B buyer accounts (e.g., wwjc 20,740 org_users) from diluting per-rep metrics.

### 3.4 One-org-only guardrail (do NOT build cohort VMs on these)
- `sales_quotas` (actual-vs-quota) → **sarreid only**; `commitment_reports` / Mixpanel `view_commitments` → **ufi only**; `placement_reports` / `view_placements` → **3 orgs** (ufi, cci, clm). `[from-live]`
- These are real but **fail cross-org coverage**. They may power *org-scoped conditionals*, never a cohort-wide Rep Intelligence VM. Building "attainment / commitment / placement" VMs would silently apply to ≤3 orgs.
- Also: `authenticated_sessions`, `audit_log_entries`, `user_stacks`, `projects` lack native `organization_id` — usable (except `audit_log_entries`, polymorphic) only via `org_users` joins that re-introduce B2B-buyer conflation; filter to iPad-active seats.

---

## 4. Provenance map — one row per rep insight (action-first)

| # | Insight (so-what) | Feeds required | We HAVE | Client must add | Confidence if complete | If a piece is missing |
|---|---|---|---|---|---|---|
| **R1** | **Rep activity & cadence** — who's logging in, writing orders, going quiet | `login_events`, `orders` | **All** | — | **FULL** (owned, ERP-independent) | Never dark. Stale feed → flag org dormant. |
| **R2** | **Coverage / territory penetration** — how much of the assigned book each rep is actually touching | `orders`, `org_users.territory_codes` / `customers` | Most | territory accuracy | **STRONG** | Territory format preflight (Spine §7.3); if territory blank, report touched-accounts only. |
| **R3** | **Catalog/asset engagement** — what reps present & share (feature depth) | Mixpanel, `shared_resources`, `smart_stacks` | Partial (Mixpanel BigQuery) | confirm Mixpanel export | **STRONG** w/ Mixpanel | Mixpanel-coverage gate → degrade to login/order effort. |
| **R4** | **Quote→submit discipline** — drafts that never become orders | `orders` (`order_type`, `is_submitted`) | **All** | — | **STRONG** | eCat-SALE filter (Spine §6.5) separates quotes from sales. |
| **R5** | **Rep → revenue outcome** — whose customers actually invoiced, realization by rep | `portal_invoices`, `portal_orders` (name bridge), identity | Owned-side only | **invoice + order feed** | **STRONG** (never FULL w/o CORROBORATED completeness) | **Identity gate (3.1, 3-tier):** Tier 2 → names; Tier 1 (`rep_number`-only) → no names; **Tier 0 (no `rep_number`: ufi/heb/kll/lpf) → behavior-only**; no feed → behavior-only. Cohort grain only (re-keying, Spine §2). |
| **R6** | **Book-of-business health by rep** — concentration & decline inside a rep's accounts | `portal_invoices`, customer identity, rep identity | Owned-side only | **invoice feed** | **STRONG** | Inherits R5 gates + customer grain = billing entity (Spine §7.2). |

**Never:** rank reps by revenue while silently dropping the reps whose `rep_number` didn't resolve — that fabricates a leaderboard (Spine §7.1). Suppress or label instead.

---

## 5. Confidence & degrade-vs-suppress summary
- **Behavior insights (R1–R4):** floor at **STRONG–FULL**, ERP-independent — the always-on core of the Rep layer.
- **Outcome insights (R5–R6):** capped at **STRONG** (FULL needs `FEED_COMPLETENESS=CORROBORATED`), and **gated on rep-identity ≥80%** (Spine §7.1). Below the gate they **degrade to behavior-only**, never go dark silently.
- **One-line rule:** *the Rep layer always ships; the ERP only decides whether it ships with outcomes attached.*

---

## 6. Validation appendix `[from-live]`

**Cohort:** 21 orgs (sc, scw, ufi, gh, pf, sarreid, bcf, wwjc, lpf, clli, jyc, cci, shl, clm, kll, clc, mhc, bri, ril, heb, vic). Read-only Postgres, 2026-06-26.

**Behavior-feed completeness (the floor):**
| Signal | Finding |
|---|---|
| `login_events` present & fresh | **20/21** orgs last login = 2026-06-26; **mhc** stale (2026-02-28) — matches its stale invoice feed |
| Login volume (LTM-ish) | 1,971 (vic) → 85,092 (sc) — all orgs have a usable behavior floor |
| iPad-active seats (`last_ipad_login_at`) | 41 (vic) → 164 (pf) — the real rep-roster size |
| Raw `org_users` (B2B inflation) | wwjc 20,740 · jyc 16,181 · gh 7,997 vs ~40–160 active seats → **must use active-seat proxy** (gate 3.3) |

**Rep-identity — the 3-tier upgrade gate (Spine §7.1, validated 2026-06-26 incl. spot-check):**
| Tier | Condition | Orgs |
|---|---|---|
| **2 — named reachable** (date-aligned bridge ≥80%, 8 orgs) | `rep_number` + `portal_orders.rep_name` | sarreid 100% · clc 100% · mhc 100% (⚠ DORMANT) · cci 100% · wwjc 98.8% · pf 89.7% · ril 87.7% · bcf 81.8% |
| **1 — `rep_number`-only** (date-aligned bridge <80%, 9 orgs) | `rep_number` present, no usable name | gh 39% · scw 36% · sc 3.2% · clm · clli · bri · vic · shl · jyc (0% bridge) |
| **0 — no ERP rep key** (`rep_number` ≈0%) | no key at all → behavior-only | **ufi · heb · kll · lpf** (verified 0% across 120k–251k invoices each) |

**Mixpanel coverage (the ceiling) `[from-live]`:** CORROBORATED **20/21** (all in `mixpanel.events` 29–42 event types + feature reports, fresh to 06-25); only **mhc** LOGINS-ONLY. Username on events 95–99%.

**One-org-only (excluded from cohort VMs):** `sales_quotas`→sarreid; `commitment_reports`/`view_commitments`→ufi; `placement_reports`/`view_placements`→ufi, cci, clm.

**Implication:** the behavior floor (R1–R4) is universal, fresh, and now Mixpanel-deep across the cohort; the revenue-outcome ceiling (R5–R6) is named-reachable for **8** orgs, `rep_number`-only for **9**, and **structurally impossible** (Tier 0) for 4 (date-aligned bridge, 2026-06-29). Design for behavior-only as the default, with outcomes as the unlock. *(Re-run on the live cohort before client use.)*
