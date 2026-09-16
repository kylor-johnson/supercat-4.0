# Narrative Fix Review — 2026-05-12

Status check on the narrative fix agent and composite narrative agent outputs.
Reviewed against `health_operator_v3.py` (current) and the v3.2-composite-narrative CSV.

---

## FIXED

None confirmed. All five narrative fixes listed below were **not applied** to the current operator. The narrative fix agent either targeted a different file, did not write its changes, or did not save. The code as it stands today is pre-fix.

---

## NOT FIXED

### Fix 1 — Ops narrative: surface individual feed outliers when aggregate passes

**Status: NOT FIXED**

The freshness block in `_build_ops_narrative` (lines 344–360) still short-circuits to `"data feeds running on cadence"` whenever `fresh_score >= 80`, without checking `stale_feeds` for individual outlier feeds:

```python
if fresh_score >= 80:
    parts.append(f"data feeds running on cadence")
elif stale_feeds:
    worst = max(stale_feeds, key=lambda x: x[1])
    ...
```

If any feed in `stale_feeds` has `staleness_ratio > 4.0` but the weighted aggregate is still `>= 80`, it is silently dropped. `asi`'s v3.2 output confirms the bug is live: Portal Invoices is 5× overdue yet the ops narrative reads `data feeds running on cadence`.

**Required fix:** Before emitting the "on cadence" phrase, check `stale_feeds` for any entry with `stale_ratio > 4.0`. If present, emit a named-outlier sentence alongside (or instead of) the healthy summary.

---

### Fix 2 — Severity language: "declining" vs "critical" for per-feed staleness

**Status: NOT FIXED**

Urgency is still derived from the aggregate `fresh_score`, not the worst feed's individual `staleness_ratio`:

```python
urgency = "critical" if fresh_score < 30 else "declining"
```

`sbl`'s Customers feed is 141 days stale (141× overdue). The v3.2 output confirms: `data freshness declining — the Customers feed last ran 141d ago against a ~1d expected cadence`. "Declining" for a feed that has not run in five months is incorrect.

