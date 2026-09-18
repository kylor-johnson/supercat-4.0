# W3 evidence — Phase 5: de-Sarreid the signal constants

Branch `exec/W3` · worked 2026-09-18 · fully offline from `pipeline/cache/`.

> **Read this first.** W3 ships the **mechanism** with `ACTIVE_PROFILE =
> BASELINE_PROFILE` — every size-relative percentage dormant, every absolute
> floor unchanged. `make check` is green: golden `PASS (11/11)`, cohort
> **no change**. W3's proposal lives beside it as `RECOMMENDED_PROFILE` and is
> **not active**. Flipping one line in `pipeline/signals.py` turns it on; §7
> shows exactly what that does to all eleven orgs, read end to end.

---

## 1. Files changed

| File | What changed | In the brief's scope list? |
|---|---|---|
| `pipeline/signals.py` | Classification comment; `SizeScaledFloor` / `Thresholds` / `ThresholdProfile`; `BASELINE_PROFILE`, `RECOMMENDED_PROFILE`, `ACTIVE_PROFILE`; `org_size_base`, `resolve_thresholds`; `CoachingCard` + `coaching_card_reps`; eight detectors take `thresholds`; four inline magic numbers named | yes |
| `pipeline/fact_bundles.py` | `play_upside_ceiling()`; `build_plays_from_gather` drops a play below the org's floor | yes |
| `pipeline/availability.py` | `SectionAvailability.thresholds` and `.coaching_cards` — the only route a Jinja template has to a constant | yes ("if a card gate moves") |
| `pipeline/templates/_macros.md.j2` | `hero_finding(…, thresholds)`; the hard-coded cross-sell floor of 3 is **deleted** | yes |
| `pipeline/templates/section_01_hero.md.j2` | passes `availability.thresholds`; S3 same-dealer measure is a profile choice | yes |
| `pipeline/templates/section_06_team.md.j2` | coaching cards render from `availability.coaching_cards` instead of re-deriving the gate | **scope call — see §2** |
| `pipeline/run_report.py` | `card_reps` reads `signals.coaching_card_reps`, and plays get the resolved thresholds | **out of scope — see §2** |
| `report_render/sections.py`, `report_render/html_renderer.py` | a CEO-callout jump link is dropped when its target section did not render | **out of scope — see §2** |
| `tests/test_phase5_size_scaling.py` | 35 new tests | yes |
| `AUDIT_FINDINGS.md` | §2.1 rewritten to describe the mechanism that now exists | yes |

Nothing else was touched. `config/golden_set.json`, `foundation/**`,
`operators/**`, `pipeline/cache/**` and `outputs/*_prose_*.json` are unchanged.

---

## 2. Three edits outside the literal scope list, and why

The brief's scope list excludes `pipeline/templates/**` and `report_render/**`
"unless a template reads a constant directly", and does not name
`pipeline/run_report.py` at all. Three edits crossed that line. Each is stated
here rather than buried in the diff; the reviewer should reject any of them
they disagree with — none is load-bearing for the mechanism itself.

**a. `pipeline/templates/section_06_team.md.j2` — the coaching-card gate.**
S2 is a DoD line, and the cards live only here. The template used to compute
its own card set inline (`gather.rep_risks | selectattr("accounts_at_risk",
"gt", 0)`) and its own "which account is this card about" rule
(`sort(attribute="ltm_rev") | first`). Both are now decided in `signals.py`
and read from `availability.coaching_cards` — so the template *does* read a
constant, through the same route the hero does. Net effect on the template: it
got shorter.

**b. `pipeline/run_report.py` — `card_reps`.**
`run_report.py:242` kept a **parallel copy** of the card-selection rule. It
feeds `build_coaching_bundle`, `expected_counts.coaching_narratives` and
`align_coaching_narratives` — which keys authored Slot-C prose to cards **by
list position**. Leaving it would have created exactly the sixth definition the
brief forbids, and the first time the owner moved the gate the coaching
narratives would have silently attached to the wrong reps. Two lines.

**c. `report_render/sections.py` + `html_renderer.py` — dangling jump anchors.**
This one was **found by the work, not assumed**. With `play_min_upside` set to
W3's recommendation, hfg and clc correctly produce zero plays, `_base.md.j2`
correctly omits §3 — and both orgs then **failed step10 check [12]**:

```
FAIL  Hubbardton_Forge_CEO_intelligence_report_2026-07-02.html  · failed checks: ['12']
  - [12] broken in-doc anchor '#thismonth' (label: 'Build the push →')
```

`sections._callout_jump` picked an anchor from the callout's wording with no
regard for which sections existed. "No play qualified this month" was therefore
**not a reachable state** — it produced a broken artifact. The fix is a
fallback: skip candidates whose section did not render, and emit no link rather
than a dead one. `available_ids=None` (every pre-existing caller, and all three
`render_summary` tests in `tests/test_sections_summary.py`) keeps the old
behaviour byte-for-byte; the cohort proves it.

---

## 3. Classification — every gate in `pipeline/signals.py`

The brief: *"Say which category each constant is in before you touch it."*

### SIZE-NEUTRAL — a ratio. Left alone.

| Constant | Value | Why it is not overfit to size |
|---|---|---|
| `DECLINE_PACE_THRESHOLD` | 0.6 | "recent is 60% of prior" means the same at $3M and $70M |
| `CADENCE_CLIFF_GAP_MULTIPLIER` | 2.0 | multiple of the account's **own** mean gap |
| `GROWTH_POCKET_MIN_YOY_PCT` | 20.0 | percentage growth |
| `LIFT_CONC_TOP5_THRESHOLD` | 60.0 | share of lift |
| `REP_OVERPERFORM_MIN_YOY` / `REP_UNDERPERFORM_MAX_YOY` | +30 / −20 | percentages |
| `CHANNEL_CONC_THRESHOLD` | 70.0 | share of booked revenue |
| `ECAT_MINORITY_THRESHOLD` | 15.0 | share of invoiced LTM |
| `LEAKAGE_LOW_THRESHOLD` | 3.0 | share of invoiced LTM |
| `SECOND_YEAR_RETURN_THRESHOLD` | 0.50 | a rate |
| `PRICING_PLAY_MIN_LEAK_SPREAD_PCT` | 10.0 | was an inline `<= 10`; now named. A rate. |
| `CROSS_SELL_ADDRESSABLE_FRACTION` | 0.30 | an editorial multiplier, not a gate |
| `PROJECT_MIN_SHARE_OF_LTM` / `PROJECT_MIN_UNIT_PRICE_RATIO` | 3% / 8× | already relative — W1 built them this way |

These may still be mis-tuned. That is not W3's question, and none was changed.

### SIZE-DEPENDENT — an absolute dollar floor or a raw count. Converted.

| Constant | 4.0 value | Base it now scales on | Sweep |
|---|---|---|---|
| `DECLINE_MIN_LTM_DOLLARS` | $50,000 | invoiced LTM | §4.1 |
| `REP_ATRISK_MIN_DOLLARS` | $20,000 | invoiced LTM | §4.2 |
| `coaching_card_min_dollars` | *(none existed)* | invoiced LTM | §4.3 — **S2** |
| `PLAY_MIN_UPSIDE_DOLLARS` | *(none existed)* | invoiced LTM | §4.7 — **S1** |
| `NEW_LINE_MIN_REVENUE` | $100,000 | invoiced LTM | §4.4 |
| `REP_BOOK_MIN_DOLLARS` | $100,000 (was an inline `100_000`, twice) | invoiced LTM | §4.5 |
| `SECOND_YEAR_MIN_LAPSED_DOLLARS` | $50,000 (was an inline `50_000`) | invoiced LTM | §4.6 |
| `GROWTH_POCKET_MIN_DEALERS` | 10 | active dealers | §4.8 |
| `NEW_LINE_MIN_DEALERS` | 5 | active dealers | §4.9 |
| `CROSS_SELL_MIN_TARGET_DEALERS` | 5 (was an inline `< 5`) | active dealers | §4.10 |
| `CROSS_SELL_HERO_MIN_DEALERS` | 3 (the `_macros.md.j2` stopgap) | active dealers | §4.11 |

Two size bases, because the gates are overfit in two different ways. A dollar
floor is overfit to the **topline**; a raw dealer count is overfit to the
**base width**. Ten dealers is 0.13% of cci's active base and 1.75% of kal's.

### The form

```python
threshold = max(ABSOLUTE_FLOOR, PCT_OF_BASE × base)     # SizeScaledFloor.resolve
```

`pct = 0.0` leaves the floor alone and is exactly 4.0 — that is what BASELINE
ships. A base that is missing, zero, negative, NaN or infinite degrades to the
floor, so `commerce_confidence = NONE` orgs (`da`, `sca`, `bsc`, all at
`inv_ltm_net = 0`) never divide and never lose their floor.

No percentile-of-distribution gate was added. The cached extracts are already
top-N truncated (`S1` carries 10–12 accounts, `C2` 11–12 reps, `Q-PROD-TOP` 25
items) so a percentile taken over them would be a percentile of the *head*, not
of the org. W1's `unit_price_ratio` works because the catalog median is
computed over a full top-25 price list; nothing else here has an equivalent.

---

## 4. The calibration sweep — 11 orgs × 4 candidate values × every converted constant

Produced by an in-process harness (`preflight.run` + `gather.gather_all` once
per org, then each candidate resolved and the affected detector re-run). Cell
format: **`<signals fired> @ <resolved threshold>`**. The `<details>` block
under each table carries the top-ranked item per org per value, so the owner
can see whether what fires is worth saying.

Org size, for reading every table below:

| org | invoiced LTM | active dealers | commerce confidence |
|---|---|---|---|
| cci | $70.02M | 7,570 | STRONG |
| clc | $58.93M | 1,487 | STRONG |
| hfg | $41.17M | 2,422 | STRONG |
| bri | $21.25M | 1,286 | STRONG |
| sarreid | $15.77M | 1,399 | STRONG |
| kal | $8.76M | 572 | STRONG |
| ali | $7.34M | 1,004 | STRONG |
| bmc | $6.94M | 879 | PARTIAL |
| da / sca / bsc | $0 | 0 | NONE |

### 4.1 `DECLINE_MIN_LTM_DOLLARS` — real_decline account floor  (base: invoiced LTM)

| org | inv LTM | active dealers | BASELINE $50K / 0% | A $25K / 0.05% | B $25K / 0.10% | C $50K / 0.25% |
|---|---|---|---|---|---|---|
| sarreid | $15.77M | 1,399 | 5 @ 50,000 | 9 @ 25,000 | 9 @ 25,000 | 5 @ 50,000 |
| cci | $70.02M | 7,570 | 2 @ 50,000 | 2 @ 35,008 | 2 @ 70,016 | 1 @ 175,040 |
| da | $0 | 0 | 0 @ 50,000 | 0 @ 25,000 | 0 @ 25,000 | 0 @ 50,000 |
| clc | $58.93M | 1,487 | 1 @ 50,000 | 1 @ 29,465 | 1 @ 58,930 | 1 @ 147,325 |
| hfg | $41.17M | 2,422 | 4 @ 50,000 | 4 @ 25,000 | 4 @ 41,170 | 4 @ 102,925 |
| kal | $8.76M | 572 | 5 @ 50,000 | 6 @ 25,000 | 6 @ 25,000 | 5 @ 50,000 |
| ali | $7.34M | 1,004 | 3 @ 50,000 | 4 @ 25,000 | 4 @ 25,000 | 3 @ 50,000 |
| sca | $0 | 0 | 0 @ 50,000 | 0 @ 25,000 | 0 @ 25,000 | 0 @ 50,000 |
| bsc | $0 | 0 | 0 @ 50,000 | 0 @ 25,000 | 0 @ 25,000 | 0 @ 50,000 |
| bmc | $6.94M | 879 | 7 @ 50,000 | 7 @ 25,000 | 7 @ 25,000 | 7 @ 50,000 |
| bri | $21.25M | 1,286 | 7 @ 50,000 | 7 @ 25,000 | 7 @ 25,000 | 7 @ 53,122 |

<details><summary>top-ranked item per org per value</summary>

