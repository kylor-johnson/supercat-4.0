# Known Limitations — Insightful Product 2.0

**Phase 1 External Report System**
Last updated: 2026-04-07
Evidence basis: 13-org validation set (sccon, ali, fc, bri, mlc, cci, abol, tel, ah, fsf, ril, jyc, clli)

These limitations are stable, cross-client findings from the Phase 1 validation run.
They are **not** client-specific incident notes.

This document is **not** a runtime input. Do not add it to the operator read chain.
It informs QA practices and future system development, not report generation logic.

---

## 1. Data Source Limitations

### 1.1 `portal_orders` denominator quality is not guaranteed

`portal_orders` is intended to represent ERP-synced total business across all channels. In practice, the quality of the sync varies by account. Three patterns have been observed:

- **Valid denominator**: ERP GMV is meaningfully larger than eCat GMV (5–10×+), consistent with a real all-channel picture.
- **Partial sync**: eCat GMV equals or exceeds `portal_orders` GMV — the ERP sync captured only a subset of total business, making the denominator smaller than the numerator. This is an invalid state for VM-45.
- **No data**: `portal_orders` is empty. The denominator is unavailable.

In the 8-org validation set, 3 of 5 orgs with `portal_orders` data failed the VM-45 denominator validity gate. Do not assume a credible denominator without running the gate check.

### 1.2 `sales_quotas` staleness is a platform-wide pipeline gap

The `sales_quotas` entity was stale (229–242 days) in all 8 tested orgs. This is not an account-specific data issue — it reflects a platform-wide pipeline gap in quota data. It does not affect LTM order or ERP calculations, but should be disclosed as a standing caveat in every report Appendix rather than investigated per-org.

The same pipeline gap affected additional entities in some orgs: `riser_prices`, `commitment_reports`, `customer_payment_informations`, `placement_reports`, `kit_items`, `contract_prices`, `options`, `option_groups`, `matrix_options`. These are more common in accounts on legacy or higher-complexity plans.

### 1.3 Severely stale core data invalidates product and inventory sections

For accounts where `products`, `inventories`, and `customers` have not synced in more than 180 days, the product and inventory sections of the report cannot be trusted. Report generation should exclude those sections and add a staleness warning to the Executive Summary rather than surface potentially outdated catalog data.

### 1.4 `order_origin = 'ECAT'` in `portal_orders` returns zero

Across all tested orgs, `portal_orders.order_origin = 'ECAT'` returns 0 rows. This field does not yet identify eCat-sourced orders in the ERP sync. Do not use it to calculate eCat-originated share within `portal_orders`. The VM-45 eCat capture rate uses total `orders` GMV as the numerator and total `portal_orders` GMV as the denominator — not a filtered subset of `portal_orders`.

---

## 2. VM-Specific Limitations

### 2.1 VM-45: eCat Capture Rate requires denominator validity check

VM-45 must only render when all three conditions are met:

1. `portal_orders` data is present and GMV > 0
2. `portal_orders_gmv > ecat_gmv` (ERP total must exceed eCat; if eCat equals or exceeds ERP, the sync is partial)
3. `ecat_gmv >= 0.05 × portal_orders_gmv` (eCat must be at least 5% of ERP total; below this threshold the rate is not interpretable as an activation signal)

If any condition fails, VM-45 must be omitted entirely. Never substitute a denominator-less commentary about eCat GMV in isolation.

Validated across 5 applicable orgs: 2 rendered (bri, cci), 3 skipped due to partial sync (sccon, ali, fc).

### 2.2 Enrollment / onboarding velocity — intentionally excluded from external reporting

VM-15 (Enrollment Funnel) and VM-44 (Onboarding Velocity) are **out of scope for the external report system** as a deliberate product-scope decision.

**Reason**: Enrollment data is too often a weakly governed top-of-funnel list. The enrolled population frequently includes open-registration discovery users (architects, designers, end consumers) who are not ERP buying accounts, making client-facing claims about enrollment conversion or onboarding velocity unreliable or misleading. The two enrollment architecture patterns observed across the 13-org validation set — dealer-controlled (high ERP match, e.g., `clli` at 98.9%) and open-registration (low ERP match, e.g., `jyc` at 8%) — produce such different data surfaces that a single enrollment metric framing does not hold consistently.