**Required fix:** `urgency = "critical" if stale_ratio > 4.0 else "declining"` where `stale_ratio` is `worst[1]` (the worst feed's per-feed ratio, already computed on line 349), not the aggregate score.

---

### Fix 3 — Adoption narrative: truncates at two unused features

**Status: NOT FIXED**

The narrative join still caps at two feature messages:

```python
top_msgs = "; ".join(feature_msgs[:2])
```

For `ihm`, which has three unused features (Smart Stacks, Inventory Management, Sales Data), the output is: `Smart Stacks haven't been used — a CS demo of the feature could unlock this; Inventory Management feed has gone quiet — no imports in 90 days.` Sales Data is silently dropped. The adoption score is `2 of 5 features` (three unused), but a CS rep reading the narrative would see only two.

**Required fix:** Either remove the `[:2]` slice, or add a trailing phrase like `"(+1 more)"` when `len(feature_msgs) > 2`.

---

### Fix 4 — Engagement urgency language for cooling 2024+ cohorts

**Status: NOT FIXED**

`_build_engagement_narrative` does not accept `value_delivery_score` or `cohort_year` as parameters. The velocity label at cooling-off range still reads `"cooling off — worth monitoring at {ratio:.1f}x baseline"` regardless of cohort or outcome context. `ihm`'s v3.2 output: `Pace is cooling off — worth monitoring at 0.6x baseline.` — same mild language.

**Required fix:** Add `value_delivery_score` and `cohort_year` parameters to `_build_engagement_narrative` (propagated from the scoring loop). When `velocity_ratio < 0.65 AND value_delivery_score < 40 AND cohort_year >= 2023`, escalate language to something like: `"cooling off at {ratio:.1f}x — a 2024 cohort with zero orders and declining velocity warrants immediate CS review"`.

Note: this is a cross-dimension coupling in a per-dimension function. See **DISCUSS** section.

---

### Fix 5 — Ops narrative: day count omitted for errored imports with stale last run

**Status: NOT FIXED**

The import health sub-signal narrative (lines 330–341) never includes a day count:

```python
parts.append(
    f"{n_healthy} of {n_total} import feeds healthy; "
    f"{errored_str} last ran with errors"
)
```

`dals`'s v3.2 output: `0 of 1 import feeds healthy; Products last ran with errors.` — no mention that Products hasn't run in 75 days. The Products feed also does not appear in the freshness sub-signal for `dals` (likely insufficient run history), so the day count is never surfaced anywhere in the ops narrative.

**Required fix:** When building the errored feed list, include `days_since_last_run` for any errored feed where that value exceeds 60. Requires joining import error data with the `days_since_last` computed during freshness scoring, or querying the value separately.

---

## COMPOSITE NARRATIVE: PASS / NEEDS WORK

| Org | Score | Band | Result | Notes |
|-----|-------|------|--------|-------|
| **ih** | 97.5 | Thriving | **PASS** | 3 sentences, accurate, all-green. No action needed. |
| **clm** | 85.3 | Thriving | **PASS** | 4 sentences, "Monitor closely" on the 9% user penetration is the right call. Multifile Import freshness issue is a scoring model concern (Flag D), not a narrative failure. |
| **ml** | 69.4 | Healthy | **PASS** | 4 sentences, correctly names ops as strength and value delivery as drag, action-forward. |
| **sbl** | 84.0 | Thriving | **NEEDS WORK** | Correctly names ops as drag and directs to data team, but "Flag the ops issues" undersells severity: 4 of 6 feeds broken, Customers 141× overdue. Language should match Fix 2 once that's applied. Also: does not flag the sbl-type anomaly (Thriving with majority feeds broken) — by design, but worth a note in output. |
| **asi** | 83.7 | Thriving | **NEEDS WORK** | Composite is accurate to the scores it received, but the underlying ops narrative is wrong (Fix 1 not applied). "data feeds running on cadence" fed a false-clean signal upstream; the composite can't correct for a broken input. Once Fix 1 lands, ops will drop and the composite pattern will likely shift. |
| **ihm** | 54.7 | Watch | **NEEDS WORK** | Fires Pattern 3 ("reps logging in consistently, feature adoption gap"). "Consistently" overstates 80 logins from 21 reps at 0.6× velocity. The 2024 cohort + zero iPad orders + cooling velocity is an urgency signal the composite misses entirely — a CS reader gets a coaching-opportunity framing on what is arguably a near-dormant account. |
| **dals** | 43.8 | Watch | **NEEDS WORK** | Fires Pattern 4 ("platform is generating outcomes, but engagement thin"). "Value delivery (50) is holding its own" is misleading — 50 means only 1 of 2 channels producing outcomes (inventory flowing, zero iPad orders). More critically, the composite narrative never mentions ops at 10/100 with catalog at 33% and a broken Products import. Pattern 4 doesn't have an ops-warning injection when `ops_score < 20`. A CS rep reading only the composite would not know the data infrastructure is in critical condition. |

---

## V3.2 FLAGS: CAPTURED / NOT CAPTURED

| Flag | Description | Status |
|------|-------------|--------|
| **Flag A** | sbl-type: account scores Thriving despite majority import feeds failing — no composite guard | **NOT CAPTURED** — not documented in METHODOLOGY.md, README.md, or the operator as a TODO/comment. |
| **Flag B** | ihm-type: import health passes despite universal staleness (stale-but-not-errored feeds not detected) | **NOT CAPTURED** — not documented anywhere. |
| **Flag C** | Active-user denominator inflation for `iPad+Catalog+Portal` bundles with >500 enabled_users | **NOT CAPTURED** — README.md documents the denominator switch for `Full` and `iPad+Catalog+Cart` bundles only; `iPad+Catalog+Portal` is not listed in `INFLATED_DENOM_BUNDLES` and the gap is not flagged as a known limitation. |
| **Flag D** | Multifile Import burst-weight persisting for 180 days after a feed is retired | **NOT CAPTURED** — not in METHODOLOGY.md, README.md, or the operator. `clm`'s ops narrative (`data freshness critical — the Multifile Import feed last ran 29d ago`) is a live example. |
| **Flag E** | Sharing threshold ≥3 events is below workflow-level (~10 events) | **CAPTURED** — METHODOLOGY.md §7, lines 208–215 explicitly documents this as a planned V3.2 refinement. |

---

## DISCUSS

**1. The fix agent did not apply any of the five fixes.**
All five issues remain in the code exactly as originally identified. Before re-running the narrative fix agent, confirm it is writing to `Health V3/health_operator_v3.py` and not a temp copy or different path. Verify the file's `git diff` after the next run.

**2. Fix 4 requires an architectural decision, not just a line change.**
Escalating urgency for `cohort_year >= 2023 AND velocity < 0.65 AND value_delivery < 40` requires `_build_engagement_narrative` to receive cross-dimension context. Currently, each narrative function is isolated — it only sees its own dimension's inputs. Three options: (a) pass `value_delivery_score` and `cohort_year` as extra parameters to the engagement narrative function; (b) apply the urgency escalation post-hoc in the scoring loop after all four narratives are built; (c) handle it in `_build_composite_narrative` instead and leave dimension narratives single-dimension. Option (b) is cleanest — a single post-processing step that rewrites the engagement narrative when the cross-dimension flag pattern fires. Option (a) works but couples the function signature to other dimension outputs. **This needs a human call before code is written.**

**3. `dals` composite narrative pattern mismatch.**
Pattern 4 fires when `e < 55 AND v >= 50`. For `dals` (e=40, v=50, ops=10), the pattern correctly identifies engagement as the structural gap but the "platform is generating outcomes" framing is misleading when ops is at 10. Pattern 4 should inject an ops-warning sentence when `ops_score < 30`. This is a composite narrative logic change, not a dimension narrative fix.

**4. Flags A–D have no home.**
Four model behavior flags from the findings report are not documented anywhere. They need to land in METHODOLOGY.md (§8 "What This Is Not" or a new §9 "Known Limitations and V3.2 Roadmap") before they get lost. Suggested format: a table with flag description, affected account type, severity, and planned version. This is documentation work, not code work.

**5. `sbl` Thriving band with 4/6 feeds broken is a legitimate CS confusion risk.**
A CSM receiving a Thriving account with a 141× overdue feed and four broken imports will reasonably question the score. Even if the math is correct (engagement and usage are genuinely high), the ops ops_score of 55 is not communicating the severity. This is partly a Fix 2 issue (urgency language), partly a Flag A issue (no composite guard for this pattern), and partly a customer-communication issue. Worth a short explicit conversation before the June run.