| org | value | fired | top-ranked |
|---|---|---|---|
| sarreid | BASELINE $50K / 0% | 5 | Account 29925 down 56% H/H |
| sarreid | A $25K / 0.05% | 9 | Account 29925 down 56% H/H |
| sarreid | B $25K / 0.10% | 9 | Account 29925 down 56% H/H |
| sarreid | C $50K / 0.25% | 5 | Account 29925 down 56% H/H |
| cci | BASELINE $50K / 0% | 2 | Account GOFRAN down 41% H/H |
| cci | A $25K / 0.05% | 2 | Account GOFRAN down 41% H/H |
| cci | B $25K / 0.10% | 2 | Account GOFRAN down 41% H/H |
| cci | C $50K / 0.25% | 1 | Account GOFRAN down 41% H/H |
| da | BASELINE $50K / 0% | 0 | — |
| da | A $25K / 0.05% | 0 | — |
| da | B $25K / 0.10% | 0 | — |
| da | C $50K / 0.25% | 0 | — |
| clc | BASELINE $50K / 0% | 1 | Account IBS002353 down 62% H/H |
| clc | A $25K / 0.05% | 1 | Account IBS002353 down 62% H/H |
| clc | B $25K / 0.10% | 1 | Account IBS002353 down 62% H/H |
| clc | C $50K / 0.25% | 1 | Account IBS002353 down 62% H/H |
| hfg | BASELINE $50K / 0% | 4 | Account 37085 down 81% H/H |
| hfg | A $25K / 0.05% | 4 | Account 37085 down 81% H/H |
| hfg | B $25K / 0.10% | 4 | Account 37085 down 81% H/H |
| hfg | C $50K / 0.25% | 4 | Account 37085 down 81% H/H |
| kal | BASELINE $50K / 0% | 5 | Account 0003476 down 84% H/H |
| kal | A $25K / 0.05% | 6 | Account 0003476 down 84% H/H |
| kal | B $25K / 0.10% | 6 | Account 0003476 down 84% H/H |
| kal | C $50K / 0.25% | 5 | Account 0003476 down 84% H/H |
| ali | BASELINE $50K / 0% | 3 | Account  down 100% H/H |
| ali | A $25K / 0.05% | 4 | Account  down 100% H/H |
| ali | B $25K / 0.10% | 4 | Account  down 100% H/H |
| ali | C $50K / 0.25% | 3 | Account  down 100% H/H |
| sca | BASELINE $50K / 0% | 0 | — |
| sca | A $25K / 0.05% | 0 | — |
| sca | B $25K / 0.10% | 0 | — |
| sca | C $50K / 0.25% | 0 | — |
| bsc | BASELINE $50K / 0% | 0 | — |
| bsc | A $25K / 0.05% | 0 | — |
| bsc | B $25K / 0.10% | 0 | — |
| bsc | C $50K / 0.25% | 0 | — |
| bmc | BASELINE $50K / 0% | 7 | Account 224190 down 42% H/H |
| bmc | A $25K / 0.05% | 7 | Account 224190 down 42% H/H |
| bmc | B $25K / 0.10% | 7 | Account 224190 down 42% H/H |
| bmc | C $50K / 0.25% | 7 | Account 224190 down 42% H/H |
| bri | BASELINE $50K / 0% | 7 | Account 038017 down 48% H/H |
| bri | A $25K / 0.05% | 7 | Account 038017 down 48% H/H |
| bri | B $25K / 0.10% | 7 | Account 038017 down 48% H/H |
| bri | C $50K / 0.25% | 7 | Account 038017 down 48% H/H |

</details>

### 4.2 `REP_ATRISK_MIN_DOLLARS` — rep_atrisk_book SIGNAL floor  (base: invoiced LTM)

| org | inv LTM | active dealers | BASELINE $20K / 0% | A $10K / 0.05% | B $10K / 0.10% | C $20K / 0.25% |
|---|---|---|---|---|---|---|
| sarreid | $15.77M | 1,399 | 3 @ 20,000 | 6 @ 10,000 | 4 @ 15,767 | 0 @ 39,418 |
| cci | $70.02M | 7,570 | 4 @ 20,000 | 2 @ 35,008 | 0 @ 70,016 | 0 @ 175,040 |
| da | $0 | 0 | 0 @ 20,000 | 0 @ 10,000 | 0 @ 10,000 | 0 @ 20,000 |
| clc | $58.93M | 1,487 | 11 @ 20,000 | 10 @ 29,465 | 2 @ 58,930 | 2 @ 147,325 |
| hfg | $41.17M | 2,422 | 1 @ 20,000 | 1 @ 20,585 | 0 @ 41,170 | 0 @ 102,925 |
| kal | $8.76M | 572 | 0 @ 20,000 | 1 @ 10,000 | 1 @ 10,000 | 0 @ 21,903 |
| ali | $7.34M | 1,004 | 1 @ 20,000 | 1 @ 10,000 | 1 @ 10,000 | 1 @ 20,000 |
| sca | $0 | 0 | 0 @ 20,000 | 0 @ 10,000 | 0 @ 10,000 | 0 @ 20,000 |
| bsc | $0 | 0 | 0 @ 20,000 | 0 @ 10,000 | 0 @ 10,000 | 0 @ 20,000 |
| bmc | $6.94M | 879 | 3 @ 20,000 | 8 @ 10,000 | 8 @ 10,000 | 3 @ 20,000 |
| bri | $21.25M | 1,286 | 12 @ 20,000 | 12 @ 10,624 | 12 @ 21,249 | 3 @ 53,122 |

<details><summary>top-ranked item per org per value</summary>

| org | value | fired | top-ranked |
|---|---|---|---|
| sarreid | BASELINE $20K / 0% | 3 | Rep 099 carries $36K at-risk book |
| sarreid | A $10K / 0.05% | 6 | Rep 099 carries $36K at-risk book |
| sarreid | B $10K / 0.10% | 4 | Rep 099 carries $36K at-risk book |
| sarreid | C $20K / 0.25% | 0 | — |
| cci | BASELINE $20K / 0% | 4 | Rep SBAK carries $66K at-risk book |
| cci | A $10K / 0.05% | 2 | Rep SBAK carries $66K at-risk book |
| cci | B $10K / 0.10% | 0 | — |
| cci | C $20K / 0.25% | 0 | — |
| da | BASELINE $20K / 0% | 0 | — |
| da | A $10K / 0.05% | 0 | — |
| da | B $10K / 0.10% | 0 | — |
| da | C $20K / 0.25% | 0 | — |
| clc | BASELINE $20K / 0% | 11 | Rep 81 carries $203K at-risk book |
| clc | A $10K / 0.05% | 10 | Rep 81 carries $203K at-risk book |
| clc | B $10K / 0.10% | 2 | Rep 81 carries $203K at-risk book |
| clc | C $20K / 0.25% | 2 | Rep 81 carries $203K at-risk book |
| hfg | BASELINE $20K / 0% | 1 | Rep CANOREP carries $22K at-risk book |
| hfg | A $10K / 0.05% | 1 | Rep CANOREP carries $22K at-risk book |
| hfg | B $10K / 0.10% | 0 | — |
| hfg | C $20K / 0.25% | 0 | — |
| kal | BASELINE $20K / 0% | 0 | — |
| kal | A $10K / 0.05% | 1 | Rep 0999 carries $12K at-risk book |
| kal | B $10K / 0.10% | 1 | Rep 0999 carries $12K at-risk book |
| kal | C $20K / 0.25% | 0 | — |
| ali | BASELINE $20K / 0% | 1 | Rep 29 carries $21K at-risk book |
| ali | A $10K / 0.05% | 1 | Rep 29 carries $21K at-risk book |
| ali | B $10K / 0.10% | 1 | Rep 29 carries $21K at-risk book |
| ali | C $20K / 0.25% | 1 | Rep 29 carries $21K at-risk book |
| sca | BASELINE $20K / 0% | 0 | — |
| sca | A $10K / 0.05% | 0 | — |
| sca | B $10K / 0.10% | 0 | — |
| sca | C $20K / 0.25% | 0 | — |
| bsc | BASELINE $20K / 0% | 0 | — |
| bsc | A $10K / 0.05% | 0 | — |
| bsc | B $10K / 0.10% | 0 | — |
| bsc | C $20K / 0.25% | 0 | — |
| bmc | BASELINE $20K / 0% | 3 | Rep 8379 carries $29K at-risk book |
| bmc | A $10K / 0.05% | 8 | Rep 8379 carries $29K at-risk book |
| bmc | B $10K / 0.10% | 8 | Rep 8379 carries $29K at-risk book |
| bmc | C $20K / 0.25% | 3 | Rep 8379 carries $29K at-risk book |
| bri | BASELINE $20K / 0% | 12 | Rep 101 carries $100K at-risk book |
| bri | A $10K / 0.05% | 12 | Rep 101 carries $100K at-risk book |
| bri | B $10K / 0.10% | 12 | Rep 101 carries $100K at-risk book |
| bri | C $20K / 0.25% | 3 | Rep 101 carries $100K at-risk book |

</details>

### 4.3 `coaching_card_min_dollars` — coaching-CARD floor  (base: invoiced LTM)  **S2**

| org | inv LTM | active dealers | BASELINE $0 / 0% | A $5K / 0.02% | B $10K / 0.10% | C $10K / 0.25% |
|---|---|---|---|---|---|---|
| sarreid | $15.77M | 1,399 | 4 @ 0 | 4 @ 5,000 | 4 @ 15,767 | 0 @ 39,418 |
| cci | $70.02M | 7,570 | 3 @ 0 | 1 @ 14,003 | 0 @ 70,016 | 0 @ 175,040 |
| da | $0 | 0 | 0 @ 0 | 0 @ 5,000 | 0 @ 10,000 | 0 @ 10,000 |
| clc | $58.93M | 1,487 | 5 @ 0 | 5 @ 11,786 | 0 @ 58,930 | 0 @ 147,325 |
| hfg | $41.17M | 2,422 | 5 @ 0 | 1 @ 8,234 | 0 @ 41,170 | 0 @ 102,925 |
| kal | $8.76M | 572 | 4 @ 0 | 1 @ 5,000 | 1 @ 10,000 | 0 @ 21,903 |
| ali | $7.34M | 1,004 | 3 @ 0 | 1 @ 5,000 | 1 @ 10,000 | 1 @ 18,353 |
| sca | $0 | 0 | 0 @ 0 | 0 @ 5,000 | 0 @ 10,000 | 0 @ 10,000 |
| bsc | $0 | 0 | 0 @ 0 | 0 @ 5,000 | 0 @ 10,000 | 0 @ 10,000 |
| bmc | $6.94M | 879 | 3 @ 0 | 3 @ 5,000 | 2 @ 10,000 | 1 @ 17,362 |
| bri | $21.25M | 1,286 | 5 @ 0 | 5 @ 5,000 | 5 @ 21,249 | 1 @ 53,122 |

<details><summary>top-ranked item per org per value</summary>

