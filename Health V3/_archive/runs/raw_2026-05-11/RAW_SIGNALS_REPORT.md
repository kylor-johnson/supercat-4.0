# Health V3 — Raw Signal Distribution Report
**Score date:** 2026-05-11 · **Population:** 104 / 104 MAL orgs (no exclusions)
**Cache:** `Health V3/cache/2026-05-11/` · **MAL:** `Health V2/inputs/master_account_list_2026-04-14_canonical.csv`
**Extractor:** `Health V3/raw_signals_extractor.py`
**Outputs in this folder:**
- `raw_signals_2026-05-11.csv` — one row per org, 43 columns of raw signal values
- `distribution_summary.csv` — quantiles for the 7 distribution-summary signals
- `aux_stats.csv` — the auxiliary % statistics
- `_compact_table.md` — same as raw CSV but rendered as markdown (sorted by ARR)

This run is intentionally a **non-banded, non-composite, non-weighted** read of the same cache the canonical V3 operator used today. Use it to evaluate whether the band breakpoints in `health_operator_v3.py` are placed at natural data breaks.

> **Methodology notes**
> - Pure cache read; no live DB connections.
> - `active_user_ratio` reproduces the operator's denominator-fallback (`enabled_users → active_users_365d` when `enabled_users = 0`), but is **uncapped** (the operator caps at 1.0 before banding; here you can see the raw stale-denominator excess, e.g. `soi` at 1.50, `mlc` at 1.11). `denom_fallback_applied` flags rows that used the fallback.
> - `days_since_last_login` is computed against `datetime.utcnow()` at extractor runtime — same idiom the operator uses. The cache snapshot was taken 2026-05-11 ~17:18 UTC, so 0 days simply means "the org logged in today".
> - `feat_*` columns: **1** = applicable and used, **0** = applicable but not used, **-1** = not applicable (config flag off). `features_applicable` / `features_used` count only the 0/1 cells.
> - `channels_*` follow the operator's value-delivery applicability gates (`eoc / eoo / esp / inv_in_history`) and use the *same* thresholds (`ipad_orders_90d >= 50`, `mp_share >= 3`, `portal_orders > 0`, `inv_runs_90d > 0`). These are not raw, but they are uncompressed: counts of applicable vs achieved, not a score.
> - Freshness applies the operator's `runs >= 3` + initial-load carve-out gating, but **the ratio itself is the raw `days_since_last / mean_gap`** — no banding. 3 orgs (`tel`, `ol`, `dals`) had zero measurable feeds (no imports with ≥ 3 runs in 180d).

---

## 1. Per-org raw signals (all 104 orgs, sorted by ARR desc)

Wide-form raw signals. Identification, engagement, adoption summary, value delivery, operational health, freshness. The full 43-column matrix (including individual `feat_*` flags, `enabled_users`, `active_users_365d`, `denom_fallback_applied`, ghost/new-org flags, config flags) is in `raw_signals_2026-05-11.csv`.

