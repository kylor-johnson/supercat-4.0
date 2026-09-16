# Health V3.0 Readiness Review — 2026-05-11

## 1. Verdict

**Needs calibration**

---

## 2. Per-check summary

### Check 1 — Math integrity: **Pass**

All 104 rows are `scoring_status = complete` with `dimensions_scored = 4`. Every dimension score sits in `[0, 100]` (engagement min 26.7 / max 96.0; adoption min 33.3 / max 100; value_delivery min 0.0 / max 100; operational_health min 0.0 / max 100) with zero nulls. `health_score` matches `round(mean(4 dims), 1)` within tolerance for every row; the five rows where the absolute difference is exactly `0.1` (`jcusa`, `vcg`, `bri`, `clli`, `mli`) are banker's-rounding tie-breaks on `.x5` means (e.g., jcusa raw mean 83.35 → operator 83.3, naive `round(…, 1)` 83.4) — within the spec's "within 0.1" allowance, not a bug. Health-band assignment matches the band ladder in every row.

### Check 2 — Override sanity: **Pass**

`ghost_account = true` count is 0, which is expected. No row in the CSV has `logins_90d = 0` (verified by parsing every `engagement_narrative`), so the override correctly did not fire for anyone. The three pre-flagged candidates (`st`, `tel`, `hmjc`) each have ≥ 1 login in 90d (st: 7 logins / 22 users / last login 4d ago; tel: 12 / 20 / 66d; hmjc: 10 / 118 / 7d), so none qualifies under §5.1. The single high-ARR Critical row (`tel`, ARR \$13,440, health 19.2) was reached organically through low dimension scores (E=26.7, A=50.0, V=0.0, O=0.0), not via override — and it correctly did *not* trigger ghost because it has 12 logins, not zero. No false-negative ghost cases exist in the run.

### Check 3 — Carveout sanity: **Pass with one investigation flag**

- **Contract pricing (`wac`, `fal`):** both narratives include the literal string `(contract pricing — price check skipped)`. wac: catalog 100%, opsHealth 74.4. fal: catalog 98%, opsHealth 83.3. Carveout is firing as designed.
- **Price-level pricing (12 orgs):** 11 of 12 score 91–100% catalog completeness — strong evidence the `prices_json` clause in `load_pg_catalog` is functioning correctly for price-level shapes (kll 97%, jc 91%, ta 100%, cci 93%, ufi 100%, kal 92%, clm 100%, clc 100%, rw 100%, pf 100%, vic 99%). Operational_health for these 11 ranges 76.5–97.2, all ≥ 70.
- **Outlier:** `mfc` scores 29% catalog (1,507 of 5,257 products complete) → catalog_score 20, freshness 20, imports 100 → opsHealth 46.7. Per the user's stated rule, an opsHealth < 60 with catalog as a drag in a price-level org is a Bug. However, the strong contrary evidence (the other 11 carveout orgs all sail through) suggests the carveout SQL itself is intact and mfc's gap is `long_description` or `image_exists`, not `prices_json`. Surfaced in the anomaly list as a single mfc-specific investigation rather than a portfolio-wide carveout failure.

### Check 4 — Applicability sanity: **Pass**

iPad-only orgs (`tam`, `gsa`, `hf`) all show `mobile_sites` flags `False/False/False` and have no portal/catalog/sales-portal references in their adoption or value-delivery narratives; `bundle_config_mismatch = false` for all three. `bp` (the known anomaly) correctly carries `bundle_config_mismatch = true`, with catalog and online ordering treated as applicable in the 7-feature adoption denominator (mobile_sites flags won, per spec). The narrative does not yet *call out* the mismatch as a data-hygiene flag in plain English — that's covered under Known V3.1 gap (descriptive-not-interpretive narratives), not a Check 4 failure.

### Check 5 — Archetype reasonableness: **Mixed — Reds drift one band high**

Greens line up perfectly. Non-ghost actives line up perfectly. Reds drift: 4 of 5 land in **Watch** rather than Kylor's expected **At Risk / Critical**. Only `tel` lands where Kylor placed it.