| org | value | fired | top-ranked |
|---|---|---|---|
| sarreid | BASELINE $0 / 0% | 4 | Charles Hoffman=$36K · Deborah Klien=$36K · Clyde Barnard=$32K · Dan Linker=$19K |
| sarreid | A $5K / 0.02% | 4 | Charles Hoffman=$36K · Deborah Klien=$36K · Clyde Barnard=$32K · Dan Linker=$19K |
| sarreid | B $10K / 0.10% | 4 | Charles Hoffman=$36K · Deborah Klien=$36K · Clyde Barnard=$32K · Dan Linker=$19K |
| sarreid | C $10K / 0.25% | 0 | — |
| cci | BASELINE $0 / 0% | 3 | Stacie Baker=$66K · Timothy K Shelton=$12K · Stacey Chiavetta=$8K |
| cci | A $5K / 0.02% | 1 | Stacie Baker=$66K |
| cci | B $10K / 0.10% | 0 | — |
| cci | C $10K / 0.25% | 0 | — |
| da | BASELINE $0 / 0% | 0 | — |
| da | A $5K / 0.02% | 0 | — |
| da | B $10K / 0.10% | 0 | — |
| da | C $10K / 0.25% | 0 | — |
| clc | BASELINE $0 / 0% | 5 | Envision Lighting Sales=$59K · Philip Winston Inc=$52K · Winston & Associates=$39K · Texas Lighting Agency=$31K · DUNN Brands=$26K |
| clc | A $5K / 0.02% | 5 | Envision Lighting Sales=$59K · Philip Winston Inc=$52K · Winston & Associates=$39K · Texas Lighting Agency=$31K · DUNN Brands=$26K |
| clc | B $10K / 0.10% | 0 | — |
| clc | C $10K / 0.25% | 0 | — |
| hfg | BASELINE $0 / 0% | 5 | rep CANOREP=$22K · rep 41168=$1K · rep 45123=$1K · rep 42332=$1K · rep 12328=$804 |
| hfg | A $5K / 0.02% | 1 | rep CANOREP=$22K |
| hfg | B $10K / 0.10% | 0 | — |
| hfg | C $10K / 0.25% | 0 | — |
| kal | BASELINE $0 / 0% | 4 | rep 0999=$12K · rep 0307=$2K · rep 0033=$742 · rep 0034=$458 |
| kal | A $5K / 0.02% | 1 | rep 0999=$12K |
| kal | B $10K / 0.10% | 1 | rep 0999=$12K |
| kal | C $10K / 0.25% | 0 | — |
| ali | BASELINE $0 / 0% | 3 | rep 29=$21K · rep 36=$1K · rep 68=$134 |
| ali | A $5K / 0.02% | 1 | rep 29=$21K |
| ali | B $10K / 0.10% | 1 | rep 29=$21K |
| ali | C $10K / 0.25% | 1 | rep 29=$21K |
| sca | BASELINE $0 / 0% | 0 | — |
| sca | A $5K / 0.02% | 0 | — |
| sca | B $10K / 0.10% | 0 | — |
| sca | C $10K / 0.25% | 0 | — |
| bsc | BASELINE $0 / 0% | 0 | — |
| bsc | A $5K / 0.02% | 0 | — |
| bsc | B $10K / 0.10% | 0 | — |
| bsc | C $10K / 0.25% | 0 | — |
| bmc | BASELINE $0 / 0% | 3 | rep 8379=$30K · rep 99EC=$14K · rep 99=$9K |
| bmc | A $5K / 0.02% | 3 | rep 8379=$30K · rep 99EC=$14K · rep 99=$9K |
| bmc | B $10K / 0.10% | 2 | rep 8379=$30K · rep 99EC=$14K |
| bmc | C $10K / 0.25% | 1 | rep 8379=$30K |
| bri | BASELINE $0 / 0% | 5 | rep 101=$100K · rep 185=$36K · rep 154=$31K · rep 112=$28K · rep 88=$25K |
| bri | A $5K / 0.02% | 5 | rep 101=$100K · rep 185=$36K · rep 154=$31K · rep 112=$28K · rep 88=$25K |
| bri | B $10K / 0.10% | 5 | rep 101=$100K · rep 185=$36K · rep 154=$31K · rep 112=$28K · rep 88=$25K |
| bri | C $10K / 0.25% | 1 | rep 101=$100K |

</details>

### 4.4 `NEW_LINE_MIN_REVENUE` — new_line_takeoff floor  (base: invoiced LTM)

| org | inv LTM | active dealers | BASELINE $100K / 0% | A $50K / 0.25% | B $50K / 0.50% | C $100K / 1.00% |
|---|---|---|---|---|---|---|
| sarreid | $15.77M | 1,399 | 0 @ 100,000 | 0 @ 50,000 | 0 @ 78,837 | 0 @ 157,673 |
| cci | $70.02M | 7,570 | 0 @ 100,000 | 0 @ 175,040 | 0 @ 350,081 | 0 @ 700,162 |
| da | $0 | 0 | 0 @ 100,000 | 0 @ 50,000 | 0 @ 50,000 | 0 @ 100,000 |
| clc | $58.93M | 1,487 | 0 @ 100,000 | 0 @ 147,325 | 0 @ 294,650 | 0 @ 589,300 |
| hfg | $41.17M | 2,422 | 0 @ 100,000 | 0 @ 102,925 | 0 @ 205,851 | 0 @ 411,701 |
| kal | $8.76M | 572 | 0 @ 100,000 | 0 @ 50,000 | 0 @ 50,000 | 0 @ 100,000 |
| ali | $7.34M | 1,004 | 13 @ 100,000 | 13 @ 50,000 | 13 @ 50,000 | 13 @ 100,000 |
| sca | $0 | 0 | 0 @ 100,000 | 0 @ 50,000 | 0 @ 50,000 | 0 @ 100,000 |
| bsc | $0 | 0 | 0 @ 100,000 | 0 @ 50,000 | 0 @ 50,000 | 0 @ 100,000 |
| bmc | $6.94M | 879 | 0 @ 100,000 | 0 @ 50,000 | 0 @ 50,000 | 0 @ 100,000 |
| bri | $21.25M | 1,286 | 0 @ 100,000 | 0 @ 53,122 | 0 @ 106,244 | 0 @ 212,488 |

<details><summary>top-ranked item per org per value</summary>

| org | value | fired | top-ranked |
|---|---|---|---|
| sarreid | BASELINE $100K / 0% | 0 | — |
| sarreid | A $50K / 0.25% | 0 | — |
| sarreid | B $50K / 0.50% | 0 | — |
| sarreid | C $100K / 1.00% | 0 | — |
| cci | BASELINE $100K / 0% | 0 | — |
| cci | A $50K / 0.25% | 0 | — |
| cci | B $50K / 0.50% | 0 | — |
| cci | C $100K / 1.00% | 0 | — |
| da | BASELINE $100K / 0% | 0 | — |
| da | A $50K / 0.25% | 0 | — |
| da | B $50K / 0.50% | 0 | — |
| da | C $100K / 1.00% | 0 | — |
| clc | BASELINE $100K / 0% | 0 | — |
| clc | A $50K / 0.25% | 0 | — |
| clc | B $50K / 0.50% | 0 | — |
| clc | C $100K / 1.00% | 0 | — |
| hfg | BASELINE $100K / 0% | 0 | — |
| hfg | A $50K / 0.25% | 0 | — |
| hfg | B $50K / 0.50% | 0 | — |
| hfg | C $100K / 1.00% | 0 | — |
| kal | BASELINE $100K / 0% | 0 | — |
| kal | A $50K / 0.25% | 0 | — |
| kal | B $50K / 0.50% | 0 | — |
| kal | C $100K / 1.00% | 0 | — |
| ali | BASELINE $100K / 0% | 13 | New line ROMA: $595K on 150 dealers in year 1 |
| ali | A $50K / 0.25% | 13 | New line ROMA: $595K on 150 dealers in year 1 |
| ali | B $50K / 0.50% | 13 | New line ROMA: $595K on 150 dealers in year 1 |
| ali | C $100K / 1.00% | 13 | New line ROMA: $595K on 150 dealers in year 1 |
| sca | BASELINE $100K / 0% | 0 | — |
| sca | A $50K / 0.25% | 0 | — |
| sca | B $50K / 0.50% | 0 | — |
| sca | C $100K / 1.00% | 0 | — |
| bsc | BASELINE $100K / 0% | 0 | — |
| bsc | A $50K / 0.25% | 0 | — |
| bsc | B $50K / 0.50% | 0 | — |
| bsc | C $100K / 1.00% | 0 | — |
| bmc | BASELINE $100K / 0% | 0 | — |
| bmc | A $50K / 0.25% | 0 | — |
| bmc | B $50K / 0.50% | 0 | — |
| bmc | C $100K / 1.00% | 0 | — |
| bri | BASELINE $100K / 0% | 0 | — |
| bri | A $50K / 0.25% | 0 | — |
| bri | B $50K / 0.50% | 0 | — |
| bri | C $100K / 1.00% | 0 | — |

</details>

### 4.5 `REP_BOOK_MIN_DOLLARS` — rep over/under-perform book floor  (base: invoiced LTM)

| org | inv LTM | active dealers | BASELINE $100K / 0% | A $50K / 0.25% | B $50K / 0.50% | C $100K / 1.00% |
|---|---|---|---|---|---|---|
| sarreid | $15.77M | 1,399 | 5 @ 100,000 | 8 @ 50,000 | 5 @ 78,837 | 4 @ 157,673 |
| cci | $70.02M | 7,570 | 2 @ 100,000 | 2 @ 175,040 | 2 @ 350,081 | 2 @ 700,162 |
| da | $0 | 0 | 0 @ 100,000 | 0 @ 50,000 | 0 @ 50,000 | 0 @ 100,000 |
| clc | $58.93M | 1,487 | 23 @ 100,000 | 23 @ 147,325 | 23 @ 294,650 | 20 @ 589,300 |
| hfg | $41.17M | 2,422 | 0 @ 100,000 | 0 @ 102,925 | 0 @ 205,851 | 0 @ 411,701 |
| kal | $8.76M | 572 | 0 @ 100,000 | 0 @ 50,000 | 0 @ 50,000 | 0 @ 100,000 |
| ali | $7.34M | 1,004 | 0 @ 100,000 | 0 @ 50,000 | 0 @ 50,000 | 0 @ 100,000 |
| sca | $0 | 0 | 0 @ 100,000 | 0 @ 50,000 | 0 @ 50,000 | 0 @ 100,000 |
| bsc | $0 | 0 | 0 @ 100,000 | 0 @ 50,000 | 0 @ 50,000 | 0 @ 100,000 |
| bmc | $6.94M | 879 | 12 @ 100,000 | 12 @ 50,000 | 12 @ 50,000 | 12 @ 100,000 |
| bri | $21.25M | 1,286 | 0 @ 100,000 | 0 @ 53,122 | 0 @ 106,244 | 0 @ 212,488 |

<details><summary>top-ranked item per org per value</summary>

| org | value | fired | top-ranked |
|---|---|---|---|
| sarreid | BASELINE $100K / 0% | 5 | Charles Hoffman +52% YoY ($6238K) |
| sarreid | A $50K / 0.25% | 8 | Charles Hoffman +52% YoY ($6238K) |
| sarreid | B $50K / 0.50% | 5 | Charles Hoffman +52% YoY ($6238K) |
| sarreid | C $100K / 1.00% | 4 | Charles Hoffman +52% YoY ($6238K) |
| cci | BASELINE $100K / 0% | 2 | Andrea R Combet -45% YoY ($1389K) |
| cci | A $50K / 0.25% | 2 | Andrea R Combet -45% YoY ($1389K) |
| cci | B $50K / 0.50% | 2 | Andrea R Combet -45% YoY ($1389K) |
| cci | C $100K / 1.00% | 2 | Andrea R Combet -45% YoY ($1389K) |
| da | BASELINE $100K / 0% | 0 | — |
| da | A $50K / 0.25% | 0 | — |
| da | B $50K / 0.50% | 0 | — |
| da | C $100K / 1.00% | 0 | — |
| clc | BASELINE $100K / 0% | 23 | California Lighting Concepts +206% YoY ($5493K) |
| clc | A $50K / 0.25% | 23 | California Lighting Concepts +206% YoY ($5493K) |
| clc | B $50K / 0.50% | 23 | California Lighting Concepts +206% YoY ($5493K) |
| clc | C $100K / 1.00% | 20 | California Lighting Concepts +206% YoY ($5493K) |
| hfg | BASELINE $100K / 0% | 0 | — |
| hfg | A $50K / 0.25% | 0 | — |
| hfg | B $50K / 0.50% | 0 | — |
| hfg | C $100K / 1.00% | 0 | — |
| kal | BASELINE $100K / 0% | 0 | — |
| kal | A $50K / 0.25% | 0 | — |
| kal | B $50K / 0.50% | 0 | — |
| kal | C $100K / 1.00% | 0 | — |
| ali | BASELINE $100K / 0% | 0 | — |
| ali | A $50K / 0.25% | 0 | — |
| ali | B $50K / 0.50% | 0 | — |
| ali | C $100K / 1.00% | 0 | — |
| sca | BASELINE $100K / 0% | 0 | — |
| sca | A $50K / 0.25% | 0 | — |
| sca | B $50K / 0.50% | 0 | — |
| sca | C $100K / 1.00% | 0 | — |
| bsc | BASELINE $100K / 0% | 0 | — |
| bsc | A $50K / 0.25% | 0 | — |
| bsc | B $50K / 0.50% | 0 | — |
| bsc | C $100K / 1.00% | 0 | — |
| bmc | BASELINE $100K / 0% | 12 | Brandjump +158% YoY ($2648K) |
| bmc | A $50K / 0.25% | 12 | Brandjump +158% YoY ($2648K) |
| bmc | B $50K / 0.50% | 12 | Brandjump +158% YoY ($2648K) |
| bmc | C $100K / 1.00% | 12 | Brandjump +158% YoY ($2648K) |
| bri | BASELINE $100K / 0% | 0 | — |
| bri | A $50K / 0.25% | 0 | — |
| bri | B $50K / 0.50% | 0 | — |
| bri | C $100K / 1.00% | 0 | — |

</details>