| org_shortname | bundle | arr | logins_90d | active_user_ratio | days_since_last_login | features_applicable | features_used | channels_applicable | channels_achieved | ipad_orders_90d | portal_orders_90d | mp_share_events_90d | catalog_pct | freshness_avg_staleness_ratio | freshness_worst_ratio | import_types_active | import_types_healthy |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| wwjc | Full (Cart+Portal) | $40,340 | 2907 | 0 | 0 | 8 | 8 | 6 | 6 | 287 | 4158 | 218 | 0.9966 | 0.764 | 1.575 | 9 | 9 |
| pf | iPad+Catalog | $39,009 | 6253 | 0.66 | 0 | 6 | 6 | 4 | 4 | 752 | 1636 | 444 | 1 | 1.546 | 4.795 | 10 | 10 |
| scw | Full (Cart+Portal) | $38,779 | 7444 | 0.01 | 0 | 8 | 8 | 6 | 6 | 3189 | 6566 | 993 | 0.7044 | 1.144 | 5.829 | 15 | 15 |
| hfg | iPad+Catalog+Portal | $36,300 | 4126 | 0.5 | 0 | 6 | 6 | 4 | 4 | 525 | 5518 | 141 | 0.9427 | 8.435 | 27.348 | 9 | 8 |
| jyc | Full (Cart+Portal) | $35,400 | 2582 | 0 | 0 | 8 | 8 | 6 | 6 | 1083 | 522 | 86 | 1 | 1.418 | 4.962 | 9 | 6 |
| el | iPad+Catalog+Portal | $33,095 | 2136 | 0.32 | 0 | 7 | 7 | 5 | 4 | 45 | 544 | 140 | 0.2593 | 16.823 | 140.499 | 9 | 9 |
| bri | Full (Cart+Portal) | $31,445 | 946 | 0.05 | 0 | 8 | 8 | 6 | 6 | 71 | 30039 | 31 | 0.9676 | 10.178 | 45.131 | 11 | 9 |
| clm | iPad+Catalog+Portal | $30,480 | 1990 | 0.09 | 0 | 7 | 7 | 5 | 4 | 45 | 19825 | 138 | 1 | 3.601 | 28.371 | 9 | 8 |
| kal | Full (Cart+Portal) | $29,045 | 1235 | 0.03 | 0 | 8 | 8 | 6 | 5 | 30 | 2628 | 69 | 0.9238 | 1.074 | 1.966 | 7 | 6 |
| clli | iPad+Catalog+Portal | $28,740 | 2221 | 0.03 | 0 | 7 | 6 | 5 | 4 | 18 | 40962 | 116 | 0.9318 | 5.047 | 31.361 | 7 | 7 |
| clc | Full (Cart+Portal) | $28,059 | 1837 | 0.06 | 0 | 8 | 7 | 6 | 4 | 44 | 30987 | 112 | 1 | 31.768 | 147.714 | 9 | 8 |
| sarreid | iPad+Catalog+Portal | $27,968 | 6004 | 0.56 | 0 | 7 | 7 | 5 | 5 | 164 | 2920 | 221 | 0.9296 | 1.64 | 6.607 | 10 | 10 |
| ril | Full (Cart+Portal) | $27,025 | 990 | 0.17 | 0 | 8 | 8 | 6 | 6 | 326 | 1161 | 34 | 0.9823 | 1.966 | 2.827 | 6 | 6 |
| kll | Full (Cart+Portal) | $26,780 | 1761 | 0.06 | 0 | 8 | 7 | 6 | 5 | 9 | 31794 | 44 | 0.9706 | 30.984 | 122.04 | 7 | 6 |
| eli | iPad+Catalog+Cart | $26,570 | 2040 | 0.04 | 0 | 7 | 4 | 5 | 3 | 64 | 0 | 298 | 0.9418 | 3.451 | 11.211 | 4 | 3 |
| cci | iPad+Catalog+Portal | $26,480 | 2454 | 0.58 | 0 | 7 | 7 | 5 | 5 | 1030 | 15251 | 158 | 0.9312 | 1.941 | 9.235 | 9 | 6 |
| bcf | Full (Cart+Portal) | $26,340 | 3634 | 0.04 | 0 | 8 | 8 | 6 | 6 | 417 | 1474 | 237 | 0.8184 | 0.621 | 2.583 | 13 | 13 |
| lpf | Full (Cart+Portal) | $26,079 | 3088 | 0.02 | 0 | 8 | 7 | 6 | 6 | 255 | 15685 | 162 | 0.9916 | 3.962 | 28.371 | 8 | 7 |
| sbmh | Full (Cart+Portal) | $26,079 | 2266 | 0.01 | 0 | 8 | 8 | 6 | 6 | 523 | 1337 | 600 | 0.9749 | 0.703 | 2.198 | 6 | 5 |
| shl | Full (Cart+Portal) | $25,700 | 2091 | 0.02 | 0 | 8 | 8 | 6 | 5 | 8 | 51293 | 89 | 0.9874 | 2.762 | 7.827 | 9 | 4 |
| asi | Full (Cart+Portal) | $25,684 | 1796 | 0.12 | 0 | 7 | 7 | 5 | 5 | 1287 | 590 | 3 | 0.6539 | 1.121 | 4.733 | 7 | 7 |
| ufi | iPad+Catalog+Portal | $25,475 | 6957 | 0.8 | 0 | 6 | 6 | 4 | 4 | 610 | 15311 | 591 | 1 | 0.864 | 2.24 | 7 | 7 |
| rw | iPad+Catalog+Portal | $25,374 | 2592 | 0.73 | 0 | 7 | 4 | 5 | 3 | 2337 | 0 | 215 | 0.9994 | 2.614 | 8.236 | 6 | 6 |
| prog | iPad-only | $25,200 | 290 | 0.28 | 0 | 3 | 2 | 2 | 1 | 4 | 0 | 7 | 0.9772 | 51.17 | 89.412 | 4 | 3 |
| sc | iPad+Catalog+Portal | $24,936 | 15719 | 0.86 | 0 | 7 | 7 | 5 | 5 | 8092 | 3940 | 402 | 0.6162 | 2.074 | 7.743 | 13 | 13 |
| gh | Full (Cart+Portal) | $24,336 | 6246 | 0.01 | 0 | 8 | 8 | 6 | 6 | 2550 | 6812 | 814 | 0.5965 | 0.87 | 4.846 | 14 | 14 |
| gl | Full (Cart+Portal) | $24,309 | 486 | 0.05 | 0 | 8 | 7 | 6 | 5 | 5 | 2558 | 42 | 0.993 | 1.463 | 7.799 | 7 | 6 |
| ta | Full (Cart+Portal) | $24,260 | 2997 | 0.09 | 0 | 8 | 8 | 6 | 6 | 478 | 1056 | 246 | 0.9981 | 3.785 | 11.245 | 8 | 8 |
| fc | Full (Cart+Portal) | $24,099 | 1914 | 0 | 0 | 8 | 8 | 6 | 6 | 452 | 724 | 115 | 0.2845 | 8.478 | 32.819 | 8 | 7 |
| jc | iPad+Catalog+Portal | $24,029 | 299 | 0.23 | 3 | 7 | 7 | 5 | 4 | 12 | 72 | 10 | 0.915 | 0.947 | 1.347 | 12 | 12 |
| fsf | Full (Cart+Portal) | $22,560 | 1501 | 0.03 | 0 | 8 | 8 | 6 | 6 | 255 | 1656 | 103 | 0.9245 | 4.107 | 24.514 | 9 | 9 |
| ih | iPad+Catalog+Portal | $22,140 | 3587 | 0.89 | 0 | 7 | 7 | 5 | 5 | 720 | 1707 | 89 | 0.9576 | 0.968 | 3.505 | 9 | 9 |
| wac | iPad-only | $22,104 | 3127 | 0.59 | 0 | 5 | 5 | 3 | 3 | 857 | 0 | 83 | 0.9996 | 21.877 | 113.391 | 6 | 5 |
| dccl | iPad+Catalog+Cart | $22,038 | 551 | 0.09 | 0 | 7 | 5 | 5 | 3 | 73 | 0 | 294 | 0.8544 | 9.548 | 36.208 | 7 | 4 |
| sccon | Full (Cart+Portal) | $21,819 | 2414 | 0.03 | 0 | 7 | 7 | 6 | 6 | 2330 | 975 | 118 | 0.7317 | 0.796 | 4.361 | 15 | 15 |
| vic | Full (Cart+Portal) | $21,780 | 333 | 0.06 | 0 | 8 | 7 | 6 | 5 | 0 | 13263 | 26 | 0.9901 | 1.425 | 4.869 | 7 | 6 |
| ali | iPad+Catalog+Portal | $21,680 | 717 | 0.19 | 0 | 7 | 6 | 5 | 4 | 0 | 7174 | 120 | 1 | 2.27 | 6.697 | 6 | 5 |
| cfg | iPad+Catalog+Cart | $21,066 | 1351 | 0.02 | 0 | 5 | 3 | 4 | 2 | 68 | 0 | 86 | 0.9409 | 5.685 | 13.528 | 6 | 6 |
| ihw | iPad+Catalog+Portal | $20,730 | 3449 | 0.84 | 0 | 7 | 7 | 5 | 5 | 483 | 356 | 37 | 0.835 | 0.943 | 3.7 | 14 | 12 |
| mli | iPad-only | $19,236 | 4505 | 0.85 | 0 | 5 | 5 | 3 | 2 | 10 | 0 | 356 | 0.6614 | 26.199 | 95.178 | 6 | 6 |
| big | iPad-only | $18,729 | 1767 | 0.87 | 0 | 5 | 3 | 3 | 1 | 3 | 0 | 155 | 0.7109 | 0.892 | 3.823 | 7 | 7 |
| ah | iPad+Catalog+Cart | $18,560 | 1317 | 0.02 | 0 | 7 | 4 | 5 | 3 | 185 | 0 | 308 | 0.9931 | 0.991 | 2.549 | 5 | 5 |
| vcg | iPad-only | $18,455 | 3458 | 0.49 | 0 | 5 | 5 | 3 | 3 | 50 | 0 | 102 | 0.9569 | 11.767 | 53.337 | 7 | 3 |
| ml | iPad+Catalog | $17,979 | 1627 | 0.46 | 0 | 6 | 4 | 4 | 2 | 2 | 0 | 59 | 0.9769 | 3.998 | 9.604 | 3 | 3 |
| fal | iPad-only | $17,840 | 1876 | 0.85 | 0 | 4 | 3 | 2 | 2 | 630 | 0 | 131 | 0.9833 | 7.231 | 32.33 | 5 | 4 |
| sbl | iPad-only | $17,624 | 1400 | 0.63 | 0 | 5 | 5 | 3 | 3 | 87 | 0 | 52 | 0.9983 | 39.348 | 140.523 | 6 | 2 |
| mh | iPad-only | $17,420 | 4446 | 0.82 | 0 | 4 | 4 | 2 | 2 | 65 | 0 | 683 | 0.9721 | 5.001 | 16.148 | 8 | 5 |
| gc | iPad+Catalog+Cart | $16,980 | 782 | 0.05 | 0 | 7 | 4 | 5 | 3 | 244 | 0 | 355 | 0.9888 | 6.678 | 32.382 | 5 | 4 |
| mlg | iPad-only | $16,687 | 1644 | 0.69 | 0 | 5 | 5 | 3 | 2 | 17 | 0 | 154 | 0.9922 | 2.14 | 6.342 | 5 | 2 |
| kii | iPad+Catalog+Cart | $16,642 | 1063 | 0.21 | 0 | 7 | 5 | 5 | 3 | 645 | 0 | 38 | 0.7167 | 3.034 | 9.869 | 7 | 3 |
| mah | iPad+Catalog+Cart | $16,642 | 229 | 0.04 | 0 | 7 | 5 | 5 | 2 | 151 | 0 | 2 | 0.6853 | 2.786 | 16.139 | 7 | 5 |
| gblx | iPad-only | $16,200 | 356 | 0.61 | 0 | 4 | 3 | 3 | 2 | 0 | 0 | 20 | 1 | 31.062 | 103.159 | 4 | 3 |
| wag | iPad-only | $16,087 | 1823 | 0.6 | 0 | 4 | 4 | 2 | 2 | 835 | 0 | 50 | 0.974 | 1.168 | 2.531 | 4 | 1 |
| fms | iPad-only | $15,439 | 3921 | 0.45 | 0 | 5 | 5 | 3 | 3 | 168 | 0 | 163 | 0.8766 | 13.432 | 77.907 | 6 | 2 |
| mpc | iPad+Catalog+Cart | $15,282 | 1983 | 0.06 | 0 | 5 | 3 | 4 | 2 | 1237 | 0 | 56 | 0.9897 | 1.626 | 3.24 | 4 | 4 |
| bp | iPad-only | $15,279 | 683 | 0.46 | 0 | 7 | 4 | 5 | 2 | 4 | 0 | 3 | 0.7924 | 1.244 | 4.091 | 5 | 4 |
| tam | iPad-only | $14,060 | 1020 | 0.52 | 0 | 5 | 3 | 3 | 3 | 103 | 0 | 50 | 0.9955 | 0.218 | 0.32 | 6 | 6 |
| tla | iPad-only | $13,567 | 2288 | 0.43 | 0 | 5 | 5 | 3 | 2 | 21 | 0 | 63 | 0.2626 | 13.433 | 77.908 | 6 | 3 |
| tel | iPad+Catalog | $13,440 | 12 | 0.1 | 67 | 4 | 1 | 3 | 0 | 0 | 0 | 0 | 0.1966 |  |  | 0 | 0 |
| mfc | iPad+Catalog | $13,440 | 116 | 0.02 | 3 | 5 | 3 | 3 | 1 | 0 | 0 | 25 | 0.2867 | 3.64 | 3.903 | 2 | 2 |
| ol | iPad-only | $13,380 | 40 | 0.38 | 0 | 4 | 2 | 2 | 0 | 21 | 0 | 0 | 0.9988 |  |  | 0 | 0 |
| all | iPad-only | $12,920 | 600 | 0.69 | 0 | 4 | 3 | 2 | 1 | 3 | 0 | 26 | 0.0248 | 59.987 | 118.338 | 2 | 2 |
| mlc | iPad-only | $12,675 | 629 | 1.11 | 0 | 5 | 4 | 3 | 2 | 20 | 0 | 19 | 0.9985 | 16.188 | 42.564 | 3 | 3 |
| vl | iPad+Catalog+Portal | $11,420 | 1011 | 0.71 | 0 | 6 | 6 | 5 | 4 | 26 | 567 | 58 | 0.9975 | 32.284 | 140.524 | 6 | 4 |
| yw | iPad-only | $11,385 | 709 | 0.9 | 0 | 4 | 2 | 2 | 1 | 20 | 0 | 52 | 0.6036 | 1.296 | 1.57 | 6 | 5 |
| am | iPad-only | $11,082 | 345 | 0.85 | 0 | 4 | 3 | 2 | 1 | 23 | 0 | 31 | 0.9437 | 1.162 | 1.162 | 2 | 2 |
| ap | iPad+Catalog+Cart | $11,040 | 383 | 0.01 | 0 | 6 | 4 | 5 | 2 | 0 | 0 | 16 | 0.7936 | 2.372 | 7.343 | 6 | 5 |
| hf | iPad-only | $10,365 | 600 | 0.37 | 0 | 5 | 4 | 3 | 2 | 1 | 0 | 42 | 0.8888 | 1.736 | 4.657 | 4 | 2 |
| eglo | iPad-only | $10,340 | 620 | 0.69 | 0 | 5 | 5 | 3 | 2 | 11 | 0 | 25 | 0.9626 | 26.833 | 130.099 | 5 | 2 |
| gcl | iPad-only | $9,864 | 314 | 0.66 | 0 | 4 | 2 | 2 | 2 | 76 | 0 | 7 | 0.8686 | 1.868 | 3.845 | 6 | 6 |
| jcusa | iPad-only | $9,670 | 753 | 0.01 | 0 | 8 | 7 | 6 | 6 | 101 | 684 | 24 | 1 | 3.449 | 14.744 | 7 | 7 |
| df | iPad-only | $9,560 | 237 | 0.6 | 0 | 5 | 4 | 3 | 2 | 2 | 0 | 5 | 0.9933 | 0.498 | 0.498 | 4 | 3 |
| kkc | iPad-only | $9,540 | 230 | 0.33 | 0 | 4 | 3 | 2 | 1 | 0 | 0 | 7 | 0.9961 | 19.205 | 19.244 | 3 | 3 |
| da | iPad-only | $9,399 | 1618 | 0.65 | 0 | 5 | 5 | 3 | 3 | 1124 | 0 | 88 | 0.999 | 1.66 | 4.94 | 5 | 2 |
| kl | iPad-only | $9,360 | 400 | 0.32 | 0 | 3 | 3 | 2 | 0 | 5 | 0 | 1 | 0.905 | 63.514 | 107.649 | 3 | 3 |
| rf | iPad-only | $9,300 | 1544 | 0.65 | 0 | 4 | 3 | 2 | 1 | 16 | 0 | 229 | 0.8116 | 5.999 | 18.31 | 4 | 2 |
| afx | iPad-only | $9,150 | 215 | 0.39 | 0 | 5 | 4 | 3 | 1 | 0 | 0 | 1 | 0.9529 | 2.026 | 5.081 | 5 | 4 |
| heb | iPad-only | $9,140 | 493 | 0.3 | 0 | 5 | 4 | 3 | 2 | 32 | 0 | 48 | 0.9954 | 18.784 | 51.025 | 6 | 6 |
| gsa | iPad-only | $8,799 | 493 | 0.42 | 0 | 4 | 4 | 3 | 2 | 5 | 0 | 81 | 0.7067 | 1.188 | 2.505 | 5 | 5 |
| uhc | iPad-only | $8,739 | 1705 | 0.95 | 0 | 5 | 4 | 3 | 2 | 894 | 0 | 2 | 0.9847 | 1.294 | 3.479 | 3 | 3 |
| abol | iPad-only | $8,700 | 67 | 0.29 | 4 | 6 | 4 | 4 | 2 | 0 | 0 | 11 | 0.9109 | 0.733 | 1.747 | 3 | 2 |
| sca | iPad-only | $8,700 | 365 | 0.65 | 0 | 4 | 3 | 2 | 2 | 95 | 0 | 7 | 0.9894 | 3.162 | 4.085 | 2 | 2 |
| swc | iPad-only | $8,700 | 168 | 0.39 | 0 | 4 | 4 | 3 | 2 | 0 | 0 | 15 | 0.9781 | 0.718 | 0.72 | 4 | 4 |
| dals | iPad-only | $8,700 | 126 | 0.18 | 0 | 4 | 3 | 2 | 1 | 0 | 0 | 6 | 0.3348 |  |  | 1 | 0 |
| krb | iPad-only | $8,700 | 9 | 0.06 | 0 | 4 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 18.514 | 18.514 | 3 | 3 |
| etl | iPad-only | $8,700 | 907 | 0.88 | 0 | 4 | 4 | 3 | 3 | 142 | 0 | 15 | 0.963 | 3.906 | 11.412 | 5 | 5 |
| soi | iPad-only | $8,700 | 227 | 1.5 | 0 | 4 | 2 | 2 | 1 | 0 | 0 | 3 | 0.9682 | 3.215 | 5.252 | 2 | 2 |
| lss | iPad-only | $8,700 | 298 | 0.58 | 0 | 5 | 4 | 3 | 3 | 68 | 0 | 75 | 0.9329 | 3.584 | 6.989 | 5 | 4 |
| ihm | iPad-only | $8,403 | 80 | 0.95 | 0 | 5 | 2 | 3 | 1 | 0 | 0 | 3 | 1 | 4.295 | 7.408 | 4 | 4 |
| hmjc | iPad-only | $7,908 | 10 | 0.03 | 7 | 5 | 3 | 3 | 1 | 0 | 0 | 0 | 0.8718 | 91.271 | 140.52 | 4 | 4 |
| arl | iPad-only | $7,830 | 774 | 0.81 | 0 | 5 | 2 | 3 | 2 | 120 | 0 | 40 | 1 | 94.504 | 133.041 | 4 | 4 |
| eglo_can | iPad-only | $7,830 | 454 | 0.89 | 0 | 5 | 5 | 3 | 1 | 9 | 0 | 2 | 0.9994 | 37.99 | 95.748 | 5 | 3 |
| cf | iPad-only | $7,830 | 44 | 0.1 | 6 | 4 | 4 | 3 | 1 | 0 | 0 | 2 | 0.9398 | 64.01 | 77.701 | 4 | 4 |
| vce | iPad-only | $7,830 | 514 | 0.83 | 0 | 5 | 5 | 3 | 2 | 16 | 0 | 42 | 0.6093 | 1.187 | 2.745 | 6 | 5 |
| hh | iPad-only | $7,830 | 17 | 0.07 | 3 | 4 | 3 | 3 | 1 | 0 | 0 | 0 | 0.7877 | 76.866 | 140.54 | 4 | 3 |
| luc | iPad-only | $7,830 | 68 | 0.52 | 6 | 5 | 3 | 3 | 1 | 0 | 0 | 16 | 0.9984 | 66.945 | 106.366 | 3 | 2 |
| sp | iPad-only | $6,960 | 282 | 0.46 | 0 | 3 | 1 | 2 | 1 | 123 | 0 | 0 | 0.7863 | 5.263 | 18.102 | 7 | 5 |
| bsc | iPad-only | $6,960 | 313 | 0.58 | 0 | 5 | 5 | 3 | 2 | 9 | 0 | 6 | 0.9905 | 6.218 | 28.935 | 6 | 5 |
| st | iPad+Catalog | $6,960 | 7 | 0.05 | 4 | 5 | 2 | 3 | 0 | 0 | 0 | 0 | 0.9822 | 1.456 | 2.561 | 2 | 2 |
| hvl | iPad-only | $5,405 | 380 | 0.22 | 0 | 4 | 3 | 2 | 0 | 0 | 0 | 2 | 0.919 | 117.248 | 117.248 | 2 | 2 |
| rac | iPad-only | $4,539 | 647 | 0.57 | 0 | 4 | 4 | 3 | 3 | 123 | 0 | 52 | 0.9618 | 47.572 | 140.531 | 3 | 3 |
| pw | iPad-only | $4,500 | 89 | 0.27 | 0 | 4 | 3 | 3 | 1 | 0 | 0 | 0 | 0.8076 | 47.561 | 140.499 | 4 | 4 |
| ssi | iPad-only | $4,500 | 128 | 0.37 | 0 | 4 | 4 | 3 | 2 | 0 | 0 | 3 | 0.8838 | 5.004 | 12.838 | 3 | 3 |
| tl | iPad-only | $4,392 | 219 | 0.2 | 0 | 4 | 3 | 2 | 0 | 0 | 0 | 1 | 0.2237 | 0.519 | 0.519 | 2 | 2 |

