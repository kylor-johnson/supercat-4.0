# Customer Intelligence Brief — Run Prompt

> **Status**: Production v5.1 — 2026-06-29. v5 wired the runtime onto the **invoiced spine**: the run sequence
> executes **G-00 `TOTAL_BUSINESS_PROVENANCE` FIRST** and threads its four outputs (`total_business_source` /
> `feed_completeness` / `commerce_confidence` / `report_through_date`) into every section that prints a dollar.
> Nothing that prints a Total bypasses G-00. **v5.1 (B3 — last Rung-2 build step) wires the Layer-1 exception
> `S1` (account-health $-at-risk) and `K7`/`Q-ECON-LEAK` (customer-grain price leakage) into the
> `09_v4_design.md` §15 Revenue-at-Risk headline and §16 competitive-loss banner — *consume* the already-gated
> Layer-1 outputs, never re-derive them, never upgrade their confidence.** The authority spec (gate rules /
> query library / section design / health score) and the Layer-1 sources (exception layer / `query_library_v2.md`
> Domain 10) are **locked/read-only** here — this operator *consumes* them. v4 baseline 2026-06-16.

Reusable prompt for producing a Customer Intelligence Brief for a specific customer account. Hand this to any capable agent (Cursor, etc.) and it will execute the full workflow: org readiness check → **G-00 provenance preflight** → MCP-driven data gathering → section building → brief assembly.

**Prerequisites:**

- Cursor with `user-supercat-postgres-vpn` and `user-bigquery-admin` MCPs enabled.
- VPN active (both MCPs require it).

**Rough runtime:** 3–8 min total depending on data richness and number of sections rendering.

**Hard rule:** If anything fails (MCP connection, query error, structural defect), stop and report. Do not improvise around missing data.

---

## The prompt

Everything below the line is the prompt body. Fill in the client parameters, then copy from the line break to the end of file and paste into a new agent chat.

---

You are producing a **Customer Intelligence Brief** for a specific customer account. Read the entire prompt before starting.

## Client Parameters

| Parameter | Value |
|-----------|-------|
| Client name | `{{CLIENT_NAME}}` |
| Shortname | `{{SHORTNAME}}` |
| Org ID | `{{ORG_ID}}` |
| Customer code | `{{CUSTOMER_CODE}}` |
| Run date | `{{RUN_DATE}}` |

## Run Directory

All output goes under: `Customer Intelligence/runs/{{SHORTNAME}}/{{CUSTOMER_CODE}}/`

Create `cache/` subdirectory for raw query results.

## MCP Access

- **Postgres**: `user-supercat-postgres-vpn` → tool: `execute_sql`, param: `sql`
- **BigQuery**: `user-bigquery-admin` → tool: `sql` (or check available tools)

Both are read-only for this workflow. Never write, update, or delete data.

## Authority Files

Read these before starting any work:

1. `Customer Intelligence/authority/customer_query_library.md` — all CQ queries (v5: Provenance Anchor — CQ-01/10/22/23 read invoiced net; CQ-23 invoice-only cohort fix from B1)
2. `Customer Intelligence/authority/customer_brief_sections.md` — section rendering specs (v5: every Total carries a G-00 provenance label; three rendering modes)
3. `Customer Intelligence/authority/customer_gate_rules.md` — conditional rendering gates (v5: **G-00 `TOTAL_BUSINESS_PROVENANCE` runs FIRST**; v4 G-10 fill rate population, G-11 new items)
4. `Customer Intelligence/authority/health_score_spec.md` — health & engagement score formulas (v5: score capped at G-00 `COMMERCE_CONFIDENCE`; engagement is §12-only, never blended; v4 H6 fallback)

**Layer-1 sources consumed by §15/§16 (v5.1 — read-only; consume the gated output, do NOT re-derive in this brief):**

5. `Customer Intelligence/09_v4_design.md` §15 (Revenue-at-Risk / Opportunity) + §16 (competitive-loss banner) — the **design contract** these renderings implement. Locked.
6. `Insightful Product 4.0/selling_customer_exception_layer.md` — **exception S1** (account-health $-at-risk). Already Spine-gated and provenance-capped; suppressed at `NONE`, floored/labeled at `PARTIAL`. Confidence = `LEAST(STRONG, COMMERCE_CONFIDENCE)`.
7. `Insightful Product 4.0/query_library_v2.md` Domain 10 — **K7 / `Q-ECON-LEAK`** (tier-aware same-SKU dispersion leakage at customer grain; `house_suspect` rows excluded from the headline pending per-org owner review). Confidence caps at `COMMERCE_CONFIDENCE`; **directional + labeled until owner sign-off — never present a hard leakage dollar to a client.**

> **The invoiced-truth contract (v5 — read once, applies to every dollar in the brief).** "Total business" =
> `SUM(portal_invoices.net_amount)` clamped to `report_through_date` (Spine §1, locked). Booked
> `portal_orders.total_amount` is **intent**, off 4×–9× from invoiced, and is only a *labeled fallback* when no
> invoice feed exists. **G-00 (run first) decides per-org which source every Total reads, the confidence/
> completeness word stamped on it, and the window clamp.** A Total is **suppressed entirely** when
> `feed_completeness ∈ {PROVABLY INCOMPLETE, DEAD}`. Do not resurrect booked GMV as "Total GMV."

---

## Step 0 — Pre-flight

