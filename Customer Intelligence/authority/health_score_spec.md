# Customer Intelligence — Health & Engagement Score Specifications

> **Status**: Production v5 — 2026-06-29 (**confidence discipline**: the composite now inherits its lowest
> input's confidence and is capped at G-00 `COMMERCE_CONFIDENCE`; signals decomposed into invoiced-truth core
> vs soft). v4 baseline 2026-06-16 (arithmetic normalization bug, H6 fill rate fallback).
> **Scope**: Defines the composite Account Health Score (0–100) and Rep Engagement Score (0–10) used in the Customer Intelligence Brief.
> **Authority**: The brief generator must use these formulas exactly. Do not improvise scoring.

---

## Confidence discipline (v5 — the binding rule, Spine §5.3)

> **A composite is never more confident than its weakest input, or it is suppressed.** The Account Health Score
> blends invoiced-truth signals with eCat-only and cadence signals; without discipline it launders a
> low-confidence input into a confident-looking 0–100 number (reconciliation defect **W3**). Two rules now bind it:

1. **Cap + label.** The whole score carries the G-00 `COMMERCE_CONFIDENCE` tier and is **capped at it**. If
   `COMMERCE_CONFIDENCE = PARTIAL`, render the score as a band ("Watch–Healthy") not a false-precision integer,
   with the completeness caveat. If `NONE` / `FEED_COMPLETENESS ∈ {PROVABLY INCOMPLETE, DEAD}`, **do not emit a
   numeric score** — show lifecycle stage + soft signals only.
2. **Decompose, don't blend.** Signals are tagged by confidence class and the score is split so a soft signal
   never silently inflates the headline:

   | Class | Signals | Confidence |
   |---|---|---|
   | **Invoiced-truth core** | H1 trajectory, H5 breadth, H6 fill rate, H8 category stability | inherits G-00 (STRONG ceiling) |
   | **Cadence** (booked timing) | H2 recency, H3 frequency | booked-order timing — fine as-is, labeled |
   | **Soft / eCat-only** | H4 eCat adoption | eCat-channel behavior — **LIMITED**; shown as a separate labeled signal, never the thing that moves the headline tier |
   | **Conditional** | H7 market conversion | only when commitment data exists |

   The headline score is the normalized core+cadence composite (capped at G-00). **H4 (eCat adoption) is reported
   as a labeled soft signal beside the score, not blended into a confident headline** — if including it would
   change the score's *label*, footnote that the change is eCat-only-driven.

---

## Account Health Score (0–100)

A weighted composite of 8 signals, each already computed by existing CQ queries. The score appears in the brief header (§1) alongside the lifecycle stage badge, with a per-signal breakdown in the lifecycle section. **All revenue-derived signals are now on the invoiced spine** (H1 reads CQ-01 `total_business_yoy_pct` computed on invoiced net; H4 reads `ecat_capture_pct_display`, capped ≤100%).

### Signal Weights

| # | Signal | Source | Max Points | Scoring Logic |
|---|--------|--------|------------|---------------|
| H1 | Spend trajectory | CQ-01 `total_business_yoy_pct` (**invoiced** net YoY) | 20 | > +10% = 20; 0% to +10% = 15; -10% to 0% = 8; < -10% = 0 |
| H2 | Order recency | CQ-01 `days_since_last_order` | 15 | < 30d = 15; 30–90d = 10; 90–180d = 5; > 180d = 0 |
| H3 | Order frequency | CQ-07 `orders_per_month` vs org median | 15 | >= org median = 15; >= 50% of median = 10; >= 25% of median = 5; < 25% = 0 |
| H4 | eCat adoption (**soft / eCat-only — LIMITED**) | CQ-01 `ecat_capture_pct_display` (capped ≤100%) | 10 | > 30% = 10; 10–30% = 7; > 0% = 4; 0% or no eCat = 0 |
| H5 | Product breadth | CQ-02 distinct categories (LTM) + `is_new_category` count | 10 | >= 5 categories = 7 + (1 per new category, max 3) = max 10; 3–4 cats = 5; 1–2 cats = 2 |
| H6 | Fill rate | CQ-15 `fill_rate_pct` vs `org_fill_rate` — see H6 fallback rules below | 10 | >= org rate = 10; within 5 pts = 7; > 5 pts below = 3 |
| H7 | Market conversion | CQ-17 commitment trend (last 3 commitments) | 10 | Item count growing or stable = 10; item count declining = 5; no commitment data = SKIP |
| H8 | Category stability | CQ-20 `share_shift_pts` | 10 | No category with negative shift > 5 pts = 10; 1 category shifting = 5; 2+ categories shifting = 0 |