This is not a temporary data-quality gap. It is a scope boundary: external reports prefer omission over pseudo-precision when the denominator population cannot be reliably defined.

**For internal or future specialized use**: Q-15 and Q-44 remain in `query_library.md` tagged as `internal only`. Key findings from validation for future internal work:
- `enrollment_applicants.status` is not limited to `accepted / rejected / pending`; a `notified` status (pending-communication stage) was observed in org `ril`
- Two distinct enrollment architecture types exist: dealer-controlled (high match) and open-registration / public-facing (low match as expected structural outcome, not a data error)
- The `hideable = NULL` catalog visibility behavior is unrelated to enrollment but was also identified in the same validation set (see §3.5)

### 2.3 VM-38b: Pending engineering dependency

VM-38b (enhanced product velocity trend) depends on `invoice_date` being added to the `sales_data` table. This field does not currently exist in any tested org. VM-38b must remain `pending_engineering` until the schema is updated. Do not promote it to active status.

VM-38a (current-capability product velocity using `portal_order_items`) is available for orgs with B2B Cart data.

### 2.4 VM-19: Channel mix requires confirmed B2B Cart server orders

VM-19 should only render when `HAS_CART = true` AND confirmed server orders > 0. eCat Online - Catalog/Portal subscriptions provide read-only access and do not generate `order_source = 'server'` orders. Presence of "eCat Online" in `recurring_services` alone is insufficient to confirm B2B Cart eligibility — always verify actual server order count.

---

## 3. Query and Data-Quality Limitations

### 3.1 OOS × ERP join: absent sales history ≠ high-demand item

When joining out-of-stock catalog items to `sales_data` on `base_item_code`, a NULL result for `amount_invoiced` does not mean the item is a "best seller you can't sell." It may mean the item has no recent ERP sales history at all — it could be discontinued, archived, or low-velocity. Only surface OOS items as demand-impacting when the ERP sales-history join returns a non-NULL value with meaningful invoiced volume.

### 3.2 Duplicate quote clusters are a recurring data-quality pattern

Same-customer, same-amount, same-day order clusters (count ≥ 2) appear in approximately 4 of 6 commerce orgs tested. They range from incidental pairs (low risk) to rapid resubmissions within a 4-minute window (high risk of GMV overstatement). These must be flagged in the Appendix but should not be auto-excluded without human confirmation — some same-day same-amount orders are legitimate (multiple locations, multiple buyers, back-to-back event orders).

Sub-class: **rapid resubmission** — same customer, same total, 3+ orders within a 10-minute window. This pattern suggests accidental multi-tap or system retry behavior and should be elevated as a higher-confidence duplicate flag.

### 3.3 Zero-dollar orders appear occasionally but are rarely material

Zero-dollar orders appear in approximately 2 of 6 commerce orgs tested, typically representing less than 1% of order volume. At this rate they are not material to GMV calculations. If zero-dollar order volume exceeds 1% of total orders, investigate for marketing supply orders, sample requests, or import artifacts before surfacing GMV figures.

### 3.4 Showroom and internal operational accounts inflate rep volume

For accounts with large rep teams, accounts named with "showroom," "admin," "marketing," "training," "test," or "demo" patterns in the rep name fields may represent operational accounts placing floor set, sample, or training orders — not rep performance activity. These orders should be:

- **Included** in total org eCat GMV
- **Excluded** from individual rep leaderboard and performance rankings
- **Classified** in the Appendix as legitimate operational ordering or flagged for review

Exact exclusion logic (keyword matching rules, role-based verification) is still pending further validation (see Section 5).

### 3.5 `hideable = NULL` is the default product visibility state in many orgs

The `hideable` field on the `products` table has three possible values: `true` (explicitly hidden), `false` (explicitly visible), and `NULL` (not set — default state). In most production orgs, the majority of active products have `hideable = NULL`.

