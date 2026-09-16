# v6.2 Reconciliation Log

> **What this tracker owns**: per-account ops cleanup tasks for accounts where billing-implied enabled count diverges from v6.2 `modeled_users` (per `_root/07 §4.5` reconciliation flag thresholds: `|gap_users| > 3 AND |gap_dollars| > $60`).
>
> **Discipline** (operator-stamped 2026-05-26 — Stage 4.1 `lpf` production proof finding): v6.2 modeled-canonical wins per Appendix B (`_meta/stage4_prompts/PLANNING_AGENT_HANDOFF.md`). For each row below, internal SuperCat ops cleanup is required pre-`[EFFECTIVE_DATE]` to align billing-side enabled count with v6.2 modeled (disable phantom enabled accounts in the customer's environment for Pattern 1 rows; verify operational reality for Pattern 2 rows). Brief math stands as v6.2 stamps it. **Client copy NEVER mentions "unused users," "phantom accounts," or any user-cleanup language** per `_root/04 §3` audience-discipline.
>
> **Read by**: planning agent during Stage 4 per-account sessions (verifies ops cleanup is entered for flagged accounts); CSM/Ops team (executes per-account cleanup); operator (per-account stamps when reconciliation cannot be operationally cleared by `[EFFECTIVE_DATE]` and re-routing per `_root/06` is required).
> **Owner**: CEO (via planning agent — planning agent populates rows from cohort sweep; CSM/Ops team updates `ops_status` per-account; operator stamps escalations).
> **Last updated**: 2026-05-26 (created at Stage 4.1 `lpf` production proof closeout; pre-populated with 37 flagged accounts from cohort-wide sweep against v6.2 + billing math).
> **Primary sources**: `_master-account-data-v6.2.csv` (canonical v6.2 data — operator-stamped Appendix B); `_root/07 §4.5` (reconciliation flag thresholds + resolution discipline); `_root/05 §2.1.5` (After-row canonicality); `_root/04 §4.9` (drafter-facing operational note).

---

## Sweep methodology + headline counts

Cohort sweep run 2026-05-26 across all 107 pending v6.2 rows (filter: `migration_status == 'migration_pending'`, `current_user_rate > 0`). For each row:

- `implied_billed_enabled = current_provided_users + ROUND(current_user_mrr ÷ current_user_rate)`
- `gap_users = implied_billed_enabled − modeled_users`
- `gap_dollars = current_user_mrr − MAX(modeled_users − current_provided_users, 0) × current_user_rate`
- Material gap flag: `|gap_users| > 3 AND |gap_dollars| > $60` (per `_root/07 §4.5` thresholds)
- Routing flip: `format_route(v6.2 delta) ≠ format_route(enabled-canonical delta at graduated rate ladder)` (informational only — not an operational re-route under the stamped discipline; flagged to signal HIGHER URGENCY for ops cleanup since the gap is material enough to cross a format boundary)

**Headline counts (2026-05-26 sweep)**: 37 flagged of 107 pending (34%). Pattern 1 (phantom enabled cleanup): 24. Pattern 2 (under-modeled / verify): 13. Routing flips under enabled-canonical: 14.

---

## Pattern reference

**Pattern 1 (billed_enabled > modeled)**: customer's billing-side enabled count exceeds v6.2 model. Implies phantom enabled accounts (e.g. former employees never deactivated, test/demo accounts left enabled, view-only roles incorrectly counted as billable). Ops action: verify which enabled accounts are operationally needed; disable phantoms pre-`[EFFECTIVE_DATE]`. Most common pattern.

**Pattern 2 (billed_enabled < modeled)**: customer's billing-side enabled count is lower than v6.2 model. Implies either (a) trailing-avg includes peak season (currently in trough; modeled stands), or (b) v6.2 modeled is stale (billing reduced recently; update v6.2). Ops action: verify operational reality; resolve per (a) or (b).

---

## Active accounts (37 flagged; routing-flips at top of table = highest urgency)

| ord_id | company | tier | driver | provided | active | modeled | billed | gap_u | gap_$ | pattern | v6_fmt | alt_fmt | flip? | owner | cohort | ops_status | target_date | ops_action_required |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `cst` | Coaster | T1 | user_rate_normalization | 80 | 0 | 80 | 135 | +55 | $+1100 | 1 (phantom) | Format B | CEO Letter | **YES** | Kylor + CEO | Renewal-Based | pending | pre-Renewal date (typically 2026-09-01) | Verify 55 phantom enabled account(s) (~$1100/mo billing-side) and disable pre-effective-date; reconcile billing to v6.2 modeled. |
| `rw` | RENWIL | T3 | user_count_variance | 50 | 58 | 61 | 92 | +31 | $+591 | 1 (phantom) | Good News | CEO Letter | **YES** | Kylor | Deferred | pending | pre-TBD (typically 2026-09-01) | Verify 31 phantom enabled account(s) (~$591/mo billing-side) and disable pre-effective-date; reconcile billing to v6.2 modeled. |
| `vcg` | Visual Comfort Signature | T1 | user_rate_normalization | 25 | 54 | 64 | 81 | +17 | $+306 | 1 (phantom) | Format B | CEO Letter | **YES** | Kylor | June | pending | pre-1-Jul (typically 2026-09-01) | Verify 17 phantom enabled account(s) (~$306/mo billing-side) and disable pre-effective-date; reconcile billing to v6.2 modeled. |
| `mali` | Magic Lite | T2 | module_compression | 40 | 0 | 40 | 55 | +15 | $+375 | 1 (phantom) | Good News | Format B | **YES** | Kylor + CEO | Renewal-Based | pending | pre-Renewal date (typically 2026-09-01) | Verify 15 phantom enabled account(s) (~$375/mo billing-side) and disable pre-effective-date; reconcile billing to v6.2 modeled. |
| `ufi` | Universal Furniture | T3 | user_rate_normalization | 25 | 69 | 78 | 93 | +15 | $+300 | 1 (phantom) | Format B | CEO Letter | **YES** | Kylor | June | pending | pre-1-Jul (typically 2026-09-01) | Verify 15 phantom enabled account(s) (~$300/mo billing-side) and disable pre-effective-date; reconcile billing to v6.2 modeled. |
| `mh` | Magnussen Home | T1 | user_rate_normalization | 25 | 56 | 63 | 76 | +13 | $+260 | 1 (phantom) | Format B | CEO Letter | **YES** | Kylor | June | pending | pre-1-Jul (typically 2026-09-01) | Verify 13 phantom enabled account(s) (~$260/mo billing-side) and disable pre-effective-date; reconcile billing to v6.2 modeled. |
| `mli` | Maxim Lighting | T1 | user_rate_normalization | 25 | 61 | 86 | 95 | +9 | $+162 | 1 (phantom) | Format B | CEO Letter | **YES** | Kylor | June | pending | pre-1-Jul (typically 2026-09-01) | Verify 9 phantom enabled account(s) (~$162/mo billing-side) and disable pre-effective-date; reconcile billing to v6.2 modeled. |
| `vl` | Ciana Varaluz LLC | T1 | user_rate_normalization | 25 | 33 | 44 | 53 | +9 | $+180 | 1 (phantom) | Format B | CEO Letter | **YES** | Kylor | June | pending | pre-1-Jul (typically 2026-09-01) | Verify 9 phantom enabled account(s) (~$180/mo billing-side) and disable pre-effective-date; reconcile billing to v6.2 modeled. |
| `lpf` | Linon/Powell Furniture | T3 | user_rate_normalization | 25 | 41 | 44 | 51 | +7 | $+140 | 1 (phantom) | Format A | Format B | **YES** | Kylor | June | pending | pre-1-Jul (typically 2026-09-01) | Verify 7 phantom enabled account(s) (~$140/mo billing-side) and disable pre-effective-date; reconcile billing to v6.2 modeled. |
| `jyc` | Jamie Young Company | T3 | user_count_variance | 25 | 1313 | 70 | 77 | +7 | $+140 | 1 (phantom) | Good News | Format A | **YES** | Kylor | Deferred | pending | pre-TBD (typically 2026-09-01) | Verify 7 phantom enabled account(s) (~$140/mo billing-side) and disable pre-effective-date; reconcile billing to v6.2 modeled. |
| `fms` | Visual Comfort - Studio /Fans | T1 | user_rate_normalization | 25 | 0 | 87 | 81 | -6 | $-108 | 2 (under-modeled) | CEO Letter | Format B | **YES** | Kylor | June | pending | pre-1-Jul (typically 2026-09-01) | Verify 6 user gap (billing under-counts v6.2 model by ~$108/mo). Confirm whether (a) trailing-avg includes peak season — modeled stands, OR (b) v6.2 modeled is stale — update v6.2 + re-route per `_root/06`. |
| `bcf` | Braxton Culler | T3 | at_book_tier_shift | 25 | 136 | 44 | 50 | +6 | $+120 | 1 (phantom) | Format A | Format B | **YES** | Kylor | June | pending | pre-1-Jul (typically 2026-09-01) | Verify 6 phantom enabled account(s) (~$120/mo billing-side) and disable pre-effective-date; reconcile billing to v6.2 modeled. |
| `gh` | Gabby | T3 | multi_org_retirement | 25 | 48 | 45 | 50 | +5 | $+90 | 1 (phantom) | Format B | CEO Letter | **YES** | CEO | June | pending | pre-1-Jul (typically 2026-09-01) | Verify 5 phantom enabled account(s) (~$90/mo billing-side) and disable pre-effective-date; reconcile billing to v6.2 modeled. |
| `ml` | Millennium Lighting | T1 | module_compression | 25 | 50 | 49 | 53 | +4 | $+80 | 1 (phantom) | Good News | Format A | **YES** | Kylor | Deferred | pending | pre-TBD (typically 2026-09-01) | Verify 4 phantom enabled account(s) (~$80/mo billing-side) and disable pre-effective-date; reconcile billing to v6.2 modeled. |
| `mlg` | Minka Lighting Group | T1 | rate_architecture | 25 | 54 | 66 | 25 | -41 | $-3075 | 2 (under-modeled) | Good News | Good News | no | Kylor | Renewal-Based | pending | pre-Renewal date (typically 2026-09-01) | Verify 41 user gap (billing under-counts v6.2 model by ~$3075/mo). Confirm whether (a) trailing-avg includes peak season — modeled stands, OR (b) v6.2 modeled is stale — update v6.2 + re-route per `_root/06`. |
| `gblx` | Globalux | T1 | included_user_reduction | 50 | 0 | 50 | 75 | +25 | $+625 | 1 (phantom) | CEO Letter | CEO Letter | no | Kylor | June | pending | pre-1-Jul (typically 2026-09-01) | Verify 25 phantom enabled account(s) (~$625/mo billing-side) and disable pre-effective-date; reconcile billing to v6.2 modeled. |
| `clli` | Craftmade | T3 | user_rate_normalization | 25 | 185 | 65 | 53 | -12 | $-240 | 2 (under-modeled) | CEO Letter | CEO Letter | no | Kylor | June | pending | pre-1-Jul (typically 2026-09-01) | Verify 12 user gap (billing under-counts v6.2 model by ~$240/mo). Confirm whether (a) trailing-avg includes peak season — modeled stands, OR (b) v6.2 modeled is stale — update v6.2 + re-route per `_root/06`. |
| `arl` | Arabela Lighting | T1 | included_user_reduction | 25 | 19 | 37 | 25 | -12 | $-300 | 2 (under-modeled) | CEO Letter | CEO Letter | no | Kylor + CEO | Renewal-Based | pending | pre-Renewal date (typically 2026-09-01) | Verify 12 user gap (billing under-counts v6.2 model by ~$300/mo). Confirm whether (a) trailing-avg includes peak season — modeled stands, OR (b) v6.2 modeled is stale — update v6.2 + re-route per `_root/06`. |
| `clc` | Capital Lighting Fixture Co. | T3 | user_rate_normalization | 25 | 109 | 68 | 57 | -11 | $-220 | 2 (under-modeled) | CEO Letter | CEO Letter | no | CEO + Kylor | July | pending | pre-1-Aug (typically 2026-09-01) | Verify 11 user gap (billing under-counts v6.2 model by ~$220/mo). Confirm whether (a) trailing-avg includes peak season — modeled stands, OR (b) v6.2 modeled is stale — update v6.2 + re-route per `_root/06`. |
| `wac` | WAC/Modern Forms Lighting | T1 | user_rate_normalization | 25 | 83 | 97 | 86 | -11 | $-198 | 2 (under-modeled) | CEO Letter | CEO Letter | no | Kylor | June | pending | pre-1-Jul (typically 2026-09-01) | Verify 11 user gap (billing under-counts v6.2 model by ~$198/mo). Confirm whether (a) trailing-avg includes peak season — modeled stands, OR (b) v6.2 modeled is stale — update v6.2 + re-route per `_root/06`. |
| `bri` | Bulbrite | T3 | tier_base_increase (re-stamped 2026-05-26 from included_user_reduction per CL-026 + CL-023 joint resolution; secondary_drivers = included_user_reduction post-re-stamp) | 25 | 140 | 62 | 51 | -11 | $-275 | 2 (under-modeled) | Format B | Format B | no | Kylor | June | pending | pre-1-Jul (typically 2026-09-01) | Verify 11 user gap (billing under-counts v6.2 model by ~$275/mo). Confirm whether (a) trailing-avg includes peak season — modeled stands, OR (b) v6.2 modeled is stale — update v6.2 + re-route per `_root/06`. (Reconciliation ops-cleanup workstream unchanged by 2026-05-26 driver-stamp re-stamping; primary-driver re-stamp is independent of user-billing reconciliation per CL-025 + CL-026 RESOLVED entries.) |
| `el` | Eurofase Inc. | T3 | user_rate_normalization | 25 | 66 | 82 | 73 | -9 | $-180 | 2 (under-modeled) | CEO Letter | CEO Letter | no | CEO + Kylor | July | pending | pre-1-Aug (typically 2026-09-01) | Verify 9 user gap (billing under-counts v6.2 model by ~$180/mo). Confirm whether (a) trailing-avg includes peak season — modeled stands, OR (b) v6.2 modeled is stale — update v6.2 + re-route per `_root/06`. |
| `sarreid` | Sarreid, Ltd. | T3 | user_rate_normalization | 25 | 55 | 54 | 63 | +9 | $+144 | 1 (phantom) | CEO Letter | CEO Letter | no | CEO + Kylor | July | pending | pre-1-Aug (typically 2026-09-01) | Verify 9 phantom enabled account(s) (~$144/mo billing-side) and disable pre-effective-date; reconcile billing to v6.2 modeled. |
| `all` | Accord Lighting | T1 | user_rate_normalization | 25 | 40 | 45 | 37 | -8 | $-160 | 2 (under-modeled) | CEO Letter | CEO Letter | no | Kylor + CEO | July | pending | pre-1-Aug (typically 2026-09-01) | Verify 8 user gap (billing under-counts v6.2 model by ~$160/mo). Confirm whether (a) trailing-avg includes peak season — modeled stands, OR (b) v6.2 modeled is stale — update v6.2 + re-route per `_root/06`. |
| `kl` | Coleto Brands | Kichler | T1 | user_rate_normalization | 25 | 31 | 33 | 25 | -8 | $-160 | 2 (under-modeled) | CEO Letter | CEO Letter | no | Kylor | Post-Migration | pending | pre-TBD (typically 2026-09-01) | Verify 8 user gap (billing under-counts v6.2 model by ~$160/mo). Confirm whether (a) trailing-avg includes peak season — modeled stands, OR (b) v6.2 modeled is stale — update v6.2 + re-route per `_root/06`. |
| `mlc` | Matteo Lighting | T1 | included_user_reduction | 25 | 33 | 42 | 34 | -8 | $-200 | 2 (under-modeled) | CEO Letter | CEO Letter | no | Kylor + CEO | July | pending | pre-1-Aug (typically 2026-09-01) | Verify 8 user gap (billing under-counts v6.2 model by ~$200/mo). Confirm whether (a) trailing-avg includes peak season — modeled stands, OR (b) v6.2 modeled is stale — update v6.2 + re-route per `_root/06`. |
| `eli` | Elegant Furniture & Lighting | T3 | user_rate_normalization | 25 | 44 | 71 | 64 | -7 | $-140 | 2 (under-modeled) | CEO Letter | CEO Letter | no | CEO + Kylor | July | pending | pre-1-Aug (typically 2026-09-01) | Verify 7 user gap (billing under-counts v6.2 model by ~$140/mo). Confirm whether (a) trailing-avg includes peak season — modeled stands, OR (b) v6.2 modeled is stale — update v6.2 + re-route per `_root/06`. |
| `sbl` | Schonbek Lighting | T1 | user_rate_normalization | 25 | 66 | 74 | 67 | -7 | $-126 | 2 (under-modeled) | CEO Letter | CEO Letter | no | Kylor | June | pending | pre-1-Jul (typically 2026-09-01) | Verify 7 user gap (billing under-counts v6.2 model by ~$126/mo). Confirm whether (a) trailing-avg includes peak season — modeled stands, OR (b) v6.2 modeled is stale — update v6.2 + re-route per `_root/06`. |
| `big` | Baker-McGuire | T1 | user_rate_normalization | 25 | 45 | 52 | 58 | +6 | $+120 | 1 (phantom) | CEO Letter | CEO Letter | no | CEO | Post-Migration | pending | pre-TBD (typically 2026-09-01) | Verify 6 phantom enabled account(s) (~$120/mo billing-side) and disable pre-effective-date; reconcile billing to v6.2 modeled. |
| `ta` | Theodore Alexander | T3 | tier_base_increase | 25 | 54 | 36 | 42 | +6 | $+120 | 1 (phantom) | Format B | Format B | no | Kylor | June | pending | pre-1-Jul (typically 2026-09-01) | Verify 6 phantom enabled account(s) (~$120/mo billing-side) and disable pre-effective-date; reconcile billing to v6.2 modeled. |
| `scw` | Summer Classics Retail | T3 | platform_discount_correction | 25 | 121 | 48 | 53 | +5 | $+90 | 1 (phantom) | CEO Letter | CEO Letter | no | CEO | June | pending | pre-1-Jul (typically 2026-09-01) | Verify 5 phantom enabled account(s) (~$90/mo billing-side) and disable pre-effective-date; reconcile billing to v6.2 modeled. |
| `rf` | Rowe Furniture | T1 | user_rate_normalization | 25 | 28 | 28 | 33 | +5 | $+100 | 1 (phantom) | CEO Letter | CEO Letter | no | Kylor | June | pending | pre-1-Jul (typically 2026-09-01) | Verify 5 phantom enabled account(s) (~$100/mo billing-side) and disable pre-effective-date; reconcile billing to v6.2 modeled. |
| `ril` | Ratana International Ltd. | T3 | tier_base_increase | 25 | 35 | 31 | 36 | +5 | $+125 | 1 (phantom) | Format B | Format B | no | Kylor | June | pending | pre-1-Jul (typically 2026-09-01) | Verify 5 phantom enabled account(s) (~$125/mo billing-side) and disable pre-effective-date; reconcile billing to v6.2 modeled. |
| `sbmh` | Somerset Bay and Modern History | T3 | tier_base_increase | 25 | 29 | 32 | 37 | +5 | $+100 | 1 (phantom) | Format A | Format A | no | Kylor | June | pending | pre-1-Jul (typically 2026-09-01) | Verify 5 phantom enabled account(s) (~$100/mo billing-side) and disable pre-effective-date; reconcile billing to v6.2 modeled. |
| `pf` | Palecek | T1 | module_compression | 25 | 102 | 120 | 125 | +5 | $+100 | 1 (phantom) | Good News | Good News | no | Kylor | Deferred | pending | pre-TBD (typically 2026-09-01) | Verify 5 phantom enabled account(s) (~$100/mo billing-side) and disable pre-effective-date; reconcile billing to v6.2 modeled. |
| `wag` | Wendover Art Group | T2 | platform_discount_correction | 25 | 48 | 50 | 54 | +4 | $+100 | 1 (phantom) | CEO Letter | CEO Letter | no | CEO + Kylor | July | pending | pre-1-Aug (typically 2026-09-01) | Verify 4 phantom enabled account(s) (~$100/mo billing-side) and disable pre-effective-date; reconcile billing to v6.2 modeled. |
| `sc` | Summer Classics ( Wholesale) | T3 | user_rate_normalization | 25 | 112 | 113 | 117 | +4 | $+72 | 1 (phantom) | CEO Letter | CEO Letter | no | CEO | June | pending | pre-1-Jul (typically 2026-09-01) | Verify 4 phantom enabled account(s) (~$72/mo billing-side) and disable pre-effective-date; reconcile billing to v6.2 modeled. |

---

## Ops cleanup status legend

- `pending` — initial state at row creation; no ops investigation started yet
- `in-progress` — CSM/Ops has opened investigation; verification underway with customer's SuperCat admin or via Postgres login activity
- `cleared` — billing-side enabled count now equals v6.2 modeled (Pattern 1: phantoms disabled; Pattern 2 case (a): trough confirmed, modeled stands)
- `re-modeled` — v6.2 modeled updated to match operational reality (Pattern 2 case (b): v6.2 was stale; new modeled stamped per operator)
- `escalated` — gap cannot be operationally cleared by `[EFFECTIVE_DATE]`; operator escalation per `_root/CONTRACTS.md §2`; brief may re-route per `_root/06` 6-step flow under updated v6.2 values

---

## Re-sweep cadence

This tracker is the snapshot from the 2026-05-26 cohort sweep. Re-sweep is required:

1. When v6.2 is re-stamped with material updates (add `enabled_users` column add planned; future ERP-sourced corrections; etc.) — re-run `/tmp/v6_2_reconciliation_sweep.py` against the new v6.2; reconcile this tracker's row set against the new sweep output; archive cleared rows; add newly-flagged rows.
2. Pre-bulk-production (before Stage 4 scales beyond proof gate) — confirm tracker is current; all flagged rows have `ops_status` ≠ `pending` (in-progress / cleared / re-modeled / escalated).
3. On any individual account's `effective_date` − 30 days — pre-send check: verify ops cleanup is `cleared` or `re-modeled`; if `pending` or `in-progress`, escalate per the row's `ops_status` workflow.

---

## Footer — generated 2026-05-26 by `/tmp/build_reconciliation_log.py` from cohort sweep. Total flagged: 37 / 107 pending (35%).