### H6 Fill Rate — Fallback Rules (v4, audit finding §1)

H6 **must** use the CQ-15 query result (`fill_rate_pct` vs `org_fill_rate`). Do not substitute proxy metrics.

| Condition | Action |
|-----------|--------|
| CQ-15 returns a valid `fill_rate_pct` for this customer AND `FILL_RATE_POPULATION` gate passes (see `customer_gate_rules.md` G-10) | Score H6 normally using the table above |
| CQ-15 returns `fill_rate_pct = 0` (or NULL) but `FILL_RATE_POPULATION` gate **fails** (org doesn't populate `quantity_invoiced`) | **SKIP H6** — exclude from both numerator and denominator. Do not use replacement order %, return rate, or any other proxy. |
| CQ-15 cannot run for this customer (e.g., no `portal_order_items` rows) | **SKIP H6** — same as above |

**Why**: The v3 pilot found wwjc/21762 scored H6 = 7/10 using a "replacement order %" proxy instead of actual CQ-15 fill rate. The customer's real fill rate was 96.6% (vs 82.0% org average), which should have scored 10/10. Using improvised proxies corrupts the score.

### Computation Rules

1. **Sum applicable signals.** If a signal's gate is false (e.g., no eCat orders → H4 skipped; no commitment data → H7 skipped; no invoice data → H5/H6/H8 skipped), exclude it from both the numerator and the max denominator.

2. **Normalize** (v4 — arithmetic fix, audit finding §1):
   ```
   score = ROUND(100 × earned_points / max_possible_points)
   ```
   **Worked example** (wwjc/21762): earned = 84, max = 90 → `ROUND(100 × 84 / 90)` = `ROUND(93.33)` = **93**.
   - Use standard rounding (≥ 0.5 rounds up).
   - The denominator is the **sum of `Max Points` for scored signals only** — do NOT include skipped signals in the denominator.
   - Common bug: including a skipped signal's weight in the denominator deflates the score. Double-check: if N signals are scored, the denominator must equal the sum of exactly those N signals' max points.

3. **Minimum signals**: Require at least 3 signals to produce a score. If fewer than 3 are available, render lifecycle stage label only (no numeric score).

4. **Competitive loss penalty**: If CQ-01 shows `ecat_yoy_pct < 0` AND `total_business_yoy_pct > 0` (eCat capture declining while **invoiced** total business grows), subtract 5 points from the **normalized** score (floor at 0). Apply this AFTER normalization, not before. **Suppressed** when the Total is suppressed (`PROVABLY INCOMPLETE`/`DEAD`) — the penalty rides the invoiced Total.

5. **Confidence cap (v5 — Spine §5.3, applied LAST):** stamp the score with the G-00 `COMMERCE_CONFIDENCE`
   tier and cap its presentation at it:
   - `STRONG` → numeric score as computed.
   - `PARTIAL` / `STALE` → render as a **2-label band** (e.g. "Watch–Healthy") + completeness caveat, not a
     false-precision integer.
   - `NONE` / `FEED_COMPLETENESS ∈ {PROVABLY INCOMPLETE, DEAD}` → **no numeric score**; lifecycle stage + soft
     signals only, with the reason.
   - If H4 (eCat-only, LIMITED) being scored would change the score's **label tier**, keep H4 as a separate
     labeled soft signal and footnote that the difference is eCat-only-driven (do not let a LIMITED input set
     the headline tier).

### Score Labels

| Range | Label | Visual |
|-------|-------|--------|
| 80–100 | Strong | `████████████████████░░░░` |
| 60–79 | Healthy | `████████████████░░░░░░░░` |
| 40–59 | Watch | `████████████░░░░░░░░░░░░` |
| 20–39 | At Risk | `████████░░░░░░░░░░░░░░░░` |
| 0–19 | Critical | `████░░░░░░░░░░░░░░░░░░░░` |

### Rendering

**Header (§1):**
```
GROWING ████████████████████░░░░  Score: 82/100 (Strong · STRONG confidence)
```
On a `PARTIAL` feed, render the band form instead:
```
GROWING ████████████░░░░░░░░░░░░  Score: Watch–Healthy (PARTIAL — invoiced feed stale/incomplete)
```

**Lifecycle section — per-signal breakdown:**

| Signal | Status | Points |
|--------|--------|--------|
| Spend trajectory | Accelerating (+17.7% YoY) | 20/20 |
| Order recency | 11 days since last order | 15/15 |
| Order frequency | 3.5/month (Top 15%) | 15/15 |
| eCat adoption | 25.8% penetration | 7/10 |
| Product breadth | 6 categories (+1 new) | 8/10 |
| Fill rate | 88.1% (vs 91.4% org) | 3/10 |
| Market conversion | Declining (112 → 23 items) | 5/10 |
| Category stability | Bedroom -9 pts | 5/10 |
| **Competitive loss penalty** | — | -5 |
| **Total** | | **73/100 (Healthy)** |

---

## Rep Engagement Score (0–10)

> **v5 placement (reconciliation W4 / FIX-LIST item 6).** This is a **behavioral** metric with **no dollar
> attached** — by the founding-goal definition it is vanity if it leads. It is therefore: (a) **never blended**
> into the Account Health Score, and (b) **demoted out of the headline/lead** — it renders only in §12 as a
> supporting signal. Its dollar-bearing future is the **rep-behavior × commercial-outcome fusion**, which is
> **owner-gated (roadmap Rung 4)** — do not build that fusion here. Until then, present engagement as context,
> not as a standalone score in the brief lead.

A composite metric from CQ-13 Mixpanel data. Only computed when `HAS_MIXPANEL_CUSTOMER` gate passes AND the customer has > 0 events.

### Components

| # | Component | Source | Max Points | Scoring Logic |
|---|-----------|--------|------------|---------------|
| E1 | Session-to-order rate | CQ-13: `order_submitted` / `customer_selections` | 4 | >= 25% = 4; 15–25% = 3; 5–15% = 2; > 0% = 1; 0% = 0 |
| E2 | Event volume | CQ-13: total events / 6 (monthly rate) | 2 | >= 50/mo = 2; 10–50/mo = 1.5; 1–10/mo = 1; 0 = 0 |
| E3 | Event diversity | CQ-13: count of distinct event types | 2 | >= 6 types = 2; 3–5 = 1.5; 1–2 = 1; 0 = 0 |
| E4 | Recency | CQ-13 Step 2: `last_activity` | 2 | < 30d = 2; 30–90d = 1; > 90d = 0 |

### Computation

`engagement_score = ROUND(E1 + E2 + E3 + E4, 1)` (range: 0.0–10.0)

### Rendering

In §12 (Rep Engagement):
```
Engagement score: 8.4/10 — [X]% session-to-order rate (vs. avg 12%)
```

Classify intensity:
- >= 7.0: "High engagement"
- 4.0–6.9: "Moderate engagement"
- 1.0–3.9: "Low engagement"
- 0: "No engagement data"