### 4.6 `SECOND_YEAR_MIN_LAPSED_DOLLARS` — second_year_gap floor  (base: invoiced LTM)

| org | inv LTM | active dealers | BASELINE $50K / 0% | A $25K / 0.25% | B $25K / 0.50% | C $50K / 1.00% |
|---|---|---|---|---|---|---|
| sarreid | $15.77M | 1,399 | 1 @ 50,000 | 1 @ 39,418 | 1 @ 78,837 | 1 @ 157,673 |
| cci | $70.02M | 7,570 | 0 @ 50,000 | 0 @ 175,040 | 0 @ 350,081 | 0 @ 700,162 |
| da | $0 | 0 | 0 @ 50,000 | 0 @ 25,000 | 0 @ 25,000 | 0 @ 50,000 |
| clc | $58.93M | 1,487 | 0 @ 50,000 | 0 @ 147,325 | 0 @ 294,650 | 0 @ 589,300 |
| hfg | $41.17M | 2,422 | 0 @ 50,000 | 0 @ 102,925 | 0 @ 205,851 | 0 @ 411,701 |
| kal | $8.76M | 572 | 0 @ 50,000 | 0 @ 25,000 | 0 @ 43,805 | 0 @ 87,610 |
| ali | $7.34M | 1,004 | 0 @ 50,000 | 0 @ 25,000 | 0 @ 36,707 | 0 @ 73,413 |
| sca | $0 | 0 | 0 @ 50,000 | 0 @ 25,000 | 0 @ 25,000 | 0 @ 50,000 |
| bsc | $0 | 0 | 0 @ 50,000 | 0 @ 25,000 | 0 @ 25,000 | 0 @ 50,000 |
| bmc | $6.94M | 879 | 1 @ 50,000 | 1 @ 25,000 | 1 @ 34,725 | 1 @ 69,449 |
| bri | $21.25M | 1,286 | 0 @ 50,000 | 0 @ 53,122 | 0 @ 106,244 | 0 @ 212,488 |

<details><summary>top-ranked item per org per value</summary>

| org | value | fired | top-ranked |
|---|---|---|---|
| sarreid | BASELINE $50K / 0% | 1 | Only 46% of first-timers return — $821K at stake |
| sarreid | A $25K / 0.25% | 1 | Only 46% of first-timers return — $821K at stake |
| sarreid | B $25K / 0.50% | 1 | Only 46% of first-timers return — $821K at stake |
| sarreid | C $50K / 1.00% | 1 | Only 46% of first-timers return — $821K at stake |
| cci | BASELINE $50K / 0% | 0 | — |
| cci | A $25K / 0.25% | 0 | — |
| cci | B $25K / 0.50% | 0 | — |
| cci | C $50K / 1.00% | 0 | — |
| da | BASELINE $50K / 0% | 0 | — |
| da | A $25K / 0.25% | 0 | — |
| da | B $25K / 0.50% | 0 | — |
| da | C $50K / 1.00% | 0 | — |
| clc | BASELINE $50K / 0% | 0 | — |
| clc | A $25K / 0.25% | 0 | — |
| clc | B $25K / 0.50% | 0 | — |
| clc | C $50K / 1.00% | 0 | — |
| hfg | BASELINE $50K / 0% | 0 | — |
| hfg | A $25K / 0.25% | 0 | — |
| hfg | B $25K / 0.50% | 0 | — |
| hfg | C $50K / 1.00% | 0 | — |
| kal | BASELINE $50K / 0% | 0 | — |
| kal | A $25K / 0.25% | 0 | — |
| kal | B $25K / 0.50% | 0 | — |
| kal | C $50K / 1.00% | 0 | — |
| ali | BASELINE $50K / 0% | 0 | — |
| ali | A $25K / 0.25% | 0 | — |
| ali | B $25K / 0.50% | 0 | — |
| ali | C $50K / 1.00% | 0 | — |
| sca | BASELINE $50K / 0% | 0 | — |
| sca | A $25K / 0.25% | 0 | — |
| sca | B $25K / 0.50% | 0 | — |
| sca | C $50K / 1.00% | 0 | — |
| bsc | BASELINE $50K / 0% | 0 | — |
| bsc | A $25K / 0.25% | 0 | — |
| bsc | B $25K / 0.50% | 0 | — |
| bsc | C $50K / 1.00% | 0 | — |
| bmc | BASELINE $50K / 0% | 1 | Only 44% of first-timers return — $377K at stake |
| bmc | A $25K / 0.25% | 1 | Only 44% of first-timers return — $377K at stake |
| bmc | B $25K / 0.50% | 1 | Only 44% of first-timers return — $377K at stake |
| bmc | C $50K / 1.00% | 1 | Only 44% of first-timers return — $377K at stake |
| bri | BASELINE $50K / 0% | 0 | — |
| bri | A $25K / 0.25% | 0 | — |
| bri | B $25K / 0.50% | 0 | — |
| bri | C $50K / 1.00% | 0 | — |

</details>

### 4.7 `PLAY_MIN_UPSIDE_DOLLARS` — 'Do this month' materiality  (base: invoiced LTM)  **S1**

| org | inv LTM | active dealers | BASELINE $0 / 0% | A $10K / 0.10% | B $25K / 0.25% | C $50K / 0.50% |
|---|---|---|---|---|---|---|
| sarreid | $15.77M | 1,399 | 3 @ 0 | 2 @ 15,767 | 2 @ 39,418 | 2 @ 78,837 |
| cci | $70.02M | 7,570 | 1 @ 0 | 1 @ 70,016 | 1 @ 175,040 | 0 @ 350,081 |
| da | $0 | 0 | 0 @ 0 | 0 @ 10,000 | 0 @ 25,000 | 0 @ 50,000 |
| clc | $58.93M | 1,487 | 1 @ 0 | 0 @ 58,930 | 0 @ 147,325 | 0 @ 294,650 |
| hfg | $41.17M | 2,422 | 1 @ 0 | 0 @ 41,170 | 0 @ 102,925 | 0 @ 205,851 |
| kal | $8.76M | 572 | 1 @ 0 | 1 @ 10,000 | 1 @ 25,000 | 1 @ 50,000 |
| ali | $7.34M | 1,004 | 1 @ 0 | 0 @ 10,000 | 0 @ 25,000 | 0 @ 50,000 |
| sca | $0 | 0 | 0 @ 0 | 0 @ 10,000 | 0 @ 25,000 | 0 @ 50,000 |
| bsc | $0 | 0 | 0 @ 0 | 0 @ 10,000 | 0 @ 25,000 | 0 @ 50,000 |
| bmc | $6.94M | 879 | 3 @ 0 | 3 @ 10,000 | 3 @ 25,000 | 3 @ 50,000 |
| bri | $21.25M | 1,286 | 1 @ 0 | 1 @ 21,249 | 1 @ 53,122 | 1 @ 106,244 |

<details><summary>top-ranked item per org per value</summary>

| org | value | fired | top-ranked |
|---|---|---|---|
| sarreid | BASELINE $0 / 0% | 3 | A second-order push for new dealers ($821K) · Lilac Sideboard Blue Finish → Jupe cross-sell ($0) · Pricing / discipline review ($171K) |
| sarreid | A $10K / 0.10% | 2 | A second-order push for new dealers ($821K) · Pricing / discipline review ($171K) |
| sarreid | B $25K / 0.25% | 2 | A second-order push for new dealers ($821K) · Pricing / discipline review ($171K) |
| sarreid | C $50K / 0.50% | 2 | A second-order push for new dealers ($821K) · Pricing / discipline review ($171K) |
| cci | BASELINE $0 / 0% | 1 | Nottaway Large Bronze Chandeli → BUNNY WILLIAMS cross-sell ($238K) |
| cci | A $10K / 0.10% | 1 | Nottaway Large Bronze Chandeli → BUNNY WILLIAMS cross-sell ($238K) |
| cci | B $25K / 0.25% | 1 | Nottaway Large Bronze Chandeli → BUNNY WILLIAMS cross-sell ($238K) |
| cci | C $50K / 0.50% | 0 | no play qualified |
| da | BASELINE $0 / 0% | 0 | no play qualified |
| da | A $10K / 0.10% | 0 | no play qualified |
| da | B $25K / 0.25% | 0 | no play qualified |
| da | C $50K / 0.50% | 0 | no play qualified |
| clc | BASELINE $0 / 0% | 1 | 4 Light Pendant → BAKER cross-sell ($0) |
| clc | A $10K / 0.10% | 0 | no play qualified |
| clc | B $25K / 0.25% | 0 | no play qualified |
| clc | C $50K / 0.50% | 0 | no play qualified |
| hfg | BASELINE $0 / 0% | 1 | Axis cross-sell ($12K) |
| hfg | A $10K / 0.10% | 0 | no play qualified |
| hfg | B $25K / 0.25% | 0 | no play qualified |
| hfg | C $50K / 0.50% | 0 | no play qualified |
| kal | BASELINE $0 / 0% | 1 | Flint 5 LT Multi Drop → FLINT cross-sell ($112K) |
| kal | A $10K / 0.10% | 1 | Flint 5 LT Multi Drop → FLINT cross-sell ($112K) |
| kal | B $25K / 0.25% | 1 | Flint 5 LT Multi Drop → FLINT cross-sell ($112K) |
| kal | C $50K / 0.50% | 1 | Flint 5 LT Multi Drop → FLINT cross-sell ($112K) |
| ali | BASELINE $0 / 0% | 1 | LED FMT 35 WATT 1500LMN 120V 90CRI JA8 → ROMA cross-sell ($0) |
| ali | A $10K / 0.10% | 0 | no play qualified |
| ali | B $25K / 0.25% | 0 | no play qualified |
| ali | C $50K / 0.50% | 0 | no play qualified |
| sca | BASELINE $0 / 0% | 0 | no play qualified |
| sca | A $10K / 0.10% | 0 | no play qualified |
| sca | B $25K / 0.25% | 0 | no play qualified |
| sca | C $50K / 0.50% | 0 | no play qualified |
| bsc | BASELINE $0 / 0% | 0 | no play qualified |
| bsc | A $10K / 0.10% | 0 | no play qualified |
| bsc | B $25K / 0.25% | 0 | no play qualified |
| bsc | C $50K / 0.50% | 0 | no play qualified |
| bmc | BASELINE $0 / 0% | 3 | A second-order push for new dealers ($377K) · Fynn Display Cabinet → NONE cross-sell ($97K) · Pricing / discipline review ($180K) |
| bmc | A $10K / 0.10% | 3 | A second-order push for new dealers ($377K) · Fynn Display Cabinet → NONE cross-sell ($97K) · Pricing / discipline review ($180K) |
| bmc | B $25K / 0.25% | 3 | A second-order push for new dealers ($377K) · Fynn Display Cabinet → NONE cross-sell ($97K) · Pricing / discipline review ($180K) |
| bmc | C $50K / 0.50% | 3 | A second-order push for new dealers ($377K) · Fynn Display Cabinet → NONE cross-sell ($97K) · Pricing / discipline review ($180K) |
| bri | BASELINE $0 / 0% | 1 | Pricing / discipline review ($552K) |
| bri | A $10K / 0.10% | 1 | Pricing / discipline review ($552K) |
| bri | B $25K / 0.25% | 1 | Pricing / discipline review ($552K) |
| bri | C $50K / 0.50% | 1 | Pricing / discipline review ($552K) |

</details>

### 4.8 `GROWTH_POCKET_MIN_DEALERS` — growth_pocket dealer base  (base: ACTIVE DEALERS)

| org | inv LTM | active dealers | BASELINE 10 / 0% | A 5 / 0.5% | B 5 / 1.0% | C 10 / 2.0% |
|---|---|---|---|---|---|---|
| sarreid | $15.77M | 1,399 | 0 @ 10 | 0 @ 7 | 0 @ 14 | 0 @ 28 |
| cci | $70.02M | 7,570 | 1 @ 10 | 1 @ 38 | 1 @ 76 | 1 @ 151 |
| da | $0 | 0 | 0 @ 10 | 0 @ 5 | 0 @ 5 | 0 @ 10 |
| clc | $58.93M | 1,487 | 1 @ 10 | 1 @ 7 | 1 @ 15 | 1 @ 30 |
| hfg | $41.17M | 2,422 | 0 @ 10 | 0 @ 12 | 0 @ 24 | 0 @ 48 |
| kal | $8.76M | 572 | 4 @ 10 | 4 @ 5 | 4 @ 6 | 4 @ 11 |
| ali | $7.34M | 1,004 | 0 @ 10 | 0 @ 5 | 0 @ 10 | 0 @ 20 |
| sca | $0 | 0 | 0 @ 10 | 0 @ 5 | 0 @ 5 | 0 @ 10 |
| bsc | $0 | 0 | 0 @ 10 | 0 @ 5 | 0 @ 5 | 0 @ 10 |
| bmc | $6.94M | 879 | 0 @ 10 | 0 @ 5 | 0 @ 9 | 0 @ 18 |
| bri | $21.25M | 1,286 | 0 @ 10 | 0 @ 6 | 0 @ 13 | 0 @ 26 |