| Org | Kylor expected | V3 produced | Match? | Dimension breakdown if mismatch |
|---|---|---|---|---|
| sc | Healthy/Thriving | Thriving (90.9) | Match | — |
| scw | Healthy/Thriving | Thriving (89.2) | Match | — |
| ufi | Healthy/Thriving | Thriving (97.8) | Match | — (price-level + Green: ops 97.2, catalog 100%) |
| gh | Healthy/Thriving | Thriving (85.8) | Match | — |
| mli | Healthy/Thriving | Thriving (88.7) | Match | — |
| st | At Risk/Critical | **Watch (49.6)** | **Mismatch** | E 46.7 / A 60.0 / V 0.0 / O 91.7 — 1 of 22 users active, V=0 (no iPad orders, no sharing, no portal traffic) but ops carries the average back to 49.6 |
| hmjc | At Risk/Critical | **Watch (50.4)** | **Mismatch** | E 46.7 / A 60.0 / V 33.3 / O 61.7 — 3 of 118 enabled users (3% active ratio); breadth-of-features point system gives partial credit |
| tel | At Risk/Critical | Critical (19.2) | Match | — |
| hh | At Risk/Critical | **Watch (50.4)** | **Mismatch** | E 46.7 / A 75.0 / V 33.3 / O 46.7 |
| mfc | At Risk/Critical | **Watch (53.3)** | **Mismatch** | E 53.3 / A 80.0 / V 33.3 / O 46.7 — V drag is portal/sharing absence; A still high because applicability gate counts every iPad/SmartStacks/sharing surface that's "configured" with low usage thresholds |
| kll | Watch or better, non-ghost | Thriving (80.2) | Match | — |
| fsf | Watch or better, non-ghost | Thriving (88.2) | Match | — |

`sc` deduplicated (Greens + non-ghost active). The systematic Red-to-Watch drift is a calibration signal, not a per-org coincidence — surfaced in the anomaly list. mfc's breakdown is included regardless of match status per instruction.

### Check 6 — Distribution shape: **Fail (calibration)**

The HANDOFF guideline is "Thriving rare-but-present (5–15%); Healthy/Watch the bulk; Critical < 10% outside ghost spikes." This run produces **53% Thriving (55/104)** and 11% Watch (11/104). That inverts the expected shape — Thriving is the modal band rather than the rare top end. Combined with the Check 5 finding that Reds drift into Watch, the band thresholds (or, more likely, the underlying point-system thresholds in Adoption/Value Delivery — which give 100/100 scores easily because applicability gates are binary and channel thresholds are intentionally low per README §3 "Thresholds are intentionally low for V1") need a calibration discussion before V3.0 ships to CS as a portfolio segmentation tool.

### Anomalies the cache-population agent did NOT pre-flag

- **Bundle/config-mismatch flag is over-counted by ~7×.** Of the 23 mismatch flags, 20 are false positives caused by a string-matching bug in the operator (`mal_bundle == "Full"` exact match misses the actual MAL string `"Full (Cart+Portal)"`). Real mismatches are 3: `bp`, `jcusa`, `abol`. Detail in anomaly list.
- **9 support fires look real.** Spot-check: cfg, vcg, ah, sc, wwjc, clli, pf, shl, ufi — all are paying \$18K–\$40K ARR active customers in Healthy/Thriving bands with at least one open `l3 - engineering intervention` conversation. Not random orgs with stale tags; these are big-engaged accounts hitting engineering issues, exactly the support-modifier intent.

---

## 3. Anomaly list