> Flags: **0 orgs** flagged `ghost_account` (no org has ARR ≥ $5K *and* `logins_90d = 0` — there are no zero-login orgs in the 2026-05-11 cache at all). **0 orgs** flagged `new_org_excluded` (all 104 MAL orgs have first_login_at ≥ 90 days ago).

---

## 2. Distribution summary

### 2.1 Quantiles for the seven anchor signals

| Signal | n | Min | 10th pct | 25th pct | Median | 75th pct | 90th pct | Max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| logins_90d | 104 | 7 | 97 | 314 | 927 | 2,102 | 3,620 | 15,719 |
| active_user_ratio (uncapped) | 104 | 0.00 | 0.02 | 0.06 | 0.37 | 0.65 | 0.85 | 1.50 |
| days_since_last_login | 104 | 0 | 0 | 0 | 0 | 0 | 0 | 67 |
| catalog_pct | 104 | 0.000 | 0.605 | 0.811 | 0.957 | 0.993 | 1.000 | 1.000 |
| freshness_avg_staleness_ratio | 101 | 0.22 | 0.87 | 1.30 | 3.45 | 13.43 | 47.56 | 117.25 |
| features_used / features_applicable | 104 | 0.25 | 0.57 | 0.70 | 0.875 | 1.00 | 1.00 | 1.00 |
| channels_achieved / channels_applicable | 104 | 0.00 | 0.33 | 0.50 | 0.67 | 1.00 | 1.00 | 1.00 |