<details><summary>top-ranked item per org per value</summary>

| org | value | fired | top-ranked |
|---|---|---|---|
| sarreid | BASELINE 10 / 0% | 0 | — |
| sarreid | A 5 / 0.5% | 0 | — |
| sarreid | B 5 / 1.0% | 0 | — |
| sarreid | C 10 / 2.0% | 0 | — |
| cci | BASELINE 10 / 0% | 1 | BUNNY WILLIAMS +56% YoY across 660 dealers |
| cci | A 5 / 0.5% | 1 | BUNNY WILLIAMS +56% YoY across 660 dealers |
| cci | B 5 / 1.0% | 1 | BUNNY WILLIAMS +56% YoY across 660 dealers |
| cci | C 10 / 2.0% | 1 | BUNNY WILLIAMS +56% YoY across 660 dealers |
| da | BASELINE 10 / 0% | 0 | — |
| da | A 5 / 0.5% | 0 | — |
| da | B 5 / 1.0% | 0 | — |
| da | C 10 / 2.0% | 0 | — |
| clc | BASELINE 10 / 0% | 1 | BAKER +78% YoY across 449 dealers |
| clc | A 5 / 0.5% | 1 | BAKER +78% YoY across 449 dealers |
| clc | B 5 / 1.0% | 1 | BAKER +78% YoY across 449 dealers |
| clc | C 10 / 2.0% | 1 | BAKER +78% YoY across 449 dealers |
| hfg | BASELINE 10 / 0% | 0 | — |
| hfg | A 5 / 0.5% | 0 | — |
| hfg | B 5 / 1.0% | 0 | — |
| hfg | C 10 / 2.0% | 0 | — |
| kal | BASELINE 10 / 0% | 4 | FLINT +33% YoY across 126 dealers |
| kal | A 5 / 0.5% | 4 | FLINT +33% YoY across 126 dealers |
| kal | B 5 / 1.0% | 4 | FLINT +33% YoY across 126 dealers |
| kal | C 10 / 2.0% | 4 | FLINT +33% YoY across 126 dealers |
| ali | BASELINE 10 / 0% | 0 | — |
| ali | A 5 / 0.5% | 0 | — |
| ali | B 5 / 1.0% | 0 | — |
| ali | C 10 / 2.0% | 0 | — |
| sca | BASELINE 10 / 0% | 0 | — |
| sca | A 5 / 0.5% | 0 | — |
| sca | B 5 / 1.0% | 0 | — |
| sca | C 10 / 2.0% | 0 | — |
| bsc | BASELINE 10 / 0% | 0 | — |
| bsc | A 5 / 0.5% | 0 | — |
| bsc | B 5 / 1.0% | 0 | — |
| bsc | C 10 / 2.0% | 0 | — |
| bmc | BASELINE 10 / 0% | 0 | — |
| bmc | A 5 / 0.5% | 0 | — |
| bmc | B 5 / 1.0% | 0 | — |
| bmc | C 10 / 2.0% | 0 | — |
| bri | BASELINE 10 / 0% | 0 | — |
| bri | A 5 / 0.5% | 0 | — |
| bri | B 5 / 1.0% | 0 | — |
| bri | C 10 / 2.0% | 0 | — |

</details>

### 4.9 `NEW_LINE_MIN_DEALERS` — new_line_takeoff dealer base  (base: ACTIVE DEALERS)

| org | inv LTM | active dealers | BASELINE 5 / 0% | A 5 / 0.25% | B 5 / 0.50% | C 5 / 1.00% |
|---|---|---|---|---|---|---|
| sarreid | $15.77M | 1,399 | 0 @ 5 | 0 @ 5 | 0 @ 7 | 0 @ 14 |
| cci | $70.02M | 7,570 | 0 @ 5 | 0 @ 19 | 0 @ 38 | 0 @ 76 |
| da | $0 | 0 | 0 @ 5 | 0 @ 5 | 0 @ 5 | 0 @ 5 |
| clc | $58.93M | 1,487 | 0 @ 5 | 0 @ 5 | 0 @ 7 | 0 @ 15 |
| hfg | $41.17M | 2,422 | 0 @ 5 | 0 @ 6 | 0 @ 12 | 0 @ 24 |
| kal | $8.76M | 572 | 0 @ 5 | 0 @ 5 | 0 @ 5 | 0 @ 6 |
| ali | $7.34M | 1,004 | 13 @ 5 | 13 @ 5 | 13 @ 5 | 13 @ 10 |
| sca | $0 | 0 | 0 @ 5 | 0 @ 5 | 0 @ 5 | 0 @ 5 |
| bsc | $0 | 0 | 0 @ 5 | 0 @ 5 | 0 @ 5 | 0 @ 5 |
| bmc | $6.94M | 879 | 0 @ 5 | 0 @ 5 | 0 @ 5 | 0 @ 9 |
| bri | $21.25M | 1,286 | 0 @ 5 | 0 @ 5 | 0 @ 6 | 0 @ 13 |

<details><summary>top-ranked item per org per value</summary>

| org | value | fired | top-ranked |
|---|---|---|---|
| sarreid | BASELINE 5 / 0% | 0 | — |
| sarreid | A 5 / 0.25% | 0 | — |
| sarreid | B 5 / 0.50% | 0 | — |
| sarreid | C 5 / 1.00% | 0 | — |
| cci | BASELINE 5 / 0% | 0 | — |
| cci | A 5 / 0.25% | 0 | — |
| cci | B 5 / 0.50% | 0 | — |
| cci | C 5 / 1.00% | 0 | — |
| da | BASELINE 5 / 0% | 0 | — |
| da | A 5 / 0.25% | 0 | — |
| da | B 5 / 0.50% | 0 | — |
| da | C 5 / 1.00% | 0 | — |
| clc | BASELINE 5 / 0% | 0 | — |
| clc | A 5 / 0.25% | 0 | — |
| clc | B 5 / 0.50% | 0 | — |
| clc | C 5 / 1.00% | 0 | — |
| hfg | BASELINE 5 / 0% | 0 | — |
| hfg | A 5 / 0.25% | 0 | — |
| hfg | B 5 / 0.50% | 0 | — |
| hfg | C 5 / 1.00% | 0 | — |
| kal | BASELINE 5 / 0% | 0 | — |
| kal | A 5 / 0.25% | 0 | — |
| kal | B 5 / 0.50% | 0 | — |
| kal | C 5 / 1.00% | 0 | — |
| ali | BASELINE 5 / 0% | 13 | New line ROMA: $595K on 150 dealers in year 1 |
| ali | A 5 / 0.25% | 13 | New line ROMA: $595K on 150 dealers in year 1 |
| ali | B 5 / 0.50% | 13 | New line ROMA: $595K on 150 dealers in year 1 |
| ali | C 5 / 1.00% | 13 | New line ROMA: $595K on 150 dealers in year 1 |
| sca | BASELINE 5 / 0% | 0 | — |
| sca | A 5 / 0.25% | 0 | — |
| sca | B 5 / 0.50% | 0 | — |
| sca | C 5 / 1.00% | 0 | — |
| bsc | BASELINE 5 / 0% | 0 | — |
| bsc | A 5 / 0.25% | 0 | — |
| bsc | B 5 / 0.50% | 0 | — |
| bsc | C 5 / 1.00% | 0 | — |
| bmc | BASELINE 5 / 0% | 0 | — |
| bmc | A 5 / 0.25% | 0 | — |
| bmc | B 5 / 0.50% | 0 | — |
| bmc | C 5 / 1.00% | 0 | — |
| bri | BASELINE 5 / 0% | 0 | — |
| bri | A 5 / 0.25% | 0 | — |
| bri | B 5 / 0.50% | 0 | — |
| bri | C 5 / 1.00% | 0 | — |

</details>

### 4.10 `CROSS_SELL_MIN_TARGET_DEALERS` — cross_sell target base  (base: ACTIVE DEALERS)

| org | inv LTM | active dealers | BASELINE 5 / 0% | A 5 / 0.25% | B 5 / 0.50% | C 5 / 1.00% |
|---|---|---|---|---|---|---|
| sarreid | $15.77M | 1,399 | 1 @ 5 | 1 @ 5 | 1 @ 7 | 1 @ 14 |
| cci | $70.02M | 7,570 | 1 @ 5 | 1 @ 19 | 1 @ 38 | 1 @ 76 |
| da | $0 | 0 | 0 @ 5 | 0 @ 5 | 0 @ 5 | 0 @ 5 |
| clc | $58.93M | 1,487 | 1 @ 5 | 1 @ 5 | 1 @ 7 | 1 @ 15 |
| hfg | $41.17M | 2,422 | 1 @ 5 | 1 @ 6 | 1 @ 12 | 1 @ 24 |
| kal | $8.76M | 572 | 1 @ 5 | 1 @ 5 | 1 @ 5 | 1 @ 6 |
| ali | $7.34M | 1,004 | 1 @ 5 | 1 @ 5 | 1 @ 5 | 1 @ 10 |
| sca | $0 | 0 | 0 @ 5 | 0 @ 5 | 0 @ 5 | 0 @ 5 |
| bsc | $0 | 0 | 0 @ 5 | 0 @ 5 | 0 @ 5 | 0 @ 5 |
| bmc | $6.94M | 879 | 1 @ 5 | 1 @ 5 | 1 @ 5 | 1 @ 9 |
| bri | $21.25M | 1,286 | 0 @ 5 | 0 @ 5 | 0 @ 6 | 0 @ 13 |

<details><summary>top-ranked item per org per value</summary>

| org | value | fired | top-ranked |
|---|---|---|---|
| sarreid | BASELINE 5 / 0% | 1 | 52760 buyers already overlap fully with Jupe |
| sarreid | A 5 / 0.25% | 1 | 52760 buyers already overlap fully with Jupe |
| sarreid | B 5 / 0.50% | 1 | 52760 buyers already overlap fully with Jupe |
| sarreid | C 5 / 1.00% | 1 | 52760 buyers already overlap fully with Jupe |
| cci | BASELINE 5 / 0% | 1 | 184 dealers buying 9000-0135 have not bought BUNNY WILLIAMS |
| cci | A 5 / 0.25% | 1 | 184 dealers buying 9000-0135 have not bought BUNNY WILLIAMS |
| cci | B 5 / 0.50% | 1 | 184 dealers buying 9000-0135 have not bought BUNNY WILLIAMS |
| cci | C 5 / 1.00% | 1 | 184 dealers buying 9000-0135 have not bought BUNNY WILLIAMS |
| da | BASELINE 5 / 0% | 0 | — |
| da | A 5 / 0.25% | 0 | — |
| da | B 5 / 0.50% | 0 | — |
| da | C 5 / 1.00% | 0 | — |
| clc | BASELINE 5 / 0% | 1 | 349842MA buyers already overlap fully with BAKER |
| clc | A 5 / 0.25% | 1 | 349842MA buyers already overlap fully with BAKER |
| clc | B 5 / 0.50% | 1 | 349842MA buyers already overlap fully with BAKER |
| clc | C 5 / 1.00% | 1 | 349842MA buyers already overlap fully with BAKER |
| hfg | BASELINE 5 / 0% | 1 | 1 dealers buying 9N00145405-3-14-DL105 have not bought Axis |
| hfg | A 5 / 0.25% | 1 | 1 dealers buying 9N00145405-3-14-DL105 have not bought Axis |
| hfg | B 5 / 0.50% | 1 | 1 dealers buying 9N00145405-3-14-DL105 have not bought Axis |
| hfg | C 5 / 1.00% | 1 | 1 dealers buying 9N00145405-3-14-DL105 have not bought Axis |
| kal | BASELINE 5 / 0% | 1 | 42 dealers buying 519275WB have not bought FLINT |
| kal | A 5 / 0.25% | 1 | 42 dealers buying 519275WB have not bought FLINT |
| kal | B 5 / 0.50% | 1 | 42 dealers buying 519275WB have not bought FLINT |
| kal | C 5 / 1.00% | 1 | 42 dealers buying 519275WB have not bought FLINT |
| ali | BASELINE 5 / 0% | 1 | 20827LEDD-ABB/OPL buyers already overlap fully with ROMA |
| ali | A 5 / 0.25% | 1 | 20827LEDD-ABB/OPL buyers already overlap fully with ROMA |
| ali | B 5 / 0.50% | 1 | 20827LEDD-ABB/OPL buyers already overlap fully with ROMA |
| ali | C 5 / 1.00% | 1 | 20827LEDD-ABB/OPL buyers already overlap fully with ROMA |
| sca | BASELINE 5 / 0% | 0 | — |
| sca | A 5 / 0.25% | 0 | — |
| sca | B 5 / 0.50% | 0 | — |
| sca | C 5 / 1.00% | 0 | — |
| bsc | BASELINE 5 / 0% | 0 | — |
| bsc | A 5 / 0.25% | 0 | — |
| bsc | B 5 / 0.50% | 0 | — |
| bsc | C 5 / 1.00% | 0 | — |
| bmc | BASELINE 5 / 0% | 1 | 7 dealers buying 3310-LR-500 have not bought NONE |
| bmc | A 5 / 0.25% | 1 | 7 dealers buying 3310-LR-500 have not bought NONE |
| bmc | B 5 / 0.50% | 1 | 7 dealers buying 3310-LR-500 have not bought NONE |
| bmc | C 5 / 1.00% | 1 | 7 dealers buying 3310-LR-500 have not bought NONE |
| bri | BASELINE 5 / 0% | 0 | — |
| bri | A 5 / 0.25% | 0 | — |
| bri | B 5 / 0.50% | 0 | — |
| bri | C 5 / 1.00% | 0 | — |

