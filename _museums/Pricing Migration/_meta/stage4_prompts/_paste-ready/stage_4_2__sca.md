# Stage 4.2 — Paste-Ready Session — `ord_id = sca` (Shadow Catchers) — **v2 (post-CL-027 refresh)**

> **v2 refresh stamp 2026-05-26 (post-CL-027 RESOLVED at `_root/05 §2.1.2` source)**: this paste-ready is a refreshed version of v1 (2026-05-26 original). The v1 drafter subagent run hard-stopped at Step 5 per `_root/CONTRACTS.md §2` because `_root/05 §2.1.2` (Format B URN canonical block) carried a single expansion-baked `[IF excess users remain after new included base]` sub-block that produced direction-inverted prose for sca's URN-primary + IUR-secondary REDUCTION-direction case (legacy `provided=25 → new included=10`). The v1 drafter's hard-stop was design-correct. **CL-027 RESOLVED 2026-05-26 at source**: planning agent landed a parallel `[IF excess users remain AND secondary driver = included_user_reduction (base shrinking from legacy to current tier standard)]` sub-block at `_root/05 §2.1.2` mirroring the pre-existing §2.1.3 line 123 CEO Letter pattern (direction-neutral "adjusting" prose); §2.1.7 routing rewritten to dispatch URN+IUR-secondary to the appropriate sub-block by direction; §4 weaving matrix row 5 count re-tallied 7 → 26 (25 reduction + 1 expansion = `bcf`); §2.4.1 Option A semantic extended to cover URN-side §2.1.2 / §2.1.3 alongside the pre-existing TBI-side §2.3.2 / §2.3.3 (closes the CL-026 / CL-023 TBI-side-only scope-gap). Two planning-agent self-corrections logged at CL-027 RESOLVED entry: (1) v1's pre-flight observation 2 was WRONG (claimed §2.1.7 sub-block describes "legacy-allotment-reducing-to-new-tier-standard"; actual §2.1.7 pre-CL-027 routed URN+IUR-secondary to §2.1.2's EXPANSION-only sub-block; conflated IUR-primary §2.4.x reduction-orientation with URN+IUR-secondary §2.1.7 routing); (2) CL-026 / CL-023 joint resolution had a TBI-side-only scope-gap. v2 corrects pre-flight observation 3 + data observations 1 + 2 below. **Run this v2 paste-ready in a fresh Cursor agent chat**. sca is the FIRST production proof to exercise the newly-added §2.1.2 reduction-aware sub-block.
>
> **Planning-agent paste-ready artifact** — created 2026-05-26 by Stage 4.2 planning agent (second-completing Format B production-proof per Stage 4.2 cohort execution sequence; `cci` Format B standard-variant proof closed-out + APPROVED 2026-05-26; `bri` Format B production-proof attempt #2 hard-stopped at Step 5 2026-05-26 per CL-026 IUR-on-expansion field-signature mismatch; CL-026 + CL-023 jointly RESOLVED 2026-05-26 via `_root/05` source-fix + v6.2 10-row re-stamps + Decision 1 stamp-both + Decision 2 Option A semantic clarification; `bri` re-paste-run deferred per operator-stamped next-action `apply_source_fix_only_no_bri`; `sca` selected as next clean Format B candidate from the 18-row remaining-clean cohort; v1 sca run 2026-05-26 hard-stopped at Step 5 — CL-027 RESOLVED 2026-05-26 at `_root/05 §2.1.2` source via Option 2 proper source-fix; v2 paste-ready refresh follows).
> **Source**: `_meta/stage4_prompts/stage_4_2__format-b__per-account-drafter.md` (canonical 697-line Format B drafter prompt; APPROVED 2026-05-26 by operator + production-proven via `cci` 2026-05-26 closeout).
> **Substitution applied**: `[ORD_ID]` → `sca` throughout (13 occurrences resolved; lowercase `[ord_id]` placeholders in file paths preserved for fresh-agent resolution per `_root/07 §6`).
> **Operator action**: copy this entire file's content + paste into a fresh Cursor agent chat as the first message. Do not modify.
> **Fresh-agent expectation**: per Appendix A.3 — one account in (`sca`), two files out (`format-b-notices/sca__<company-slug>__brief.md` + `format-b-notices/sca__<company-slug>__delivery-email.md`), conformance block, STOP.

---

## Planning-agent pre-session annotation (informational; read first)

The planning agent performed the routing pre-flight against the v6.2 row + routing CSV joint state per Appendix A.4 + Appendix B.5.1 `csv.DictReader` discipline + Appendix B.5.2 canonicality check (operator-stamped 2026-05-26). **THREE conditional firings + TWO soft-drift observations surface during pre-flight** — all expected for `sca`'s shape (none blocking; all enumerated in the data-observations section below + routed to the conformance block):

1. **`_root/04 §4.4` high-delta annual-dollar lede rule FIRES** — `delta_pct = +30.9%` (> 30% threshold). The lede paragraph (Section 3b) MUST name the annual dollar impact (`$224 × 12 = $2,688/year`) alongside the monthly change inside the same sentence per `_root/04 §4.4` Format B variant. QB-078 + QB-106 (annual figure reconciliation within ±$1) both fire and PASS.

2. **`_root/04 §4.7` early-adopter tenure paragraph FIRES** — `cohort_year = 2015` (at the threshold; "`cohort_year ≤ 2015`" per `_root/04 §4.7`). Section 3f of the brief populates per §4.7 Format B variant with `[YEAR] = 2015`. (This is the FIRST production proof to fire §4.7 — `cci` was 2021 and did not fire; `lpf` Format A 2026-05-26 was a separate format.)

3. **`_root/05 §2.1.7` URN + IUR secondary-driver integration sub-block FIRES — REDUCTION-direction variant per CL-027 RESOLVED source-fix** — `migration_driver = user_rate_normalization` (URN-primary) + `secondary_drivers = included_user_reduction` (IUR-secondary). Per `_root/05 §2.1.7` templated coverage + post-CL-027 RESOLVED 2026-05-26 source-fix at §2.1.2 (added parallel `[IF excess users remain AND secondary driver = included_user_reduction (base shrinking from legacy to current tier standard)]` sub-block to Format B URN canonical block mirroring §2.1.3 line 123 CEO Letter pattern; sca's data `current_provided_users = 25 > included_users = 10` is the REDUCTION-direction case the new sub-block was added to handle). Section 3h secondary-driver weaving integrates URN+IUR within Section 3g primary block per `_root/05 §1.3` (NEVER as a separate section); the post-CL-027 §2.1.2 reduction-direction sub-block prose reads "Your included base is also adjusting from the legacy [LEGACY_INCLUDED] to the current [TIER] standard of [NEW_INCLUDED]. With [TRAILING_AVG] average users, [NEW_EXCESS] are now above the [NEW_INCLUDED]-user included base, billed at the graduated rate: [EXCESS_MATH_BREAKDOWN] = $[NEW_USER_CHARGE]/month" — direction-neutral "adjusting" prose (NOT "expanding"); substitute `[LEGACY_INCLUDED] = 25`, `[NEW_INCLUDED] = 10`, `[TIER] = T1`, `[TRAILING_AVG] = 18`, `[NEW_EXCESS] = 8`, `[EXCESS_MATH_BREAKDOWN]` per the graduated ladder math (8 excess @ $25 first-band rate), `[NEW_USER_CHARGE] = $200`. QB-092 PASSES (integration is within primary block); `§4.5` operations-unchanged sentence FORK to IUR-fork variant per `_root/05 §2.13` non-negotiable. **This is the FIRST production proof to fire the URN+IUR secondary-integration REDUCTION-direction pattern + the FIRST production proof to exercise the freshly-landed CL-027 §2.1.2 reduction-aware sub-block.**

**Plus TWO soft-drift observations (both v6.2-canonical wins per Appendix B; routing decision unaffected; cite verbatim in "Conflicts between sources")**:

a. **Routing CSV health_band drift**: routing CSV `health_band = Healthy` (`health_score = 79.8`); v6.2 `health_band = Thriving` (`health_score = 82.4`). v6.2 wins per `_root/07 §1` source-of-truth hierarchy + Appendix B canonicality. Both bands are above the §4.13 override threshold (Watch / At Risk / Critical / VD<40); full Section 3b lede in scope either way; routing decision unaffected.

b. **Routing CSV migration_confidence drift**: routing CSV `migration_confidence = careful`; v6.2 `migration_confidence = value_led`. v6.2 wins per Appendix B. Confidence is drafter-facing orientation only (not in client copy per `_root/04 §3`); routing decision unaffected.

The 6-step trace, CSV-canonical reconciliation, reconciliation-tracker pre-flight, and data observations below are the planning-agent's pre-flight evidence; the fresh drafter re-derives independently in Step 3 of the prompt below and paste-verifies in the conformance block. If the fresh drafter's re-derivation disagrees with the pre-flight at any step, the fresh drafter STOPs and surfaces per `_root/CONTRACTS.md §2` — do not silently proceed.

### `csv.DictReader` attestation (per `PLANNING_AGENT_HANDOFF.md` Appendix B.5.1)

All v6.2 values below were parsed via Python `csv.DictReader` against `_master-account-data-v6.2.csv`: `sca` is at **csv.DictReader data row 83** (canonical locator); absolute file line ~261 (cosmetic — v6.2 carries reconciliation-tracker carry rows above the active data block that shift absolute line numbers); v1 paste-ready cited "line 85" cosmetically — both v1's "line 85" and absolute "line 261" are non-canonical; csv.DictReader row index is the canonical locator. All routing CSV values were parsed via `csv.DictReader` against `migration_comm_tiers_2026-05-19.csv` (`sca` at data row 34). **No visual CSV inspection was used.** Fresh drafter re-runs the same `csv.DictReader` pattern at Step 4 data load.

### Routing 6-step trace for `sca` (planning-agent pre-flight 2026-05-26)

| Step | Check | v6.2 column → value | Result |
|---|---|---|---|
| 1 | Status filter | `ghost_account = FALSE`; `migration_status = migration_pending` | PASS |
| 2 | Decrease check | `delta_mrr = +$224` (> 0) | not decrease → Format B in scope |
| 3 | Entity overlay | `parent_entity = Shadow Catchers` (= `company`); `billing_entity` blank; `paying_entity` blank; `brands = 1` | not entity child → standalone in scope |
| 4 | Annual overlay | `deal_type = Monthly` | not Annual → flat effective date; `_root/04 §4.16` does not fire; `renewal_date` deferred decision NOT triggered |
| 5 | Health override | `health_band = Thriving` (82.4 composite); `VD = 100`; `OH = 72.4`; `engagement = 71.7`; `adoption = 75` | no override → full Section 3b lede in scope (v6.2-canonical Thriving; routing CSV's Healthy 79.8 loses per Appendix B; either band is above §4.13 override threshold) |
| 6 | Delta-tier dispatch | `delta_mrr = +$224` (in `$80 < $224 ≤ $400` Format B dollar band) AND `delta_pct = +30.9%` (just above the 10%–30% Format B pct band; the pct value is at the upper boundary +0.9 pts; per `_root/06 §3` higher-touch-wins precedence ONLY applies to dollar-band boundaries [$75/12%; $700/8%] per the §3 worked-examples — the standalone "delta_pct > 30%" condition triggers `_root/04 §4.4` high-delta lede rule WITHIN Format B, NOT a CEO Letter format flip since `delta_mrr = $224 << $400` CEO Letter dollar floor; routing CSV `comm_action = "Format B — Notice + Meeting Offer"` confirms the operator-stamped routing decision; fresh drafter verifies §3 precedence reading at Step 3) | **Format B — Notice + Meeting Offer** (standard variant; NOT CEO Pre-Call → Format B; `_root/04 §4.4` annual-dollar lede rule FIRES inside Format B due to `delta_pct > 30%` — Section 3b lede names annual dollar impact alongside monthly change) |

### Routing CSV cross-check (`migration_comm_tiers_2026-05-19.csv` row 34 for `sca`)

- `comm_action = "Format B — Notice + Meeting Offer"` ✓ (matches re-derived format)
- `flags = "EARLY-ADOPTER-2015 | EXPANSION-T1_TO_T2"` (annotation-layer flags per `_root/06 §5.5`; non-blocking on routing; cite verbatim in routing block — both flags cross-reference v6.2-canonical firings: EARLY-ADOPTER-2015 mirrors `cohort_year = 2015` triggering `_root/04 §4.7` early-adopter paragraph at Section 3f; EXPANSION-T1_TO_T2 mirrors `new_tier_base = $749 > current_platform_mrr = $725` triggering `_root/04 §4.6` platform-base-grown follow-on at Section 3i)
- `hold_condition` blank ✓
- `post_hold_action` blank ✓
- `nuances` blank ✓
- `tier` `T1` ✓ (matches v6.2)
- `deal_type` `Monthly` ✓ (matches v6.2)
- `migration_driver` `user_rate_normalization` ✓ (matches v6.2; NO driver disagreement — distinct from `bri` 2026-05-26 pre-flight which had v6.2 IUR vs routing CSV discount_correction drift)
- `migration_confidence` `careful` — v6.2 says `value_led`; v6.2 wins per Appendix B (drafter-facing only; routing unaffected; cite as soft drift)
- `health_band` `Healthy` (`health_score = 79.8`) — v6.2 says `Thriving` (`health_score = 82.4`); v6.2 wins per Appendix B (2.6-point composite drift; both bands above §4.13 override; routing unaffected; cite as soft drift)

### Reconciliation-tracker pre-flight (per `_root/07 §4.5` + Appendix B.4 reconciliation discipline)

- **`sca` is NOT in the 37-row flagged set** in `_meta/v6_2_reconciliation_log.md` (sca is in the unflagged accounts pool from the 107-row pending cohort sweep 2026-05-26). Verified via `grep "^| \`sca\`" _meta/v6_2_reconciliation_log.md` returning no match.
- Inline threshold attestation (csv.DictReader-canonical):
  - `current_provided_users = 25`; `current_user_mrr = $0`; `current_user_rate = $20`
  - **`current_user_mrr = $0`** — sca is currently billed for ZERO user excess (the legacy pricing absorbs the full 25 provided users into the $725 platform_mrr line; no separate user-excess line on today's invoice). This is unusual but operationally consistent: with `current_provided_users = 25` AND `trailing_avg_users = 18` (under provided), there is no excess to bill on legacy plan.
  - `implied_billed_excess = ROUND($0 ÷ $20) = 0` → `implied_billed_enabled = 25 + 0 = 25` (matches `enabled_users = 25` v6.2 column)
  - `modeled_users = 18` (v6.2 stamped; matches `trailing_avg_users = 18`)
  - `gap_users = 25 − 18 = +7` (|gap| = 7; threshold is `> 3` → **TRIPPED** on user count)
  - `gap_dollars = $0 − MAX(18 − 25, 0) × $20 = $0 − $0 = $0` (|gap_$| = $0; threshold is `> $60` → **NOT TRIPPED** on dollar gap; because modeled excess (18−25=−7, floor at 0) ⇒ $0 modeled user charge × legacy rate; and billed is also $0)
  - **Material-gap flag: FALSE** (both thresholds must trip per `_root/07 §4.5`; only user-count gap fires but dollar gap is $0; no `⚠️ USER BILLING RECONCILIATION NEEDED` row fires in routing block — distinct from `bri` pre-flight which had BOTH legs tripping per Pattern 2 under-modeled)
- After-row math discipline per CL-025 still applies (format-agnostic): `[NEW_EXCESS]` = v6.2 `excess_users` = `8` (`modeled_users = 18` minus `included_users = 10`); `[NEW_USER_CHARGE]` = v6.2 `user_charge` = `$200` (graduated ladder sanity check: 8 excess @ $25 first-band rate = $200 ✓); `[NEW_MRR]` = v6.2 `new_total_mrr` = `$949` (recomposes: `tier_base = $749 + user_charge = $200 = $949` ✓). Drafter does NOT recompute from `enabled_users = 25` or any billing-side derivation.
- `enabled_users` column on v6.2 (position 15 post-`active_users` per Stage 4.1 closeout): `enabled_users = 25` (matches `implied_billed_enabled = 25`; drafter does not paste this value anywhere in client copy; surfaced here for the threshold attestation only).

### CSV-canonical key fields for `sca` (cite verbatim in conformance block per Appendix B operator stamp 2026-05-26)

| v6.2 column | value |
|---|---|
| `ord_id` | `sca` |
| `company` | `Shadow Catchers` |
| `parent_entity` | `Shadow Catchers` (= `company`; not an entity-child) |
| `billing_entity` | blank |
| `paying_entity` | blank |
| `cohort_year` | `2015` ← **`_root/04 §4.7` early-adopter tenure paragraph FIRES** (cohort_year ≤ 2015 per §4.7 threshold; Section 3f populates with [YEAR]=2015) |
| `deal_type` | `Monthly` |
| `current_mrr` | `$725` |
| `current_platform_mrr` | `$725` |
| `current_user_mrr` | `$0` ← **unusual but operationally consistent**: legacy plan billed ZERO user excess (25 provided absorbs the 18 trailing-avg actual; no excess to bill on legacy structure) |
| `current_user_rate` | `$20`/user (legacy rate; below `$25` ladder first band per `_root/05 §2.1.1` URN field signature — URN-primary canonical case) |
| `current_provided_users` | `25` |
| `trailing_avg_users` | `18` |
| `active_users` | `17` |
| `enabled_users` | `25` (routing-block use only; NEVER in client copy per `_root/04 §3` audience-discipline + CL-025) |
| `current_stack` | `iPad` (narrow stack — iPad-only deployment; useful for the Section 3b lede's relationship-stat sentence framing per `_root/04 §4.2`) |
| `current_sites` | `1` |
| `assigned_tier` | `T1` |
| `tier_base` | `$749` |
| `included_users` | `10` (T1 — substitute as `[NEW_INCLUDED] = 10` into `_root/03 §1` T1 tier block at Section 3j) |
| `modeled_users` | `18` |
| `excess_users` | `8` |
| `user_charge` | `$200` |
| `brands` | `1` |
| `new_total_mrr` | `$949` |
| `assumptions` | `"Current user rate $20/user → new graduated ($25/$22/$20/$18)."` (drafter-facing; informs URN driver block prose orientation) |
| `delta_mrr` | `+$224` |
| `delta_pct` | `+30.9%` ← **`_root/04 §4.4` high-delta annual-dollar lede rule FIRES** (delta_pct > 30%; Section 3b lede names `$224 × 12 = $2,688/year` alongside monthly change; QB-078 + QB-106 fire) |
| `risk_label` | `6-Significant (>30%)` |
| `migration_driver` | `user_rate_normalization` (URN-primary; Section 3g pastes `_root/05 §2.1.2` Format B URN canonical block; field signature OK per post-2026-05-26 audit: user_rate $20 < $25 ladder first band; `_root/05 §2.1.1` PASS) |
| `secondary_drivers` | `included_user_reduction` ← **`_root/05 §2.1.7` URN+IUR secondary integration REDUCTION-direction sub-block FIRES (post-CL-027 RESOLVED at `_root/05 §2.1.2` source 2026-05-26)**; Section 3h integrates within primary block per `_root/05 §1.3` (NEVER as a separate section); IUR-secondary reduction-direction semantic (`current_provided_users = 25` > `included_users = 10`; legacy allotment 25 → new included 10 — clean reduction case; sca is one of 25 v6.2 accounts in the URN+IUR-secondary REDUCTION-direction sub-cohort); first production proof to exercise the post-CL-027 §2.1.2 reduction-aware sub-block ("Your included base is also adjusting from the legacy [LEGACY_INCLUDED] to the current [TIER] standard of [NEW_INCLUDED]" — direction-neutral "adjusting" prose mirroring the pre-existing §2.1.3 line 123 CEO Letter pattern); IUR-as-secondary semantic scope per `_root/05 §2.4.1` covers both reduction-direction (sca + 24 others) AND expansion-direction (bcf) URN-primary cases per CL-026 + CL-023 + CL-027 joint-resolution-sequence 2026-05-26; `§4.5` operations-unchanged sentence FORK to IUR-fork variant per `§2.13` non-negotiable + `_root/04 §4.5` (fork is shape-agnostic — applies regardless of reduction or expansion direction); `§4.9` billing-basis footnote REQUIRED per `§2.13` non-negotiable + `_root/04 §4.9` (URN + IUR both fire the footnote; one paste of §4.9 suffices for both drivers since the footnote text covers excess-user billing universally per `_root/04 §4.9` source text) |
| `migration_status` | `migration_pending` |
| `migration_confidence` | `value_led` ← **routing CSV says `careful`; v6.2 wins per Appendix B; drafter-facing only; routing unaffected** |
| `health_score` | `82.4` ← **routing CSV says `79.8`; v6.2 wins per Appendix B; 2.6-point composite drift; both bands above §4.13 override; routing unaffected** |
| `health_band` | `Thriving` ← **routing CSV says `Healthy`; v6.2 wins per Appendix B; routing unaffected** |
| `engagement_score` | `71.7` |
| `adoption_score` | `75` |
| `value_delivery_score` | `100` |
| `operational_health_score` | `72.4` |
| `composite_narrative` | `"Shadow Catchers is in Thriving territory (82), but the score sits just above the Healthy cutoff — engagement (72) is the relative weakness while value delivery (100) is doing the lifting. A focused check-in on engagement would solidify the Thriving position before any drift sets in."` (drafter-facing; routing-block + lede-stat-orientation only; not literal lede copy; the engagement-weakness observation stays INTERNAL — never in client copy per `_root/04 §3` audience-discipline; useful drafter context for Section 3b lede stat selection: pick a value-delivery anchor over an engagement anchor per `_root/04 §4.2`) |
| `ghost_account` | `FALSE` |
| `support_fire` | `FALSE` |
| `bundle_config_mismatch` | `FALSE` |
| `migration_segment` | `Narrative` |
| `notice_cohort` | `June` |
| `notice_deadline` | `1-Jul` |
| `messaging_headline` | `"User pricing standardized at $25/user with volume-based graduated rates. At 82/100 health with strong value delivery, the platform is delivering exceptional value."` (drafter-facing; routing-block + lede-stat-orientation only; not literal lede copy) |
| `artifact_type` | `Simplified value summary` |
| `delivery_owner` | `Kylor` |

### Routing CSV row fields for `sca` (paste-cite in conformance block alongside v6.2 fields; data row 34)

| routing CSV column | value | notes |
|---|---|---|
| `comm_action` | `Format B — Notice + Meeting Offer` | matches re-derived format ✓ |
| `flags` | `EARLY-ADOPTER-2015 \| EXPANSION-T1_TO_T2` | cite verbatim in routing block; both flags cross-reference v6.2-canonical firings (EARLY-ADOPTER-2015 mirrors `cohort_year = 2015` triggering `_root/04 §4.7` at Section 3f; EXPANSION-T1_TO_T2 mirrors `tier_base = $749 > current_platform_mrr = $725` triggering `_root/04 §4.6` at Section 3i — small $24 gap but still > 0); non-blocking on routing |
| `hold_condition` | blank | not held |
| `post_hold_action` | blank | not held |
| `nuances` | blank | no per-account routing annotation |
| `tier` | `T1` | matches v6.2 ✓ |
| `deal_type` | `Monthly` | matches v6.2 ✓ |
| `migration_driver` | `user_rate_normalization` | **matches v6.2 ✓** — distinct from `bri` pre-flight which had driver disagreement; no "Conflicts between sources" entry for driver routing for `sca` |
| `migration_confidence` | `careful` | v6.2 says `value_led`; v6.2 wins per Appendix B; cite as soft drift in "Conflicts between sources" |
| `health_band` | `Healthy` | v6.2 says `Thriving`; v6.2 wins per Appendix B; cite as soft drift in "Conflicts between sources" |
| `health_score` | `79.8` | v6.2 says `82.4`; v6.2 wins per Appendix B; 2.6-point drift; band drift cited above |

### Data observations (non-blocking; surface in conformance block "conflicts" / "observations" section if relevant)

1. **`migration_driver = user_rate_normalization` (URN-primary) + `secondary_drivers = included_user_reduction` (IUR-secondary; REDUCTION-direction case)** — Section 3g pastes `_root/05 §2.1.2` (Format B URN canonical block; post-CL-027 RESOLVED 2026-05-26 carries TWO direction-specific `[IF excess users remain ...]` sub-blocks; sca dispatches to the NEW reduction-direction sub-block). Apply `_root/05 §2.1.6` conditional context paragraphs: `§4.9` billing-basis footnote REQUIRED for URN per `_root/05 §2.13` non-negotiable + `_root/04 §4.9`; `§4.6` platform-base-grown follow-on FIRES (observation 9 — small $24 gap but `new_tier_base > current_platform_mrr`); `§4.10` URN platform-base conditional sentence FIRES (observation 10 — Before platform base $725 ≠ After platform base $749); `§4.7` early-adopter FIRES (observation 4 — `cohort_year = 2015`). **Plus `_root/05 §2.1.7` URN+IUR secondary integration REDUCTION-direction sub-block FIRES** (observation 1 — secondary_drivers includes IUR + `current_provided_users = 25 > included_users = 10` is reduction-direction shape; routes to the post-CL-027 §2.1.2 reduction-aware sub-block "Your included base is also adjusting from the legacy [LEGACY_INCLUDED] to the current [TIER] standard of [NEW_INCLUDED]"; direction-neutral "adjusting" prose — NOT "expanding"). **Plus `_root/04 §4.5` IUR-fork variant FIRES** for operations-unchanged sentence per `_root/05 §2.13` non-negotiable (secondary includes IUR triggers fork same as primary IUR; fork is shape-agnostic — applies for both reduction and expansion direction).

2. **`secondary_drivers = included_user_reduction` (post-CL-027 RESOLVED first production exercise; v2 paste-ready corrects v1's pre-flight error)** — Section 3h secondary-driver weaving fires per `_root/05 §4` matrix row 5 `user_rate_normalization, included_user_reduction` (the post-CL-027 26-occurrence row — 25 REDUCTION + 1 EXPANSION = `bcf`; sca is in the 25-reduction sub-cohort). Per CL-016 RESOLVED 2026-05-22 + post-CL-026 / CL-023 / CL-027 joint-resolution-sequence 2026-05-26: §2.1.7 templated routing dispatches URN+IUR-secondary by direction-shape; REDUCTION-direction (sca) routes to the post-CL-027 §2.1.2 `[IF excess users remain AND secondary driver = included_user_reduction (base shrinking)]` sub-block with "Your included base is also adjusting from the legacy [LEGACY_INCLUDED] to the current [TIER] standard of [NEW_INCLUDED]" direction-neutral "adjusting" prose; EXPANSION-direction (bcf only) routes to the pre-existing §2.1.2 `[IF excess users remain AND new included base > legacy included base (base expanding)]` sub-block with "expanding from [LEGACY_INCLUDED] to [NEW_INCLUDED] — absorbing [N] users" expansion-baked prose. Section 3h is integrated WITHIN Section 3g per `_root/05 §1.3`, NOT a separate section. QB-092 PASSES (integration is within primary block); QB-093 N/A (MOR+IUR not applicable — sca is URN+IUR); QB-094 N/A (MOR+URN not applicable). The IUR-as-secondary semantic scope per `_root/05 §2.4.1` (CL-026 + CL-023 + CL-027 joint-resolution-sequence) covers both expansion AND reduction direction-cases across TWO cohorts: TBI-primary + IUR-secondary (9 accounts; expansion shape; integrated at §2.3.2 / §2.3.3 expansion-baked prose) + URN-primary + IUR-secondary (26 accounts; 25 reduction + 1 expansion; integrated at the two-sub-block §2.1.2 / §2.1.3 dispatch). For sca, the reduction-direction §2.1.2 sub-block governs verbatim — NO planning-agent paraphrase, NO direction-mixing.

**v1 → v2 self-correction note (transparency)**: v1 paste-ready observation 2 (2026-05-26 first issue) claimed "§2.4 prose orientation in §2.1.7 sub-block describes legacy-allotment-reducing-to-new-tier-standard." That was WRONG. v1's planning agent conflated the IUR-primary §2.4.x source (which IS reduction-oriented at primary scope per §2.4.1 definition) with the URN+IUR-secondary §2.1.7 routing (which pre-CL-027 routed to §2.1.2's EXPANSION-only sub-block; reduction-direction was uncovered). The v1 drafter caught the error via CL-024 paste-verification against `_root/05 §2.1.2` direct source-read + invoked `_root/CONTRACTS.md §2` hard-stop. CL-027 RESOLVED at source 2026-05-26 closes the §2.1.2 reduction-direction gap. v2 corrects this observation. The v2 drafter does NOT inherit v1's pre-flight error — the v2 routing trace + observation 1 + 2 above all reflect the post-CL-027 correct routing dispatch.

3. **`delta_pct = +30.9%` (just above 30% threshold; Format B band by dollar; high-delta lede rule FIRES)** — `_root/04 §4.4` high-delta annual-dollar lede rule FIRES (only fires when `delta_pct > 30%`; sca is 30.9% — just inside the firing condition). Section 3b lede names annual dollar impact (`$224 × 12 = $2,688/year`) alongside monthly change inside the same sentence per §4.4 Format B variant. QB-078 (high-delta annual-dollar sentence check) PASSES; QB-106 (annual-figure reconciliation within ±$1 of `delta_mrr × 12`) PASSES at `$2,688` exact. The dispatch stays Format B (NOT CEO Letter / NOT CEO Pre-Call) because `delta_mrr = $224 << $400` CEO Letter dollar floor per `_root/06 §3` — `_root/04 §4.4` firing is a LEDE-VOICE rule (extra annual-dollar sentence inside the §4.1 tenure-aware lede), NOT a format-flip routing rule. (Distinct from `cci` pre-flight which was 13.9% and did not fire §4.4.)

4. **`cohort_year = 2015` (11 years tenure; AT the §4.7 early-adopter threshold)** — `_root/04 §4.7` early-adopter tenure paragraph FIRES (only fires when `cohort_year ≤ 2015`; sca is exactly 2015 — inside the firing condition). Section 3f of the brief populates with the §4.7 Format B variant verbatim; substitute `[YEAR] = 2015` per `cohort_year`. The §4.7 Format B variant names the year, names years of tenure (11 years from 2015 to 2026), and frames the platform-then-vs-platform-now distinction with the "fundamentally different product" framing per the §4.7 source-text Format B subsection. QB checks specific to §4.7: drafter verifies §4.7 Format B variant (vs Format A variant) is pasted at Section 3f; no paraphrase. (Distinct from `cci` 2021 and `bri` 2023 — both did NOT fire §4.7; `sca` is the first Format B production proof to exercise §4.7.) **Note**: Section 3e tenure-aware variant per `_root/04 §4.1` ALSO fires — for `cohort_year = 2015`, the §4.1 variant is the longest-tenure-band ("over a decade" / "10+ years" register; verify exact §4.1 variant selector at Step 5 — the §4.1 source text owns the tenure-band granularity). Sections 3e + 3f BOTH render for sca: Section 3e is one short tenure-aware sentence per §4.1; Section 3f is the early-adopter paragraph per §4.7. These coexist per template Section 3 structure (the template separates them as distinct sections — Section 3e is sentence-grain; Section 3f is paragraph-grain).

5. **`migration_driver = platform_discount_correction` (PDC)** — does NOT fire as PRIMARY (v6.2 says URN). Section 3e tenure-aware variant stays in standard `_root/04 §4.1` form (no `_root/04 §4.14` substitution). QB-088 N/A. (No driver disagreement on routing CSV for `sca` — distinct from `bri` 2026-05-26 pre-flight which had routing CSV `discount_correction` vs v6.2 IUR drift.)

6. **`health_band = Thriving` (82.4 composite; VD=100; engagement=71.7; adoption=75; OH=72.4; v6.2-canonical wins over routing CSV `Healthy` 79.8 per Appendix B)** — Section 3b lede + relationship-first form in full scope; no `_root/04 §4.13` health override (both v6.2's `Thriving` AND routing CSV's `Healthy` are above the Watch/At-Risk/Critical/VD<40 override threshold); QB-087 N/A. **The composite_narrative's "engagement (72) is the relative weakness" observation STAYS INTERNAL** per `_root/04 §3` audience-discipline + composite_narrative field annotation — never in client copy. Useful drafter-facing context for Section 3b lede stat selection: prefer a value-delivery anchor over an engagement anchor per `_root/04 §4.2` (the lede stat sentence should highlight what sca is doing well, not flag the weakness).

7. **`assigned_tier = T1`** — Section 3j pastes `_root/03 §1` T1 — Commerce Essentials block; substitute `[NEW_INCLUDED] = 10` from v6.2 `included_users = 10` (T1 carries the `[NEW_INCLUDED]` placeholder per `_root/03 §1` T1 source; distinct from T3 which hard-codes "Up to 40 users"). The T1 tier block introduces sca to the formal T1 product description for the first time (sca's 2015 cohort year predates the T1/T2/T3 tier architecture per `_root/01 §3`; this is part of the 2026 normalization).

8. **`comm_action = "Format B — Notice + Meeting Offer"` (standard; NOT CEO Pre-Call → Format B)** — routing block carries `CEO awareness required before send: NO`. QB-025 N/A (no CEO Pre-Call confirmation required). Section 3p close is the standard Format B active meeting offer per `_root/04 §4.12`; no per-account CEO-call calibration sentence needed. Email Section 3 Paragraph 1 Sentence 1a uses the DEFAULT relationship-hook form (NOT the CEO-Pre-Call-acknowledgement form).

9. **`tier_base = $749` vs `current_platform_mrr = $725`** — `new_tier_base > current_platform_mrr` ($749 > $725; gap = $24 — small but positive); `_root/04 §4.6` platform-base-grown follow-on paragraph FIRES at Section 3i after the pricing table; substitute `[YEAR] = 2015` per `cohort_year`. (The small $24 gap means the platform-base-grown framing language must be calibrated — §4.6's source text handles the framing universally; drafter pastes verbatim. The gap exists, so §4.6 fires; the magnitude doesn't affect rule firing.) QB-080 verifies §4.6 paste verbatim with correct year. Routing CSV `flags = "EXPANSION-T1_TO_T2"` is the operator's cross-reference of this firing — paste-cite as confirmation that §4.6 firing matches routing CSV intent.

10. **`_root/04 §4.10` URN platform-base conditional sentence FIRES** — applies when "Before platform base ≠ After platform base" per Format B form per `_root/04 §4.10`. Before platform base = `current_platform_mrr = $725`; After platform base = `tier_base = $749`. These differ by $24 → §4.10 conditional sentence FIRES (the rule fires on inequality, not magnitude). Paste verbatim per Step 5 Section 3g URN conditional context paragraphs (per `_root/05 §2.1.6`). QB-084 verifies §4.10 paste verbatim. (Same firing pattern as `cci` — but cci was a much larger gap of $1,710 → $2,295 = $585. sca's gap is much smaller but the rule firing is binary, not magnitude-dependent.)

11. **`_root/04 §4.9` billing-basis footnote required after URN pricing table** — URN-primary fires §4.9 per `_root/04 §4.9` line 268 ("inside the `user_rate_normalization` block AND inside the `included_user_reduction` block"). Paste verbatim italicized sentence immediately after the URN pricing table at Section 3i. QB-083 verifies. **Note**: `secondary_drivers` includes IUR — IUR also fires §4.9 per the same source line. Per the §4.9 source text, ONE paste of the footnote suffices (the footnote text covers excess-user billing universally per `_root/04 §4.9` source); the drafter does NOT paste §4.9 twice (once for URN, once for IUR). The IUR-secondary integration in `_root/05 §2.1.7` does NOT introduce a separate footnote; the URN block's §4.9 footnote covers the URN+IUR-secondary case end-to-end.

12. **Value-anchor Section 3k `cost_per_order` inclusion check** — inclusion gates per `_root/04 §4.8`: `ltm_orders > 0` AND `cost_per_order < $200`. `cost_per_order = new_total_mrr × 12 / ltm_orders = $949 × 12 / ltm_orders = $11,388 / ltm_orders`. Threshold satisfied iff `ltm_orders > 56.94` (since $11,388 / 57 = $199.8). Fresh agent computes from Postgres §4.3 at Step 4; if `ltm_orders > 57`, value-anchor Section 3k IS in scope; if `ltm_orders ≤ 56`, OMIT Section 3k. `delta_per_order` second sentence inclusion check: `delta_per_order = $224 × 12 / ltm_orders = $2,688 / ltm_orders`; threshold `delta_per_order < $50` iff `ltm_orders > 53.76`; if `ltm_orders > 54`, append second sentence; else omit. Cannot pre-derive without Postgres fetch; surface result in conformance block. QB-082 verifies §4.8 threshold compliance. (sca's threshold for inclusion is much lower than cci's `ltm_orders > 150` — because sca's $949 new_total_mrr is smaller than cci's $2,495; the threshold scales with subscription size.)

13. **`migration_segment = Narrative`** — Format B's primary segment per `_root/06 §1`. No cross-format drift signal. The `artifact_type = Simplified value summary` is drafter-facing orientation only (not a literal artifact name; the literal artifact is the Format B brief per Section 3 of the prompt below).

14. **`current_stack = iPad`** — narrow stack (iPad-only; no Catalog / Portal / Cart / CPQ / CC modules — narrower than cci's iPad+Catalog+Portal+CPQ+CC and narrower than bri's iPad+Catalog+Cart+Portal). The Section 3b lede's relationship-stat sentence per `_root/04 §4.2` drafter judgment should reflect this narrow deployment — the lede stat should highlight what the iPad rep app is delivering for sca (orders / GMV / customer reach), not "surfaces in use" (which would point at the narrowness). Postgres §4.2/§4.3 stats will inform the specific anchor.

15. **`current_user_mrr = $0` (unusual but operationally consistent)** — sca's legacy plan absorbs all 25 provided users into the $725 platform_mrr line; no separate user-excess billing on today's invoice. Operationally consistent because `trailing_avg_users = 18 < current_provided_users = 25` (no excess to bill on legacy structure). The Before-row pricing-table math reflects this: `[LEGACY_USER_CHARGE] = $0` per CL-025 + `_root/05 §2.1.5`; `[LEGACY_EXCESS] = ROUND($0 / $20) = 0`. The Before-row pricing table will show user-charge = $0 (the customer's actual today-invoice user charge); the After-row pricing table shows `user_charge = $200` (the new graduated-ladder charge for 8 modeled excess @ $25 first-band rate). The customer's invoice goes from no user-excess line to a $200 user-excess line — the URN driver block prose at `_root/05 §2.1.2` orients the customer to this shift in billing structure; the IUR-secondary integration at `_root/05 §2.1.7` orients them to the included-user allotment moving from 25 (legacy) → 10 (new T1).

16. **CSV-canonical reconciliation flag check** — `sca` is NOT in `_meta/v6_2_reconciliation_log.md` (verified via reconciliation-tracker pre-flight section above; user-count gap of +7 trips the |gap| > 3 threshold but dollar gap of $0 does NOT trip the |gap_$| > $60 threshold; per `_root/07 §4.5` both must trip for material-gap flag — sca is NOT flagged). After-row math discipline per CL-025 still applies (format-agnostic): drafter pastes v6.2 `new_total_mrr=$949` / `excess_users=8` / `user_charge=$200` as After-row values; does NOT recompute from billing math or `enabled_users=25`.

### Output file path pre-derivation (per `_root/07 §6`)

- Brief output: `format-b-notices/sca__shadow-catchers__brief.md` (slug derivation per `_root/07 §6`: `Shadow Catchers` → lowercase → no special chars → spaces → hyphens → `shadow-catchers`; fresh agent re-derives per `_root/07 §6` canonical at Step 8)
- Delivery email output: `format-b-notices/sca__shadow-catchers__delivery-email.md` (same slug as brief)

(The fresh agent re-derives the slug at Step 8 per `_root/07 §6` — paths above are planning-agent informational pre-derivation only. If `_root/07 §6` slug rules disagree with the pre-derivation, fresh agent's canonical resolution wins.)

---

---

# Stage 4.2 — Format B Notice + Meeting Offer — Per-Account Drafter (paste-ready for `ord_id = sca`)

> **Session parameter pre-substituted**: `[ORD_ID]` = `sca` (Shadow Catchers); planning agent pre-flight verified in annotation block above (Format B standard variant confirmed; routing CSV `comm_action = "Format B — Notice + Meeting Offer"`; flags = `EARLY-ADOPTER-2015 | EXPANSION-T1_TO_T2` cross-referencing §4.7 + §4.6 firings; no holds; reconciliation flag NOT tripped despite +7 user-count gap because dollar gap is $0; data observations enumerated including THREE conditional firings: §4.4 high-delta annual-dollar lede; §4.7 early-adopter tenure paragraph; §2.1.7 URN+IUR secondary integration sub-block; plus TWO soft-drift observations: routing CSV health_band/score and migration_confidence both v6.2 wins per Appendix B). Fresh-agent expectation: re-derive in Step 3; paste-verify the trace in conformance block; if disagreement at any step, STOP and surface per `_root/CONTRACTS.md §2`.
> **Workspace root**: `/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/Pricing Migration/`
> **Pattern inheritance**: structural form inherits from `_meta/stage4_prompts/stage_4_1__format-a__per-account-drafter.md` (657 lines; the gold-standard per Stage 4 PLANNING_AGENT_HANDOFF.md §5) — same 8-step canonical skeleton per Appendix A.11; same Appendix A.1–A.12 design constraints in Step 1; same After-row math discipline (CL-025) in Step 4; per-format adjustments confined to Step 3 routing dispatch (Format B delta-tier band + CEO Pre-Call → Format B variant), Step 5 brief assembly (`format-b-notices/_brief-template.md` 354 lines; `_root/05 §N.2` driver blocks vs Format A's `§N.4`), and Step 6 delivery email (`format-b-notices/_delivery-email-template.md` 157 lines; 3-paragraph body + active meeting-offer close).

---

## You are a per-account pricing migration notice drafter for SuperCat's 2026 book normalization

You will produce **one Format B Notice + Meeting Offer brief + one delivery email** for **one** SuperCat wholesale customer account — `sca` (Shadow Catchers; the operator-stamped ord_id for this session). **One account in, two files out, conformance block, STOP.**

You are **explicitly NOT**: a SaaS renewal writer; a subscription-uplift author; a CRM sequence or campaign author; a contract negotiator or procurement responder; a template builder (that was Stage 3 — the templates are operator-approved and in the workspace; your job is to populate the template, not author a new one).

The recipient is a **CFO / owner / principal of a furniture / lighting / decor wholesaler** — not a procurement officer, IT buyer, or platform admin. Per `_root/04 §1.1` (operator-stamped 2026-05-26): *"Write for a principal who runs a wholesale business, not a software buyer renewing a SaaS seat."*

You do not improvise. When a rule is ambiguous or a data field is missing, you STOP and surface to the operator per `_root/CONTRACTS.md §2`.

---

## Step 1 — Design constraints (Stage 4 drafter-prompt Appendix A, verbatim from `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` Appendix A; operator-stamped 2026-05-26)

These 12 constraints govern this drafter session. They are operator-stamped 2026-05-26 at Stage 4 prep; revising any of them requires the rule-change protocol per `_root/CONTRACTS.md §3`. If you find yourself paraphrasing any constraint, STOP and re-read.

### A.1. Name the job correctly

Stage 4 drafters are **per-account pricing migration notice drafters** for SuperCat's 2026 book normalization — one brief + one delivery email wrapper for **one** wholesaler principal per session.

**Explicitly NOT**: SaaS renewal / auto-renew / subscription uplift writers; CRM sequence or campaign authors; contract negotiators or procurement responders; template builders (that was Stage 3).

Archived `_fresh-agent-prompt.md` files used "pricing migration communications specialist" and batched 3 accounts — **keep the domain, drop the batching**, anchor to `_root/` + rebuilt Stage 3 templates.

### A.2. Lock audience and relationship register (`_root/04 §1` + `§1.1`)

The audience-register table (operator-stamped 2026-05-26 at source — `_root/04 §1.1`):

| Dimension | This program | SaaS-renewal drift to forbid |
|---|---|---|
| Reader | CFO / owner / principal of a furniture / lighting / decor wholesaler | Procurement, IT buyer, "platform admin" |
| Relationship | Vendor-to-principal or CEO-to-CEO (CEO Letter) | Service-rep-to-buyer, CSM check-in |
| Register | Declarative, empathetic on impact, firm on architecture | Cheerful renewal, "excited to partner," soft upsell |
| What they're evaluating | A specific invoice change with a mechanical explanation | Subscription tier change or contract term sheet |

One line for this session: *"Write for a principal who runs a wholesale business, not a software buyer renewing a SaaS seat."*

### A.3. Lock artifact type — two files, one account, one format

Stage 4.2 output is always:

- `format-b-notices/[ord_id]__[company-slug]__brief.md` — substantive notice (attached PDF in send workflow)
- `format-b-notices/[ord_id]__[company-slug]__delivery-email.md` — short wrapper carrying the **active meeting offer** (the Format-B-distinguishing close)

Per `_root/07 §6` and `_root/01 §5`:

- One account per agent session (this session: the `sca` in Step 3)
- Artifacts plus active meeting offer for Narrative (Format B's primary segment); Format B's close is an **active invitation**, distinct from Format A's passive offer and the CEO Letter's specific-date call commitment per `_root/04 §4.12`
- Brief = the case; email = the envelope plus the meeting offer

Forbid in this session: "3-email nurture sequence," "renewal reminder cadence," "customer success outreach."

### A.4. Routing = hard gate before any prose (`_root/06 §2`)

You re-derive format from the **6-step flow**, not memory or `comm_action` alone:

`status filter → decrease → entity → annual → health → delta tier`

Critical stops to encode (you STOP and escalate per `_root/CONTRACTS.md §2` if any fire):

- `parent_entity` child → no standalone Format B brief; entity packet (Stage 4.5)
- HOLD → read `post_hold_action`; no draft unless it resolves to sendable Format B
- Watch / At Risk / Critical → most routes defer to CSM/CEO; Format B is rare in these health bands per `_root/06 §4.2`
- Wrong format folder → escalate per `_root/CONTRACTS.md §2`; never "closest format"
- **CEO Pre-Call → Format B variant** (`comm_action = "CEO Pre-Call → Format B"`, typically `delta_mrr ≥ $600`): the CEO must have **already called the account** before this brief is sent. Drafter confirms in routing block; if call has not happened, STOP and surface — do NOT send Format B in advance of the pre-call.

Routing pre-flight has ALREADY been run by the planning agent BEFORE this prompt was pasted (per `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` Appendix B.5.1 `csv.DictReader` discipline + Appendix B.5.2 canonicality check). The planning agent verified the account routes to Format B per the 6-step flow against the v6.2 row + routing CSV joint state. **Your Step 3 below is to re-confirm the routing trace and paste-verify it in the conformance block.** If your re-derivation disagrees with the planning agent's pre-flight, STOP and surface — do not silently proceed.

### A.5. Path-reference contract — enforce harder than Stage 3

Stage 3 templates have `[INSERT _root/XX §N.M …]` pointers. **Stage 4 production artifacts carry the actual rule prose, fetched verbatim from the owning `_root/` doc, with bracketed tokens substituted from v6.2 + Postgres.** This is the path-reference inversion at production scope (Stage 4 handoff §4 architectural concept #8).

Required per template section:

1. Open the named `_root/` section
2. Paste character-for-character (drivers `_root/05 §N.2` for Format B, closes `_root/04 §4.12` Format B variant, tiers `_root/03 §1`, etc.)
3. Substitute only `[BRACKETED_TOKENS]` from v6.2 + Postgres per `_root/07 §2` + `§4`
4. **Zero paraphrase of owned rule prose** — including short sentences (strict-placeholder precedent operator-stamped 2026-05-26 Stage 3.1 review pass)

**Allowed drafter-generated prose (narrow, for Format B)**:

- **Relationship lede** (Section 3b of the brief) per `_root/04 §4.1` + `§4.2` — 2–3 sentences naming tenure + at least one account-specific platform stat, landing dollar / date in same paragraph. Tenure-band variants live in §4.1; substitute by `cohort_year` from v6.2. **When `delta_pct > 30%`: lede MUST name annual dollar impact alongside monthly change per `_root/04 §4.4` Format B variant** — fires for `sca` (delta_pct = 30.9%).
- **Delivery email Sentence 1a** (one of three forms): DEFAULT relationship hook OR CEO Pre-Call acknowledgement OR OMITTED for health-override per `_root/04 §4.13`. Drafter-generated within Format B register per `_root/04 §4.12`.
- **Delivery email Sentence 1b**: dollar-change effective-date sentence per `_root/04 §4.13` form **with attachment pointer appended** (the pointer phrase is the drafter-generated portion; the §4.13 form itself is pasted verbatim).
- **CEO Pre-Call → Format B variant calibration** at Section 3p close: optional one-sentence per-account acknowledgement of the prior CEO call within Format B's active register per `_root/04 §4.12`. NOT applicable for `sca` (standard Format B).

Everything else = fetch-and-paste verbatim from `_root/`.

### A.6. Migration mechanics vocabulary, not SaaS vocabulary

Driver explanation comes from `_root/05` block for the account's v6.2 `migration_driver` value — NOT "your subscription is increasing."

Explanation = why the number changed under the new architecture (URN / TBI / IUR / MOR / PDC / ABTS / ADR / SA — see `_root/05 §1.1` for the canonical 11 values; Format B carries all 8 increase-side drivers).

**Forbidden framings** — cite `_root/04 §3` (the 32-row forbidden-phrase table, expanded 2026-05-26 with 6 SaaS-renewal rows via Stage 4 prep Source-fix Session A); the table is the canonical anti-SaaS-vocabulary list. **Do NOT re-list ad hoc.** Grep `_root/04 §3` at draft time for any phrase you are tempted to use.

**Formal-notice line**: paste-only verbatim from `_root/04 §4.12` ("pricing modification under your SuperCat licensing agreement") — not custom contract language. Required immediately after the Format B close per `_root/04 §4.12`'s "immediately after each close, except Good News" instruction.

### A.7. Data pipeline — kill pre-refactor habits

Stage 4 uses `_root/07` only:

| Source | Role |
|---|---|
| v6.2 CSV (`_master-account-data-v6.2.csv`) | Authoritative numbers, driver, health, routing |
| Postgres MCP (`user-supercat-postgres-vpn`) | Live lede stats only |
| Routing CSV (mirror in `_root/06 §2 + §7`) | `comm_action`, `post_hold_action`, HOLD resolution, `nuances` column |
| HTML model | Cross-check only; v6.2 wins on conflict |

Hard rules:

- **Never read `_archive/` per-account exemplars** (Format B archived exemplars are flagged drift sources)
- **Never read `Migration-Health Artifacts/` templates**
- **Never invent stats**; Postgres fail → `composite_narrative` fallback per `_root/07 §5`
- **Lede stat guardrail**: output metrics only; never provisioned-vs-active ratios per `_root/04 §4.2`

### A.8. Format-specific register (Format B only for this session)

| Format | Close register | Format B production must enforce |
|---|---|---|
| Format B | **Active meeting offer** per `_root/04 §4.12` Format B variant | Open-ended invitation ("happy to find time" / "let's grab 20 minutes"); NEVER a specific calendar date (CEO Letter register); NEVER assistant-coordinated booking (CEO Letter register); CSM coordinates directly with contact; no expansion-eligible / discovery-call framing per `_root/04 §2.6` |

Format B close in Format A style (passive "conversation welcome") = hard fail in review. Format B close in CEO Letter style (specific calendar date / assistant booking) = hard fail. Format B email body exceeding 3 paragraphs = drift signal — back out and consult `_root/04 §4.12` Format B register.

### A.9. Internal vs client-facing

Per `_root/04 §2.5` and `§2.14`:

- **Routing block** stays in draft for operator review; **removed before send** (per `_root/04 §2.14` non-negotiable + QB-047)
- **Health bands, dimension scores, `support_fire`, CEO-awareness flags, billing-entity routing, peer-range dollars** → routing block only (NEVER in client copy)
- **"Log in CRM" / cohort tags** → NEVER in client copy
- **Peer dollar ranges** (the T1/T2/T3 floor/midpoint/ceiling values in `_root/03 §5`) → INTERNAL-ONLY per CL-003 + operator stamp 2026-05-22 universal
- **CEO call pre-confirmation** (CEO Pre-Call → Format B variant): routing block carries `⚠️ CEO PRE-CALL CONFIRMED — [CEO_NAME] called [CONTACT_NAME] on [PRE_CALL_DATE]` per `_root/07 §7.5` conditional; client copy carries one-sentence acknowledgement (sentence 1a) only — NEVER re-summarizes the CEO call's content

### A.10. Conformance block = drift audit

End this session with the canonical conformance block per `_root/00_manifest.md §5` PLUS the per-account additions enumerated below in Step 8. Required additions for Stage 4 per-account drafter sessions:

- Manifest echo (files read with last-updated dates)
- QB-NNN results for every applicable check in `_root/08` — by ID, not "looks good"
- Explicit: 0 inlined rule prose paraphrases, 0 archive reads
- Math reconciliation: Before / After / Delta totals vs the v6.2 row (QB-104 + QB-105; **QB-106 FIRES for `sca` because `delta_pct = 30.9% > 30%`** — annual figure = `$224 × 12 = $2,688` reconciles within ±$1)
- Format-B-specific blockers by ID (see Step 7 checklist) — including QB-025 CEO awareness handling if CEO Pre-Call variant (NOT applicable for `sca` — standard Format B)
- Routing 6-step trace: each step's evaluation result + terminal format selected (this session: Format B)
- Postgres-stat fetch: query used + result OR fallback used (per `_root/07 §5`)
- **CL-024 strict + paste-verification carry-forward**: every owned rule prose paste-quoted verbatim in the conformance block (proves you fetched-and-pasted, not paraphrased — same paste-verification discipline that surfaced the Thesis source-fix at Stage 3.5 review pass)

### A.11. Prompt structure — 8 steps (this prompt)

This prompt mirrors the Stage 4.1 8-step skeleton (`_meta/stage4_prompts/stage_4_1__format-a__per-account-drafter.md`), adapted for Format B production scope:

1. Role + design constraints (this Step 1)
2. Required reading (Step 2)
3. Routing verification (Step 3)
4. Data load (Step 4)
5. Brief assembly (Step 5)
6. Delivery email assembly (Step 6)
7. Anti-drift discipline + QB-NNN self-audit (Step 7)
8. Output + conformance block (Step 8)

One prompt per format (this is Stage 4.2 — Format B). NOT one mega-prompt across formats.

### A.12. "Do not write like this" contrast pairs

**Wrong (SaaS renewal)**:

> "As your renewal approaches, we're updating your subscription to reflect current list pricing…"

**Right (migration notice)**:

Relationship-first lede → dollar + effective date → driver block from `_root/05 §N.2` (verbatim paste; Format B blocks) → operations-unchanged sentence (verbatim paste from `_root/04 §4.5`) → roadmap (verbatim paste from `_root/03 §3`) → Format B active meeting offer (verbatim paste from `_root/04 §4.12` Format B variant) → formal-notice line (verbatim paste from `_root/04 §4.12`).

**Wrong (Format A close mistakenly carried into Format B)**:

> "If you have questions about this change, we welcome the conversation."

**Right (Format B active meeting offer)**:

Verbatim paste of the `_root/04 §4.12` Format B close — open-ended invitation register; CSM coordinates directly with contact; never a specific calendar date.

**Wrong (template builder)**:

> `[INSERT _root/05 §2.1.2 — user_rate_normalization Format B canonical block]`

**Right (production drafter — what you do this session)**:

Verbatim paste of the actual `_root/05 §2.1.2` block content, with `[CURRENT_RATE]` / `[NEW_RATE]` / `[LADDER_BAND]` / `[ANNUAL_DELTA]` tokens substituted from v6.2 + Postgres. The `[INSERT ...]` pointer lives in the Stage 3 template (`format-b-notices/_brief-template.md`); your job is to resolve the pointer into actual rule prose in the production artifact.

---

## Step 2 — Required reading (read in this exact order; echo every file's last-updated date in your first response per `_root/00_manifest.md §6` manifest-echo contract)

**Do not skip files. Do not skim.** The cost of one extra read is five seconds; the cost of a missed precedent is unrecoverable drift in a production artifact that goes to a CFO.

### Folder orientation (the contract layer)

1. `Pricing Migration/AGENTS.md`
2. `Pricing Migration/00_README.md`
3. `Pricing Migration/_root/00_manifest.md` — **the index.** §2 is the manifest table (echo every row's title + last-updated date in your first response per §6). §5 is the canonical conformance-block format. §6 is the manifest-echo contract.
4. `Pricing Migration/_root/CONTRACTS.md` — operator contract, agent contract, rule-change protocol (§3), anti-archive rule (§4), path-reference contract (§5).

### The rule layer (all 10 numbered docs — every section this session pastes from)

5. `_root/01_why_we_are_migrating.md` — strategic register; relationship-before-price principle.
6. `_root/02_who_is_being_migrated.md` — 8 segments (Narrative is Format B's primary segment per `_root/06 §1`); $200/$400/$600 ownership boundaries; entity overlay (§3); health overrides (§4); annual overlay (§5); cohort assignment (§6); errata (§7); 109/107/2 reconciliation (§8).
7. `_root/03_what_we_sell.md` — T1/T2/T3 verbatim tier blocks (§1) — you paste **T1** into Section 3j of the brief; user-rate ladder (§2 Block A) — paste graduated-rate summary string into pricing-at-a-glance row; "What's Coming in 2026" roadmap (§3) — verbatim into Section 3l of the brief (CL-005 mandatory; this is the most additive change in the Format B rebuild — archived Format B template OMITTED this); INTERNAL peer ranges (§5) — NEVER in client copy.
8. `_root/04_communication_posture.md` — **the highest-rule-density doc.** §1 voice posture; §1.1 audience register (operator-stamped 2026-05-26 via Stage 4 prep Source-fix Session A); §2 14 non-negotiables; §3 32-row forbidden-phrase table (the canonical anti-SaaS-vocabulary list — expanded 2026-05-26 with 6 SaaS-renewal rows; grep this at draft time); §4.1 tenure-aware lede variants (you select the variant for `cohort_year = 2015` — the longest-tenure band); §4.2 lede stat guardrail; §4.3 above-the-midpoint user-count clause; **§4.4 high-delta annual-dollar-impact lede (above 30% — FIRES for `sca` at 30.9%)**; §4.5 operations-unchanged sentence + IUR fork variant (**IUR-fork FIRES for `sca` because `secondary_drivers` includes IUR**); §4.6 platform-base-grown sentence (Format B applies as follow-on paragraph after pricing table per template Section 3i — **FIRES for `sca` because `tier_base = $749 > current_platform_mrr = $725`**, small $24 gap); **§4.7 early-adopter tenure paragraph (when `cohort_year ≤ 2015` — FIRES for `sca` at exactly 2015)**; §4.8 value-anchor section ($200 threshold); §4.9 billing-basis footnote (URN AND IUR for Format B — **FIRES for `sca`; one paste of §4.9 covers both URN-primary AND IUR-secondary**); §4.10 platform-base conditional URN sentence (Format B form — **FIRES for `sca` because Before platform base $725 ≠ After platform base $749**); §4.11 "How This Compares" position vocabulary; **§4.12 Format B close (active meeting offer) + formal-notice line**; §4.13 health-band lede override + standalone dollar-change sentence; §4.14 platform_discount_correction substitution (NOT applicable — sca is URN-primary, not PDC); §4.16 Annual-cohort voice rules (NOT applicable — sca is Monthly); §5 driver-voice orientation.
9. `_root/05_driver_taxonomy.md` — 11 `migration_driver` values; Section 2 = increase-side; **Format B carries all 8 increase-side drivers**: paste **`§2.1.2` URN canonical block** into Section 3g of the brief (sca's `migration_driver = user_rate_normalization`); §N.6 conditional context paragraphs (apply `§2.1.6` URN conditional set — fires §4.9 + §4.6 + §4.10 + §4.7 + §4.5 IUR-fork); §N.7 secondary-driver-integration sub-blocks (**`§2.1.7` URN+IUR secondary integration sub-block FIRES for `sca` because `secondary_drivers = included_user_reduction`**); §4 secondary-driver weaving matrix — you integrate URN+IUR within the URN primary block per §1.3, never as a separate section; §N.5 pricing-table row template per driver (paste `§2.1.5` URN row template). **CL-016 (operator-stamped 2026-05-22)**: MOR + IUR templated coverage at §2.6.6 + §4 weaving matrix row applies for 6 v6.2 accounts (NOT applicable to sca); MOR + URN per-account narrative pattern per §2.6.7 applies for 2 v6.2 accounts (NOT applicable to sca); URN + IUR templated coverage at §2.1.7 + §2.4.7 (**applies to sca**). **CL-026 + CL-023 jointly RESOLVED 2026-05-26**: post-resolution `_root/05 §2.4.1` semantic scope of IUR-as-secondary covers BOTH reduction-side cases (sca's case: `current_provided_users = 25 > included_users = 10`, legacy allotment moving down to new-tier standard) AND expansion-side cases (the 9-account cluster bri/bcf/ihw/sccon/ali/vic/ih/fc/ta/sbmh — not applicable to sca but cited here for awareness of the broadened semantic scope).
10. `_root/06_format_routing.md` — §1 Format B definition (CS-led; active meeting offer; meaningful delta) + CEO Pre-Call → Format B routing pattern (5th routing pattern per §1); §2 6-step routing-decision flow (you re-confirm this in Step 3); §3 delta-tier dispatch + Δ_pct vs Δ_mrr precedence + **higher-touch-wins precedence at boundaries** — **read carefully for `sca` because `delta_pct = 30.9%` is just above the standard Format B 10-30% pct band; the dollar band $80<$224≤$400 is squarely Format B; per §3 the dispatch should stay Format B because `delta_mrr` dominates the dollar-band assignment AND `delta_mrr = $224 << $400` CEO Letter dollar floor; §3 precedence verification is canonical (fresh drafter re-derives)**; §4 overrides (§4.1 entity; §4.2 health; §4.3 annual); §5 `comm_action` vocabulary (`Format B — Notice + Meeting Offer` standard); §5.5 `post_hold_action` / `nuances` companion columns.
11. `_root/07_data_pipeline.md` — §2 53-column v6.2 field guide; §3 canonical loader (with `ghost_account = TRUE` + `migration_status = 'already_migrated'` filter — Format B drafters never see filtered rows but verify); §4 3 verbatim Postgres MCP queries (you run these); §4.4 derived metrics (`cost_per_order` / `annual_subscription` / `delta_per_order`; **plus `annual_delta = delta_mrr × 12` for `sca` because `delta_pct > 30%`**); §4.5 user-billing reconciliation (**NOT TRIPPED for `sca` despite +7 user-count gap because dollar gap is $0 — both must trip per §4.5 threshold**); §5 9-row fallback table for Postgres unavailability; §6 file-naming convention (output naming `[ord_id]__[company-slug]__brief.md` etc.; slug for sca = `shadow-catchers`); §7 per-format routing-block field-list matrix (**Format B row — canonical for Section 2 of the brief; does NOT carry `Expansion eligible` field; DOES carry `CEO awareness required before send` conditional — NO for `sca`**); **§7.5 delivery-email routing-block subset matrix per format (operator-stamped 2026-05-26 via Stage 4 prep Source-fix Session B — Format B column = canonical for Section 2 of the delivery email).**
12. `_root/08_quality_bar.md` — 138 QB-NNN checks (125 blockers + 5 warnings + 8 audit-only); §10 entity-packet checks (QB-127–138 — NOT applicable to this session). You run every QB-NNN whose `Applies to:` field covers Format B or "all formats" in Step 7. **Format-B-specific checks to highlight for `sca`**: **QB-078 (high-delta annual-dollar sentence when `delta_pct > 30%` — FIRES)**; **QB-084 (URN platform-base conditional per `§4.10` — FIRES)**; QB-083 (billing-basis footnote per §4.9 — FIRES for URN AND IUR; one paste covers both); QB-080 (§4.6 platform-base-grown follow-on — FIRES with [YEAR]=2015); **QB-106 (annual figure reconciliation when `delta_pct > 30%` — FIRES; annual = $224 × 12 = $2,688)**; QB-092 (secondary-driver weaving WITHIN primary block — FIRES for URN+IUR); QB-093 (MOR + IUR integration per CL-016 — N/A); QB-094 (MOR + URN per-account narrative per §2.6.7 — N/A); QB-025 (CEO awareness handling for CEO Pre-Call variant — N/A).
13. `_root/09_changelog.md` — **read every entry**, particularly Stage 3.2 review pass (Format B templates APPROVED; CL-012 + CL-016 source fixes applied at `_root/05`; subject-line normalized; CL-023 filed for v6.2 TBI+URN secondary re-evaluation); Stage 3.5 prep (dual-canonical v6.2 architecture; `_root/04 §4.15` Parent-letter voice register — NOT applicable to standalone Format B); **Stage 4 prep Source-fix Sessions A + B 2026-05-26** (CL-015 RESOLVED at `_root/04 §4.16`; CL-022 RESOLVED at `_root/07 §7.5`; `_root/04 §1.1` Audience register; 6 SaaS-renewal rows added to `_root/04 §3`); Stage 4.1 lpf production proof closeout (CL-025 RESOLVED — v6.2 reconciliation discipline at planning-agent layer; `_meta/v6_2_reconciliation_log.md` created; `enabled_users` column added to v6.2; this discipline is format-agnostic and applies to Format B identically); **Stage 4.2 cci production proof closeout 2026-05-26** (first Format B proof; URN-only single-driver; no secondary; established the Format B production reference); **Stage 4.2 bri hard-stop + CL-026 + CL-023 joint-resolution 2026-05-26** (drafter subagent hard-stopped at Step 5 per `_root/CONTRACTS.md §2` due to v6.2 IUR-on-expansion field-signature mismatch; full-cohort audit run 89.7% clean baseline; CL-026 + CL-023 jointly RESOLVED via `_root/05` source-fix at 8 sections + v6.2 10-row re-stamps + Decision 1 stamp-both + Decision 2 Option A semantic clarification; post-resolution audit 91.6% clean; bri re-paste-run deferred; `sca` selected as the next clean Format B candidate). **The post-resolution `_root/05` is what your Step 5 reads — particularly `§2.4.1` IUR primary-vs-secondary semantic scope which `sca` exercises via secondary IUR, AND `§2.1.7` URN+IUR templated coverage which `sca` exercises.**

### The dual-canonical v6.2 data files

14. `_master-account-data-v6.2.csv` — the row you read for this session is the one whose `ord_id` matches the `sca` parameter in Step 3 (CSV line 85 per planning-agent pre-flight; fresh drafter re-verifies via `csv.DictReader`). **Read the header row first to map column positions**; then read the specific account's row.

### The Format B templates (the source of every production artifact this session writes)

15. `format-b-notices/_brief-template.md` (354 lines) — the brief template you populate (Stage 3.2 APPROVED 2026-05-26 with `_root/05` source fixes; delivery-email routing block reference updated 2026-05-26 to `_root/07 §7.5` matrix as canonical per Stage 4 prep Source-fix Session B). Every `[INSERT _root/XX §N.M ...]` pointer in this template you resolve by fetch-and-paste in your brief output.
16. `format-b-notices/_delivery-email-template.md` (157 lines) — the delivery email template you populate (Stage 3.2 APPROVED 2026-05-26; Section 2 routing block updated 2026-05-26 to reference `_root/07 §7.5` matrix as canonical per Stage 4 prep Source-fix Session B strip-and-replace landing).

### The Stage 4.1 + Stage 4.2 production proofs (the pattern references)

17. `format-a-notices/lpf__linon-powell-furniture__brief.md` (137 lines) — Stage 4.1 lpf APPROVED 2026-05-26 brief. **Reference for structural form + path-reference contract enforcement at production scope — NOT for Format-A-specific prose patterns**. Read for: how the §2 routing block is populated; how `_root/` rule prose is pasted verbatim (no paraphrase); how the After-row math reconciles to v6.2-canonical values per CL-025; how the conformance discipline materializes in the artifact. Format A's close register (passive) and 6-driver scope differ from Format B; do NOT inherit Format-A-specific prose into the Format B brief. The structural-discipline lessons inherit; the format-specific prose does not.
18. `format-a-notices/lpf__linon-powell-furniture__delivery-email.md` (44 lines) — Stage 4.1 lpf delivery email APPROVED 2026-05-26. Same structural-discipline-only reference as item 17. Format B's email has 3 paragraphs (vs Format A's 4-sentence wrapper) and an active meeting-offer close (vs Format A's passive offer); structural form inherits, format-specific prose does not.
19. `format-b-notices/cci__currey-and-company__brief.md` (133 lines) — **Stage 4.2 cci APPROVED 2026-05-26 brief (FIRST Format B production proof)**. Read for: how Format B's specific Section 3 sequencing materializes (Section 3b lede → 3c standalone dollar → 3d consolidated framing → 3e tenure-aware → 3f early-adopter [OMITTED for cci because 2021>2015; ENABLED for sca because 2015≤2015] → 3g URN block from §2.1.2 → 3h secondary weaving [OMITTED for cci because no secondary; ENABLED for sca because secondary IUR] → 3i pricing table + §4.9 footnote + §4.6 follow-on → 3j tier block [T3 for cci; T1 for sca] → 3k value-anchor → 3l roadmap → 3m How-This-Compares → 3n at-a-glance summary → 3o operations-unchanged [DEFAULT for cci because no IUR; IUR-FORK for sca because secondary IUR] → 3p Format B close → formal-notice line); how the Section 3b lede integrates relationship + dollar + date in 2-3 sentences; how §4.6 + §4.10 are pasted verbatim with [YEAR] substituted from cohort_year. The cci proof is your closest production reference — same URN primary, similar Section 3 structure. **Key differences from cci to anticipate for sca**: §4.4 high-delta sentence FIRES (cci 13.9% did not fire); §4.7 early-adopter paragraph FIRES (cci 2021 did not fire); §2.1.7 URN+IUR secondary integration FIRES (cci had blank secondary); §4.5 IUR-fork variant FIRES in operations-unchanged sentence (cci was DEFAULT); T1 tier block (cci was T3).
20. `format-b-notices/cci__currey-and-company__delivery-email.md` (47 lines) — **Stage 4.2 cci APPROVED 2026-05-26 delivery email (FIRST Format B production proof)**. Read for: how the 3-paragraph body structures (Paragraph 1 opener with Sentence 1a relationship hook + Sentence 1b dollar-change-with-attachment-pointer; Paragraph 2 operations-unchanged [DEFAULT for cci; IUR-FORK for sca]; Paragraph 3 active meeting offer + formal-notice line); how the §4.12 verbatim close paste integrates `[EFFECTIVE_DATE]` substitution; how Sentence 1a relationship hook is calibrated within Format B register (8-15 words; names relationship without specific stats). Same structural reference as item 19 for the brief — sca's email follows the same scaffold with the §4.5 fork to IUR-variant for Paragraph 2.

### The cleanup tracker (the in-flight CL-NNN list — read for status of relevant items)

21. `_meta/stage3_cleanup.md` — items relevant to Format B for `sca`: CL-001 (no "no account-specific adjustments" sentence anywhere); CL-002 (value-anchor threshold `cost_per_order < $200` per `_root/04 §4.8` operator stamp 2026-05-22 — NOT archived $35); CL-003 (no peer dollar ranges in client copy — universal); CL-004 (no "equivalent platforms" / unnamed-competitor pricing sentence anywhere); CL-005 (mandatory "What's Coming in 2026" block via `_root/03 §3` — ADDED to Format B; the archived Format B template omits this); CL-011 (`platform_discount_correction` is canonical driver name — NOT applicable; sca is URN-primary); CL-012 (TBI secondary marker at `_root/05 §2.3.2` — NOT applicable; sca is URN-primary, not TBI); CL-015 (RESOLVED 2026-05-26 — `_root/04 §4.16` Annual-cohort voice rules — NOT applicable; sca is Monthly); CL-016 (RESOLVED 2026-05-22 + reconfirmed 2026-05-26 — MOR + IUR templated coverage at `_root/05 §2.6.6` + `§4` — NOT applicable; sca is URN+IUR, not MOR+IUR; BUT URN+IUR templated coverage at `_root/05 §2.1.7` + `§2.4.7` applies — sca exercises §2.1.7 directly); CL-017 (Critical-band per-account judgment — NOT applicable; sca is Thriving); CL-022 (RESOLVED 2026-05-26 — `_root/07 §7.5` landed); **CL-023 (RESOLVED 2026-05-26 — joint with CL-026; `_root/05 §2.4.1` IUR-as-secondary semantic scope now covers reduction-side AND expansion-side; sca's IUR-secondary is reduction-side — clean case, post-resolution); CL-024 (RESOLVED 2026-05-26 — strict + paste-verification protocol — applies to sca); CL-025 (RESOLVED 2026-05-26 — v6.2 reconciliation discipline; format-agnostic — applies to Format B identically per Appendix B.4; sca's threshold check is NOT tripped because dollar gap is $0); CL-026 (RESOLVED 2026-05-26 — joint with CL-023; v6.2 10-row re-stamps applied + `_root/05` source-fix landed; sca is NOT in the re-stamped set; sca is the first Format B production proof to exercise the post-resolution URN+IUR semantic).**
22. `_meta/v6_2_reconciliation_log.md` — read for status of `sca`. The planning agent has already pre-flighted that `sca` is NOT in the 37-row flagged set (per Appendix B.5.2 canonicality check at candidate stamp). Re-confirm in conformance block. If `sca` IS flagged at draft time (operator override of standard filter), the After-row math discipline per CL-025 still applies — v6.2 modeled wins; client copy NEVER mentions "unused users" / "phantom accounts."

### Do NOT read

- `_archive/**` per-account exemplars — anti-archive rule per `_root/CONTRACTS.md §4` applies absolutely; Format B archived exemplars are explicitly flagged drift sources. Never open them.
- `Migration-Health Artifacts/` templates — strategic reference materials abstracted into `_root/`. Reading them is scope creep.
- `_reference/2026-05-20__execution_plan_v3.3.md` or `_reference/migration_revenue_model_2026-05-14.html` — strategic source material; abstracted into `_root/01`–`_root/07`. Reading is scope creep.
- `_meta/stage2_prompts/**` — pre-refactor template-build prompts.
- `_meta/stage3_prompts/**` — Stage 3 template-build prompts (not relevant to Stage 4 production drafting).
- `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` — planning-agent-specific handoff doc; the Appendix A constraints relevant to this session are embedded verbatim in Step 1 above.
- Per-account brief / email outputs in `format-*-notices/` from prior sessions OTHER than the Stage 4.1 lpf precedent at items 17–18 + Stage 4.2 cci precedent at items 19–20 (each session is otherwise independent).
- `_meta/stage4_prompts/_paste-ready/stage_4_2__bri.md` (the bri attempt hard-stopped 2026-05-26; superseded by post-CL-026 resolution; not a reference for sca).
- `~/Downloads/**` or anything outside `Pricing Migration/` per `AGENTS.md` hard rules.

---

## Step 3 — Routing verification (re-derive the 6-step flow against the v6.2 row before drafting any prose)

**Operator-supplied parameter for this session**: `sca` — substitute the operator-stamped `ord_id` here at paste time.

You re-derive the format using the 6-step flow per `_root/06 §2`. The planning agent ran the same flow pre-flight; your job is to re-confirm and paste-verify the trace in the conformance block. If your re-derivation disagrees with Format B at any step, STOP and surface per `_root/CONTRACTS.md §2`.

### The 6 steps (per `_root/06 §2`)

1. **Status filter** — `ghost_account = FALSE` AND `migration_status ≠ 'already_migrated'`. Read these two columns from the v6.2 row for `sca`. If either condition fails: this account is loader-filtered per `_root/07 §3`; no brief drafted; STOP.
2. **Decrease check** — `delta_mrr < 0`. If TRUE: routes to Good News (not Format B); STOP and surface.
3. **Entity overlay** — `parent_entity` is non-blank AND `parent_entity ≠ company`. If TRUE: this is an entity-child; folds into entity packet per `_root/02 §3` + `_root/06 §4.1`; no standalone Format B brief; STOP and surface.
4. **Annual overlay** — `deal_type = 'Annual'`. If TRUE: the Format B draft still proceeds per `_root/06 §4.3` (Annual overlay does not change format selection), but **the lede effective-date framing shifts to renewal-date framing per `_root/04 §4.16.2`** (operator-stamped 2026-05-26 via Stage 4 prep Source-fix Session A). NOT applicable for `sca` (`deal_type = Monthly`).
5. **Health override** — `health_band ∈ {Watch, At Risk, Critical}` OR `value_delivery_score < 40`. If TRUE: Format B is rare in these health bands per `_root/02 §4` + `_root/06 §4.2`. Read `notice_cohort` — if `Post-Migration`, the brief is deferred; STOP and surface. Critical-band routing is per-account per `post_hold_action` per CL-017 — consult routing CSV directly. If the account legitimately routes to Format B under a Watch/At-Risk override, the `§4.13` health-band lede override fires (Section 3b is suppressed; the brief opens with the standalone dollar-change sentence in Section 3c). NOT applicable for `sca` (`health_band = Thriving`; `value_delivery_score = 100`).
6. **Delta-tier dispatch** — per `_root/06 §3` table with operator-stamped Δ_pct vs Δ_mrr precedence:
   - Format A near-flat range: `|delta_mrr| ≤ $80/mo` OR `|delta_pct| ≤ 10%` with `delta_mrr < $400`
   - **Format B standard: `$80 < delta_mrr ≤ $400` OR `10% < delta_pct ≤ 30%`**
   - CEO Letter: `$400 < delta_mrr < $600`
   - **CEO Pre-Call → Format B: `delta_mrr ≥ $600`** (still Format B in artifact form; CEO has pre-called the account before this brief sends)
   - Higher-touch-wins precedence: at boundaries ($75/12%; $700/8%) the higher-touch format wins per the `_root/06 §3` precedence rule (a $75/12% account routes to Format B, not Format A; a $700/8% account routes to CEO Pre-Call → Format B, not standard Format B)
   - For Format B: confirm the dispatch lands on Format B (standard OR CEO Pre-Call variant); if not, STOP and surface.
   - **For `sca` specifically**: `delta_mrr = $224` (squarely in Format B's `$80 < $224 ≤ $400` dollar band); `delta_pct = +30.9%` (just above the 10-30% Format B pct band by 0.9 pts). The dollar band assignment dominates (`delta_mrr = $224 << $400` CEO Letter dollar floor; no format flip). The §3 precedence rule (higher-touch-wins) applies at the $75/12% and $700/8% boundary cases per the §3 worked examples — NOT at the standalone `delta_pct > 30%` case when `delta_mrr` is mid-Format-B-band. Read `_root/06 §3` carefully and verify the standalone `delta_pct > 30%` reading. The `delta_pct > 30%` condition triggers `_root/04 §4.4` (high-delta annual-dollar LEDE-VOICE rule WITHIN Format B), NOT a format-flip routing rule. Routing CSV `comm_action = "Format B — Notice + Meeting Offer"` confirms the operator-stamped routing decision.

### CSV-canonical reconciliation (per Stage 3.5 review-pass lesson — `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` Appendix B; operator-stamped 2026-05-26)

For EVERY routing-relevant field above, **paste-cite the CSV column + row + value** in your conformance block. Not from rule-layer enumeration (which may have drifted); from `_master-account-data-v6.2.csv` directly. The CSV is canonical; the rule layer reconciles to the CSV. If a rule-layer enumeration claim disagrees with the CSV value for this row, the CSV wins — surface the discrepancy.

Specifically for Format B: paste-cite `ord_id` + `company` + `ghost_account` + `migration_status` + `delta_mrr` + `delta_pct` + `parent_entity` + `deal_type` + `health_band` + `value_delivery_score` + `notice_cohort` + `migration_driver` + `secondary_drivers` from the v6.2 row, PLUS routing-CSV `comm_action` + `flags` + `hold_condition` + `post_hold_action` + `nuances` (Format B's CEO-Pre-Call-variant flagging surfaces here). **For `sca` specifically**: cite the soft-drift observations on `health_band`/`health_score` and `migration_confidence` (routing CSV says Healthy 79.8 + careful; v6.2 says Thriving 82.4 + value_led; v6.2 wins per Appendix B).

### Format B pre-conditions (additional checks before drafting)

Per the Format B brief template's "What this template is NOT for" section:

- `migration_driver ∈ {module_compression, user_count_variance, rate_architecture}` → decrease-side; Good News only per `_root/05 §3` / `§3.2` / `§3.3`. If routing produces Format B with one of these primary drivers, the routing is suspect — STOP and escalate per `_root/CONTRACTS.md §2`. NOT applicable for `sca` (`migration_driver = user_rate_normalization`).
- `migration_driver = already_migrated` → status-marker leak per `_root/05 §1.4`; loader filters per `_root/07 §3`. No brief drafted. NOT applicable for `sca`.
- **CEO Pre-Call → Format B variant** (`comm_action = "CEO Pre-Call → Format B"`): the CEO has already called the account BEFORE this brief sends per `_root/06 §1` 5th routing pattern. NOT applicable for `sca` (`comm_action = "Format B — Notice + Meeting Offer"` standard).

If `secondary_drivers` is non-empty, consult `_root/05 §4` (secondary-driver weaving matrix); if no entry covers the combination, STOP and surface per CL-023. **For `sca`**: `secondary_drivers = included_user_reduction`; combination `user_rate_normalization, included_user_reduction` IS in `_root/05 §4` matrix (templated at `§2.1.7`). Section 3h secondary-driver weaving integrates URN+IUR within Section 3g primary block per `_root/05 §1.3` (NEVER as a separate section).

---

## Step 4 — Data load (v6.2 row + Postgres MCP queries + routing CSV)

### v6.2 row read (canonical for numbers + driver + health + routing)

Read the row from `_master-account-data-v6.2.csv` whose `ord_id` column equals `sca`. Per `_root/07 §2` 53-column field guide, paste-cite the full v6.2 row in the conformance block's CSV-canonical reconciliation section.

Key fields you substitute into the brief + email (per `_root/07 §2`):

- `company` → `[ACCOUNT_NAME]` everywhere → `Shadow Catchers`
- `current_mrr` → `[CURRENT_MRR]` (lede + summary table + delivery email routing block) → `$725`
- `new_total_mrr` → `[NEW_MRR]` (lede + summary table + delivery email routing block) → `$949`
- `delta_mrr` → `[DELTA]` (with `+$` prefix for increase; computed as `new_total_mrr − current_mrr = $949 − $725 = $224`; QB-105 reconciliation)
- `delta_pct` → `[DELTA_PCT]` (with `+` prefix; never leads the lede per `_root/04 §2.1`) → `+30.9%`; **`delta_pct = 30.9% > 30%`: lede MUST name annual dollar impact (`$224 × 12 = $2,688/year`) alongside monthly change per `_root/04 §4.4` Format B variant — QB-078 + QB-106**
- `cohort_year` → `[COHORT_YEAR]` (routing block + tenure-aware lede variants per `_root/04 §4.1`) → `2015`; **`cohort_year = 2015 ≤ 2015`: §4.7 early-adopter tenure paragraph FIRES at Section 3f of the brief**
- `deal_type` → routing block "Contract" field → `Monthly` (not Annual; §4.16 does not fire)
- `assigned_tier` → `[NEW_TIER_LABEL]` → `T1`; selects `_root/03 §1` T1 block to paste into Section 3j
- `included_users` → `[NEW_INCLUDED]` → `10` (substituted into the T1 tier block; T1 carries the placeholder per `_root/03 §1`)
- `migration_driver` → `[DRIVER]` → `user_rate_normalization`; selects `_root/05 §2.1.2` Format B URN canonical block to paste into Section 3g
- `secondary_drivers` → `included_user_reduction`; integrated within URN primary block via `_root/05 §2.1.7` URN+IUR templated coverage (Section 3h; FIRES); §4.5 fork to IUR-variant fires in operations-unchanged sentence
- `health_band` + `value_delivery_score` → routing block only (NEVER in client copy per `_root/04 §2.5`) → `Thriving` + `100`
- `support_fire` → routing block `⚠️ SUPPORT FIRE` conditional row only → `FALSE` (NOT fires)
- `billing_entity` → routing block conditional row when non-blank AND ≠ `company` → blank (NOT fires)
- `comm_action` → routing block `Comm_action:` row → `Format B — Notice + Meeting Offer` (substitute verbatim from routing CSV)

**Format B does NOT carry `Expansion eligible`** in its routing block per `_root/07 §7` matrix and per `_root/04 §2.6` (Format B's meeting offer is a migration meeting, NOT a discovery call). **Format B DOES carry `CEO awareness required before send`** as conditional (NO for standard / YES for CEO Pre-Call variant). For `sca`: `CEO awareness required before send: NO`.

If a field you need is blank or null in v6.2, consult `_root/07 §5` fallback table; if no fallback applies, STOP and surface.

### Postgres MCP queries (lede stats only — per `_root/07 §4`)

Run the 3 verbatim Postgres queries from `_root/07 §4.1` / `§4.2` / `§4.3` against MCP `user-supercat-postgres-vpn`:

1. **Org resolution** (`_root/07 §4.1`) — resolve `ord_id = sca` → `org_id` in `organizations` table.
2. **Active org users + 90-day login activity** (`_root/07 §4.2`) — populate `active_org_users` + `logged_in_90d` + `total_logins_90d` for the routing block + the lede's relationship-stat sentence.
3. **LTM eCat orders + GMV + customers served** (`_root/07 §4.3`) — populate `ltm_orders` + `ltm_gmv` + `ltm_customers_served` for the routing block + the lede's data-point references + the value-anchor `cost_per_order` derivation.

**Fallback if any query fails**: per `_root/07 §5` 9-row fallback table — render the prescribed fallback in the routing block (e.g. `Postgres live data: UNAVAILABLE — fell back to composite_narrative` for §4.1 failure; `ltm_orders = 0 — value anchor omitted` for §4.3 empty). Do not delete the routing-block line; render the fallback per `§5`.

### Routing CSV (mirror in `_root/06 §2 + §7`; `nuances` column per `_root/06 §5.5`)

Read the row from `migration_comm_tiers_2026-05-19.csv` whose `ord_id` matches `sca` (data row 34 per planning-agent pre-flight; fresh drafter re-verifies). Confirm:

- `comm_action = "Format B — Notice + Meeting Offer"` matches the format you re-derived per `_root/06 §5` vocabulary
- `post_hold_action` is blank
- `nuances` blank (no per-account routing annotation)
- `flags = "EARLY-ADOPTER-2015 | EXPANSION-T1_TO_T2"` — cite verbatim in routing block (both flags cross-reference v6.2-canonical firings)
- Soft drifts: routing CSV `health_band = Healthy`/`health_score = 79.8` vs v6.2 `Thriving`/`82.4` (v6.2 wins); routing CSV `migration_confidence = careful` vs v6.2 `value_led` (v6.2 wins) — cite as soft drifts in "Conflicts between sources"

If `comm_action` does NOT match Format B (standard or CEO Pre-Call variant), STOP and surface — the routing CSV is the operator's per-account routing decision record; mismatch is a structural failure.

### Derived metrics (per `_root/07 §4.4`)

Compute and cite in conformance block:

- `cost_per_order = new_total_mrr × 12 / ltm_orders = $949 × 12 / ltm_orders = $11,388 / ltm_orders` (rounded to 2 decimal places; only if `ltm_orders > 0`)
- `annual_subscription = new_total_mrr × 12 = $949 × 12 = $11,388`
- `delta_per_order = delta_mrr × 12 / ltm_orders = $224 × 12 / ltm_orders = $2,688 / ltm_orders` (rounded; only if `ltm_orders > 0`)
- **Annual delta dollars (FIRES for `sca` because `delta_pct = 30.9% > 30%`)**: `delta_mrr × 12 = $224 × 12 = $2,688` — required in lede per `_root/04 §4.4` Format B variant; QB-106 reconciles within ±$1 (sca: $2,688 exact)
- User-billing reconciliation per `_root/07 §4.5`: threshold NOT TRIPPED for `sca` (user-count gap +7 trips |gap|>3 but dollar gap $0 does NOT trip |gap_$|>$60; both must trip per §4.5; no `⚠️ USER BILLING RECONCILIATION NEEDED` row in routing block).

### After-row math discipline (CL-025 RESOLVED 2026-05-26 — operator-stamped Discipline (1) at Stage 4.1 lpf production proof closeout per `PLANNING_AGENT_HANDOFF.md` Appendix B.4)

**The brief's After-row pricing-table math is populated DIRECTLY from v6.2 stamped values, NOT recomputed from billing math or derived enabled count.** This discipline is format-agnostic — applies to Format B identically to Format A:

- `[NEW_EXCESS]` = v6.2 `excess_users` column = `8` (modeled-canonical per `_root/05 §2.1.5`; do NOT recompute from `enabled_users = 25` column)
- `[NEW_USER_CHARGE]` = v6.2 `user_charge` column = `$200` (computed by v6.2 at the graduated-rate ladder; sanity check: 8 excess @ $25 first-band rate = $200 ✓)
- `[NEW_MRR]` = v6.2 `new_total_mrr` column = `$949` (canonical; recomposes: `$749 tier_base + $200 user_charge = $949` ✓)
- `[LEGACY_EXCESS]` = `ROUND(current_user_mrr ÷ current_user_rate) = ROUND($0 ÷ $20) = 0` (Before-row IS billing-canonical — derived from current invoice math; sca's legacy plan has NO user-excess line)
- `[LEGACY_USER_CHARGE]` = v6.2 `current_user_mrr` column = `$0` (Before-row = customer's actual today-invoice user charge; sca pays ZERO user excess on legacy)

**Reconciliation handling**: per `_root/07 §4.5`, compute `implied_billed_excess = ROUND(current_user_mrr ÷ current_user_rate) = ROUND($0 ÷ $20) = 0` and `narrative_excess = trailing_avg_users − current_provided_users = 18 − 25 = -7 (floor at 0) = 0`. If `|gap| > 3 users AND |gap × current_user_rate| > $60`:

1. The `⚠️ USER BILLING RECONCILIATION NEEDED` line fires in the brief's routing block per `_root/07 §7` template (internal-routing-block only; removed before send).
2. The After-row math STAYS at v6.2 stamped values (do NOT shift to enabled-canonical; do NOT re-version the brief).
3. The brief APPROVES as-drafted; the reconciliation gap is closed via INTERNAL SuperCat ops cleanup pre-`[EFFECTIVE_DATE]` (planning agent verifies the account has a row in `_meta/v6_2_reconciliation_log.md`; if not present, planning agent appends a new row at review-pass approval; CSM/Ops team owns the per-account cleanup workstream).
4. **Client copy NEVER mentions "unused users," "phantom accounts," or any user-cleanup language** per `_root/04 §3` audience-discipline; the ops cleanup is a SuperCat-side workstream, not a customer conversation topic. The verbatim `_root/04 §4.9` footnote stays unchanged in the brief; the §4.9 drafter-facing operational note (appended 2026-05-26) explains that the footnote is operationally accurate by `[EFFECTIVE_DATE]` because by that date enabled = v6.2 modeled (via ops cleanup).

**For `sca` specifically**: reconciliation flag NOT tripped (user-count gap +7 trips |gap|>3 BUT dollar gap $0 does NOT trip |gap_$|>$60; both must trip per §4.5 threshold). No `⚠️ USER BILLING RECONCILIATION NEEDED` row fires in sca's routing block. The conformance block's "Conflicts between sources" section notes the +7 user-count gap as informational (not a flag firing).

---

## Step 5 — Brief assembly (`format-b-notices/sca__shadow-catchers__brief.md`)

Output path: `format-b-notices/sca__shadow-catchers__brief.md` per `_root/07 §6` naming convention. `[company-slug] = shadow-catchers` per `_root/07 §6` slug derivation (`Shadow Catchers` → lowercase → spaces → hyphens → `shadow-catchers`).

You populate `format-b-notices/_brief-template.md` section-by-section. Every `[INSERT _root/XX §N.M ...]` pointer in the template you resolve by **fetch-and-paste verbatim** — open the named `_root/` section, copy the named content character-for-character into the production artifact, substitute only `[BRACKETED_TOKENS]` from v6.2 + Postgres data.

### Section walkthrough (per `format-b-notices/_brief-template.md` Sections 3b → 3p; full template is canonical — this is reading-order convenience)

1. **Internal routing note (Section 2 of the template)** — populate per `_root/07 §7` Format B matrix; include every required field + every applicable conditional row. **Format B does NOT carry `Expansion eligible`**; **Format B DOES carry `CEO awareness required before send` (NO for `sca`)**. **For `sca`**: routing block carries `Comm_action: Format B — Notice + Meeting Offer`; `flags: EARLY-ADOPTER-2015 | EXPANSION-T1_TO_T2`; `CEO awareness required before send: NO`; `Soft drift (v6.2 wins): routing CSV health_band Healthy / health_score 79.8 vs v6.2 Thriving / 82.4` + `routing CSV migration_confidence careful vs v6.2 value_led`. Removed before send per `_root/04 §2.14` + QB-047.

2. **Section 3b — Lede paragraph (Thriving / Healthy accounts only — `sca` is Thriving)** — drafter-generated; 2–3 sentences. Lead with relationship (tenure + at least one account-specific platform stat per `_root/04 §4.1` + `§4.2`); deliver dollar / date second. Tenure-band variants per `_root/04 §4.1` — for `sca` `cohort_year = 2015` selects the longest-tenure-band variant (e.g. "over a decade with us" / "11 years"; verify exact §4.1 variant phrasing at draft time). **For `sca`: `delta_pct = 30.9% > 30%` triggers `_root/04 §4.4` Format B variant** — lede MUST name annual dollar impact: "a change of $224/month ($2,688/year)" inside the same sentence per §4.4 form. Standard relationship lede otherwise (no CEO Pre-Call variant; no PDC substitution since sca is URN-primary not PDC; no health-band override since Thriving). Lede stat selection per `_root/04 §4.2` + composite_narrative orientation: prefer a value-delivery anchor over an engagement anchor (sca's VD=100; engagement=71.7 is the relative weakness — INTERNAL observation; lede surfaces VD-anchored stats from Postgres §4.3 LTM orders/GMV or §4.2 90-day activity). Drafter does NOT mention "engagement" in client copy.

3. **Section 3c — Standalone dollar-change sentence** — verbatim from `_root/04 §4.13`. For Thriving / Healthy: second sentence after the lede paragraph. **Per operator-stamped strict-placeholder precedent 2026-05-26 (Stage 3.1 review pass): fetch verbatim from §4.13 even though it has only 4 bracketed tokens — preserves path-reference contract end-to-end.** Substitute `[EFFECTIVE_DATE]` (sca is Monthly; flat effective date), `[CURRENT_MRR] = $725`, `[NEW_MRR] = $949`, `[DELTA] = +$224`, `[DELTA_PCT] = +30.9%` from v6.2.

4. **Section 3d — Consolidated 2026 framing sentence** — verbatim from `_root/04 §3` (the table row's "Replacement" column; the iterated phrasing operator-stamped). No substitution; copy character-for-character.

5. **Section 3e — Tenure-aware variant sentence** — one short sentence per `_root/04 §4.1` tenure-band variants; substitute `[YEAR] = 2015` from `cohort_year`. For `sca` at `cohort_year = 2015`, the §4.1 variant is the longest-tenure-band (10+ years register; verify exact §4.1 variant selector at draft time — the §4.1 source text owns the tenure-band granularity). NOT replaced by §4.14 since sca is URN-primary not PDC.

6. **Section 3f — Early-adopter tenure paragraph (FIRES for `sca`)** — `cohort_year = 2015 ≤ 2015`: paste the early-adopter tenure paragraph from `_root/04 §4.7` Format B variant verbatim; substitute `[YEAR] = 2015` from `cohort_year`. The §4.7 Format B variant names the year, names years of tenure (11 years from 2015 to 2026), and frames the platform-then-vs-platform-now distinction with the "fundamentally different product" framing. **This is the first Format B production proof to fire §4.7** (cci was 2021 and bri was 2023 — both did not fire). Drafter pastes §4.7 Format B variant character-for-character; QB-NNN paste-verifies in conformance block.

7. **Section 3g — Driver dispatch (Format B carries all 8 increase-side drivers; sca is `user_rate_normalization`)** — paste `_root/05 §2.1.2` Format B URN canonical block. Apply `§2.1.6` conditional context paragraphs: `§4.9` billing-basis footnote (REQUIRED for URN per `§2.13` non-negotiable + `_root/04 §4.9`; one paste covers both URN-primary AND IUR-secondary per `§4.9` source text covering excess-user billing universally); `§4.6` platform-base-grown FIRES (FOLLOW-ON paragraph after pricing table at Section 3i, NOT inline; `tier_base = $749 > current_platform_mrr = $725`; small $24 gap but rule firing is binary); `§4.10` URN platform-base conditional sentence FIRES (Before platform base $725 ≠ After platform base $749; paste verbatim inside URN block); `§4.7` early-adopter at Section 3f (NOT inside the URN block — separate template section); `§4.5` operations-unchanged sentence with IUR-FORK variant at Section 3o (because `secondary_drivers` includes IUR per `§2.13` non-negotiable). **Plus `§2.1.7` URN+IUR secondary integration sub-block FIRES** — paste verbatim per templated coverage; integration is WITHIN the URN primary block per `_root/05 §1.3`, not a separate section.

8. **Section 3h — Secondary-driver weaving (FIRES for `sca`)** — `secondary_drivers = included_user_reduction`: integrate per `_root/05 §4` matrix row `user_rate_normalization, included_user_reduction` (the URN+IUR templated coverage row) WITHIN the primary URN block at Section 3g, NEVER as a separate section per `_root/05 §1.3`. The `_root/05 §2.1.7` URN+IUR sub-block is the canonical paste. The post-CL-026 + CL-023 joint-resolution 2026-05-26 IUR-as-secondary semantic scope at `_root/05 §2.4.1` covers BOTH reduction-side cases (sca's case: `current_provided_users = 25 > included_users = 10`, legacy allotment moving down) AND expansion-side cases (the 9-account cluster — not applicable to sca). For sca, the §2.1.7 templated paste covers the URN+IUR integration end-to-end; drafter does not separately paste §2.4.7 (which is the IUR-primary version of the URN-secondary integration, not applicable here). QB-092 PASSES if integration is within primary block; QB-093/QB-094 N/A.

9. **Section 3i — Pricing-table row template (URN) + billing-basis footnote + §4.6 follow-on** — pricing table immediately follows driver prose. Row template owned by `_root/05 §2.1.5` URN; substitute Before/After values from v6.2 + the §4.9 footnote attestation per CL-025. **Billing-basis footnote** — required per `_root/04 §4.9` (URN AND IUR both fire it; one paste suffices). Paste verbatim italicized sentence immediately after the URN pricing table. **Platform-base-grown follow-on paragraph (`_root/04 §4.6`)** — FIRES because `new_tier_base = $749 > current_platform_mrr = $725`. Format B applies §4.6 as a **separate follow-on paragraph AFTER the pricing table** per template Section 3i (Format B does NOT inline §4.6 into the driver block — that is Format A's pattern via §2.5.4 placeholder per CL-013). Drafter pastes §4.6 verbatim with `[YEAR] = 2015` substituted from `cohort_year`.

10. **Section 3j — Tier verbatim block (T1 for `sca`)** — paste the verbatim "What You're Getting at $749" block for `assigned_tier = T1` from `_root/03 §1`. Substitute `[NEW_INCLUDED] = 10` from `included_users` (T1 carries the placeholder per `_root/03 §1` T1 source).

11. **Section 3k — "What This Works Out To" value-anchor section (conditional; depends on Postgres ltm_orders)** — include only if `cost_per_order < $200` per `_root/04 §4.8` (operator-stamped 2026-05-22; **CL-002 — NOT archived $35**) AND `ltm_orders > 0`. For `sca`: threshold inclusion iff `ltm_orders > 57` (since `$11,388 / 57 ≈ $199.8`). Append second sentence (delta-per-order reframe) only if `delta_per_order < $50` iff `ltm_orders > 54` (since `$2,688 / 54 ≈ $49.8`). Fresh agent computes from Postgres §4.3 at Step 4.

12. **Section 3l — "What's Coming in 2026" roadmap** — verbatim from `_root/03 §3`. **No substitution.** Remove the trailing `*[Operator note — remove before sending: …]*` line per `_root/04 §2.14` + QB-046. **(Particularly important for Format B: the archived template OMITTED this section entirely; the new template ADDS it via CL-005 — operator decision 2026-05-22, mandatory across all 4 formats.)**

13. **Section 3m — "How This Compares" (conditional; drafter judgment)** — include only if the drafter judges it adds clarity for THIS account AND `_root/04 §4.11` indicates appropriate. If included: position vocabulary per `_root/04 §4.11` ("at the base rate" / "below the midpoint" / "near the midpoint" / "above the midpoint"); user-count clause per `_root/04 §4.3` if "above the midpoint" fires; structural-fairness sentence per `_root/04 §2.7` / `§4.11`. **NEVER peer dollar ranges in client copy** (CL-003 universal); **NEVER "equivalent platforms" / unnamed-competitor pricing sentence** (CL-004 universal); **NEVER "no account-specific adjustments" sentence** (CL-001). For `sca`'s small $24 platform-base gap + $200 user_charge: drafter judgment may OMIT Section 3m if it does not add clarity; surface judgment in conformance block.

14. **Section 3n — "Your Pricing at a Glance" summary table** — every Format B brief carries this table. Substitute Before/After values from v6.2: Before-row `current_mrr = $725` / `current_platform_mrr = $725` / `current_user_mrr = $0` / `current_user_rate = $20`; After-row `new_total_mrr = $949` / `tier_base = $749` / `user_charge = $200` / graduated-ladder summary string from `_root/03 §2 Block A` (e.g. `"Graduated ($25/$22/$20/$18)"`).

15. **Section 3o — Operations-unchanged paragraph + IUR fork (FIRES for `sca`)** — paste `_root/04 §4.5` **IUR-FORK variant** (NOT DEFAULT) because `secondary_drivers` includes `included_user_reduction` per `_root/05 §2.13` non-negotiable + `_root/04 §4.5`. Drafter pastes §4.5 IUR-fork variant character-for-character. (Distinct from `cci` which had blank secondary and pasted DEFAULT variant; sca is the first Format B production proof to fire IUR-fork variant.)

16. **Section 3p — Format B close paragraph (active meeting offer)** — paste verbatim from `_root/04 §4.12` Format B variant (active meeting offer; CSM coordinates directly; never a specific date; never assistant-coordinated booking). Substitute `[EFFECTIVE_DATE]` from v6.2 + cohort calendar (sca: `notice_cohort = June`; `notice_deadline = 1-Jul`; effective date per cohort calendar). **Standard Format B (NOT CEO Pre-Call variant)** for sca; no CEO-call calibration sentence.

17. **Formal-notice line (immediately after close)** — required per `_root/04 §4.12`'s "immediately after each close, except Good News" instruction. Paste verbatim italicized form from `_root/04 §4.12`; substitute `[EFFECTIVE_DATE]`.

---

## Step 6 — Delivery email assembly (`format-b-notices/sca__shadow-catchers__delivery-email.md`)

Output path: `format-b-notices/sca__shadow-catchers__delivery-email.md` per `_root/07 §6`. `[company-slug] = shadow-catchers` matches the brief.

You populate `format-b-notices/_delivery-email-template.md`. **Format B's email body is 3 paragraphs** (longer than Format A's 4-sentence wrapper because the active meeting offer + optional relationship hook push the count up — but do NOT exceed 3 paragraphs; the substance lives in the attached brief).

### Section walkthrough

1. **Section 1 — Subject + From + To + Attachment header** — per template. Subject pattern: `Shadow Catchers: your SuperCat pricing is changing — effective [EFFECTIVE_DATE]`. Same convention as Format A for cross-format consistency.

2. **Section 2 — Internal routing block** — populate per **`_root/07 §7.5` Format B column matrix** (operator-stamped 2026-05-26 via Stage 4 prep Source-fix Session B; CL-022 RESOLVED). Include every required Format B field + every applicable conditional row. **Format B does NOT carry `Expansion eligible` field; DOES carry `CEO awareness required before send` (NO for sca).** For `sca`: cite `Soft drift (v6.2 wins): routing CSV health_band / migration_confidence drift` as conditional observation row per `_root/07 §7.5` Format B column. Removed before send per `_root/04 §2.14`.

3. **Section 3 — Email body skeleton — 3 paragraphs**:
   - **Paragraph 1 — opener**: Sentence 1a CONDITIONAL — **DEFAULT for `sca` (standard Format B, Thriving)**: drafter writes a one-sentence relationship hook (8–15 words) — names relationship without specific stats (stats stay in the brief). NOT CEO Pre-Call variant (no acknowledgement of prior CEO call). NOT OMITTED (no health-band override). Sentence 1b ALWAYS PRESENT: drafter writes a one-sentence dollar-change effective-date sentence per `_root/04 §4.13` standalone form **with attachment pointer appended** ("…the attached brief walks through what's behind it and what you're getting at the new price."). Per strict-placeholder precedent: §4.13 sentence is fetched from `_root/04 §4.13` verbatim; only the attachment-pointer phrase is drafter-generated.
   - **Paragraph 2 — operations-unchanged**: paste `_root/04 §4.5` **IUR-FORK variant** (because `secondary_drivers` includes IUR per `§2.13` non-negotiable). Verbatim.
   - **Paragraph 3 — active meeting offer + formal-notice line**: paste verbatim `_root/04 §4.12` Format B close (active meeting offer). Optional per-account calibration of ONE sentence (preserving active register; NEVER a specific date; NEVER assistant-coordinated booking). NOT applicable for `sca` (standard Format B; no CEO Pre-Call variant). Then paste verbatim italicized formal-notice line from `_root/04 §4.12`; substitute `[EFFECTIVE_DATE]`.
   - **Signature**: `[CSM_NAME] | Customer Success | SuperCat`

4. **Section 4 — Email-specific pre-send checks** — confirmed before send (template scaffolding; not part of email body). Same conformance discipline as the brief. Format B specifics: QB-025 CEO awareness check N/A (standard); QB-086 active meeting offer register (NOT Format A passive; NOT CEO Letter specific-date).

5. **Section 5 — Day-7 follow-up template** — drafter-facing scaffolding for the conditional day-7 follow-up if no meeting accepted. **Format B follows up at day 7** (vs Format A's day-10) because the meeting offer is active. Same voice constraints as original email — no minimizing, no apology, no specific date, no assistant booking. If no response to day-7 follow-up, offer stays open passively until effective date; do NOT send a third active prompt (would cross into pressure register per `_root/04 §2.4`).

---

## Step 7 — Anti-drift discipline + QB-NNN self-audit (`_root/08` 138-check checklist)

You run every QB-NNN whose `Applies to:` field covers Format B or "all formats" before the conformance block. The list below is convenience indexing of Format-B-specific blockers; consult `_root/08` directly as canonical (138 checks total post Stage 4 prep Source-fix Session B; §10 entity-packet checks NOT applicable to this session).

### Drift-control + conformance (every session)

- **QB-001** — manifest-echo contract.
- **QB-002** — conformance block present in final reply, canonical format per `_root/00_manifest.md §5`.
- **QB-003** — files-read completeness.
- **QB-004** — no unauthorized archive reads.
- **QB-007** — no rule restated outside its owning `_root/` doc (path-reference contract).

### Routing (this brief is the right brief for this account)

- **QB-011** — `ord_id = sca` resolves cleanly to one v6.2 row (CSV line 85), not filtered.
- **QB-013** — format derived from the 6-step routing-decision flow per `_root/06 §2`.
- **QB-018** — Δ_pct / Δ_mrr boundary handled per `_root/06 §3` precedence — for `sca`: delta_pct 30.9% just above 30% pct band threshold; delta_mrr $224 squarely in $80<$224≤$400 dollar band; dispatch stays Format B; §4.4 high-delta lede rule fires inside Format B (lede-voice rule, not format-flip).
- **QB-019** — entity-children do NOT receive a standalone Format B brief — N/A for sca (standalone).
- **QB-024** — brief written to `format-b-notices/`.
- **QB-025** — CEO Pre-Call variant CEO-awareness check — N/A for sca (standard Format B).

### Data-pipeline

- **QB-028** — canonical loader from `_root/07 §3`.
- **QB-030** — three Postgres queries verbatim from `_root/07 §4`.
- **QB-031** — derived metrics computed per `_root/07 §4.4`.
- **QB-032** + **QB-110** — user-billing reconciliation per `_root/07 §4.5`; ⚠️ flag NOT FIRES for sca (user-count gap +7 but dollar gap $0; both must trip per §4.5 threshold); After-row math stays at v6.2-canonical per CL-025.
- **QB-036** + **QB-037** — brief routing block complete per `_root/07 §7` Format B matrix (NO `Expansion eligible` field; YES `CEO awareness required before send: NO` for sca).
- **NEW (Source-fix Session B)** — delivery-email routing block complete per **`_root/07 §7.5` Format B column** (operator-stamped 2026-05-26).

### Voice / content

- **QB-040** / **QB-062** — lede leads with dollar + date, not percentage.
- **QB-041** — no "we're adjusting your pricing" variants.
- **QB-042** / **QB-065** — no apology for the change or prior pricing.
- **QB-043** / **QB-068** / **QB-069** — no health bands or dimension scores in client copy.
- **QB-045** / **QB-072** — universality claim uses "every account we work with" without hedge.
- **QB-046** — "What's Coming in 2026" present verbatim from `_root/03 §3`; operator-note line stripped. **Particularly important for Format B: archived template OMITS this section; CL-005 ADDS it.**
- **QB-047** — internal routing-note blockquote removed from delivered version (both brief + email).
- **QB-054** — no competitor-pricing reference (named OR unnamed).
- **QB-059** — no "no account-specific adjustments" sentence.
- **QB-063** — no minimizing language ("modest," "small," "minor") — particularly important for sca's small $24 platform-base gap (do NOT minimize).
- **QB-067** — no support-issue context in body (⚠️ flag stays in routing block).
- **QB-071** — no peer-range dollar values anywhere in client copy.
- **QB-077** — "above the midpoint" carries `_root/04 §4.3` user-count clause when applicable.
- **QB-078** — **high-delta annual-dollar sentence in lede when `delta_pct > 30%`** — **FIRES for `sca` (30.9% > 30%); annual = `$224 × 12 = $2,688`** must appear in same sentence as monthly change per `_root/04 §4.4` Format B variant.
- **QB-079** — `_root/04 §4.5` operations-unchanged sentence verbatim; **correct variant: IUR-FORK for `sca`** (secondary includes IUR per `§2.13` non-negotiable).
- **QB-080** — `_root/04 §4.6` platform-base-grown sentence verbatim with correct cohort year — **FIRES for `sca` with [YEAR]=2015**; applied as follow-on paragraph after pricing table for Format B per Section 3i.
- **QB-082** — value-anchor inclusion / exclusion respects `_root/04 §4.8` $200 threshold (CL-002; NOT archived $35) — for `sca`: threshold inclusion iff `ltm_orders > 57`.
- **QB-083** — billing-basis footnote verbatim after URN OR IUR pricing table per `_root/04 §4.9` — **FIRES for `sca` (URN-primary + IUR-secondary; ONE paste of §4.9 covers both per §4.9 source text)**.
- **QB-084** — **URN platform-base conditional sentence (Format B form) when Before platform base ≠ After platform base per `_root/04 §4.10`** — **FIRES for `sca` (Before $725 ≠ After $749)**.
- **QB-085** — "How This Compares" position vocabulary only; no peer-range dollars.
- **QB-086** — **Format B close verbatim per `_root/04 §4.12` Format B variant (active meeting offer; NOT Format A passive; NOT CEO Letter specific-date)**; formal-notice line present.
- **QB-087** — Watch / At Risk / Critical / VD<40 lede override applied if triggered — N/A for sca (Thriving).
- **QB-088** — `_root/04 §4.14` discount-correction substitution applied at Section 3e when `migration_driver = platform_discount_correction` — N/A for sca (URN-primary).
- **NEW (Source-fix Session A)** — for `deal_type = 'Annual'`: §4.16.2 lede effective-date renewal-date resolution — N/A for sca (Monthly); §4.16.3 formal-notice line token resolution — N/A.
- **NEW (Source-fix Session A)** — grep `_root/04 §3` 32-row table at draft time for any forbidden phrase (including the 6 new SaaS-renewal rows added 2026-05-26).

### Driver content

- **QB-089** — driver block verbatim from `_root/05 §2.1.2` for sca (URN Format B canonical block).
- **QB-090** — every bracketed placeholder substituted from v6.2 / Postgres.
- **QB-091** — conditional sub-blocks (`[IF ...]`) rendered iff condition holds.
- **QB-092** — **secondary-driver weaving integrated WITHIN primary block, not separately (per `_root/05 §1.3`)** — FIRES for `sca` (URN+IUR via `§2.1.7` templated sub-block).
- **QB-093** — MOR + IUR integration per `_root/05 §2.6.6` + `§4` weaving matrix per CL-016 — N/A for sca (URN+IUR, not MOR+IUR).
- **QB-094** — MOR + URN per-account narrative integration per `_root/05 §2.6.7` + `§4` matrix — N/A for sca (URN+IUR, not MOR+URN).
- **QB-095** — no improvised content for drivers Format B does not carry (MC, UCV, RA).
- **CL-026 + CL-023 post-resolution check (informational)** — the URN+IUR integration at `§2.1.7` exercises the freshly-resolved IUR-as-secondary semantic scope per `_root/05 §2.4.1` (post-2026-05-26 source-fix). For sca's reduction-side case (`current_provided_users = 25 > included_users = 10`), the §2.1.7 templated paste covers the integration end-to-end without needing the expansion-side semantic clarification. Surface in conformance block as observation: "sca exercises the post-CL-026 reduction-side IUR-as-secondary semantic at §2.1.7; expansion-side scope (9-account cluster) not applicable."

### Product / pricing language

- **QB-099** — tier block verbatim from `_root/03 §1` T1 for sca.
- **QB-100** — user-rate ladder uses 1–10 / 11–25 / 26–50 / 51+ bands (`_root/03 §2 Block A`).
- **QB-101** + **QB-102** — no unpublished SKU names; no INTERNAL peer / competitive tables in client copy.

### Math reconciliation

- **QB-104** — pricing-table Before total = `current_mrr = $725`; After total = `new_total_mrr = $949` exactly.
- **QB-105** — stated Δ MRR = `new_total_mrr − current_mrr = $949 − $725 = $224` within ±$1.
- **QB-106** — **when `delta_pct > 30%`, annual figure = `delta_mrr × 12 = $224 × 12 = $2,688` within ±$1 (FIRES for `sca`; exact reconciliation)**.
- **QB-107** — `tier_base = $749` and `included_users = 10` match T1 in `_root/03 §1`.
- **QB-108** — boundary cases reconcile with `_root/06 §3` precedence — for sca: delta_pct 30.9% just above 30% pct-band threshold; delta_mrr $224 mid-Format-B-dollar-band; dispatch stays Format B per §3.
- **QB-110** — user-billing reconciliation per `_root/07 §4.5`; After-row stays v6.2-canonical per CL-025; not tripped for sca (dollar gap $0).
- **QB-111** — `support_fire = TRUE` ⚠️ flag handled correctly — N/A for sca (`support_fire = FALSE`).

### Manifest-echo + path-reference contract drift control

- **QB-125** — manifest-echo dates match `_root/00_manifest.md §2` table values exactly. If divergence: STOP and flag per `_root/00_manifest.md §6` (§3-propagation failure).

### Path-reference contract zero-inlined-prose target

**Hard target: COUNT = 0 paraphrased or inlined `_root/` rule prose.** Every rule paste in your brief + email artifact is verbatim from the owning `_root/` section. The drafter-generated prose is narrowly scoped per Appendix A.5 (lede paragraph; delivery email Sentence 1a; delivery email Sentence 1b attachment-pointer phrase — and ONLY these for sca; no CEO Pre-Call calibration since sca is standard Format B). If you find yourself rewriting a `_root/` rule paragraph to "fit better" — STOP. Fetch and paste; substitute tokens only.

### CL-024 strict + paste-verification carry-forward

For every `_root/` rule prose paste in your brief + email, paste-quote the source verbatim in your conformance block under "CL-024 paste-verification". This proves you fetched-and-pasted (the production artifact's prose matches the source character-for-character); paraphrasing would surface as a diff between the paste-quote and the production artifact's prose.

---

## Step 8 — Output + conformance block

### Files to write (2 files, no more)

1. `format-b-notices/sca__shadow-catchers__brief.md` — populated per Step 5.
2. `format-b-notices/sca__shadow-catchers__delivery-email.md` — populated per Step 6.

Per `_root/07 §6`: `[company-slug] = shadow-catchers` (Shadow Catchers → lowercase → space → hyphen → no special chars). Re-runs use `__v2` suffix per `_root/07 §6` versioned re-run pattern.

### Conformance block (final chat message; canonical format per `_root/00_manifest.md §5` + Stage 4 per-account additions)

```
─── Conformance Block (Stage 4.2 per-account drafter) ─────────
Session task: Stage 4.2 Format B Notice + Meeting Offer draft for ord_id = sca (single-account session per Appendix A.3).
Output target: format-b-notices/sca__shadow-catchers__brief.md + format-b-notices/sca__shadow-catchers__delivery-email.md
Comm_action: Format B — Notice + Meeting Offer (paste verbatim from routing CSV row 34)

Manifest echo (per _root/00_manifest.md §1 step 6 + §6 — paste-quote ALL ENTRIES from §2 with title + Last-updated header date verified at source, NOT mtime alone per CL-024):
- 00 Root Doc Manifest — <Last-updated header date>
- C  Operator + Agent Contracts — <Last-updated header date>
- 01 Why We Are Migrating — <Last-updated header date>
- 02 Who Is Being Migrated — <Last-updated header date>
- 03 What We Sell — <Last-updated header date>
- 04 Communication Posture — <Last-updated header date>
- 05 Driver Taxonomy — <Last-updated header date>
- 06 Format Routing — <Last-updated header date>
- 07 Data Pipeline — <Last-updated header date>
- 08 Quality Bar — <Last-updated header date>
- 09 Changelog — <Last-updated header date>

Files read (with last-updated date / mtime):
- <enumerate every file from Step 2 reading list with verified Last-updated date — including the Stage 4.1 lpf precedent pair at items 17–18 + the Stage 4.2 cci precedent pair at items 19–20 as structural references>

Explicitly-authorized archive reads (per CONTRACTS §4):
- none (anti-archive rule per CONTRACTS §4; no explicit-extraction exception opened for this session)

Files NOT read (per Step 2 "Do NOT read"):
- _archive/** (anti-archive)
- Migration-Health Artifacts/ (scope creep)
- _reference/** (scope creep)
- _meta/stage2_prompts/** (scope creep)
- _meta/stage3_prompts/** (Stage 3 build prompts, not relevant)
- _meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md (Appendix A constraints embedded in Step 1 above)
- _meta/stage4_prompts/_paste-ready/stage_4_2__bri.md (hard-stopped 2026-05-26; superseded by post-CL-026 resolution; not a reference for sca)
- Other per-account briefs/emails in format-*-notices/ (out of scope EXCEPT Stage 4.1 lpf pair + Stage 4.2 cci pair as structural references)

Routing 6-step trace (per Step 3; paste-cite v6.2 column + value at each step):
1. Status filter: ghost_account = FALSE + migration_status = migration_pending → PASS
2. Decrease check: delta_mrr = +$224 → not decrease — Format B in scope
3. Entity overlay: parent_entity = Shadow Catchers (= company) → not child — standalone in scope
4. Annual overlay: deal_type = Monthly → not Annual — flat effective date
5. Health override: health_band = Thriving (v6.2; routing CSV says Healthy; v6.2 wins per Appendix B); value_delivery_score = 100 → Thriving — full lede; no §4.13 override
6. Delta-tier dispatch: delta_mrr = +$224, delta_pct = +30.9% — delta_mrr in Format B dollar band $80<$224≤$400; delta_pct just above 30% pct band threshold by 0.9 pts; per _root/06 §3 dispatch stays Format B (delta_mrr dominates dollar-band assignment; delta_mrr=$224<<$400 CEO Letter dollar floor); _root/04 §4.4 high-delta lede rule FIRES inside Format B (lede-voice rule, not format-flip) → **Format B — Notice + Meeting Offer (standard variant)**

CSV-canonical reconciliation (per Stage 3.5 review-pass lesson; paste-cite from _master-account-data-v6.2.csv row sca CSV line 85 + migration_comm_tiers_2026-05-19.csv row sca data row 34):
- ord_id = sca
- company = Shadow Catchers
- ghost_account = FALSE
- migration_status = migration_pending
- current_mrr = $725
- new_total_mrr = $949
- delta_mrr = +$224 (verified: $949 − $725 = $224 within ±$1 per QB-105)
- delta_pct = +30.9% (>30%: annual figure = $224 × 12 = $2,688 per QB-106 within ±$1 exact)
- cohort_year = 2015 (≤2015: §4.7 early-adopter FIRES at Section 3f with [YEAR]=2015)
- deal_type = Monthly
- assigned_tier = T1
- included_users = 10
- migration_driver = user_rate_normalization
- secondary_drivers = included_user_reduction (§2.1.7 URN+IUR integration FIRES at Section 3h; §4.5 IUR-fork variant FIRES at Section 3o)
- health_band = Thriving (v6.2 wins over routing CSV Healthy per Appendix B)
- health_score = 82.4 (v6.2; routing CSV says 79.8; 2.6-point soft drift; v6.2 wins)
- value_delivery_score = 100
- notice_cohort = June
- notice_deadline = 1-Jul
- support_fire = FALSE
- billing_entity = blank (not flagged in routing block)
- migration_confidence = value_led (v6.2; routing CSV says careful; v6.2 wins per Appendix B; drafter-facing only)
- comm_action (from routing CSV) = Format B — Notice + Meeting Offer
- flags (from routing CSV) = EARLY-ADOPTER-2015 | EXPANSION-T1_TO_T2 (cite verbatim in routing block)
- hold_condition / post_hold_action / nuances (from routing CSV) = blank

Reconciliation tracker pre-flight (per Appendix B.5.2 canonicality check + _root/07 §4.5):
- sca in _meta/v6_2_reconciliation_log.md flagged set: NO (verified via grep — not in 37-row flagged set)
- Threshold check inline: implied_billed_excess = ROUND($0 ÷ $20) = 0; gap_users = enabled_users 25 − modeled_users 18 = +7 (|gap| = 7 > 3 → TRIPPED on user count); gap_dollars = $0 − MAX(18−25, 0) × $20 = $0 (|gap_$| = $0; threshold > $60 → NOT TRIPPED on dollar gap); both must trip per §4.5 → material-gap flag = FALSE
- After-row math discipline per CL-025: [NEW_EXCESS] = v6.2 excess_users = 8; [NEW_USER_CHARGE] = v6.2 user_charge = $200; [NEW_MRR] = v6.2 new_total_mrr = $949 (sanity check: $749 + $200 = $949 ✓); [LEGACY_EXCESS] = ROUND($0 / $20) = 0; [LEGACY_USER_CHARGE] = $0 (current_user_mrr; legacy plan has no user-excess line)

Postgres-stat fetch (per _root/07 §4 + §5):
- Query §4.1 (org resolution): <query echoed verbatim + result>
- Query §4.2 (active users + 90d login): <result OR fallback per §5>
- Query §4.3 (LTM orders + GMV + customers): <result OR fallback per §5>
- Derived metrics per §4.4: cost_per_order = $11,388 / ltm_orders (inclusion threshold: ltm_orders > 57); annual_subscription = $11,388; delta_per_order = $2,688 / ltm_orders (second-sentence threshold: ltm_orders > 54); annual_delta = $2,688 (delta_pct>30% — QB-106 exact reconciliation)
- User-billing reconciliation per §4.5: PASS — +7 user-count gap but $0 dollar gap; both thresholds not jointly tripped

CL-024 paste-verification (REQUIRED — paste-quote verbatim every _root/ rule prose pasted into the brief + email):
1. _root/04 §4.13 standalone dollar-change sentence (Section 3c of brief): "<paste-quote verbatim source + production output>"
2. _root/04 §3 consolidated 2026 framing sentence (Section 3d of brief): "<paste-quote>"
3. _root/04 §4.1 tenure-aware variant (Section 3e of brief; longest-tenure-band variant for cohort_year=2015): "<paste-quote>"
4. _root/04 §4.7 early-adopter tenure paragraph (Section 3f of brief; FIRES for sca with [YEAR]=2015): "<paste-quote verbatim source + production output>"
5. _root/05 §2.1.2 URN Format B canonical block (Section 3g of brief): "<paste-quote verbatim source + production output>"
6. _root/05 §2.1.7 URN+IUR secondary integration sub-block (Section 3h of brief; FIRES for sca): "<paste-quote verbatim source + production output>"
7. _root/05 §2.1.5 URN pricing-table row template (Section 3i of brief): "<paste-quote>"
8. _root/04 §4.9 billing-basis footnote (URN+IUR; one paste covers both): "<paste-quote>"
9. _root/04 §4.6 platform-base-grown follow-on paragraph (FIRES for sca because $749>$725; with [YEAR]=2015): "<paste-quote>"
10. _root/04 §4.10 URN platform-base conditional sentence (FIRES for sca because Before $725 ≠ After $749): "<paste-quote>"
11. _root/03 §1 T1 tier block (Section 3j of brief; with [NEW_INCLUDED]=10): "<paste-quote>"
12. _root/03 §3 "What's Coming in 2026" (Section 3l of brief): "<paste-quote — confirm operator-note line stripped>"
13. _root/04 §4.5 operations-unchanged sentence IUR-FORK variant (Section 3o of brief; FIRES for sca because secondary includes IUR): "<paste-quote>"
14. _root/04 §4.12 Format B close (Section 3p of brief): "<paste-quote verbatim source + production output with [EFFECTIVE_DATE] substituted>"
15. _root/04 §4.12 formal-notice line (after close): "<paste-quote>"
16. _root/04 §4.5 IUR-FORK variant in delivery email Paragraph 2: "<paste-quote — same fork as brief Section 3o>"
17. _root/04 §4.12 Format B close in delivery email Paragraph 3: "<paste-quote>"
18. _root/04 §4.4 high-delta annual-dollar lede rule (FIRES for sca because delta_pct=30.9%>30%; lede names $2,688/year alongside monthly): "<paste-quote verbatim source + production lede output>"

Path-reference contract verification:
- Inlined _root/ rule prose in production artifacts: COUNT = 0 (target met)
- Drafter-generated prose narrowly scoped per Appendix A.5: Section 3b lede paragraph (relationship hook + dollar/date with §4.4 annual-dollar firing); delivery email Sentence 1a (DEFAULT relationship hook); delivery email Sentence 1b attachment-pointer phrase
- Every other prose block in brief + email = verbatim paste from owning _root/ section per CL-024 list above

QB-NNN results (every applicable check per _root/08; ID-by-ID, not "looks good"):
- Drift-control: QB-001 PASS; QB-002 PASS; QB-003 PASS; QB-004 PASS; QB-007 PASS (0 inlined rule prose)
- Routing: QB-011 PASS; QB-013 PASS; QB-018 PASS (delta_pct 30.9% boundary handled inside Format B per §3); QB-019 PASS (standalone); QB-024 PASS; QB-025 N/A (standard Format B; no CEO Pre-Call)
- Data-pipeline: QB-028 PASS; QB-030 PASS; QB-031 PASS; QB-032 + QB-110 PASS (no reconciliation flag); QB-036 + QB-037 PASS; §7.5 delivery-email matrix verified PASS
- Voice / content: QB-040/062 PASS; QB-041 PASS; QB-042/065 PASS; QB-043/068/069 PASS; QB-045/072 PASS; QB-046 PASS (operator-note stripped); QB-047 PASS; QB-054 PASS; QB-059 PASS; QB-063 PASS (small $24 gap not minimized); QB-067 PASS; QB-071 PASS; QB-077 <PASS / N/A>; **QB-078 PASS (annual-dollar sentence in lede; $2,688/year)**; **QB-079 PASS (§4.5 IUR-FORK variant — sca's secondary includes IUR)**; **QB-080 PASS (§4.6 follow-on paragraph with [YEAR]=2015)**; QB-082 <PASS — ltm_orders > 57 / N/A — ltm_orders ≤ 57>; **QB-083 PASS (§4.9 footnote for URN+IUR; one paste)**; **QB-084 PASS (§4.10 URN platform-base conditional — Before $725 ≠ After $749)**; QB-085 <PASS / N/A>; QB-086 PASS (Format B active register); QB-087 N/A (Thriving); QB-088 N/A (URN-primary, not PDC); §3 32-row table grep PASS
- §4.16 Annual checks: N/A for sca (Monthly)
- Driver content: QB-089 PASS (§2.1.2 URN block verbatim); QB-090 PASS; QB-091 PASS; **QB-092 PASS (URN+IUR via §2.1.7 within primary block; not separate section)**; QB-093 N/A (not MOR+IUR); QB-094 N/A (not MOR+URN); QB-095 PASS (no improvised MC/UCV/RA content); **CL-026 + CL-023 post-resolution observation: sca exercises reduction-side IUR-as-secondary semantic at §2.1.7 per post-2026-05-26 source-fix at §2.4.1; expansion-side scope (9-account cluster) not applicable**
- Product / pricing: QB-099 PASS (T1 verbatim from §1); QB-100 PASS; QB-101 + QB-102 PASS
- Math: QB-104 PASS ($725 / $949); QB-105 PASS ($224 reconciliation within ±$1); **QB-106 PASS ($2,688 annual reconciliation exact)**; QB-107 PASS ($749 / 10 match T1); QB-108 PASS (boundary delta_pct 30.9% handled inside Format B per §3); QB-110 PASS (reconciliation not flagged for sca); QB-111 N/A (support_fire FALSE)
- Manifest-echo: QB-125 PASS (every Last-updated date matches §2 table)

Gaps surfaced (a rule in _root/ with no check / no extraction path, OR a piece of source material with no _root/ home):
- <enumerate or "none">

Conflicts between sources (where two sources disagreed and I picked or flagged):
- **Soft drift 1 (v6.2 wins per Appendix B)**: routing CSV `health_band = Healthy` (`health_score = 79.8`) vs v6.2 `health_band = Thriving` (`health_score = 82.4`). 2.6-point composite drift; both bands above §4.13 override threshold; routing decision unaffected.
- **Soft drift 2 (v6.2 wins per Appendix B)**: routing CSV `migration_confidence = careful` vs v6.2 `migration_confidence = value_led`. Drafter-facing only (not in client copy per §3); routing unaffected.
- **Reconciliation observation (NOT a flag firing)**: user-count gap of +7 (enabled_users 25 vs modeled_users 18) trips |gap|>3 threshold but dollar gap of $0 (current_user_mrr=$0 because legacy plan absorbs all 25 provided users into platform_mrr line) does NOT trip |gap_$|>$60 threshold; both must trip per §4.5; material-gap flag = FALSE.
- <any other source disagreements>

Open questions for operator:
- <enumerate the specific decision needed — e.g. "Section 3b lede paragraph drafter-generated prose with §4.4 high-delta annual-dollar sentence: <paste production version>; operator-stamp for register-fit + §4.4 paste fidelity?" / "Section 3f §4.7 early-adopter paragraph paste with [YEAR]=2015: <paste production version>; operator-stamp for cohort-2015 framing?" / "Section 3h URN+IUR §2.1.7 secondary integration within URN primary block: <paste production version>; operator-stamp for reduction-side semantic accuracy?" / "Section 3m How-This-Compares included/omitted on drafter judgment per §4.11; operator-stamp inclusion?" / "<other ambiguity>" — or "none">
─────────────────────────────────────────────────────────────
```

**STOP after producing this conformance block + 2 file outputs.** Do not draft additional per-account briefs in this session (one ord_id in, two files out per Appendix A.3). The operator + planning agent run the audit + stamp loop next per the per-account review protocol in `_meta/stage4_prompts/README.md`.

If your routing re-derivation in Step 3 disagrees with Format B at any step, STOP and surface — do not produce production artifacts. If your QB-NNN self-audit surfaces a hard fail, STOP and surface — do not produce production artifacts. If a `_root/` rule is ambiguous and you cannot fetch verbatim prose, STOP and surface per `_root/CONTRACTS.md §2`.

**Asking is cheap. Inventing is the drift vector.**

---

*Cross-references: `_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md` (Appendix A design constraints; Appendix B CSV-canonical operator stamp; Appendix B.4 reconciliation discipline; Appendix B.5.1 csv.DictReader discipline; Appendix B.5.2 canonicality check); `_meta/stage4_prompts/stage_4_1__format-a__per-account-drafter.md` (657 lines; gold-standard 8-step skeleton; pattern-inheritance source for this prompt); `_meta/stage4_prompts/stage_4_2__format-b__per-account-drafter.md` (697 lines; the Format B drafter prompt this paste-ready is built on); `_meta/stage4_prompts/_paste-ready/stage_4_2__cci.md` (841 lines; FIRST Format B paste-ready proof — closest structural reference for sca; same URN primary; sca extends with §4.4 high-delta + §4.7 early-adopter + §2.1.7 URN+IUR secondary integration + §4.5 IUR-fork); `_meta/stage4_prompts/README.md` (per-account session review protocol); `_meta/stage4_account_ledger.md` (planning-agent ledger; row populates after this session's review-pass operator stamp); `format-b-notices/_brief-template.md` (354 lines; Stage 3.2 APPROVED 2026-05-26 with `_root/05` source fixes; the brief template you populate); `format-b-notices/_delivery-email-template.md` (157 lines; Stage 3.2 APPROVED 2026-05-26 with `_root/07 §7.5` strip-and-replace landing); `format-a-notices/lpf__linon-powell-furniture__brief.md` (137 lines; Stage 4.1 lpf APPROVED 2026-05-26; structural-discipline-only reference); `format-a-notices/lpf__linon-powell-furniture__delivery-email.md` (44 lines; Stage 4.1 lpf APPROVED 2026-05-26; structural-discipline-only reference); `format-b-notices/cci__currey-and-company__brief.md` (133 lines; Stage 4.2 cci APPROVED 2026-05-26; FIRST Format B production proof; structural reference for sca); `format-b-notices/cci__currey-and-company__delivery-email.md` (47 lines; Stage 4.2 cci APPROVED 2026-05-26; structural reference for sca); `_root/00_manifest.md §5` (canonical conformance-block format); `_root/CONTRACTS.md §2` (when in doubt — stop and surface); `_root/CONTRACTS.md §5` (path-reference contract — strict-placeholder precedent applied at Stage 4 production scope per Appendix A.5); `_root/09_changelog.md` 2026-05-26 entries: cci closeout + bri hard-stop + CL-026 + CL-023 joint resolution (sca exercises the post-resolution `_root/05 §2.4.1` IUR-as-secondary semantic for reduction-side cases via §2.1.7 templated coverage).*