Two passes, **in this order**: first G-00 provenance (sets dollar trustworthiness), then the section gates
(set section availability). G-00 is *not* optional and is *not* part of the richness count.

### Step 0.0 — G-00 `TOTAL_BUSINESS_PROVENANCE` (run FIRST, before any other query)

Run the **G-00** query from `customer_gate_rules.md` against org `{{ORG_ID}}` on `user-supercat-postgres-vpn`,
exactly as written (it is org-level — run once, cache for the session). It mirrors the Layer-1
`Q-PROV-00`/`Q-ECON-00` contract (`provenance_spine.md` §6.1/§6.3/§6.8 — locked, read-only). Record the four
session-level outputs that **every downstream Total inherits**:

| Output | Used by | Effect |
|---|---|---|
| `total_business_source` (`INVOICES`/`ORDERS`/`SALES_DATA`/`NONE`) | CQ-01, CQ-10, CQ-22, CQ-23, §1/§2, H1, competitive-loss banner | which dollar source every Total reads (invoiced net / booked fallback / magnitude / suppress) |
| `feed_completeness` (`CORROBORATED`/`UNVERIFIED — SINGLE FEED`/`PROVABLY INCOMPLETE`/`STALE`/`DEAD`) | same | the completeness word on every Total; **suppress all Totals on `PROVABLY INCOMPLETE`/`DEAD`** |
| `commerce_confidence` (`STRONG`/`PARTIAL`/`LIMITED`/`NONE` — never `FULL`) | every Total + health score | the confidence ceiling; the health score is capped at this (Spine §5.3) |
| `report_through_date` (`LEAST(MAX(invoice_date), CURRENT_DATE)`) | CQ-01/07/08/10/22/23 windows, §2, the brief "Period" line | clamps every LTM/prior window — defuses bad-date invoices; LTM ends here, NOT at `CURRENT_DATE` |

**These four values are threaded into Step 1, Step 1.5, and Step 2. Nothing that prints a dollar may bypass
them.** Determine the run's **rendering mode** now from G-00 (matches `customer_brief_sections.md` "Rendering
Modes"):

- `total_business_source = INVOICES` AND `feed_completeness ∉ {PROVABLY INCOMPLETE, DEAD}` → **Full (invoiced)** — Totals print invoiced net with the provenance label.
- `total_business_source = ORDERS` → **Orders-Only (booked)** — every dollar labeled "booked orders (no invoice feed)."
- `total_business_source = NONE` OR `feed_completeness ∈ {PROVABLY INCOMPLETE, DEAD}` → **Behavior-Only (suppressed)** — **no dollar Totals**; eCat capture in absolute dollars only, labeled "captured through eCat — not total business"; the brief states *why* the Total is suppressed (e.g. "org-wide eCat capture exceeds invoiced net — invoice feed provably incomplete"). Competitive-loss banner and revenue-at-risk headline are suppressed too (they ride the Total).

### Step 0.1 — Org Readiness (section gates)

Check if an org readiness profile already exists for this org (from a previous run). If not, run the profiler.

Follow `Customer Intelligence/operators/org_readiness_profiler.md`:

1. Run all 11 section gate queries **G-01..G-11** from `customer_gate_rules.md` against org `{{ORG_ID}}` / `{{SHORTNAME}}` (v4: includes G-10 `FILL_RATE_POPULATION` and G-11 `HAS_NEW_ITEMS`)
2. Record gate flags (true/false for each)
3. Compute data richness score (0–11) — **G-00 is excluded from the richness count** (it governs *dollar trustworthiness*, not *section coverage*; a rich org can still suppress every Total)
4. Build section manifest (which sections will render)

### Report to chat:

```
## Pre-flight: {{SHORTNAME}} (Org {{ORG_ID}})
Provenance (G-00): source=<...> · completeness=<...> · confidence=<...> · report_through=<YYYY-MM-DD>
Rendering mode: <Full (invoiced) | Orders-Only (booked) | Behavior-Only (suppressed)>
Data Richness: X/11 (Rich/Standard/Lean)
Sections: X always-on + Y conditional = Z total
Skipped: [list]
```

If richness score = 0, stop and report: *"Insufficient data — cannot produce a meaningful brief for this org."*
If G-00 returns `total_business_source = NONE`, the brief runs in Behavior-Only mode (no dollar Totals) — proceed,
but every section that would print a Total instead prints the suppression note.

---

## Step 1 — Data Gathering

Run all applicable CQ queries from `customer_query_library.md`, substituting `{{ORG_ID}}` and `{{CUSTOMER_CODE}}`.

> **Provenance threading (v5 — applies before you run anything dollar-bearing).** G-00 already ran in Step 0.0.
> The four dollar-bearing queries — **CQ-01, CQ-10, CQ-22, CQ-23** — read the **invoiced** spine and clamp their
> windows to `report_through_date` (use the queries exactly as written in the v5 library; they already carry the
> `provenance` CTE). Thread G-00's outputs:
> - `report_through_date` → the LTM/prior window clamp on CQ-01/07/08/10/22/23 (the library's `provenance` CTE
>   computes the same clamp; do not substitute `NOW()`/`CURRENT_DATE`).
> - `total_business_source = ORDERS` → use the **booked fallback variant** of CQ-23 (swap `portal_invoices`→
>   `portal_orders` per the note beneath CQ-23) and label every revenue output "booked."
> - `feed_completeness ∈ {PROVABLY INCOMPLETE, DEAD}` → you still run CQ-01/10/22/23 (their invoiced net is needed
>   for triangulation and for capture-in-absolute-dollars), but **their Totals are suppressed at render time** in
>   Step 2 — do not print them as "total business." CQ-23 lifecycle *stage* may still be reported qualitatively;
>   its cohort-forecast dollars are suppressed.
> - The ⚠ grain-bound queries (CQ-12 channel, CQ-14 buyer, CQ-21 ship-to) stay on booked `portal_orders` **for
>   grain reasons** and must be labeled "booked," never summed into or presented as the invoiced Total.

