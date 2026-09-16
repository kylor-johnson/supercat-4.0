# Health V3 Operator Audit — 2026-05-12

**Auditor:** Cursor Agent
**Operator file:** `Health V3/health_operator_v3.py`
**Spec file:** `Health V3/README.md` (v3.1.0, 2026-05-11)
**Scope:** Pure code review — no code changes made

**Legend:**
- **PASS** — implementation matches spec exactly
- **WARN** — differs from spec, but difference is minor or has a plausible justification worth noting
- **FAIL** — contradicts spec in a way that would produce incorrect scores

---

## §1 Engagement

### 1.1 `enabled_users` — NULL handling (`disabled IS NOT TRUE`)

**PASS**

The SQL uses `COALESCE(ou.disabled, false) = false`, which correctly treats `NULL` as not-disabled (i.e., enabled). This is semantically identical to `disabled IS NOT TRUE`. Rows where `ou.disabled IS NULL` are counted as enabled users, matching the spec's intent.

---

### 1.2 Internal domain exclusion

**PASS**

The `INTERNAL_DOMAINS` constant (`supercatsolutions.com`, `lojic.com`, `railsfever.com`, `samedis.com`, `jimmythrasher.com`, `upwardtechnologies.com`) is passed to the SQL as a parameterized `NOT IN` filter on `LOWER(SUBSTRING(u.email::text FROM '@(.+)$'))`. The set matches the list in §8 exactly. Users with no email record (`u.email IS NULL`) are correctly retained (counted as enabled, not excluded).

---

### 1.3 Denominator switch — `active_users_365d` fallback

**PASS**

Spec: "For Full and iPad+Catalog+Cart bundles where `enabled_users > 500`, the denominator switches to `active_users_365d`."

```python
INFLATED_DENOM_BUNDLES = frozenset({"Full", "iPad+Catalog+Cart"})
inflated = enabled > 500 and bundle in INFLATED_DENOM_BUNDLES
if (enabled == 0 or inflated) and fallback > 0:
    enabled = fallback
```

Both conditions (`enabled > 500` AND `bundle in INFLATED_DENOM_BUNDLES`) must be true. The bundle strings match the spec exactly. The additional `enabled == 0` branch (which fires when there are no provisioned users at all) is consistent with the spec's general fallback guidance in §1.

---

### 1.4 Login count bands

**PASS**

```python
LOGIN_BANDS = [(3000, 100), (1000, 88), (500, 75), (200, 60), (50, 40), (1, 20), (0, 0)]
```

Every boundary maps to the correct score per the spec table. The `band_score` function uses `value >= threshold` checked in descending order — boundary values land in the correct band (e.g., exactly 500 → 75, exactly 1000 → 88).

---

### 1.5 Active user ratio bands

**PASS**

```python
RATIO_BANDS = [(0.90, 100), (0.75, 82), (0.50, 65), (0.25, 45), (0.01, 20), (0, 0)]
```

Every boundary matches the spec table. At ratio = 0.25 → 45; at 0.249 → 20; at 0.0 → 0. The cap `ratio = min(raw_ratio, 1.0)` is applied before the band lookup, matching the spec's "capped at 100%" rule.

---

### 1.6 Velocity bands — boundary values and `(0.0, 10)` sentinel

**WARN**

The velocity bands constant:
```python
VELOCITY_BANDS = [(1.5, 100), (0.75, 90), (0.50, 60), (0.25, 30), (0.0, 10)]
```

Spec: "0 or undefined → 0". The last entry `(0.0, 10)` means that if `band_score` were called with `velocity_ratio = 0.0`, it would return **10** (since `0.0 >= 0.0` is `True`), which contradicts the spec.

The code guards against this with:
```python
velocity_score = band_score(velocity_ratio, VELOCITY_BANDS) if velocity_ratio > 0 else 0
```

The guard is correct and scores `velocity_ratio = 0.0` as **0** per the spec. The `logins_180d = 0` path also correctly sets `velocity_score = 0` and `velocity_ratio = None` before the band is ever consulted.