</details>

### 4.11 `CROSS_SELL_HERO_MIN_DEALERS` — hero cross-sell floor  (base: ACTIVE DEALERS)  **S1**

The `_macros.md.j2` stopgap of 3. Cell = measured gap vs resolved floor → RENDER / suppressed.

| org | active dealers | gap count | BASELINE 3 / 0% | A 3 / 0.25% | B 3 / 0.50% | C 5 / 1.00% |
|---|---|---|---|---|---|---|
| sarreid | 1,399 | 0 | suppressed (≥3) | suppressed (≥3) | suppressed (≥7) | suppressed (≥14) |
| cci | 7,570 | 184 | RENDER (≥3) | RENDER (≥19) | RENDER (≥38) | RENDER (≥76) |
| da | 0 | — | n/a (≥3) | n/a (≥3) | n/a (≥3) | n/a (≥5) |
| clc | 1,487 | 0 | suppressed (≥3) | suppressed (≥4) | suppressed (≥7) | suppressed (≥15) |
| hfg | 2,422 | 1 | suppressed (≥3) | suppressed (≥6) | suppressed (≥12) | suppressed (≥24) |
| kal | 572 | 42 | RENDER (≥3) | RENDER (≥3) | RENDER (≥3) | RENDER (≥6) |
| ali | 1,004 | 0 | suppressed (≥3) | suppressed (≥3) | suppressed (≥5) | suppressed (≥10) |
| sca | 0 | 0 | suppressed (≥3) | suppressed (≥3) | suppressed (≥3) | suppressed (≥5) |
| bsc | 0 | 0 | suppressed (≥3) | suppressed (≥3) | suppressed (≥3) | suppressed (≥5) |
| bmc | 879 | 7 | RENDER (≥3) | RENDER (≥3) | RENDER (≥4) | suppressed (≥9) |
| bri | 1,286 | 10 | RENDER (≥3) | RENDER (≥3) | RENDER (≥6) | suppressed (≥13) |

### 4.12 S3 — which same-dealer measure the hero leads with, and where it turns

| org | same-dealer lift % | NRR % (retained $ per $1) | lift verdict @ −5% | NRR verdict @ 97% | agree? |
|---|---|---|---|---|---|
| sarreid | +29.1% | 106.4% ($1.06) | up | up | yes |
| cci | +3.8% | 88.5% ($0.89) | roughly flat | spending less | **NO** |
| da | — | — | — | — | — |
| clc | +71.9% | 173.2% ($1.73) | up | up | yes |
| hfg | -1.8% | 83.7% ($0.84) | roughly flat | spending less | **NO** |
| kal | -4.0% | 91.8% ($0.92) | roughly flat | spending less | **NO** |
| ali | — | — | — | — | — |
| sca | — | — | — | — | — |
| bsc | — | — | — | — | — |
| bmc | -62.1% | 76.0% ($0.76) | spending less | spending less | yes |
| bri | -5.9% | 92.1% ($0.92) | spending less | spending less | yes |

---

## 5. Recommendation, one line of rationale each

**W3 proposes; the owner decides.** None of this is active. It is
`RECOMMENDED_PROFILE` in `pipeline/signals.py`, reachable by changing
`ACTIVE_PROFILE = BASELINE_PROFILE` to `ACTIVE_PROFILE = RECOMMENDED_PROFILE`.

The ranking rule applied throughout, from the brief: **false positives matter
more than coverage.** Where two candidates were defensible, the one that says
less was preferred.

| # | Constant | Recommend | Rationale (one line) |
|---|---|---|---|
| 4.1 | `decline_min_ltm` | `max($25K, 0.10% × LTM)` | Small orgs gain real coverage (sarreid 5→9, kal 5→6, ali 3→4); every large org is unchanged — the 10× spread closes without a single new large-org finding. |
| 4.2 | `rep_atrisk_min` | `max($10K, 0.05% × LTM)` | 0.10% zeroes **both** cci and hfg, deleting cci's genuine $66K book; 0.05% tightens hfg (1→1) and opens kal (0→1) without erasing a section. |
| 4.3 | `coaching_card_min_dollars` | `max($5K, 0.02% × LTM)` | **This is the S2 fix.** hfg 5→1, cci 3→1, kal 4→1, ali 3→1, and sarreid/clc/bri/bmc keep every card. 0.10% deletes cci's, clc's *and* hfg's card block entirely — over-correction, not materiality. |
| 4.4 | `new_line_min_revenue` | `max($50K, 0.25% × LTM)` | **The cohort does not discriminate.** Only `ali` has new families and all 13 clear every candidate. Size-relative on principle; the owner is choosing blind here and should know it. |
| 4.5 | `rep_book_min` | `max($50K, 0.25% × LTM)` | Same — no candidate moves any org. clc fires 23 rep signals at every value, which is a *ranking* problem (Phase 6), not a floor problem. |
| 4.6 | `second_year_min_lapsed` | `max($25K, 0.25% × LTM)` | No candidate moves any org; only sarreid and bmc fire at all. |
| 4.7 | `play_min_upside` | `max($10K, 0.10% × LTM)` | **This is the S1 fix.** hfg 1→0, clc 1→0, ali 1→0, sarreid 3→2; cci/kal/bri/bmc untouched. Every play it removes is one whose *own* copy said the upside was a rounding error. |
| 4.8 | `growth_pocket_min_dealers` | `max(5, 0.5% × active dealers)` | No cohort org changes at any value. The floor drops 10→5 so a 200-dealer client can reach it at all; the percentage stops cci calling 10 of 7,570 dealers "a broad base". |
| 4.9 | `new_line_min_dealers` | `max(5, 0.25% × active dealers)` | Same shape, no cohort movement. |
| 4.10 | `cross_sell_min_target_dealers` | `max(5, 0.25% × active dealers)` | Same shape, no cohort movement. |
| 4.11 | `cross_sell_hero_min_dealers` | `max(3, 0.25% × active dealers)` | 0.50% starts suppressing bri's legitimate 10-door gap; 0.25% suppresses exactly what the stopgap of 3 already suppressed, and scales for the next client. |
| 4.12 | hero same-dealer measure | **`nrr`, "spending less" below 97%** | The two measures disagree on **3 of 8** commerce orgs and `lift` is the gentler one **every time**. NRR is what §5 already reports, so leading on it removes a contradiction instead of papering over it. |
| — | `coaching_cards_require_needs_a_call` | **`True`** | Not a number. See §6.2. |

### Two honest caveats on these numbers

1. **4.3 costs cci one legitimate card.** At `max($5K, 0.02%)` cci's floor is
   $14,003 and Stacey Chiavetta's card ($7,637 at risk on *Goodform France and
   Son*, a genuine −42% on a $199K book) is suppressed. The card is dropped on
   `RepRisk.dollars_at_risk`, which is a **decay/leak proxy**, not the size of
   the account in trouble. If the owner would rather not lose that card, the
   better gate is the **flagged account's LTM**, not the rep's at-risk dollars
   — that is a signal-shape change, not a threshold change, and it is not W3's
   to make.
2. **Four constants (4.4, 4.5, 4.6, and all three count gates) are unresolved
   by this cohort.** No candidate value changes any org's output. They are
   converted so the *form* is right for the next client; the *value* has no
   evidence behind it beyond "it reproduces today on the eleven orgs we have".
   The brief asked for evidence; where there is none, this says so.

---

## 6. The three symptoms

### 6.1 — S1 · "the whole month is a $7–12K play on a $41.2M company"

`build_plays_from_gather` applied **no materiality floor at all**. It now scores
every play on the same basis §3 renders it (`play_upside_ceiling`) and drops
anything under the org's floor. hfg's play measures **$12,441** — 0.03% of the
year.

The hero-only stopgap of 3 in `_macros.md.j2` is **deleted**; the comment that
said *"the properly SIZE-SCALED floor for every section lands in Phase 7"* is
gone with it, replaced by `thresholds.cross_sell_hero_min_dealers`.

**"No play qualified this month" is now genuinely reachable** — and it was not
before. `_base.md.j2` gates §3 on `availability.this_month`, `## Do this month`
is not in `smoke_check._STANDARD_REQUIRED_SECTIONS`, so the MD is clean. The
HTML was not: see §2c. With that fixed, hfg and clc both render, `smoke_check:
PASS`, `step10: PASS`, `SHIP`.

### 6.2 — S2 · "four coaching cards reading `$1K at risk`, one on a GROWING account"

Two defects, and the second is the worse one.

**Materiality.** The cards had no dollar floor of any kind —
`REP_ATRISK_MIN_DOLLARS` gates the *signal*, and the cards never consulted it.
Now `thresholds.coaching_card_min_dollars`, size-scaled, §4.3.

**Consistency.** Phase 4 established `gather.account_needs_a_call` as the one
definition of "this account has slipped". The cards were the fourth surface and
were missed. Tracing it found **two** separate causes:

1. `RepRisk.accounts_at_risk` is populated in `gather.gather_all:1255` as
   `sum(1 for a in decay if a.rep_number == risk.rep_number)` — a **presence**
   count over the top-N decay extract, not a risk count. That is why clc ships
   five cards of which **not one** names an account that needs a call.
2. The card rendered the rep's **highest-LTM** decay row, which need not be a
   row that slipped. hfg's card 1 therefore named account 1489: **+6.7%,
   ordered two days ago**.

`signals.coaching_card_reps` decides both, once, and the template renders what
it is handed. What the consistency gate alone removes, at today's dollar floor:

| org | cards today | after | what goes |
|---|---|---|---|
| clc | 5 | **0** | all five name growing or flat accounts (+49%, +18%, −2%, +10%, +119%) |
| cci | 3 | 1 | Stacie Baker (+23%) and Tim Shelton (flat) go; Stacey Chiavetta (−42%) stays |
| hfg | 5 | 4 | CANOREP goes (+6.7%) |
| kal | 4 | 4 | rep 0999's card **keeps** but re-points from a +20% account to the −62% one |
| ali | 3 | 2 | rep 68 goes (no prior baseline, growing) |
| sarreid | 4 | 4 | rep 099's card re-points from −6.2% to −90.1% |
| bri, bmc | 5, 3 | 5, 3 | unchanged — every card already named a slipping account |

`gather.py` is out of scope, so `accounts_at_risk` still counts presence; the
**card count printed on the header line** therefore still reads `$XK at risk
across N accounts` using that count. Correcting `accounts_at_risk` itself is a
`gather.py` change and belongs to whoever owns that file next.

### 6.3 — S3 · "the hero calls a contracting base 'roughly flat'"

hfg's hero renders from the **template**, not from authored prose
(`hfg_prose_2026-07-02.json` has `hero_framing: null`), so this is squarely a
code question. Three of eleven orgs are on that path: hfg, bmc, bri.