### Always-run queries (9):

| Query | Section | MCP |
|-------|---------|-----|
| CQ-01 | §2 Account at a Glance | Postgres |
| CQ-07 Step 1 | §7 Buying Rhythm — Frequency | Postgres |
| CQ-07 Step 2 | §7 Buying Rhythm — Org percentile | Postgres |
| CQ-08 | §7 Buying Rhythm — Seasonality | Postgres |
| CQ-10 | §6 Spend Trajectory | Postgres |
| CQ-12 | §8 Channel Mix | Postgres |
| CQ-22 Step 1 | §9 Wallet Share — customer revenue | Postgres |
| CQ-22 Step 2 | §9 Wallet Share — cohort stats | Postgres |
| CQ-23 | §1 Header — lifecycle stage | Postgres |

**Note**: CQ-07 Step 2 requires `total_orders` from CQ-07 Step 1. CQ-22 Step 2 requires `billing_state` from CQ-01. Run CQ-01 and CQ-07 Step 1 first, then substitute into their respective Step 2 queries.

### Conditional queries (gated):

| Query | Section | Gate | MCP |
|-------|---------|------|-----|
| CQ-02 | §3 Categories | `HAS_PORTAL_INVOICES` | Postgres |
| CQ-03 | §4 Top Items | `HAS_PORTAL_INVOICES` | Postgres |
| CQ-04 | §15 Collection Mix | `COLLECTION_COVERAGE` + `HAS_PORTAL_INVOICES` | Postgres |
| CQ-05 | §5 New Intros | `HAS_PORTAL_INVOICES` + `HAS_NEW_ITEMS` (G-11) | Postgres |
| CQ-06 | §17 Next Best Product | `HAS_PORTAL_INVOICES` + V-01 tiered volume check | Postgres |
| CQ-09 | §16 Reorder Decay | `HAS_PORTAL_INVOICES` | Postgres |
| CQ-11 | §2 Price & Discount (embedded) | `HAS_PORTAL_INVOICES` | Postgres |
| CQ-13 | §12 Rep Engagement | `HAS_MIXPANEL_CUSTOMER` | BigQuery |
| CQ-14 | §13 Buyer Intelligence | `HAS_BUYER_NAMES` | Postgres |
| CQ-15 | §20 Fulfillment / Fill Rate | `HAS_PORTAL_INVOICES` + `FILL_RATE_POPULATION` (G-10) | Postgres |
| CQ-16 | §14 Returns | `HAS_RMA` | Postgres |
| CQ-17 | §10 Market Commitments | `HAS_COMMITMENT_REPORTS` | Postgres |
| CQ-18 | §11 Showroom Placements | `HAS_PLACEMENT_REPORTS` | Postgres |
| CQ-19 | §18 Cross-Sell | `HAS_PORTAL_INVOICES` | Postgres |
| CQ-20 | §21 Category Evolution | `HAS_PORTAL_INVOICES` | Postgres |
| CQ-21 | §19 Same-Store Comps | `HAS_SHIP_TO_DATA` | Postgres |
| CQ-24 | §4 Stock-out Alternatives | `HAS_PORTAL_INVOICES` + CQ-03 stock-outs | Postgres |
| CQ-25 | §10 Commitment Conversion | `HAS_COMMITMENT_REPORTS` + customer has data | Postgres |
| CQ-26 | §20 Fulfillment Impact | `HAS_PORTAL_INVOICES` + `FILL_RATE_POPULATION` (G-10) + CQ-15 backordered > 0 | Postgres |

Skip any query where the gate is `false`. Do not run it and do not report empty results.

### Post-query dependent queries:

After CQ-03 completes, classify items with `qty_available = 0` into **real stock-outs** (description not NULL — item exists in catalog) vs. **ghost SKUs** (description IS NULL — no catalog record). Only run CQ-24 for **real stock-outs** that have a `collection_code`. Do not run CQ-24 for ghost SKUs. This typically produces 0–6 additional queries.

After CQ-17 completes (if applicable), run CQ-25 to parse committed items and compute conversion rates.

### Execution strategy:

- Run the always-run Postgres queries first (they're fast — single table scans)
- Run conditional Postgres queries next (skip gated-off ones)
- Run CQ-24 (stock-out alternatives) after CQ-03 results are available
- Run CQ-25 (commitment conversion) after CQ-17 results are available
- Run BigQuery query (CQ-13) only if `HAS_MIXPANEL_CUSTOMER = true`
- CQ-06, CQ-09, and CQ-26 are computationally heavier — run last

### Customer-level gate checks:

After running conditional queries, some sections have a second customer-level gate:
- §10 Commitments: skip if customer has 0 commitment_reports
- §11 Placements: skip if customer has 0 placement_reports
- §12 Rep Engagement: skip if customer has 0 events
- §13 Buyer Intel: skip if customer has ≤ 1 distinct buyer with non-empty name
- §14 Returns: skip if customer has 0 returns
- §16 Reorder Decay: skip if no items have ≥ 3 reorder cycles. Also filter out items with avg_interval < 7 days (false positives on high-frequency accounts)
- §5 New Intros: skip if `HAS_NEW_ITEMS` gate (G-11) is false (org has zero `new_item=true` products). Do not render a "no new items" placeholder.
- §17 Next Best Product: **tiered volume gate (V-01)**: ≤5,000 LTM orders → run CQ-06 as-is; 5,001–50,000 → run CQ-06R (6-month window variant, add note "Based on most recent 6 months"); >50,000 → skip entirely. Also skip if sequence_pairs returns 0 rows.
- §18 Cross-Sell: try cohort tiers in order (v4): (1) same state + within 2x revenue, (2) same state any revenue, (3) org-wide within 2x revenue. Stop at first tier with ≥5 qualifying customers. Skip if all tiers return 0 category gaps. If target customer exceeds cohort avg by >10x, add dominance disclaimer.
- §19 Same-Store: skip if customer has < 2 distinct ship-to locations with order activity
- §20 Fulfillment / Fill Rate: **skip entirely if `FILL_RATE_POPULATION` gate (G-10) is false** — render single line: *"Fill rate data unavailable — this org does not populate invoice quantities."* When G-10 fails, also skip H6 in the health score (exclude from both numerator and denominator).
- §20 Fulfillment Impact (CQ-26): additionally skip if CQ-15 `total_backordered = 0` or CQ-26 returns no qualifying items
- §21 Category Evolution: skip if customer has no prior-year data

### Edge case handling:

- **Missing customer record**: If CQ-01 returns no row from `customers` table, the customer has no master record. Wallet share (CQ-22 Step 2) cannot compute — note this and skip cohort comparison.
- **Collateral-only accounts**: If CQ-03 shows all items at $0 or < $1 unit price, flag as *"Collateral/sample account — revenue figures reflect catalog and material shipments, not product sales."*
- **Blank order_origin**: If CQ-12 returns 100% "Unknown" channel, add note: *"Channel data not available for this client's order import."*
- **Ghost SKU vs. stock-out disambiguation** (v4): In CQ-03 results, items where `p.long_description IS NULL` are **ghost SKUs** (no catalog record). Items where description exists but `qty_available = 0` are **real stock-outs**. Format differently:
  - Stock-out: *"⚠ STOCK OUT — [item] ([description]) — [X] units sold LTM, 0 available, next receipt [date]"* — show alternatives (CQ-24)
  - Ghost SKU: *"⚠ GHOST SKU — [item] — [X] units invoiced LTM, no catalog record."* — do NOT show inventory columns or alternatives
  - Group stock-outs first (actionable), then ghost SKUs (informational) in the §4 alert box.

### Layer-1 economics consumption — S1 + K7 (v5.1; feeds §15/§16 — consume, do NOT re-derive)

These two inputs are **owned by Layer 1** and arrive **already gated**. Run them exactly as written in their
source files (substitute `{{ORG_ID}}` and the G-00 `report_through_date`); **do not modify the gating, and never
upgrade the confidence** they carry. They are org-level pushes — filter to `{{CUSTOMER_CODE}}` for this brief.

| Input | Source (read-only) | Run when | Customer slice | Confidence it carries |
|---|---|---|---|---|
| **S1** account-health $-at-risk | `selling_customer_exception_layer.md` "Exception S1" | `commerce_confidence ≠ NONE` (S1 is **suppressed at `NONE`**) | the S1 row where `subject = {{CUSTOMER_CODE}}` (may be absent → customer is not at-risk; S1 contributes $0) | `LEAST(STRONG, COMMERCE_CONFIDENCE)`; **floored/labeled at `PARTIAL`** — the `dollar_impact` is a floor, never a hard CRITICAL |
| **K7** price leakage | `query_library_v2.md` Domain 10 `Q-ECON-LEAK` | gate `leakage_dispersion_ok = true` (priced invoice lines ≥60%) | the row where `customer_bill_to_number = {{CUSTOMER_CODE}}` **AND `house_suspect = false`** (house/sample rows are excluded pending per-org owner review) | caps at `COMMERCE_CONFIDENCE`; **DIRECTIONAL + labeled until owner sign-off** — do not present a hard leakage dollar to a client |

- **S1 anchoring.** S1's windows are clamped to the same `report_through_date` G-00 returned (Step 0.0) — pass it
  in; do not anchor on `NOW()`. If `commerce_confidence = NONE`, S1 is **suppressed** (no invoice feed → $-at-risk
  unknowable): record S1 = suppressed and move on.
- **K7 anchoring.** Run `Q-ECON-LEAK` with `{{REPORT_THROUGH_DATE}}` = G-00's `report_through_date`. Take only the
  `{{CUSTOMER_CODE}}` row with `house_suspect = false`; its `leakage_dollars` is the customer's directional leakage.
  If the customer is `house_suspect = true`, K7 contributes $0 to the headline (surface it only on the per-org
  owner review list, never to the client).
- **Do not re-derive.** Do not re-author S1's decay math or K7's dispersion math inside this brief. Read the
  gated outputs (`dollar_impact`, `severity`, `confidence` for S1; `leakage_dollars`, `house_suspect` for K7) and
  carry them through Step 1.5 unchanged.

### Checkpoint:

Report to chat:
```
## Data Gathering Complete
Queries run: X of Y applicable
Queries skipped (gated): Z
Failed: [any failures]
Customer-level skips: [sections where customer has no data]
Layer-1 economics: S1=<dollar_impact|suppressed (NONE)|not at-risk> · K7=<leakage_dollars (directional)|suppressed (gate)|$0 (house)>
```

---

## Step 1.5 — Computed Metrics

After data gathering, compute these derived metrics before section building. They require outputs from multiple queries but no additional MCP calls.

### Account Health Score

Follow `authority/health_score_spec.md` exactly. For each of the 8 signals (H1–H8):

1. Check if the signal's data is available (gate passed and query returned data)
2. Score each available signal per the logic table. **H1 trajectory reads CQ-01 `total_business_yoy_pct` on invoiced net; H4 reads `ecat_capture_pct_display` (capped ≤100%).**
3. Sum earned points, divide by max possible points for available signals, multiply by 100
4. Apply competitive loss penalty (-5) if CQ-01 shows `ecat_yoy_pct < 0` AND `total_business_yoy_pct > 0` — **suppressed when the Total is suppressed** (it rides the invoiced Total)
5. Look up the score label (Strong / Healthy / Watch / At Risk / Critical)

If fewer than 3 signals are available, skip the health score and render lifecycle stage only.

#### Confidence cap (v5 — apply LAST, after normalization + penalty; Spine §5.3)

The composite never exceeds its weakest input. Stamp the score with G-00 `commerce_confidence` and cap its
**presentation** at it:

| G-00 state | Health score rendering |
|---|---|
| `commerce_confidence = STRONG` (and `feed_completeness ∉ {PROVABLY INCOMPLETE, DEAD}`) | numeric score as computed, e.g. `Score: 82/100 (Strong · STRONG confidence)` |
| `commerce_confidence ∈ {PARTIAL}` OR `feed_completeness = STALE` | render as a **2-label band**, e.g. `Score: Watch–Healthy (PARTIAL — invoiced feed stale/incomplete)` — **not** a false-precision integer |
| `commerce_confidence = NONE` OR `feed_completeness ∈ {PROVABLY INCOMPLETE, DEAD}` | **no numeric score** — render lifecycle stage + soft signals only, with the reason (e.g. "score suppressed: invoice feed provably incomplete") |

**Decompose, don't blend.** Tag signals by class so a soft signal never silently inflates the headline:
invoiced-truth core (H1, H5, H6, H8) + cadence (H2, H3) form the headline composite; **H4 eCat adoption is
LIMITED (eCat-only) — report it as a separate labeled soft signal beside the score, never the thing that moves
the headline tier.** If scoring H4 would change the score's *label tier*, footnote that the difference is
eCat-only-driven. H7 only when commitment data exists.

### Predicted Next Order Window

From CQ-07 `avg_days_between` + CQ-01 `last_order` date:

1. Guard: only compute if `avg_days_between` is not null AND CQ-07 `total_orders >= 3`
2. `predicted_center = last_order + avg_days_between` (in days)
3. `predicted_range = predicted_center ± 2 days`
4. If `predicted_center` is in the past, flag: *"Predicted window was [range] — [X] days overdue."*
5. If in the future, render: *"Predicted next order window: [range] (based on [avg_days_between]-day avg interval)"*

### Competitive Loss Signal (§2 callout + §16 banner — v5.1)

From CQ-01. This signal has **two renderings**: the always-allowed §2 callout, and the promoted top-of-brief
**§16 banner** which carries a stricter provenance gate (it asserts "total business grew," so it only fires on a
reportable invoiced Total).

1. **Detect.** Check `ecat_yoy_pct < 0` AND `total_business_yoy_pct > 0` (both on the **invoiced** canonical Total
   from CQ-01). If false, neither rendering fires.
2. **Gap (the displacement dollar).** `competitive_loss_gap = ecat_gmv_prior × (total_business_yoy_pct − ecat_yoy_pct) / 100`
   (the §16 / `09_v4_design.md` §15 canonical form). This is also a **§15 Revenue-at-Risk source** (below).
3. **§2 callout (always allowed when detected and the Total is not suppressed):** *"eCat capture declined [X]%
   while invoiced total business grew [Y]%. The ~$[gap] divergence suggests channel shift or competitive
   displacement."*
4. **§16 banner — provenance gate (v5.1).** The banner only fires when the invoiced Total is reportable:
   - **FIRE** when `total_business_source = INVOICES` AND `feed_completeness ∉ {PROVABLY INCOMPLETE, DEAD}`.
     Apply the §16 severity tier: **Critical** (eCat YoY < −25% AND total YoY > +10%, red/"URGENT") · **Warning**
     (eCat YoY < 0% AND total YoY > 0%, amber/"WATCH") · **Info** (eCat flat AND total growing >15%, gray/"MONITOR").
     On `feed_completeness ∈ {CORROBORATED, UNVERIFIED — SINGLE FEED}` and `commerce_confidence = STRONG`, render
     the banner with hard figures and the provenance line *"invoiced through {report_through_date} · {feed_completeness} · {commerce_confidence}."*
   - **DOWNGRADE / RELABEL on `feed_completeness ∈ {PARTIAL, STALE}`:** still fire, but with directional language
     ("invoiced total appears to be growing") and the completeness caveat inline; never a hard "+Y%."
   - **DOWNGRADE on `total_business_source = ORDERS` (booked, no invoices):** label both legs "booked" and drop the
     banner to the §16 **Info** tier ("MONITOR — booked-vs-eCat divergence, not a confirmed invoiced one").
   - **SUPPRESS the banner** when `feed_completeness ∈ {PROVABLY INCOMPLETE, DEAD}` OR `total_business_source = NONE`
     — the "total business grew" claim is unprovable (the gap may simply be the unfed channels). Fall back to the
     §2 capture-only note. (This matches Step 0.0 / `customer_gate_rules.md` G-00: the banner rides the Total.)
5. Also feeds the Account Health Score as a −5 penalty (Step 1.5 Health Score) — **suppressed when the Total is suppressed.**

### Revenue-at-Risk Assembly (§15 headline — v5.1; gated synthesis, not new data)

Implements `09_v4_design.md` §15. **Consume** the already-rendered section figures plus the Layer-1 S1/K7 outputs
from Step 1 — do not re-query, do not re-derive S1 or K7.

**Step A — gather the contributing sources** (each tagged with its `commerce_confidence`; all dollars on the
**invoiced** spine, windows clamped to `report_through_date`):

| # | Risk source | Value | Grain |
|---|---|---|---|
| 1 | Reorder decay | Σ LTM invoiced revenue of items with `DECAY_DETECTED` (CQ-09) | item |
| 2 | Stock-out on top items | Σ LTM invoiced revenue of top-15 items with `qty_available = 0` (CQ-03) | item |
| 3 | Fulfillment impact | Σ `item_ltm_revenue × (1 − 1/slowdown_multiplier)` for backordered items (CQ-26) | item |
| 4 | Dormancy risk | invoiced LTM revenue if `days_since_last_order > 2 × avg_days_between` (vs `report_through_date`) | account |
| 5 | Competitive-loss | `competitive_loss_gap` from the signal above | account |
| 6 | **S1 account-health $-at-risk** | the Layer-1 S1 `dollar_impact` for `{{CUSTOMER_CODE}}` (consume; floor at `PARTIAL`) | account |
| 7 | **K7 price leakage** | the Layer-1 `Q-ECON-LEAK` `leakage_dollars` for `{{CUSTOMER_CODE}}`, `house_suspect = false` (consume; **directional**) | account |

**Step B — deduplicate (avoid double-counting the same dollar):**
- **Item-grain sources (1–3):** dedupe by `item_number`. An item that appears in more than one category is
  counted **once**, at the **maximum** single-category contribution (never summed across categories).
- **Account-grain churn sources (4 & 6):** dormancy and S1 describe the **same at-risk LTM dollar** (S1 fires on
  the same early-dormancy condition). Count this dollar **once** — use **S1's `dollar_impact`** when S1 fired
  (it is the Layer-1 canonical figure); otherwise use the dormancy figure. **Never sum both.**
- **Distinct dollars (5 & 7):** competitive-loss (spend shifting away) and K7 leakage (discretionary margin given
  away) are economically distinct from churn and from each other — add each once.

**Step C — sum:** `revenue_at_risk = dedup(items 1–3) + churn(max of 4/6, counted once) + competitive_loss(5) + K7_leakage(7)`.

**Step D — inherit confidence (the headline never out-claims its weakest input):**
`headline_confidence = LEAST(commerce_confidence of every contributing source)`. S1 and K7 arrive already gated —
**pass their confidence through, never upgrade it.** Because **K7 is directional until owner sign-off**, any
headline that includes a non-zero K7 contribution is itself **directional/floored** and must footnote the K7
component as a pre-sign-off estimate (see Step F).

**Step E — suppress / floor (rides the Total, per G-00):**
- **Suppress the entire headline** when `feed_completeness ∈ {PROVABLY INCOMPLETE, DEAD}` OR
  `total_business_source = NONE`. Render: *"Revenue at Risk: suppressed — {reason} (e.g. invoice feed provably
  incomplete; eCat capture exceeds invoiced net)."* No number.