**The behavior is correct as written**, but the constant and the guard are tightly coupled: if a future maintainer changes the guard condition from `velocity_ratio > 0` to `velocity_ratio is not None` (a natural-looking refactor), `velocity_ratio = 0.0` would incorrectly score 10. The constant's comment (`# velocity_ratio > 0 → minimum 10; velocity_ratio = 0 or undefined → 0`) explains the intent, but the dependency is fragile.

---

### 1.7 Velocity formula and `logins_180d = 0` edge case

**PASS**

Formula is exactly `(logins_30d / logins_180d) × 6`:
```python
velocity_ratio = round((logins_30d / logins_180d) * 6, 2)
```

When `logins_180d = 0`:
```python
if logins_180d == 0:
    velocity_score = 0
    velocity_ratio = None
```

No division is attempted; `velocity_score = 0` and `velocity_ratio = None` as spec requires. No additional special handling is needed, and none is applied.

---

### 1.8 Engagement score formula — equal-weight average

**PASS**

```python
score = round((login_score + ratio_score + velocity_score) / 3, 1)
```

Exactly `(login_count_score + active_user_ratio_score + login_velocity_score) / 3` with equal weights.

---

## §2 Adoption

### 2.1 Sales Portal applicability gate

**PASS**

`enable_sales_portal` is read from `mobile_sites` via `BOOL_OR` aggregate in `load_pg_org_config`:
```sql
BOOL_OR(COALESCE(enable_sales_portal, false)) AS enable_sales_portal
FROM mobile_sites GROUP BY organization_id
```

Applied as: `features.append(("Sales Portal", esp, view_portal_90d > 0))` where `esp = bool(org_cfg.get("enable_sales_portal"))`. Correct table, correct flag.

---

### 2.2 Sales Portal usage signal — `view_portal_90d > 0` (Mixpanel), NOT `portal_orders_90d`

**PASS**

```python
view_portal_90d = int(mp_row.get("mp_view_portal_90d", 0) or 0)
features.append(("Sales Portal", esp, view_portal_90d > 0))
```

The BigQuery query computes `COUNTIF(event_name = 'view_portal') AS mp_view_portal_90d`. This correctly measures rep access to the Sales Portal section of the iPad app, independent of order volume — which is the spec's stated intent and the reason this signal is intentionally different from the `portal_orders_90d` signal used in §3.

---

### 2.3 Inventory Management applicability — trailing 180-day window

**PASS**

```python
inv_in_history = "Inventory" in import_types_active
```

`import_types_active` is built from `imp_pg` whose SQL filters `WHERE created_at >= NOW() - INTERVAL '180 days'`. A key of `"Inventory"` in this dict means at least one Inventory import ran in the trailing 180 days. This exactly matches the spec: "at least one Inventory `import_events` row in trailing 180 days."

---

### 2.4 `enable_sales_data` source — `organizations` table, not `mobile_sites`

**PASS**

```sql
COALESCE(o.enable_sales_data, false) AS enable_sales_data
FROM organizations o ...
```

`enable_sales_data` is read from `organizations o` (aliased `o.enable_sales_data`), not from `mobile_sites`. The other portal flags (`enable_online_catalog`, `enable_online_ordering`, `enable_sales_portal`) correctly come from `mobile_sites`. Both match §8.

---

### 2.5 `adoption_score` formula — no internal weighting

**PASS**

```python
score = round(len(used) / len(applicable) * 100, 1)
```

Exactly `(features_used / features_applicable) × 100` with no per-feature weighting.

---

## §3 Value Delivery

### 3.1 iPad orders filter — all three conditions

**PASS**

```sql
COUNT(*) FILTER (
  WHERE LOWER(order_source) = 'ipad' AND is_submitted = true
    AND order_state = 'active' AND submit_date >= NOW() - INTERVAL '90 days'
) AS ipad_orders_90d,
```

All three required conditions are present: `LOWER(order_source) = 'ipad'`, `is_submitted = true`, `order_state = 'active'`. The 90-day window is also applied at the SQL layer.

---

### 3.2 Sharing threshold — `>= 3` not `> 3`

**PASS**

```python
activities.append(("Sharing activity", True, mp_share_count >= 3))
```

Correctly uses `>= 3`.

---

### 3.3 iPad order threshold — `>= 10` not `> 10`