### 2.2 Auxiliary % statistics

| Metric | Value | Denominator |
|---|---:|---:|
| % orgs with `logins_90d = 0` | **0.0 %** | 104 |
| % orgs with `ipad_orders_90d = 0` | **22.1 %** | 104 |
| % portal-configured orgs with `portal_orders_90d = 0` | **31.4 %** | 51 portal-configured |
| % orgs with `catalog_pct ≥ 0.85` | **72.1 %** | 104 |
| % orgs with at least one import error (last run) | **50.0 %** | 102 with any imports |

> Portal-configured = `enable_online_catalog OR enable_online_ordering OR enable_sales_portal`. 51 of 104 orgs have at least one of these flags set.

---

## 3. How current bands land on the raw distribution

The user's stated reason for this run is to evaluate where current band breakpoints fall on the actual data. The bands below are pulled verbatim from `health_operator_v3.py` (`LOGIN_BANDS`, `RATIO_BANDS`, `RECENCY_BANDS`, `CATALOG_LADDER`, `FRESHNESS_BANDS`). The org counts are computed from the raw signal column.

### 3.1 `logins_90d` (LOGIN_BANDS)
| Band | Range | Score | Orgs | % |
|---|---|---:|---:|---:|
| 1 | ≥ 3,000 | 100 | 16 | 15.4 % |
| 2 | 1,000–2,999 | 88 | 34 | 32.7 % |
| 3 | 500–999 | 75 | 16 | 15.4 % |
| 4 | 200–499 | 60 | 23 | 22.1 % |
| 5 | 50–199 | 40 | 8 | 7.7 % |
| 6 | 1–49 | 20 | 7 | 6.7 % |
| 7 | 0 | 0 | 0 | 0.0 % |