| Anomaly | Classification | Recommended action |
|---|---|---|
| Bundle/config mismatch over-flags 20 `Full (Cart+Portal)` orgs as catalog-mismatch because the operator uses `mal_bundle == "Full"` exact match instead of substring (lines 829–830 of `health_operator_v3.py`); true mismatch count is 3 (bp, jcusa, abol), not 23. | Bug | Change `mal_bundle == "Full"` to `"Full" in mal_bundle` in both `bundle_says_cart` and `bundle_says_catalog` and rerun Step 4b only (no cache repopulation needed). |
| 53% Thriving (55/104) vs HANDOFF guideline of 5–15%; combined with 4 of 5 Kylor-Red orgs landing in Watch, the band ceiling is too generous. Operator matches spec; the spec's intentionally-low V3.1-calibrate-later thresholds in Adoption/Value Delivery + the 80-floor for Thriving combine to push everyone with a working data feed into the top band. | Calibration | Defer threshold adjustment to a single calibration pass after the bundle-bug fix is applied (a 0.1–1.0 reshuffle is inevitable post-fix); bring the calibrated thresholds back to README §3 / §6 for Kylor sign-off rather than tuning silently. |
| `mfc` opsHealth 46.7 (catalog 29% = 1,507/5,257 products complete) — flagged by user's literal Check 3 rule as a potential carveout bug, but the other 11 price-level orgs all score 91–100% catalog so the SQL clause is demonstrably functional. mfc's gap is most likely missing `long_description` or `image_exists`, not `prices_json`. | Calibration | Sample 5–10 incomplete mfc products against the three completeness criteria; if `prices_json` is the gap, escalate to Bug; if description/image is the gap, classify as data hygiene and leave the score as-is. |
| V3.0 narratives are descriptive, not interpretive — `bp`'s adoption narrative lists "Online Ordering" as unused without flagging it as a data-hygiene mismatch, mfc's narrative reports counts without explaining why catalog completeness is low, and Reds in general get count-only summaries that don't help a CSM decide what to do. README §1/§3/§4 example narratives describe the V3.1 destination. | Known V3.1 gap | Defer per HANDOFF Known Issue #6; surface to CS that V3.0 narratives are *what*, not *why*. |
| Seasonality not modeled — at least one of the four Red mismatches (mfc and possibly hh, both furniture-adjacent) may be measuring an off-cycle window. | Known V3.1 gap | Defer per HANDOFF Known Issue #7; revisit after 12 months of V3 history exists. |

---

## 4. Distribution sanity

Real numbers from the 104-row CSV: bands are `Thriving 55 / Healthy 36 / Watch 11 / At Risk 1 / Critical 1` (matching Agent A's pre-flag). `scoring_status` is `complete` for all 104 — zero `partial`, zero `blocked`, every row has all four dimensions. `ghost_account = true` count is **0** (expected per Kylor's note; verified that no row has both `arr ≥ 5000` and `logins_90d = 0`). `support_fire = true` count is **9**, all L3 escalations on big-ARR active customers (cfg, vcg, ah, sc, wwjc, clli, pf, shl, ufi) — the fire flag looks like it's catching real support hot spots, not stale tags. `bundle_config_mismatch = true` count is **23** but only 3 are real (bp, jcusa, abol) — the other 20 are the `Full (Cart+Portal)` string-match bug above. `denominator_quality = "stale"` count is **2** (soi: 6 active / 4 enabled; mlc: 41 active / 37 enabled — both look like the customer-portal-account inflation case the spec calls out). `support_data_available = false` is **7** orgs (gsa, mlc, ihm, eglo_can, kkc, pw, rac), none of which carry a fire flag — consistent with no domain match in HelpScout, not a bug.

Bundle distribution (MAL `bundle` column):
- iPad-only: 56 (54%)
- Full (Cart+Portal): 20 (19%)
- iPad+Catalog+Portal: 14 (13%)
- iPad+Catalog+Cart: 9 (9%)
- iPad+Catalog: 5 (5%)

Bundle × band reveals the calibration story plainly: every one of the 20 `Full (Cart+Portal)` orgs lands Healthy or Thriving (3 Healthy, 17 Thriving), every one of the 14 `iPad+Catalog+Portal` orgs lands Healthy or Thriving (2 Healthy, 12 Thriving), and 9 of 9 `iPad+Catalog+Cart` orgs land Healthy. Thriving share is being driven primarily by orgs with the most *applicable* surfaces — they earn 100/100 on Adoption and Value Delivery because the applicability point system saturates with the low V1 usage thresholds. The 11 Watch / 1 At Risk / 1 Critical rows are concentrated in iPad-only (9 of 11 Watches, plus the 1 At Risk and the 1 Critical) and in iPad+Catalog (1 Watch, 1 Critical). This bundle-stratified view strengthens the Calibration anomaly: under V3.0, having more product surfaces is a near-guarantee of Thriving, which conflates breadth-of-config with depth-of-engagement.