**PASS**

```python
activities.append(("Order volume (iPad)", True, ipad_orders_90d >= 10))
```

Correctly uses `>= 10`.

---

### 3.4 Sales Portal engagement — `portal_orders_90d > 0`, distinct from adoption signal

**PASS**

```python
activities.append(("Sales Portal engagement", esp, portal_orders_90d > 0))
```

Spec §3: "Sales Portal engagement: `portal_orders_90d > 0`". This is intentionally different from the Adoption signal (`view_portal_90d > 0`). The spec explicitly states: "Three channels can fire from the same underlying observation; that is intentional — they reflect three different config gates." The code implements this correctly.

---

### 3.5 Value delivery narrative — "Sales Portal engagement" gap description is misleading

**WARN**

When "Sales Portal engagement" is a gap (i.e., `portal_orders_90d = 0`), the narrative reads:

```python
if g == "Sales Portal engagement":
    return "Sales Portal is set up but reps haven't opened it in 90d"
```

The phrase "reps haven't opened it" characterizes the **Adoption** signal (`view_portal_90d > 0` — rep access via Mixpanel). The **Value Delivery** signal is `portal_orders_90d = 0` — absence of portal/B2B cart orders. The correct narrative should reference portal order volume (e.g., "Sales Portal is configured but no portal orders in 90d"), not rep-app-opening behavior.

This does not affect scoring — it is a narrative-only error. But CSMs reading this for a Sales Portal–enabled org with zero portal orders (but reps who do open the portal feature) will receive a misleading explanation.

---

### 3.6 `value_delivery_score` formula — no internal weighting

**PASS**

```python
score = round(len(achieved) / len(applicable) * 100, 1)
```

Exactly `(activities_achieved / activities_applicable) × 100` with no activity weighting.

---

## §4 Operational Health

### 4.1 Catalog completeness — price check OR logic

**PASS**

```sql
AND ( p.net_price > 0
      OR COALESCE(o.contract_pricing_enabled, false) = true
      OR (p.prices_json IS NOT NULL AND p.prices_json <> '{}'::text) )
```

All three conditions are present with correct OR logic. `prices_json != '{}'` is implemented as `<> '{}'::text`. `contract_pricing_enabled` is drawn from the joined `organizations` row. Contract-pricing and price-level-pricing orgs are not penalized for zero `net_price`.

---

### 4.2 Import health — excluded types correct in numerator/denominator but not in freshness

**PASS**

```python
EXCLUDED_IMPORT_TYPES_HEALTH = frozenset({
    "Multifile Import", "Import File Processing", "Product Image Downloads",
})

# Import health ratio:
scoreable_imports = [r for r in active_types
                     if r.get("import_type") not in EXCLUDED_IMPORT_TYPES_HEALTH]

# Freshness loop:
for r in active_types:   # <-- uses active_types, includes excluded types
    runs = r["run_count_180d"]
    ...
```

Excluded types are removed from `scoreable_imports` (used for the health ratio numerator and denominator), but `active_types` (used for the freshness loop) retains them. Exactly per spec: "These three types are excluded **only from the health ratio** — their `run_count_180d`, `first_run_at`, and `last_run_at` are still used by Sub-Signal 3 (Data Freshness)."

---

### 4.3 Freshness gap formula — mean vs. median

**WARN**

Spec: "Calculate the **gap denominator** ... Use the median; if `PERCENTILE_CONT()` is unavailable in the operator's SQL surface, fall back to mean gap."

Code always uses mean gap:
```python
mean_gap = days_span / max(runs - 1, 1)
```

This is `(last_run - first_run) / (runs - 1)`, i.e., the mean inter-run interval. The spec explicitly permits mean as a fallback when `PERCENTILE_CONT()` is unavailable. Since the operator uses Python/pandas (not raw SQL) for this computation, `PERCENTILE_CONT()` availability is not the constraint — a Python median is straightforward. The mean is therefore a permanent fallback rather than a forced one.

For feeds with evenly-spaced runs (daily/weekly imports), mean ≈ median. For bursty feeds with long gaps, median is more robust against outlier runs inflating the expected cadence. The practical effect is likely small but is directionally biased toward slightly longer estimated gaps for irregular feeds, producing slightly lower staleness ratios and slightly higher freshness scores than the spec-preferred calculation.