- **On `feed_completeness ∈ {PARTIAL, STALE}`** (Total not otherwise suppressed): present a **range labeled
  "floor"** — *"Revenue at Risk: ≥ $X (floor — invoiced feed partial/stale)."* S1 already contributes as a floor here.
- **On `INVOICES` + `feed_completeness ∉ {PROVABLY INCOMPLETE, DEAD}` + `STRONG`:** a single figure is allowed for
  the churn/displacement/decay portion; the K7 component remains directional (Step F).

**Step F — K7 discipline (do NOT present a hard leakage dollar to a client yet).** Never bake K7 into a bare hard
number. Either (preferred) render the headline hard portion (sources 1–6) and show K7 as a **separate directional
line** — *"+ ~$[K7] directional price-leakage (Q-ECON-LEAK) — pending owner sign-off, not a confirmed dollar"* —
with a combined "total exposure (directional)" figure beneath; **or** present the whole headline as directional
with the K7 caveat footnoted. House-suspect leakage rows are excluded entirely (per-org owner review only).

**Rendering** (top of §23 Strategic Summary; `09_v4_design.md` §15):
```
Revenue at Risk: $47K  (invoiced through {report_through_date} · {feed_completeness} · {headline_confidence})
  contributing: reorder decay $X · stock-out $X · fulfillment $X · churn/S1 $X · competitive-loss $X
  + ~$Y directional price-leakage (K7) — pending owner sign-off
```
On a suppressed Total: `Revenue at Risk: suppressed — invoice feed provably incomplete (eCat capture exceeds invoiced net).`