> **Reads cleanly.** The bottom 25 % of the distribution (≤ 314 logins) lives in three bands (60/40/20). The "0 logins" floor never fires — so the band itself is doing zero work today; what does the work is the §5.1 ghost override (logins_90d = 0 AND arr ≥ $5K). Worth noting: the spread between p75 (2,102) and max (15,719) is ~7.5× and is compressed into a single band (≥ 3,000 → 100). `sc` at 15,719 logins gets the same score as `gh` at 6,246 and `pf` at 6,253.

### 3.2 `active_user_ratio` (RATIO_BANDS, capped at 1.0 before banding)
| Band | Range | Score | Orgs | % |
|---|---|---:|---:|---:|
| 1 | ≥ 0.90 | 100 | 5 | 4.8 % |
| 2 | 0.75–0.89 | 82 | 13 | 12.5 % |
| 3 | 0.50–0.74 | 65 | 23 | 22.1 % |
| 4 | 0.25–0.49 | 45 | 19 | 18.3 % |
| 5 | 0.01–0.24 | 20 | 41 | 39.4 % |
| 6 | 0.00 | 0 | 3 | 2.9 % |

> **Severe pile-up in band 5.** 39 % of orgs fall into the 0.01–0.24 bucket — they all score 20 regardless of whether the ratio is 0.01 or 0.24. p10 = 0.02 and p25 = 0.06 both score 20. The 0.25 breakpoint is doing almost all the work in this signal; the 0.50 / 0.75 / 0.90 breakpoints only differentiate the top ~18 %. This is the strongest case in the dataset for revisiting bands or moving to a continuous score.
> The uncapped tail (`mlc 1.11`, `soi 1.50`) flags stale denominators (more 90d-active users than currently-enabled users), which the operator labels `denominator_quality = "stale"`.