The 1-day floor is correctly applied: `gap = max(mean_gap, 1.0)`. ✓

---

### 4.4 Freshness initial-load carve-out — V3.0 bug fix

**PASS**

```python
if runs < 5 and days_span <= 7 and days_since_first <= 14:
    continue
```

All three conditions are present, including `days_since_first <= 14` — the fix from V3.0 that anchors the carve-out to *recent* bursts only. The prior buggy condition (algebraic identity that always fired) is not present.

---

### 4.5 Freshness weighting — `run_count_180d`

**PASS**

```python
fresh_entries.append((fscore, r["run_count_180d"], ...))
...
total_weight = sum(w for _, w, *_ in fresh_entries)
fresh_score = round(sum(s * w for s, w, *_ in fresh_entries) / total_weight, 1)
```

Weight is `run_count_180d`, not `run_count_90d`. The `total_weight = 0` fallback (unweighted average) is defensive and correct.

---

### 4.6 Freshness minimum history — `>= 3` runs

**PASS**

```python
if runs < 3:
    continue  # min history not met
```

Exactly "at least 3 import events of this type in 180d". Types with 0, 1, or 2 runs are excluded from the freshness average.

---

### 4.7 Operational health averaging — None-is-not-zero

**PASS**

```python
sub = []
if cat_score is not None:
    sub.append(("catalog", cat_score))
if scoreable_imports:
    sub.append(("imports", imp_score))
if fresh_entries:
    sub.append(("freshness", fresh_score))

if not sub:
    return None, {"reason": "no operational signals available"}

score = round(sum(s for _, s in sub) / len(sub), 1)
```

Only available sub-signals contribute to the average. When freshness has no qualifying types, `ops_score` is the average of only catalog + imports (denominator = 2, not 3). `None` is never treated as 0. When all three sub-signals are unavailable, `ops_score = None` is returned. All per spec.

---

## §5 Overrides

### 5.1 Ghost account — trigger conditions

**PASS**

```python
GHOST_ARR_THRESHOLD = 5000
ghost = bool(mal_row["arr"] >= GHOST_ARR_THRESHOLD and (eng_data.get("logins_90d") or 0) == 0)
```

Exactly `arr >= 5000 AND logins_90d = 0`. The `or 0` fallback handles the edge case where `eng_data` is empty (no login rows for this org), which correctly flags the org as having zero logins.

---

### 5.2 Ghost account — cap value and composite-is-None edge case

**PASS (cap) / WARN (edge case)**

```python
GHOST_CAP = 20
if composite_score is not None:
    composite_score = min(composite_score, GHOST_CAP)
else:
    composite_score = GHOST_CAP
```

The `min(score, 20)` cap is correct per spec.

**WARN:** The spec states "health_score is capped at `min(computed_health_score, 20)`" — which presupposes a computed composite. When `composite_score is None` (scoring_status = blocked; n=0 or n=1), the `else` branch assigns 20 directly. The spec is silent on this edge case (a ghost account with insufficient dimension data). The code's behavior is operationally reasonable — a ghost account must have an actionable Critical-band score regardless of dimension coverage — but it is not explicitly specified and changes the scoring_status semantics (the org's health_score is no longer null despite being "blocked").

---

### 5.3 Behavioral floor — trigger thresholds

**PASS**

```python
behavioral_floor_applied = bool(
    eng_score is not None and val_score is not None
    and eng_score < 55 and val_score < 40
)
```

Spec: "engagement_score < 55 AND value_delivery_score < 40". The engagement threshold is 55 (not 40). The spec explicitly confirms: "The engagement threshold is **55, not 40** — the higher value was confirmed during spot-check calibration (2026-05-11)... the operator has always implemented `< 55`, and the operator value is correct." Code matches the spec's confirmed value.

---

### 5.4 Behavioral floor — cap value

**PASS**

```python
BEHAVIORAL_FLOOR_CAP = 40.0
if behavioral_floor_applied and composite_score is not None:
    composite_score = min(composite_score, BEHAVIORAL_FLOOR_CAP)
```