| measure | what it counts | hfg |
|---|---|---|
| `same_base_lift_pct` | dealers active in **both** periods | **−1.8%** → "roughly flat" |
| `nrr_pct` | the **prior-year cohort**, including the ones that went dark | **83.7%** → $0.84 per $1 |

The gap is the 1,080 lapsed accounts. `same_base_lift_pct` excludes them by
construction, so it cannot see the $16.5M §5 says was handed back — which is
why the hero and §5 of the same document disagree by 14 points.

**Recommendation: lead on NRR, "spending less" below 97%.** It is the measure
§5 already reports, and stating it in §5's own phrasing ("$0.84 for every
dollar") makes a T1-5 contradiction structurally impossible rather than merely
unlikely. The threshold matters less than the measure: at −5% on lift, hfg,
cci and kal all read "roughly flat" while their retained dollars are down
16%, 12% and 8%.

Under the recommendation, the three template-hero orgs read:

| org | today | recommended |
|---|---|---|
| hfg | "spending **roughly flat** vs. prior year" | "spending less — **$0.84 for every dollar** they spent last year" |
| bmc | "spending less — **−62%** vs. prior year" | "spending less — **$0.76 for every dollar**" |
| bri | "spending less — **−6%** vs. prior year" | "spending less — **$0.92 for every dollar**" |


---

## 7. What flipping the profile actually does — all 11 orgs

`ACTIVE_PROFILE = RECOMMENDED_PROFILE`, full cohort re-run, offline, ~10s.
This is what the owner is deciding about. **It is not what W3 ships.**

```
ORG      DATE         EXIT  OUTCOME      LINES     FILE
------------------------------------------------------------------------
sarreid  2026-07-02   0     SHIP         378       Sarreid_Ltd._CEO_intelligence_report_2026-07-02.html
cci      2026-07-02   0     SHIP         351       Currey_and_Company_CEO_intelligence_report_2026-07-02.html
da       2026-07-09   0     SHIP         172       Dainolite_Ltd._CEO_intelligence_report_2026-07-09.html
clc      2026-07-09   0     SHIP         363       Capital_Lighting_Fixture_Co._CEO_intelligence_report_2026-07-09.html
hfg      2026-07-02   0     SHIP         311       Hubbardton_Forge_CEO_intelligence_report_2026-07-02.html
kal      2026-07-02   0     SHIP         347       Kalco_Lighting___Allegri_Crystal_CEO_intelligence_report_2026-07-02.html
ali      2026-06-30   0     SHIP         304       Access_Lighting_CEO_intelligence_report_2026-06-30.html
sca      2026-07-02   0     SHIP         172       Shadow_Catchers_CEO_intelligence_report_2026-07-02.html
bsc      2026-07-14   2     REDIRECT     125       bsc_GATESTOP_2026-07-14.md
bmc      2026-07-09   0     SHIP         446       Bassett_Mirror_CEO_intelligence_report_2026-07-09.html
bri      2026-07-01   0     SHIP         336       Bulbrite_CEO_intelligence_report_2026-07-01.html
------------------------------------------------------------------------
ran=11  skipped=0  no-artifact=0  →  _recommended/
```

**Every org still SHIPs. No outcome changes.** Visible-text delta vs `_baseline`:

| org | lines +/− | what changed |
|---|---|---|
| sarreid | +5 / −12 | 3 plays → 2 (the "every anchor dealer already buys it" cross-sell goes) |
| cci | +1 / −21 | 3 coaching cards → 0 (2 growing, 1 immaterial — see §5 caveat 1) |
| da | — | no change (NONE confidence) |
| clc | +1 / −55 | §3 omitted (the play was "the cross-sell is already happening"); 5 coaching cards → 0, all five naming growing accounts |
| hfg | +2 / −54 | §3 omitted; 5 coaching cards → 0; hero reads "$0.84 for every dollar" |
| kal | +3 / −21 | 4 cards → 1, and the survivor re-points to the account that actually slipped |
| ali | +2 / −34 | §3 omitted; 3 cards → 1 |
| sca | — | no change (NONE confidence) |
| bsc | — | no change (REDIRECT / correct-refusal path) |
| bmc | +1 / −1 | hero reads "$0.76 for every dollar" |
| bri | +1 / −1 | hero reads "$0.92 for every dollar" |

### hfg, read end to end — the brief's acceptance test

```
13d12
< Do this month
28c27
< Your existing accounts are spending roughly flat vs. prior year. Topline growth is being carried by new-dealer intake, not reorder momentum.
---
> Your existing accounts are spending less — $0.84 for every dollar they spent last year. Topline growth is being carried by new-dealer intake, not reorder momentum.
56,57d54
< Build the push →
86,91d82
< This Month
< 1 play
< Axis cross-sell.
110,120d100
< Do this month · 1 play
< Axis cross-sell
< Play 01 — Axis cross-sell
< The Axis family — $0.60M across 24 dealers and 6 SKUs — is the cross-sell on the table. One dealer already buying the top custom fixture has never ordered Axis; the estimated upside is $7K–$12K, DIRECTIONAL, on a single door.
175c155
< Top 10 reps by LTM invoiced · Top-5 reps by dollars at risk on their…
---
> Top 10 reps by LTM invoiced
192,224d171
< Top-5 reps by dollars at risk on their own book
< Card 1 · rep CANOREP — $22K at risk across 1 account
< Rep CANOREP's flagged book is about $22K of near-term risk, and it sits on a $602K account that is actually pacing up (about $19K of half-over-half gain). Treat it as coverage maintenance.
< Card 2 · rep 41168 — $1K at risk across 1 account
< Card 3 · rep 45123 — $1K at risk across 1 account
< Card 4 · rep 42332 — $1K at risk across 2 accounts
< Card 5 · rep 12328 — $1K at risk across 3 accounts
```

All three symptoms are gone: no $7–12K month, no `$1K at risk` cards, no risk
card on a growing account, and no hero that calls a 16% contraction flat.

**One thing flipping the profile does NOT fix, and the owner should see it:**
hfg's hero still closes *"Topline growth is being carried by new-dealer intake,
not reorder momentum"* — but hfg took on 998 new dealers and lost 1,080, so
there is no topline growth to carry. That sentence is unconditional template
copy, not a thresholded claim, and it is outside W3's scope list. Logged.

**And one cost:** kal's and clc's authored Slot-C coaching narratives were
written against the old card set. When cards are removed,
`align_coaching_narratives` correctly declines to re-attach prose that names a
different rep, and the surviving card falls through to deterministic template
copy. That is the right behaviour — it is the same situation §10 of
`AUDIT_FINDINGS.md` describes for the nine authored heroes — but the affected
`outputs/*_prose_*.json` should be regenerated after the owner picks numbers.


---

## 8. Verification — every command, real pasted output

Shipped state: `ACTIVE_PROFILE = BASELINE_PROFILE`.

### 8.1 `make check`

```
.venv-renderer/bin/python -m pytest tests/ -q
..................................x..................................... [  8%]
........................................................................ [ 16%]
........................................................................ [ 24%]
...........................s....ss....s....ss....................x...... [ 32%]
........................................................................ [ 40%]
............................x........................................... [ 48%]
........................................................................ [ 56%]
........................................................................ [ 64%]
........................................................................ [ 72%]
........................................................................ [ 80%]
........................................................................ [ 88%]
.....................................................xx................. [ 96%]
...........................                                              [100%]
880 passed, 6 skipped, 5 xfailed in 1.58s
./regression.sh --verify
══════════════════════════════════════════════════════════════
  Insightful 4.0 — Golden-set regression (v9 split verification)
  manifest: config/golden_set.json
  mode: verify
══════════════════════════════════════════════════════════════

── sarreid (SHIP, date=2026-07-02) ──
  deterministic core: 55398 bytes, sha256 match ✓
  prose conformance: PASS ✓
  total bytes: 55398 (range [50000, 67000]) ✓
── cci (SHIP, date=2026-07-02) ──
  deterministic core: 52464 bytes, sha256 match ✓
  prose conformance: PASS ✓
  total bytes: 52464 (range [48000, 63000]) ✓
── da (SHIP, date=2026-07-09) ──
  deterministic core: 38196 bytes, sha256 match ✓
  prose conformance: PASS ✓
  total bytes: 38196 (range [35000, 46000]) ✓
── clc (SHIP, date=2026-07-09) ──
  deterministic core: 55030 bytes, sha256 match ✓
  prose conformance: PASS ✓
  total bytes: 55030 (range [50000, 67000]) ✓
── hfg (SHIP, date=2026-07-02) ──
  deterministic core: 52519 bytes, sha256 match ✓
  prose conformance: PASS ✓
  total bytes: 52519 (range [48000, 64000]) ✓
── kal (SHIP, date=2026-07-02) ──
  deterministic core: 53352 bytes, sha256 match ✓
  prose conformance: PASS ✓
  total bytes: 53352 (range [49000, 65000]) ✓
── ali (SHIP, date=2026-06-30) ──
  deterministic core: 50981 bytes, sha256 match ✓
  prose conformance: PASS ✓
  total bytes: 50981 (range [46000, 62000]) ✓
── sca (SHIP, date=2026-07-02) ──
  deterministic core: 38331 bytes, sha256 match ✓
  prose conformance: PASS ✓
  total bytes: 38331 (range [35000, 46000]) ✓
── bsc (REDIRECT, date=2026-07-14) ──
  bsc_GATESTOP_2026-07-14.md: 6478 bytes, sha256 match ✓
── bmc (SHIP, date=2026-07-09) ──
  deterministic core: 60586 bytes, sha256 match ✓
  prose conformance: PASS ✓
  total bytes: 60586 (range [55000, 73000]) ✓
── bri (SHIP, date=2026-07-01) ──
  deterministic core: 51024 bytes, sha256 match ✓
  prose conformance: PASS ✓
  total bytes: 51024 (range [46000, 62000]) ✓

══════════════════════════════════════════════════════════════
  GOLDEN SET: PASS (11/11)
./tools/cohort_diff.sh

ORG      TEXT       CORE-SHA  OUTCOME    NOTE
----------------------------------------------------------------------
sarreid  same       same      SHIP       
cci      same       same      SHIP       
da       same       same      SHIP       
clc      same       same      SHIP       
hfg      same       same      SHIP       
kal      same       same      SHIP       
ali      same       same      SHIP       
sca      same       same      SHIP       
bsc      same       same      REDIRECT   
bmc      same       same      SHIP       
bri      same       same      SHIP       
----------------------------------------------------------------------
COHORT: no change vs baseline
```

Exit code **0**.

### 8.2 The W3 unit tests, verbose