### Rep Engagement Score

> **v5 placement (locked).** This is a **behavioral** metric with **no dollar attached** — it is **never blended
> into the Account Health Score** and **never appears in the §1 header or brief lead**. It renders **only in §12**
> as a supporting signal. Its dollar-bearing future (rep-behavior × commercial-outcome fusion) is **owner-gated
> (roadmap Rung 4) — do not build it here.** Keep engagement out of the health score numerator/denominator and
> out of the topline.

If `HAS_MIXPANEL_CUSTOMER` gate passed AND customer has events from CQ-13:

1. Follow `authority/health_score_spec.md` engagement score formula (E1–E4)
2. Compute session-to-order rate: `order_submitted / customer_selections` from CQ-13
3. Compute monthly event volume: `total_events / 6`
4. Count distinct event types from CQ-13
5. Get recency from CQ-13 Step 2 `last_activity`
6. Sum components, render as `X.X/10` with intensity label

---

## Step 2 — Section Building

For each section in the manifest (always-on + conditional where both gates passed), build the section content following the rendering spec in `customer_brief_sections.md`.

### Provenance rendering — every Total inherits G-00 (v5, do this for §1, §2, §6, §9, and the health score)

This is the runtime half of the invoiced-truth fix. The **§1/§2 Total** is rendered from CQ-01's
`total_business_ltm` / `total_business_prior` / `total_business_yoy_pct` (the canonical **invoiced** fields) —
**never from booked `portal_orders` GMV**. Apply the G-00 outputs from Step 0.0:

1. **Source swap (§2 Total + §1 provenance line).**
   - `total_business_source = INVOICES` → render the Total as **invoiced net** (`total_business_ltm`), YoY from
     `total_business_yoy_pct`, with the provenance label line:
     *"Total business: invoiced through {report_through_date} · {feed_completeness} · {commerce_confidence}."*
   - `total_business_source = ORDERS` → render the booked Total **labeled "booked orders (no invoice feed)"** —
     never the bare phrase "Total GMV."
   - `total_business_source = SALES_DATA` → magnitude only, labeled.
2. **Suppress (overrides source swap).** If `feed_completeness ∈ {PROVABLY INCOMPLETE, DEAD}` **OR**
   `total_business_source = NONE` → **do not print any "total business" Total** in §1 or §2. Instead:
   - State the reason on the §1 provenance line (e.g. *"Total business suppressed — org-wide eCat capture
     exceeds invoiced net (feed PROVABLY INCOMPLETE); no trustworthy total can be reported."*).
   - In §2, show **eCat capture in absolute dollars only**, labeled *"captured through eCat — not total
     business."* Do not print a capture *rate/percentage* (a rate is valid only at `CORROBORATED` + `STRONG`).
   - **Suppress the competitive-loss banner and any revenue-at-risk headline** (they ride the Total).
3. **Directional/ranged + loud caveat.** On `feed_completeness ∈ {PARTIAL, STALE}` (and the Total is not
   otherwise suppressed), print the Total as **directional/ranged** with the completeness caveat inline — not as a
   single false-precision figure. (This is the one place the "no hedging" content rule below is overridden: G-00
   says hedge.)
4. **Clamp every window to `report_through_date`.** LTM = trailing 12 months ending at `report_through_date`,
   prior = the 12 months before that. The brief "Period" line and "days since last order" are both computed
   against `report_through_date`, never `CURRENT_DATE`.

> **Worked dependency:** booked GMV may still appear as a *labeled triangulation diagnostic* (e.g. `booked_over_invoiced`)
> but never as the headline Total. The legacy `Total GMV (portal)` row is removed — replace it with the
> invoiced `Total business` row (or the suppression note).

### Build order:

1. Build §1 through §21 in order (they're independent — can be parallel)
2. Build §22 (Health Score Breakdown) after all data sections
3. Build §23 (Strategic Summary) LAST — it reads all prior sections including health score

### Per-section workflow:

1. Read the section spec from `customer_brief_sections.md`
2. Read the raw query results from Step 1
3. Render the section content in markdown following the format spec
4. Apply any conditional rendering rules (stock-out callouts, staleness flags, data quality notes)

### Content rules:

- **No hedging on data** (with the G-00 exception): If a number comes from a query, state it directly. Don't say "approximately" or "around" — the data is exact. **Exception:** dollar **Totals** governed by G-00 follow the provenance rendering rules above — on `PARTIAL`/`STALE` they are intentionally directional/ranged with the completeness caveat, and on `PROVABLY INCOMPLETE`/`DEAD`/`NONE` they are suppressed. That is provenance discipline, not hedging.
- **No fabrication**: If a section's data is empty after passing both gates, note it and move on. Don't fill with assumptions.
- **YoY arrows**: Use ↑ for positive change > 5%, ↓ for negative change > 5%, → for within ±5%
- **Dollar formatting**: Use `$X.XXM` for millions, `$X.XK` for thousands, `$X.XX` for under $1K
- **Percentage formatting**: One decimal place (e.g., `25.8%`)
- **Stock-out alerts**: Always at the TOP of §4, formatted as callout box
- **Staleness flags**: Any placement/commitment data > 365 days old gets a warning

---

## Step 3 — Assembly

Compose the final `brief.md` in the run directory.

### Document structure:

```markdown
# Customer Intelligence Brief: [Customer Name] ([Customer Code])

> **Client**: {{CLIENT_NAME}} | **Org**: {{SHORTNAME}} ({{ORG_ID}})
> **Generated**: {{RUN_DATE}} | **Period**: LTM through {report_through_date} vs. prior 12 months
> **Data Richness**: X/11 | **Lifecycle Stage**: [stage] | **Health Score**: [score or band or "suppressed"] ([confidence tier])
> **Total business**: [invoiced through {report_through_date} · {feed_completeness} · {commerce_confidence}] OR [suppressed — reason]

---

[§1 Header — includes health score bar]

---

[§16 COMPETITIVE-LOSS BANNER (v5.1) — promoted top-of-brief, immediately after §1, BEFORE §2 — render ONLY when
 the §16 provenance gate fires (total_business_source = INVOICES AND feed_completeness ∉ {PROVABLY INCOMPLETE,
 DEAD}); directional/relabeled on PARTIAL/STALE/ORDERS; SUPPRESSED otherwise (fall back to §2 capture-only note)]

---

[§2 Account at a Glance — includes competitive loss signal callout if applicable]

---

[§3-§21 Rendered sections in order, separated by ---]

---

[§22 Account Health Score Breakdown]

---

[§23 Strategic Summary — OPENS with the §15 REVENUE-AT-RISK / OPPORTUNITY headline (v5.1): two stat lines, each
 carrying one G-00 provenance label. Revenue at Risk = the assembled sum from Step 1.5 (dedup'd; lowest inherited
 confidence; K7 shown as a directional line, never a hard client dollar). SUPPRESSED entirely when the Total is
 suppressed; floor-ranged on PARTIAL/STALE]

---

*Generated by SuperCat Customer Intelligence • Data as of {{RUN_DATE}} • Read-only — no data was modified*
```

### Assembly rules:

- Only include sections that rendered (skip gated-off and customer-empty sections)
- **Sequential section numbering** (v4): Renumber sections §1, §2, §3... in the output — close gaps left by gated-out sections. The canonical §-numbers from the spec are internal reference only.
- **Rep name in header** (v4): Look up the assigned rep from territory_codes (see §1 spec in `customer_brief_sections.md`). Render as: *"Prepared for: [Rep Name] — Territory [code]"*
- **ASCII seasonality bar chart** (v4): §7 monthly seasonality uses `█` / `░` bar chart format per the spec, not plain tables. Fall back to table if <6 months of history.
- **Active months cap** (v4): Display at most 12 for active months, with "All months active" note if raw value exceeds 12.
- Section separators (`---`) between every section
- No empty sections or "No data available" placeholders
- Strategic Summary must produce **5-6 priority-sequenced talking points** (v4), not 3. Part A (situation assessment) + Part B (pre-meeting priorities). See §23 spec.
- **§15 Revenue-at-Risk headline + §16 competitive-loss banner (v5.1):** place per the document structure above
  (banner after §1, headline atop §23). Both **ride the Total** — suppressed when the Total is suppressed
  (`feed_completeness ∈ {PROVABLY INCOMPLETE, DEAD}` or `source = NONE`), directional/floored on `PARTIAL`/`STALE`.
  The headline inherits the **lowest** contributing confidence; **K7 leakage is directional and labeled, never a
  hard client dollar, until owner sign-off.** Consume S1/K7 from Layer 1 — do not re-derive.
- Every claim must trace to a query result

### Save:

`Customer Intelligence/runs/{{SHORTNAME}}/{{CUSTOMER_CODE}}/brief.md`

---

## Final Report to Chat

After completing all steps, report:

1. Org readiness summary (richness score, gate flags)
2. Customer-level summary (which sections rendered, which skipped)
3. Key findings (3-5 highlights from the Strategic Summary)
4. Brief file path
5. Any data quality flags

---

## Hard Constraints

- **Provenance-first (v5).** G-00 runs before any other query. **No section that prints a dollar Total may bypass G-00.** A Total is invoiced net (or labeled booked fallback), and is **suppressed** on `feed_completeness ∈ {PROVABLY INCOMPLETE, DEAD}` or `total_business_source = NONE`. Never print booked `portal_orders` GMV as "Total GMV / Total business." Never headline eCat capture > 100%. The health score is capped at G-00 `commerce_confidence`. Rep engagement is §12-only and never blended into health or topline.
- **§15/§16 consume Layer 1 — never re-derive (v5.1).** S1 (`selling_customer_exception_layer.md`) and K7
  (`Q-ECON-LEAK`, Domain 10) arrive **already gated**. Pass their confidence through unchanged — **never upgrade
  it.** The §15 Revenue-at-Risk headline inherits the **lowest** contributing confidence and is **suppressed when
  the Total is suppressed** (floored on `PARTIAL`/`STALE`). The §16 banner fires **only** on
  `total_business_source = INVOICES` AND `feed_completeness ∉ {PROVABLY INCOMPLETE, DEAD}` (directional/relabeled on
  `PARTIAL`/`STALE`/`ORDERS`). **K7 leakage is directional and labeled until owner sign-off — never present a hard
  leakage dollar to a client.** Do not build the rep-behavior × outcome fusion (Rung 4) and do not touch segmentation.
- **Read-only MCP posture.** Every query is a SELECT. Never write, update, or delete data.
- **If anything fails, stop and report.** Do not improvise around missing data or broken queries.
- **No generic statements.** Every insight must cite specific data from the queries.
- **Follow the section specs.** The rendering format in `customer_brief_sections.md` is authoritative.
- **Follow the query library.** Use queries exactly as written in `customer_query_library.md`. Do not modify queries during execution.