Filtering catalog completeness or visibility by `hideable = false` alone will return only the explicitly-visible products — in many cases near-zero — while the `hideable = NULL` products form the effective visible catalog. The correct logic is:

```sql
WHERE deleted = false AND (hideable = false OR hideable IS NULL)
```

Confirmed in the 11-org validation set: `ah` (1,799 of 1,810 products NULL), `fsf` (4,705 of 4,775 products NULL). `ril` is an exception — all 1,529 products have `hideable = false` explicitly set. This suggests the NULL default is tied to how products were initially imported, not a universal rule.

**Impact**: Catalog completeness scores computed from `hideable = false` only will be artificially low for affected orgs. The fix is to treat `NULL` as visible by default in all catalog visibility queries.

### 3.6 Numeric buyer-ID server orders are expected behavior for B2B Cart accounts

For accounts with `HAS_CART = true`, orders where `rep_first_name IS NULL` and `org_user_id` is a numeric integer represent buyers placing orders directly through the B2B Cart (eCat Online). This is not a data anomaly — it is the expected pattern for buyer-led self-service ordering. These orders should not be flagged as non-selling submitters or excluded from commerce analytics. They should be included in channel mix analysis as server-sourced orders.

---

## 4. Dependency Limitations

### 4.1 Clicky: row-level date duplication in BigQuery

In at least one tested org (`tel`), Clicky daily_metrics tables contain duplicate rows for the same date — in some cases the same day appears up to 11 times with identical values. SUM-based aggregate queries on these tables will overcount traffic significantly. All Clicky daily_metrics queries must use `GROUP BY date WITH MAX()` aggregation to deduplicate before summing across date ranges. Raw row counts or SUM across dates without deduplication are unreliable.

This pattern should be confirmed on additional Clicky-enabled orgs and investigated at the pipeline level.

### 4.2 Clicky: `bounce_rate` column scale is unconfirmed

The `bounce_rate` field in Clicky daily_metrics tables returns large integer values (e.g., 1,100–4,300) inconsistent with a standard fraction-based scale (0–1) or percentage-based scale (0–100). The correct interpretation of this column is unknown. It must be excluded from all report outputs and all calculations until the column scale is confirmed and documented by the team responsible for the Clicky BigQuery pipeline.

### 4.3 Clicky: Portal Engagement section — now validated on both lapsed and active-commerce accounts

The Portal Engagement section has been validated on four Clicky-enabled accounts across the full quality range:

- **`tel` (Tomlinson Companies)**: lapsed account (no orders since 2022), severely stale platform data. Confirmed: binary gate works correctly, dedup guard needed (up to 11 rows per date).
- **`ah` (Alfresco Home)**: healthy active-commerce account ($6.6M LTM GMV, 1,073 orders). Confirmed: Clicky data is clean and meaningful, dedup guard needed (up to 14 rows per date), portal traffic trends are coherent and interpretable.
- **`jyc` (Jamie Young Company)**: high-traffic active account (6,684–7,955 unique visitors/month, 6.5–7.2 min sessions, 8,334 eCat orders LTM). Confirmed: dedup guard active (up to 14 rows per date on a single day), declining traffic trend coexists cleanly with high-activity report narrative without contradiction.
- **`clli` (Craftmade)**: active specification-research portal (2,954–3,801 unique visitors/month, 7.9–9.7 min sessions). Confirmed: portal engagement output is coherent even when eCat order volume is low — the session quality signal stands independently of commerce volume.

The Portal Engagement section is **now considered production-stable**. The deduplication guard (`MAX()` per date) is confirmed as required across all tested accounts. `bounce_rate` exclusion remains in effect pending pipeline investigation.

**Cross-account Clicky pipeline gaps**: A data gap spanning approximately March 24–28, 2026 was observed simultaneously on both `jyc` and `clli`. This confirms that Clicky pipeline outages can affect multiple accounts in the same date window — the same gap is not necessarily org-specific. When a Clicky data gap is observed during validation, check whether the same window appears on adjacent Clicky-enabled orgs before classifying it as an account-level data issue.

### 4.4 Peer benchmark confidence varies by cohort specificity and size

**Upstream confidence thresholds (Peer Benchmark v1.1.0, canonical — internal reference only)**:

| `benchmark_confidence` | What drives it |
|---|---|
| `high` | Tier 1 cohort with ≥ 8 steady-state peers |
| `medium` | Tier 1 cohort with 5–7 steady-state peers |
| `low` | Tier 2 or Tier 3 fallback cohort, OR ramping org |
| `none` | Tier 4 — no viable cohort; section omitted |

`benchmark_confidence`, `peer_group_level`, and `peer_group_n` are **internal-only signals**. They are used to decide whether to include the Peer Benchmarking section and to calibrate plain-language framing — they must not appear as labels in client-facing output.

`low` does not always mean weak data. A Tier 3 bundle-only cohort may have a large `peer_group_n` — the iPad-only Tier 3 cohort has n=50, larger than many Tier 1 cohorts. The signal blends cohort specificity (tier/fallback level) and peer set stability (steady-state count). These two inputs can produce the same `low` value for very different underlying situations. `medium` is not universally "better" than `low` — it means Tier 1 at a moderate peer count, not a qualitatively superior comparison set in every case.

`peer_group_n` counts **steady-state peers only** — ramping/onboarding orgs are assigned to a cohort but not counted. A smaller-than-expected `peer_group_n` for a given cohort label is expected behavior, not a data gap. Use `peer_group_n` to calibrate the strength of plain-language framing; use `benchmark_confidence` to decide whether any caveat note is warranted. Treat percentile ranks cautiously when n < 5 regardless of confidence level. These rules are reflected in `authority/peer_benchmark.md` v2.2.

### 4.5 Peer benchmark metrics systematically undervalue quote-dominant and contract-sales accounts

The primary peer value metric (`orders_90d`) counts order submissions. For accounts operating a contract or specification-sales model — where reps submit high-value quotes rather than frequent standard orders — this metric will produce Q1 (bottom quartile) standings even when eCat GMV is high.

**Observed**: `ril` (Ratana International) had $17.5M eCat GMV but ranked Q1 on orders (329 vs. peer median of 1,421) because 89% of orders are quote-type at a $16K+ AOV.

When reporting peer benchmarking for quote-heavy accounts, include a framing note that the order-count metric reflects submission frequency, not GMV productivity. Catalog completeness, orders-per-user, and data freshness are more meaningful indicators for this account type. Do not let a Q1 order volume ranking be interpreted as a platform underperformance signal without this context.

---

## 5. Validation Gaps — Pending and Resolved

Items still pending have insufficient evidence to codify as universal rules. Do not hard-code them.

| Item | Status | What's needed |
|---|---|---|
| Exact duplicate-order exclusion rules | Pending | More instances; human review to distinguish legitimate same-day clusters from accidental resubmission |
| Exact zero-dollar order exclusion rules | Pending | More orgs; need to distinguish marketing/sample orders from data artifacts |
| Final showroom/admin/training exclusion logic | Pending | Need broader keyword pattern and role-based verification approach |
| Exact catalog visibility warning threshold | Pending | Only one critical gap observed (bri: 14/906 visible); threshold TBD |
| VM-44 / enrollment scope | **Closed** | Enrollment excluded from external report system as a deliberate scope decision. See §2.2. |
| Universal OOS contamination filters | Pending | Pattern confirmed; org-specific marketing SKU formats vary |
| Peer benchmark client framing edge cases | Pending | Core framing rules consolidated in `authority/peer_benchmark.md` §7; specific edge-case language for niche Tier 1 cohorts with n<5 TBD as more orgs are validated |
| Clicky Portal Engagement validation | **Resolved** | Validated across 4 accounts spanning the full quality range: `tel` (lapsed), `ah` (active), `jyc` (high-traffic), `clli` (specification portal). §6 is production-stable. Dedup guard confirmed required on all accounts. |
| Enrollment model type classification | **Closed** | Enrollment excluded from external report scope. Architecture findings (dealer-controlled vs. open-registration) retained in §2.2 for internal/future reference. |

---

*This document should be reviewed and updated after each cohort of 5–8 org runs.*
*It is a QA reference, not a runtime authority source.*