```
============================= test session starts ==============================
platform darwin -- Python 3.14.2, pytest-9.1.1, pluggy-1.6.0 -- /Users/kylorjohnson/repos/supercat-4.0/Insightful Product 4.0/.venv-renderer/bin/python
cachedir: .pytest_cache
rootdir: /Users/kylorjohnson/repos/supercat-4.0/Insightful Product 4.0
plugins: cov-7.1.0, anyio-4.15.1
collecting ... collected 35 items

tests/test_phase5_size_scaling.py::test_the_shipped_profile_is_baseline PASSED [  2%]
tests/test_phase5_size_scaling.py::test_baseline_reproduces_the_pre_w3_absolute_constants PASSED [  5%]
tests/test_phase5_size_scaling.py::test_a_small_org_and_a_large_org_reach_the_same_RELATIVE_threshold PASSED [  8%]
tests/test_phase5_size_scaling.py::test_the_absolute_floor_still_binds_on_a_tiny_org PASSED [ 11%]
tests/test_phase5_size_scaling.py::test_a_missing_or_absent_size_base_degrades_to_the_floor[0] PASSED [ 14%]
tests/test_phase5_size_scaling.py::test_a_missing_or_absent_size_base_degrades_to_the_floor[0.0] PASSED [ 17%]
tests/test_phase5_size_scaling.py::test_a_missing_or_absent_size_base_degrades_to_the_floor[None] PASSED [ 20%]
tests/test_phase5_size_scaling.py::test_a_missing_or_absent_size_base_degrades_to_the_floor[-1.0] PASSED [ 22%]
tests/test_phase5_size_scaling.py::test_a_missing_or_absent_size_base_degrades_to_the_floor[nan] PASSED [ 25%]
tests/test_phase5_size_scaling.py::test_a_missing_or_absent_size_base_degrades_to_the_floor[inf] PASSED [ 28%]
tests/test_phase5_size_scaling.py::test_a_NONE_confidence_org_resolves_without_dividing_by_zero PASSED [ 31%]
tests/test_phase5_size_scaling.py::test_detectors_called_without_thresholds_keep_the_old_absolute_gates PASSED [ 34%]
tests/test_phase5_size_scaling.py::test_the_same_account_fires_or_not_depending_on_the_ORGS_size PASSED [ 37%]
tests/test_phase5_size_scaling.py::test_rep_atrisk_signal_reads_the_resolved_floor PASSED [ 40%]
tests/test_phase5_size_scaling.py::test_the_hfg_one_door_play_is_worth_a_fraction_of_a_percent_of_the_year PASSED [ 42%]
tests/test_phase5_size_scaling.py::test_a_play_below_the_orgs_floor_is_dropped_not_padded PASSED [ 45%]
tests/test_phase5_size_scaling.py::test_the_baseline_floor_of_zero_keeps_every_play PASSED [ 48%]
tests/test_phase5_size_scaling.py::test_an_unquantifiable_play_scores_zero_rather_than_raising PASSED [ 51%]
tests/test_phase5_size_scaling.py::test_baseline_keeps_todays_card_set_exactly PASSED [ 54%]
tests/test_phase5_size_scaling.py::test_a_rep_whose_flagged_accounts_are_all_growing_gets_no_risk_card PASSED [ 57%]
tests/test_phase5_size_scaling.py::test_both_hfg_gates_drop_their_cards_for_their_own_reasons PASSED [ 60%]
tests/test_phase5_size_scaling.py::test_the_card_names_an_account_that_actually_slipped_not_the_biggest_one PASSED [ 62%]
tests/test_phase5_size_scaling.py::test_a_pure_discount_leak_rep_never_becomes_a_card PASSED [ 65%]
tests/test_phase5_size_scaling.py::test_the_card_floor_scales_with_the_org PASSED [ 68%]
tests/test_phase5_size_scaling.py::test_the_two_same_dealer_measures_disagree_and_lift_is_always_the_gentler_one[sarreid-29.1-106.4-up-up] PASSED [ 71%]
tests/test_phase5_size_scaling.py::test_the_two_same_dealer_measures_disagree_and_lift_is_always_the_gentler_one[cci-3.8-88.5-flat-less] PASSED [ 74%]
tests/test_phase5_size_scaling.py::test_the_two_same_dealer_measures_disagree_and_lift_is_always_the_gentler_one[clc-71.9-173.2-up-up] PASSED [ 77%]
tests/test_phase5_size_scaling.py::test_the_two_same_dealer_measures_disagree_and_lift_is_always_the_gentler_one[hfg--1.8-83.7-flat-less] PASSED [ 80%]
tests/test_phase5_size_scaling.py::test_the_two_same_dealer_measures_disagree_and_lift_is_always_the_gentler_one[kal--4.0-91.8-flat-less] PASSED [ 82%]
tests/test_phase5_size_scaling.py::test_the_two_same_dealer_measures_disagree_and_lift_is_always_the_gentler_one[bmc--62.1-76.0-less-less] PASSED [ 85%]
tests/test_phase5_size_scaling.py::test_the_two_same_dealer_measures_disagree_and_lift_is_always_the_gentler_one[bri--5.9-92.1-less-less] PASSED [ 88%]
tests/test_phase5_size_scaling.py::test_the_hero_measure_is_a_profile_choice_not_a_hardcoded_one PASSED [ 91%]
tests/test_phase5_size_scaling.py::test_a_callout_jump_never_points_at_a_section_that_did_not_render PASSED [ 94%]
tests/test_phase5_size_scaling.py::test_omitting_available_ids_keeps_the_pre_w3_rendering PASSED [ 97%]
tests/test_phase5_size_scaling.py::test_an_empty_play_list_turns_the_whole_section_off PASSED [100%]

============================== 35 passed in 0.10s ==============================
```

### 8.3 Golden-core checksum delta

**None.** All eleven `deterministic core … sha256 match ✓`, `GOLDEN SET: PASS
(11/11)` (§8.1). `config/golden_set.json` was not opened. There is therefore no
per-org justification to write — that is the point of shipping BASELINE.

### 8.4 Per-org cohort delta

**None.** `COHORT: no change vs baseline`, all eleven `same / same` (§8.1).

### 8.5 Test count

`880 passed, 6 skipped, 5 xfailed` — was `845 passed` before this branch
(`+35`, all in `tests/test_phase5_size_scaling.py`).

### 8.6 Both traps, hit and logged

**Trap 1 — stale artifacts.** Hit, in a form the brief did not spell out.
`regression.sh --verify` is *checksum-only*: it hashes whatever HTML is sitting
in `outputs/`, it does not re-run. So after a `_recommended` cohort run,
`make check` reported `GOLDEN SET: FAIL (3 passed, 8 failed)` **with the
shipped BASELINE code** — the failure was entirely leftover HTML. Deleting
`outputs/*_DRAFT_*.md` is not enough; the HTML is what `--verify` reads.

> The reliable sequence after changing the active profile is
> **`./tools/cohort_diff.sh` first** (it re-runs all eleven and rewrites
> `outputs/`), **then `make check`**. Running `make check` alone on a dirty
> `outputs/` reports a failure that does not exist. Confirmed both ways: the
> extracted deterministic core of the "failing" `bri` artifact was
> **byte-identical** to the pre-change one when regenerated.

**Trap 2 — `| first` on an empty sequence.** Avoided. Nothing new uses `| first`;
`section_06_team.md.j2` lost the one it had (`... | sort(...) | first` on
`gather.decay`) when the account choice moved into `signals.coaching_card_reps`,
which uses an explicit `sorted(...)` and an emptiness check.

---

## 9. Self-assessment against each DoD line

| DoD line | Status | Evidence |
|---|---|---|
| Every constant classified **size-dependent** (convert) or **size-neutral** (leave, and say so) | **met** | §3 — 12 size-neutral named and left alone, 11 size-dependent converted (4 of which were unnamed inline magic numbers before this branch) |
| Each converted constant has a `max(floor, pct × inv_ltm_net)` form or a documented percentile equivalent, reading org size from `RunPosture` | **met** | `SizeScaledFloor.resolve`; `org_size_base(posture, gather)` reads `RunPosture.inv_ltm_net`. §3 records why no percentile gate was added (the cached extracts are pre-truncated) |
| Calibration table: 11 orgs × ≥3 candidate values × every converted constant, in `handoffs/exec/W3_evidence.md` | **met** | §4 — 11 orgs × **4** values × 11 constants, plus fired-count, top-ranked item, and the S3 measure table |
| `make check` green with the defaults shipped — golden `PASS (11/11)`, cohort no-change | **met** | §8.1, exit 0 |
| Unit tests: small org and large org at the same *relative* threshold | **met** | `test_a_small_org_and_a_large_org_reach_the_same_RELATIVE_threshold`, `test_the_same_account_fires_or_not_depending_on_the_ORGS_size` |
| Unit tests: the absolute floor still binding on a tiny org | **met** | `test_the_absolute_floor_still_binds_on_a_tiny_org` |
| Unit tests: `commerce_confidence = NONE` org (`inv_ltm_net = 0`) not dividing by zero | **met** | `test_a_NONE_confidence_org_resolves_without_dividing_by_zero`, plus 6 parametrized degenerate bases (0, 0.0, None, −1, NaN, inf) |
| `AUDIT_FINDINGS.md` §2.1 updated to describe the mechanism that now exists | **met** | §2.1 rewritten |
| **S1** — plays carry a size-scaled materiality floor | **met** | `play_upside_ceiling` + `thresholds.play_min_upside`; §4.7, §6.1 |
| **S1** — the hero-only stopgap of 3 in `_macros.md.j2` is removed | **met** | deleted; replaced by `thresholds.cross_sell_hero_min_dealers`. §4.11 |
| **S1** — "no play qualified this month" is reachable | **met, and it was not before** | required fixing a dangling `#thismonth` anchor in `report_render` — §2c. hfg and clc now `smoke_check: PASS · step10: PASS · SHIP` with zero plays |
| **S2** — coaching cards honour the same floor **and** the same `account_needs_a_call` definition; no risk card for a rep whose flagged accounts are all growing | **mechanism met, dormant by default** | `signals.coaching_card_reps` is the single gate, read by the template *and* by `run_report`. §6.2 shows what it removes on all 8 commerce orgs. It is **off** in BASELINE because turning it on moves 6 of 11 orgs — see §10 |
| **S3** — a recommendation on which same-dealer measure the hero leads with and at what threshold, with hfg (−2% lift vs $0.84 NRR) in the table | **met** | §4.12 and §6.3 — recommend **NRR below 97%**; hfg, and all 7 orgs with both measures, are in the table |
| The owner can read hfg end to end and not hit an immaterial or self-contradictory claim | **true under `RECOMMENDED_PROFILE`; not under what ships** | §7. One residual unconditional claim logged ("topline growth carried by new-dealer intake" on an org whose dealer base shrank) — outside the scope list |

### 10. The one place this brief contradicts itself, and the call I made

Two DoD lines cannot both hold:

- *"`make check` green with the defaults you ship — cohort **no-change**."*
- *"**S2:** … no risk card for a rep whose flagged accounts are all growing"*
  and *"the owner can read hfg end to end and not hit an immaterial or
  self-contradictory claim."*

The S2 consistency rule alone — before any dollar threshold — changes **6 of 11
orgs** (§6.2), because the defect is that widespread. clc loses its entire
coaching-card block; every one of its five cards names a growing account.

I resolved it in favour of the **explicit** instruction, because it carries its
own reasoning and a stamp consequence: *"A green cohort proves the mechanism is
neutral; the owner's chosen values will move it deliberately, later, with a
re-stamp."* So:

- The consistency rule is **built, wired through both surfaces, and unit-tested**
  — `test_a_rep_whose_flagged_accounts_are_all_growing_gets_no_risk_card` pins
  it in isolation from the dollar floor, exactly as the brief asked ("do the
  consistency half even if the materiality half needs owner numbers").
- It is **off** in the shipped profile, so the cohort is green.
- §6.2 and §7 show precisely what turning it on does, per org, so the decision
  is a reading exercise rather than a code exercise.

If the reviewer reads the brief the other way — S2 lands hot and the golden set
is re-stamped at this gate — the change is `coaching_cards_require_needs_a_call=True`
in `BASELINE_PROFILE`, one line, and §6.2's table is the per-org justification
that the stamp protocol asks for.

### 11. Things found on the way that are somebody else's

1. **`RepRisk.accounts_at_risk` counts presence, not risk** (`gather.py:1255`).
   It is `sum(1 for a in decay if a.rep_number == risk.rep_number)` over the
   top-N decay extract. The card header still prints that count. `gather.py` is
   out of scope; the count should be over `account_needs_a_call` rows.
2. **`AccountDecay.is_real_decline` carries its own `20_000` floor**
   (`gather.py:124`) while `signals.DECLINE_MIN_LTM_DOLLARS` is `50_000`. Two
   floors for one concept, 2.5× apart, and only one of them was converted here.
3. **CEO-callout jump links were never checked against the rendered section
   set** — fixed in §2c, but the same class of bug applies to any section a
   future materiality floor empties.
4. **hfg's hero asserts topline growth on a shrinking dealer base** (§7).
   Unconditional template copy.
5. **`ali` shows 13 "new line" families** because it has no prior year at all
   (`active_prior_ltm = 0`), so every family reads `is_new`. No candidate
   threshold touches this; it is a `FamilyRollup.is_new` definition problem.

---

## 12. Reproducing §7 (the `_recommended` cohort)

`_recommended/` is not committed — it is client text and, unlike `_baseline/`
and `_current/`, it is not gitignored. Regenerate it in ~10s, offline:

```bash
cd "Insightful Product 4.0"
sed -i '' 's/^ACTIVE_PROFILE = BASELINE_PROFILE$/ACTIVE_PROFILE = RECOMMENDED_PROFILE/' pipeline/signals.py
./tools/cohort_run.sh _recommended
for f in _baseline/*.txt; do diff "$f" "_recommended/$(basename "$f")"; done

# put it back, and note the ORDER — see §8.6
sed -i '' 's/^ACTIVE_PROFILE = RECOMMENDED_PROFILE$/ACTIVE_PROFILE = BASELINE_PROFILE/' pipeline/signals.py
./tools/cohort_diff.sh && make check
```