### 3.3 `days_since_last_login` (RECENCY_BANDS)
| Band | Range | Score | Orgs |
|---|---|---:|---:|
| 1 | ≤ 7 | 90 | 103 |
| 2 | 8–30 | 60 | 0 |
| 3 | 31–90 | 30 | 1 |
| 4 | > 90 | 0 | 0 |

> **Band is non-discriminating on this population.** 103 of 104 orgs scored 90; one (`tel`, 67 days) scored 30. Recency contributes ~30 points × `1/3` weight to engagement on `tel` — a real penalty — but for every other org the band is a near-tautology. Reasonable case for either dropping recency from the composite or moving to a finer-grained recency signal (e.g. "% of weekdays with ≥ 1 login in last 30").

### 3.4 `catalog_pct` (CATALOG_LADDER)
| Band | Range | Score | Orgs | % |
|---|---|---:|---:|---:|
| 1 | ≥ 0.95 | 100 | 54 | 51.9 % |
| 2 | 0.85–0.949 | 85 | 21 | 20.2 % |
| 3 | 0.70–0.849 | 65 | 13 | 12.5 % |
| 4 | 0.50–0.699 | 40 | 7 | 6.7 % |
| 5 | 0.25–0.499 | 20 | 5 | 4.8 % |
| 6 | 0–0.249 | 0 | 4 | 3.8 % |