Correctly `min(score, 40.0)`.

---

### 5.5 Override order of operations — behavioral floor first, then ghost

**PASS**

```python
# §5.2 behavioral floor override (applied first)
if behavioral_floor_applied and composite_score is not None:
    composite_score = min(composite_score, BEHAVIORAL_FLOOR_CAP)

# §5.1 ghost account override (applied second)
if ghost:
    if composite_score is not None:
        composite_score = min(composite_score, GHOST_CAP)
    else:
        composite_score = GHOST_CAP
```

Behavioral floor is applied before ghost account cap, exactly as specified: "The §5.2 Behavioral Floor override applies *after* the composite is computed and *before* the §5.1 Ghost Account override."

---

## §6 Composite

### 6.1 Composite formula — denominator = `dimensions_scored`

**PASS**

```python
def composite(eng, ado, val, ops):
    dims = [s for s in [eng, ado, val, ops] if s is not None]
    n = len(dims)
    if n == 0:
        return None, "blocked", 0
    if n == 1:
        return None, "blocked", 1
    score = round(sum(dims) / n, 1)
    status = "complete" if n == 4 else "partial"
    return score, status, n
```

Denominator is `n` = count of non-null scores. n=0,1 → blocked, null. n=2,3 → partial, average. n=4 → complete, average. `None` is never treated as 0.

---

### 6.2 Health bands assigned after overrides

**PASS**

```python
composite_score, status, n_dims = composite(...)
# ... overrides mutate composite_score ...
band = band_for_score(composite_score)   # called after both overrides
```

Band assignment occurs after both the behavioral floor and ghost caps are applied. A floored or capped score correctly maps to its post-override band.

---

## §8 Data Sources

### 8.1 Mixpanel org attribution

**PASS**

```sql
LOWER(COALESCE(NULLIF(organization_shortname, ''), NULLIF(current_organization_shortname, ''))) AS org_shortname
```

Exactly matches the spec: `LOWER(COALESCE(NULLIF(organization_shortname, ''), NULLIF(current_organization_shortname, '')))`. Both fields are coalesced with empty-string nullification before lowercasing.

---

### 8.2 Sharing event filter

**PASS**

```sql
WHERE event_name IN ('item_email_drafted', 'document_email_drafted', 'view_portal')
...
COUNTIF(event_name = 'item_email_drafted') AS mp_item_email_drafted_90d,
COUNTIF(event_name = 'document_email_drafted') AS mp_document_email_drafted_90d,
```

The `WHERE` clause includes `view_portal` to capture that event in the same query pass, but the sharing counts use `COUNTIF` on exactly `'item_email_drafted'` and `'document_email_drafted'` — no cross-contamination. The sum of these two columns is used for sharing in both Adoption and Value Delivery, matching the spec's `mp_sharing_events_90d` definition.

---

### 8.3 `view_portal` event filter

**PASS**

```sql
COUNTIF(event_name = 'view_portal') AS mp_view_portal_90d
```

Exact event name match. Used correctly in Adoption (`view_portal_90d > 0` for Sales Portal usage signal).

---

---

## Summary of Findings

### FAIL items
*None found.*

---

### WARN items (prioritized for next monthly run)

| Priority | Section | Item | Risk |
|----------|---------|------|------|
| 1 | §3 | **Value Delivery narrative for "Sales Portal engagement" misdescribes signal** | CSMs will see "reps haven't opened it in 90d" for an org with zero portal orders but active reps using the Sales Portal iPad feature. The signal is `portal_orders_90d = 0`, not `view_portal_90d = 0`. Narrative should read "Sales Portal is configured but no portal orders in 90d." | 
| 2 | §1 | **`VELOCITY_BANDS` constant has `(0.0, 10)` that fires incorrectly without its guard** | Behavior is correct today due to the `if velocity_ratio > 0 else 0` guard. Risk is that a future refactor changes the guard (e.g., to `if velocity_ratio is not None`) and silently scores velocity=0 orgs as 10 instead of 0. Consider either removing the `(0.0, 10)` entry and returning 0 from the `else` branch of `band_score`, or adding an inline assertion. |
| 3 | §4 | **Freshness always uses mean gap; spec preference is median** | Mean is the spec's permitted fallback, not the spec's preference. For feeds with bursty or irregular run timing, median is more robust. Since the gap computation is in Python (not SQL), `numpy.median` or `statistics.median` is trivially available. Low impact today; worth tracking if stale-feed detection proves unreliable. |
| 4 | §5.1 | **Ghost override sets `composite_score = 20` when composite is `None` (blocked)** | Spec says "capped at `min(computed, 20)`" but is silent when computed is null. The code assigns 20 directly. This is operationally defensible but changes the row's effective scoring_status: `scoring_status = "blocked"` but `health_score = 20`. If the reporting layer assumes `health_score is None` when `scoring_status = "blocked"`, this edge case could cause incorrect band display. Recommend documenting this behavior in a code comment. |