> **Bands match the data shape reasonably well.** 72 % at ≥ 0.85 matches the published intent of "thriving = mostly-complete catalogs". The bottom four orgs (`krb 0`, `all 0.025`, `tel 0.197`, `tl 0.224`) and `el 0.259` / `tla 0.263` are the genuine catalog-broken accounts — worth surfacing as a watch-list separate from the composite.

### 3.5 `freshness_avg_staleness_ratio` (FRESHNESS_BANDS)
| Band | Range | Score | Orgs | % |
|---|---|---:|---:|---:|
| 1 | ≤ 1.0 | 100 | 16 | 15.4 % |
| 2 | 1.0–1.5 | 80 | 14 | 13.5 % |
| 3 | 1.5–2.5 | 50 | 13 | 12.5 % |
| 4 | 2.5–4.0 | 20 | 15 | 14.4 % |
| 5 | > 4.0 | 0 | 43 | 41.3 % |
| — | no measurable feeds | n/a | 3 | 2.9 % |

> **Most-broken band.** 41 % of orgs are pinned at 0 (ratio > 4.0). Inside that group there is a 30× spread (4.1 → 117.2) and **the band cannot distinguish a 4.5-ratio org (one feed mildly stale) from a 117-ratio org (`hvl`, products feed completely abandoned)**. The current ladder under-resolves the *bad* tail — exactly the opposite of what a health signal should do.
>
> Suggested re-cut (or move to log-scaled): keep ≤ 1.0 → 100 and 1.0–1.5 → 80, but split everything above 4.0 into bands at, say, 6, 15, 40, > 40, so the 47-ratio (`pw`, `rac`) and 117-ratio (`hvl`) orgs aren't lumped with the 4.5-ratio orgs.

### 3.6 Adoption breadth (`features_used / features_applicable`)
| Threshold | Orgs at or above | % |
|---|---:|---:|
| = 1.0 (every applicable feature used) | 48 | 46.2 % |
| ≥ 0.85 | 56 | 53.8 % |
| ≥ 0.70 | 78 | 75.0 % |
| ≥ 0.50 | 99 | 95.2 % |
| ≥ 0.25 | 104 | 100 % |

`features_applicable` distribution (how wide is each org's applicability surface):
| applicable | n orgs |
|---:|---:|
| 3 | 3 |
| 4 | 26 |
| 5 | 29 |
| 6 | 7 |
| 7 | 20 |
| 8 | 19 |

> **Adoption breadth has the cleanest natural break: 1.0 vs. < 1.0.** 46 % of orgs use 100 % of applicable features. The signal could collapse to a binary "complete vs. has-a-gap" with very little information loss. The orgs with `features_applicable = 3` are also worth flagging — `prog`, `sp`, `kl` — they're the smallest applicability surfaces (3 features) so any band-based adoption score is computed over very small numerators.

### 3.7 Value delivery (`channels_achieved / channels_applicable`)
| Threshold | Orgs at or above | % |
|---|---:|---:|
| = 1.0 (all channels hit) | 37 | 35.6 % |
| ≥ 0.85 | 37 | 35.6 % |
| ≥ 0.70 | 48 | 46.2 % |
| ≥ 0.50 | 84 | 80.8 % |
| ≥ 0.25 | 97 | 93.3 % |
| = 0 (none hit) | 7 | 6.7 % |

`channels_applicable` distribution:
| applicable | n orgs |
|---:|---:|
| 2 | 19 |
| 3 | 37 |
| 4 | 7 |
| 5 | 21 |
| 6 | 20 |

> **Useful raw column: `channels_achieved = 0`** — 7 orgs (`tel`, `ol`, `krb`, `kl`, `hvl`, `st`, `tl`) deliver zero value across every applicable channel. That's the single most actionable subset in this dataset and currently it does not have a dedicated flag in the operator output. Worth promoting to a top-level health flag.

---

## 4. Notable outliers (for sanity-checking the raw read)

### 4.1 Highest `freshness_avg_staleness_ratio`
| org | feeds_scored | avg_ratio | worst_feed | worst_ratio |
|---|---:|---:|---|---:|
| hvl | 1 | 117.25 | Products | 117.25 |
| arl | 3 | 94.50 | Product Stories | 133.04 |
| hmjc | 4 | 91.27 | Customers | 140.52 |
| hh | 4 | 76.87 | Customers | 140.54 |
| luc | 2 | 66.95 | Images | 106.37 |

### 4.2 Lowest adoption breadth
| org | applicable | used | ratio | logins_90d | arr |
|---|---:|---:|---:|---:|---:|
| tel | 4 | 1 | 0.25 | 12 | $13,440 |
| sp | 3 | 1 | 0.33 | 282 | $6,960 |
| ihm | 5 | 2 | 0.40 | 80 | $8,403 |
| arl | 5 | 2 | 0.40 | 774 | $7,830 |
| st | 5 | 2 | 0.40 | 7 | $6,960 |
| yw | 4 | 2 | 0.50 | 709 | $11,385 |
| ol | 4 | 2 | 0.50 | 40 | $13,380 |
| soi | 4 | 2 | 0.50 | 227 | $8,700 |

### 4.3 Lowest catalog completeness
| org | total_active | complete | catalog_pct |
|---|---:|---:|---:|
| krb | 1,493 | 0 | 0.0000 |
| all | 686 | 17 | 0.0248 |
| tel | 2,253 | 443 | 0.1966 |
| tl | 5,325 | 1,191 | 0.2237 |
| el | 8,192 | 2,124 | 0.2593 |
| tla | 20,594 | 5,407 | 0.2626 |
| fc | 5,533 | 1,574 | 0.2845 |
| mfc | 5,257 | 1,507 | 0.2867 |

### 4.4 Zero achieved channels (orgs delivering nothing across applicable channels)
| org | applicable | achieved | ipad_orders_90d | portal_orders_90d | mp_share_events_90d |
|---|---:|---:|---:|---:|---:|
| tel | 3 | 0 | 0 | 0 | 0 |
| ol | 2 | 0 | 21 | 0 | 0 |
| krb | 2 | 0 | 0 | 0 | 0 |
| kl | 2 | 0 | 5 | 0 | 1 |
| hvl | 2 | 0 | 0 | 0 | 2 |
| st | 3 | 0 | 0 | 0 | 0 |
| tl | 2 | 0 | 0 | 0 | 1 |

> Note: `ol` has 21 iPad orders but they fail the `>= 50` threshold; `kl`/`hvl`/`tl` have a small mp_share trickle below the `>= 3` threshold. Whether the thresholds are correctly calibrated is itself a downstream banding question.

### 4.5 Largest gap between login volume and login recency
- `tel` is the only org with `days_since_last_login > 30`. It also has the lowest logins_90d (12) and lowest adoption ratio. Highest-confidence "at-risk" candidate in the dataset.
- `hmjc`, `cf`, `luc`, `abol`, `st`, `hh`: small logins_90d (10–68) but a login in the last week. These look like "single rep, low cadence" patterns and would benefit from a finer-grained activity signal than the current band ladder offers.

---

## 5. Headline takeaways for band-placement review

1. **`active_user_ratio` is the worst-calibrated signal.** 39 % of orgs collapse into a single band (0.01–0.24 → 20). Either re-cut the bottom (e.g. add 0.05 and 0.10 breakpoints) or move to a continuous transform — the band ladder is currently throwing away most of the discriminating power in the bottom 40 % of the distribution.
2. **`freshness_avg_staleness_ratio` cannot resolve the bad tail.** 41 % of orgs score 0, but inside that group the worst feeds range from 4.5× to 140× expected gap. A log-scaled transform or two more breakpoints (e.g. > 6, > 15, > 40) would surface the genuinely-abandoned feeds (`hvl`, `arl`, `hmjc`, `kll`, `clc`, `vl`).
3. **`days_since_last_login` does almost no work**: 103/104 score 90. Either drop it from the composite or replace it with a finer activity-cadence signal (e.g. weekday login density).
4. **`logins_90d` top band is too wide.** Everyone ≥ 3,000 scores the same; the spread inside that band is 7.5× (`pf 6,253` vs `sc 15,719`). If the goal is "discriminate among healthy power users", add a band around p90 ≈ 3,600.
5. **`catalog_pct` and adoption/value-delivery ratios are reasonably well-placed** against the natural data breaks. The 0.85 catalog threshold cleanly separates the 28 % of orgs that have real catalog gaps from the rest.
6. **Equal-weight composite would score these orgs similarly to the banded composite** on the upper half but **diverge sharply on the bottom decile**, because the bottom decile gets compressed by hard-zero bands (freshness > 4, ratio = 0) that an equal-weight raw-signal model would smooth. The 7 zero-channel orgs would be the clearest test set for a weighted-vs-equal comparison.
7. **The `ghost_account` override (logins_90d = 0 ∧ arr ≥ $5K) fired on zero orgs today** because there are no zero-login orgs in the current portfolio. It's still worth keeping for the future, but cannot be evaluated against today's data.

---

*No composite score and no band score was computed in this run. All values above are derived directly from the cache files in `Health V3/cache/2026-05-11/` and the MAL.*