---

### Full PASS list (one-line confirmation)

- §1 `COALESCE(disabled, false) = false` — NULL treated as enabled ✓
- §1 `INTERNAL_DOMAINS` exclusion set and SQL parameterization ✓
- §1 Denominator switch: `enabled > 500 AND bundle in INFLATED_DENOM_BUNDLES` ✓
- §1 Login count bands — every boundary value ✓
- §1 Active user ratio bands — every boundary value ✓
- §1 Velocity formula: `(logins_30d / logins_180d) × 6` ✓
- §1 `logins_180d = 0` → `velocity_score = 0`, `velocity_ratio = None` ✓
- §1 Velocity bands 1.5/0.75/0.50/0.25 boundary values correct ✓
- §1 Engagement score: equal average of 3 sub-signals ✓
- §2 Sales Portal applicability: `enable_sales_portal` from `mobile_sites` ✓
- §2 Sales Portal usage signal: `view_portal_90d > 0` (Mixpanel, not `portal_orders`) ✓
- §2 Inventory Management applicability: trailing 180-day window ✓
- §2 `enable_sales_data` from `organizations` (not `mobile_sites`) ✓
- §2 `adoption_score` formula: features_used / features_applicable × 100 ✓
- §3 iPad orders: all three conditions (`LOWER(order_source)='ipad'`, `is_submitted=true`, `order_state='active'`) ✓
- §3 Sharing threshold `>= 3` ✓
- §3 iPad orders threshold `>= 10` ✓
- §3 Sales Portal value delivery: `portal_orders_90d > 0` (intentionally distinct from adoption signal) ✓
- §3 `value_delivery_score` formula: activities_achieved / activities_applicable × 100 ✓
- §4 Catalog price check: all three OR conditions present with correct logic ✓
- §4 Excluded import types: out of health ratio, retained in freshness ✓
- §4 Mean gap formula: `days_span / max(runs - 1, 1)` ✓
- §4 1-day gap floor: `gap = max(mean_gap, 1.0)` ✓
- §4 Initial-load carve-out: `runs < 5 AND days_span <= 7 AND days_since_first <= 14` (V3.0 bug fix confirmed) ✓
- §4 Freshness weighted by `run_count_180d` (not `run_count_90d`) ✓
- §4 Minimum history: `runs < 3` → excluded from freshness average ✓
- §4 Operational health: averages only available sub-signals; `None` ≠ 0 ✓
- §5.1 Ghost trigger: `arr >= 5000 AND logins_90d = 0` ✓
- §5.1 Ghost cap: `min(score, 20)` ✓
- §5.2 Behavioral floor trigger: `engagement_score < 55 AND value_delivery_score < 40` (55, not 40) ✓
- §5.2 Behavioral floor cap: `min(score, 40.0)` ✓
- §5 Override order: behavioral floor applied before ghost account cap ✓
- §6 Composite denominator = `dimensions_scored` (non-null count only) ✓
- §6 `scoring_status`: complete/partial/blocked at n=4/2–3/0–1 ✓
- §6 Health bands assigned after both override caps ✓
- §8 Mixpanel org attribution: `LOWER(COALESCE(NULLIF(...), NULLIF(...)))` ✓
- §8 Sharing filter: `item_email_drafted` + `document_email_drafted` via `COUNTIF` ✓
- §8 `view_portal` event filter exact match ✓
