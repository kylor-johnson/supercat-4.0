# PORTAL-ORG-MATRIX — feasibility profile of all 55 Sales-Portal orgs

**Agent:** DATA-PROFILE (07) · **Isolation:** ON (read-only Postgres, no writes to code) · **Date:** 2026-07-17
**Source:** `user-supercat-postgres-vpn` (read-only). Numbers rounded/aggregated; **no customer, rep, or account names** — concentration is reported as shares only.
**Metric law:** `SUM(portal_invoices.net_amount)`, **RTD clamp** (`RTD = MAX(invoice_date) WHERE invoice_date ≤ CURRENT_DATE`; LTM = 12 months ending at RTD), **$5M single-row cap**, grain = `customer_bill_to_number`. `total_amount` ignored (NULL as a sales figure).
**Validation:** query reproduced the cycle-01 reference within RTD drift — **sarreid $15.98M / top1 29.93% / top10 46.34% / 0 credits** (ref $15.98M / 29.97% / 46.36% / 0); **cci $71.23M / 6.12% / 16.83% / 4,759 in-window credits** (ref $71.14M / 6.11% / 16.81% / 4,765). Rep tiers reproduce the canonical §7.1 cohort (gh 36.9→T1, scw 33.7→T1, sc 3.2→T1, bcf 84.8→T2, pf 90.6→T2, ril 87.7→T2).

**Scope confirmed:** 55 orgs carry `portal_invoices` rows; **4,877,068** total invoice rows.

---

## Column key

- **portal** — `mobile_sites.enable_sales_portal` (`Y` / `N` / `–`=null/unset). Aggregated `bool_or` across the org's sites.
- **inv / ord** — all-time `portal_invoices` / `portal_orders` row counts.
- **date span** — min→max `invoice_date`. `⚠fut` = future-dated rows present (clamp hazard); `⚠stale` = last invoice > ~90 days old.
- **topline LTM** — `SUM(net_amount)` over the clamped LTM window, $5M row cap. For ⚠stale orgs this is "LTM as of last feed," not current.
- **cust** — distinct billing entities in the window.
- **top1 / top10 / HHI** — concentration at billing-entity grain (HHI = Σ share²).
- **SAR** — single-account risk = `top1 ≥ 0.20`.
- **credit / ret** — in-window rows with `net_amount < 0`; `ret` = net-of-returns feed, `gross` = no credit memos present.
- **tier** — rep-identity tier per Provenance Spine §7.1 (date-aligned distinct-`rep_number` name bridge): **2** = named rep→revenue safe (≥82%), **1** = `rep_number` grain only, **0** = no rep key (behavior-only).
- **comma** — SERV-2178 exposure = orders / invoices with `rep_number LIKE '%,%'`.
- **terr (rows / %empty)** — `territories` master rows for the org / share of `org_users` with empty `territory_codes` (see caveat — org_users conflates B2B buyer accounts, so %empty is inflated).
- **dims** — populated invoice dimensions (>50% non-blank): **R**=rep, **B**=bill_to_state, **S**=ship_to_state, **V**=ship_via.

---

## Master matrix (one row per org, sorted by LTM topline)

| shortname (id) | portal | inv / ord | date span | topline LTM | cust | top1 / top10 / HHI | SAR | credit / ret | tier | comma (ord/inv) | terr (rows / %empty) | dims |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ufi (18) | Y | 120,663 / 116,525 | 2024-07→2026-07 | $135.40M | 4,310 | 6.8% / 25.6% / .011 | – | 0 / gross | **0** | 0 / 0 | 46 / 65% | — |
| kll (166) | Y | 196,215 / 175,886 | 2025-01→2026-07 | $86.70M | 2,334 | 4.4% / 21.8% / .008 | – | 0 / gross | **0** | 0 / 0 | 0 / 92% | B,S |
| cci (161) | Y | 171,313 / 157,321 | 2023-10→2026-07 | $71.23M | 7,789 | 6.1% / 16.8% / .006 | – | 4,759 / ret | **2** | 0 / 0 | 0 / 39% | R,B,S,V |
| clc (40) | Y | 302,676 / 244,788 | 2024-06→2026-07 | $59.00M | 1,607 | 8.0% / 32.1% / .017 | – | 9,609 / ret | **2** | 0 / 0 | 35 / 87% | R,V |
| mhc (46) | Y | 144,433 / 141,657 | 2023-12→2025-12 ⚠stale | $56.22M | 3,367 | 12.2% / 39.0% / .027 | – | 5 / ret | **2**◆dormant | 0 / 0 | 44 / 47% | R,B,S,V |
| asi (22) | Y | 55,653 / 5,571 | 2024-06→2026-07 | $54.94M | 1,634 | 4.3% / 13.0% / .004 | – | 0 / gross | **1** | 5,571 / 6,730 | 0 / 84% | R,B,S,V |
| shl (41) | Y | 449,870 / 428,534 | 2024-07→2026-07 | $50.00M | 1,158 | 14.2% / 40.9% / .032 | – | 21,461 / ret | **1** | 0 / 0 | 0 / 95% | R,B,S |
| demo (6) | Y | 16,348 / 25,693 | 2023-01→2024-11 ⚠stale | $47.08M | 1,535 | 13.4% / 34.5% / .025 | – | 413 / ret | **0** | 0 / 0 | 0 / 73% | B |
| ta (111) | Y | 60,767 / 1,582 | 2022-07→2026-07 | $46.90M | 1,615 | 6.8% / 30.6% / .015 | – | 0 / gross | **2** | 0 / 0 | 0 / 88% | R,B,S,V |
| scw (87) | Y | 91,446 / 79,693 | 2023-01→2026-07 | $44.87M | 2,019 | 4.1% / 20.2% / .007 | – | 1,187 / ret | **1** | 0 / 0 | 231 / 99% | R,B,S,V |
| pf (32) | **N** | 34,709 / 1,999 | 2025-01→2026-07 | $44.71M | 5,281 | 1.6% / 9.4% / .002 | – | 0 / gross | **2** | 0 / 0 | 0 / 43% | R,B,S,V |
| clli (149) | Y | 1,099,820 / 709,005 | 2021-01→2026-07 | $44.36M | 1,716 | 5.7% / 25.2% / .011 | – | 60,545 / ret | **1** | 0 / 0 | 61 / 93% | R,S,V |
| hfg (165) | Y | 73,904 / 58,315 | 2024-01→2026-07 | $41.05M | 2,440 | 6.5% / 25.9% / .011 | – | 0 / gross | **1** | 0 / 0 | 51 / 14% | R,B |
| clm (64) | Y | 155,215 / 143,530 | 2024-07→**4107-03** ⚠fut | $40.16M | 2,067 | 7.9% / 44.2% / .024 | – | 0 / gross | **1** | 0 / 0 | 0 / 82% | R,B,S,V |
| sc_test (85) | Y | 28,983 / 63,441 | 2022-01→2023-04 ⚠stale | $39.74M | 10,069 | 0.6% / 2.5% / .0004 | – | 1,038 / ret | **1** | 0 / 0 | 292 / 100% | R,B,S |
| gh (55) | Y | 44,848 / 103,126 | 2025-01→2026-07 | $38.99M | 2,642 | 4.8% / 22.3% / .008 | – | 1,452 / ret | **1** | 0 / 0 | 237 / 99% | R,B,S,V |
| sc (69) | Y | 71,216 / 66,381 | 2023-01→2026-07 | $33.82M | 8,095 | 0.4% / 2.9% / .0005 | – | 614 / ret | **1** | 0 / 0 | 0 / 53% | R,B,S |
| clctest (174) | Y | 137,960 / 67,820 | 2024-06→2026-01 ⚠stale | $28.96M | 1,810 | 6.9% / 29.5% / .015 | – | 4,047 / ret | **2** | 0 / 0 | 32 / 100% | R,V |
| el (152) | Y | 40,710 / 755 | 2025-01→2026-07 | $28.34M | 1,180 | 7.3% / 22.4% / .011 | – | 7,049 / ret | **1** | 0 / 0 | 0 / 28% | R,B,S,V |
| lpf (139) | Y | 254,632 / 180,865 | 2023-08→2026-07 | $25.72M | 687 | 9.9% / 47.0% / .035 | – | 0 / gross | **0** | 0 / 0 | 49 / 94% | B,S |
| ril (245) | Y | 17,851 / 2,189 | 2024-07→2026-07 | $25.46M | 994 | 3.7% / 20.8% / .008 | – | 802 / ret | **2** | 0 / 0 | 71 / 83% | R,B,S,V |
| heb (26) | – | 236,396 / 213,444 | 1980-12→2020-06 ⚠stale | $24.40M | 1,305 | 25.9% / 74.2% / .100 | **✓** | 0 / gross | **0** | 0 / 0 | 0 / 77% | — |
| fsf (225) | Y | 27,253 / 1,590 | 2024-07→2026-07 | $23.92M | 551 | 11.8% / 31.5% / .022 | – | 0 / gross | **1** | 0 / 0 | 0 / 97% | R,B |
| rw (248) | Y | 71,890 / 0 | 2023-01→2026-07 | $23.26M | 3,116 | 6.1% / 22.6% / .010 | – | 0 / gross | **1** | 0 / 0 | 0 / 23% | R,B,S,V |
| bri (222) | Y | 291,720 / 371,047 | 2024-06→2026-07 | $20.98M | 1,319 | 3.6% / 25.7% / .011 | – | 1,630 / ret | **1** | 0 / 0 | 0 / 90% | R |
| jyc (76) | Y | 111,249 / 612 | 2023-07→**2032-12** ⚠fut | $20.52M | 2,877 | 12.8% / 36.1% / .026 | – | 0 / gross | **1** | 612 / 111,249 | 100 / 99% | R,B,S,V |
| bcf (171) | Y | 25,451 / 1,801 | 2024-07→2026-07 | $19.59M | 739 | 17.5% / 41.5% / .041 | – | 0 / gross | **2** | 0 / 0 | 0 / 97% | R,B,V |
| wwjc (8) | Y | 56,719 / 51,513 | 2023-07→2026-07 | $18.43M | 3,494 | 2.9% / 12.5% / .003 | – | 0 / gross | **2** | 26,750 / 31,275 | 116 / 99.7% | R,B,S,V |
| bmc (11) | Y | 60,055 / 1,839 | 2023-12→2025-11 ⚠stale | $17.35M | 1,394 | 11.7% / 38.9% / .030 | – | 0 / gross | **1** | 0 / 0 | 37 / 81% | R,B,S,V |
| sccon (88) | Y | 16,272 / 13,491 | 2023-01→2026-07 | $17.03M | 706 | 11.1% / 33.3% / .021 | – | 182 / ret | **1** | 0 / 0 | 104 / 97% | R,B,S,V |
| sarreid (1) | Y | 43,715 / 45,453 | 2022-01→2026-07 | $15.98M | 1,416 | **29.9%** / 46.3% / .094 | **✓** | 0 / gross | **2** | 0 / 0 | 100 / 47% | R,B,S,V |
| fc (120) | Y | 21,647 / 931 | 2024-07→2026-07 | $15.26M | 1,516 | 10.3% / 31.4% / .025 | – | 339 / ret | **1** | 0 / 0 | 111 / 64% | R,B,S,V |
| ih (164) | Y | 7,563 / 6,902 | 2024-12→2026-07 | $15.05M | 1,590 | 5.6% / 18.1% / .007 | – | 696 / ret | **1** | 0 / 0 | 42 / 48% | R,B,S,V |
| sbmh (2) | Y | 13,059 / 15,514 | 2024-07→2026-07 | $13.91M | 1,460 | 4.3% / 16.6% / .006 | – | 521 / ret | **0** | 0 / 0 | 0 / 99% | B,S |
| jcusa (121) | Y | 12,263 / 2,878 | 2023-01→2026-07 | $11.94M | 912 | 10.5% / 30.6% / .018 | – | 317 / ret | **1** | 0 / 0 | 21 / 27% | R,B,S,V |
| khl (35) | Y | 21,979 / 3,105 | 2022-10→2023-08 ⚠stale | $9.68M | 582 | **36.3%** / 80.7% / .172 | **✓** | 0 / gross | **1** | 0 / 0 | 0 / 94% | R,B,S,V |
| vic (176) | Y | 117,420 / 116,485 | 2024-07→2026-07 | $8.93M | 480 | 18.7% / 75.7% / .092 | – | 2,506 / ret | **1** | 0 / 0 | 38 / 86% | R |
| kal (146) | Y | 68,556 / 94,640 | 2015-08→2026-07 | $8.71M | 839 | 6.9% / 36.7% / .019 | – | 880 / ret | **2** | 0 / 0 | 0 / 95% | R,B,S,V |
| libco (288) | Y | 7,430 / 30 | 2024-07→2026-07 | $8.23M | 248 | 4.7% / 29.0% / .014 | – | 5 / ret | **1** | 0 / 0 | 0 / 5% | R,B,S |
| ali (127) | Y | 28,907 / 29,581 | 2025-07→2026-07 | $7.32M | 1,033 | 10.8% / 44.8% / .030 | – | 1,782 / ret | **2** | 0 / 0 | 0 / 44% | R,B,S |
| demo2 (143) | Y | 6,151 / 5,670 | 2023-01→2026-05 | $7.30M | 867 | 10.0% / 34.6% / .021 | – | 7 / ret | **0** | 21 / 87% | 21 / 87% | B |
| ihw (107) | Y | 1,448 / 1,398 | 2025-07→2026-07 | $7.11M | 554 | 2.0% / 13.2% / .005 | – | 58 / ret | **1** | 125 / 58% | 125 / 58% | R,B,S,V |
| ffdm (98) | Y | 7,001 / 6,703 | 2019-01→2020-12 ⚠stale | $5.17M | 359 | 11.6% / 31.3% / .023 | – | 0 / gross | **0** | 0 / 0 | 0 / 65% | B,S,V |
| jc (65) | Y | 3,560 / 3,695 | 2013-09→2026-04 | $5.16M | 22 | 24.3% / 91.1% / .127 | **✓** | 0 / gross | **0** | 0 / 0 | 0 / 98% | B,S |
| dccl (239) | **N** | 4,676 / 4,592 | 2024-01→2026-07 | $5.14M | 203 | 11.0% / 34.0% / .024 | – | 0 / gross | **1** | 0 / 0 | 0 / 95% | R,B,V |
| cc (95) | – | 18,867 / 17,797 | 2023-01→2024-09 ⚠stale | $3.19M | 2,679 | 10.4% / 44.3% / .031 | – | 519 / ret | **2** | 0 / 0 | 51 / 61% | R,B,V |
| gl (187) | Y | 6,970 / 6,066 | 2025-12→2026-07 | $2.36M | 902 | 2.0% / 12.5% / .004 | – | 222 / ret | **0** | 0 / 0 | 0 / 83% | — |
| vl (147) | Y | 16,865 / 13,992 | 2022-04→2026-07 | $1.91M | 622 | 1.9% / 14.6% / .005 | – | 129 / ret | **2** | 0 / 0 | 0 / 32% | R,B,S,V |
| wwtest (179) | Y | 1,463 / 5,406 | 2023-03→2023-04 ⚠stale | $0.67M | 556 | 28.8% / 39.1% / .085 | **✓** | 0 / gross | **2** | 1,122 / 344 | 0 / 100% | R,B,S,V |
| tam (272) | – | 76 / 99 | 2025-09→2026-01 ⚠stale | $0.56M | 55 | 9.5% / 59.9% / .045 | – | 0 / gross | **1** | 0 / 0 | 0 / 15% | B,S,V |
| sci (226) | Y | 161 / 161 | 2024-01→2024-12 ⚠stale | $0.28M | 71 | 20.9% / 59.2% / .068 | **✓** | 0 / gross | **2** | 0 / 0 | 0 / 26% | R,B,S,V |
| bmc2 (81) | Y | 1,039 / 1,551 | 2022-08→2022-08 ⚠stale | $0.21M | 136 | 41.2% / 68.8% / .182 | **✓** | 0 / gross | **0** | 0 / 0 | 0 / 100% | — |
| test1 (5) | **N** | 6 / 6 | 2017-08→2018-05 ⚠stale | $0.017M | 4 | 41.8% / 100% / .339 | **✓** | 0 / gross | **2** | 0 / 0 | 0 / 95% | R,B,S,V |
| demo1 (106) | **N** | 2 / 2 | 2015-09→2015-09 ⚠stale | $0.005M | 1 | 100% / 100% / 1.00 | **✓** | 0 / gross | **0** | 0 / 0 | 0 / 80% | — |
| ctest (178) | Y | 7 / 667 | 2025-04→2025-05 ⚠stale | $0.00004M | 2 | 72.1% / 100% / .598 | **✓** | 0 / gross | **1** | 666 / 1 | 0 / 54% | — |

◆ **mhc** = Tier 2 (100% bridge) but **DORMANT** — last invoice 2025-12-22; names technically reachable but must carry a freshness banner and never present $-at-risk as live (Spine §7.1 / rep_copilot_operator §1).

---

## Summary layer

### Org shape — concentration
- **Single-account risk (top1 ≥ 20%): 10 of 55.** But 7 are tiny/test/stale artifacts (jc 22 custs, wwtest, sci, bmc2, test1, demo1, ctest). Among **fresh, real production** orgs only **sarreid (29.9%)** and stale legacy **heb (25.9%, feed frozen 2020)** and **khl (36.3%, feed frozen 2023)** clear the bar. **vic (18.7%)** is the only other live org near it.
- **The 55-org book is overwhelmingly diversified.** Median top1 ≈ **8%**; median HHI ≈ **.011** (very low). The big-revenue orgs (ufi 6.8%, kll 4.4%, cci 6.1%, asi 4.3%, pf 1.6%, sc 0.4%) are broad-book distributors, not concentrated ones. A "single-account-risk hero" fires on **~2–3 live orgs**, not the book.

### Returns / net-of-returns feed
- **28 of 55 carry credit memos (net-of-returns);** 27 are **gross-only** (no negative rows in window). Any "returns rate" or net-vs-gross reconciliation feature is only meaningful on the 28 — and **clli (60.5k), shl (21.5k), clc (9.6k)** dominate return volume. On the 27 gross-only orgs (incl. ufi, kll, asi, lpf, pf, sarreid) a returns metric is structurally absent, not zero.

### Rep-identity tier (per-rep feature feasibility — SERV-2388)
- **Tier 2 (named rep→revenue safe): 17 of 55** — but 5 are test/tiny (test1, sci, clctest, wwtest) or dormant (mhc). **Fresh, real, sizeable Tier-2 orgs ≈ 11:** sarreid, cci, clc, wwjc, pf, ril, bcf (the canonical 7) **+ ta, kal, vl, ali** (newly profiled here, ≥82% bridge — recommend a live gut-check before naming reps client-facing).
- **Tier 1 (`rep_number` grain, no names): 26 of 55** — includes high-revenue shl, scw, clli, clm, gh, sc, el, bri, vic, jyc. Per-rep features must ship a **`rep_number`-grain fallback**, not names.
- **Tier 0 (behavior-only, no rep key): 12 of 55** — incl. three of the top four by revenue (**ufi $135M, kll $87M**, and heb/lpf). **Per-rep revenue is impossible on the single largest orgs.** This is the headline feasibility constraint for SERV-2388.

### SERV-2178 comma-rep exposure
- **5 of 55 orgs carry comma `rep_number`s:** wwjc (26,750 ord / 31,275 inv), asi (5,571 / 6,730), jyc (612 / **111,249** inv), wwtest (1,122 / 344), ctest (666 / 1 — where Chuck reproduced it). The other 50 have **zero** comma exposure.
- The territory feature `territory_access_via_rep_number` is ON for **el, ctest** only — and **el has 0 comma rows today**, so the only live-impacted org is the test org **ctest**. The latent blast radius (if the feature is turned on for wwjc/asi/jyc) is large, but it is **not** a live outage on 50 of 55 orgs.

### Territory health
- **`territories` master table is EMPTY (0 rows) on 32 of 55 orgs**, including big live orgs asi, shl, clm, el, cci, kll, bcf, bri, rw. Any feature that reads the territories master (rep↔territory rollups, territory pickers) is **infeasible on more than half the book** without a territory build first (the SERV-2180 / KLL-analysis family).
- **`org_users.territory_codes` is empty for the vast majority of accounts** (median ~85%+), but this metric is **inflated by B2B buyer accounts** — `org_users` conflates reps and portal buyers (wwjc 20.8k users, jyc 16.2k, gh 8.0k). Read as "most seats have no territory," not "most reps." A rep-seat-scoped recount (`last_ipad_login_at IS NOT NULL`) is the correct denominator for a true SERV-2178/2254 rep-exposure number and should be the next drill-down.

### Dimensions available (for slice/filter features)
- **Rep populated on invoices: 41 of 55.** **bill_to_state: ~46**, **ship_to_state: ~38**, **ship_via: ~34.**
- **All four dims present: ~24 orgs** (incl. cci, mhc, asi, sarreid, pf, gh, jyc, kal, wwjc…). A ship-via or state-map slice degrades on the rest.
- **Dimension-poor outliers:** **ufi ($135M, top org) and heb, gl, bmc2, demo1, ctest have essentially NO usable dims** beyond customer grain — ufi in particular has no rep, no state, no ship_via on a $135M feed. **clc ($59M) and clctest have no state columns.** Any state-choropleth or ship-via feature must be gated per-org.

### Data-quality flags (do not treat as clean)
- **Future-dated feeds (clamp-critical): clm (max 4107-03), jyc (max 2032-12).** RTD clamp handles both; without it, LTM windows would be nonsense.
- **$5M single-row cap catches a real artifact: kll has one invoice row of ~$437 BILLION** (`437,466,784,090`) — excluded by the cap. Verify the cap is applied everywhere kll is reported.
- **15 stale feeds** (last invoice > ~90 days old): heb, sc_test, khl, ffdm, cc, demo, bmc, mhc, sci, tam, ctest, wwtest, bmc2, test1, demo1. Their "LTM topline" is LTM-as-of-last-feed, not current — never present as today's run rate.
- **7 orgs have data but `enable_sales_portal` is not True:** pf (**N**, $44.7M, Tier 2), dccl (N), test1/demo1 (N), heb/cc/tam (unset). **pf is the notable one** — a large, clean, Tier-2 feed with the portal flag off.
- **Test/demo orgs in the 55:** demo, demo1, demo2, sc_test, wwtest, clctest, ctest, test1, bmc2, sci, tam — exclude these (~11) from any "N of 55 production orgs" capability claim. **Real production book ≈ 44 orgs.**

---

## Golden-child honesty — how representative is sarreid?

**Plainly: sarreid is a flattering outlier, not a median org.** It is genuinely useful as a *demo* precisely because it is the opposite of typical:

| Trait | sarreid | The 55-org (≈44 production) reality |
|---|---|---|
| Concentration | top1 **29.9%**, SAR ✓ | Median top1 ~**8%**; only ~2–3 live orgs are concentrated. sarreid is **top-3 most concentrated** of all fresh orgs. |
| Rep identity | Tier 2, 100% bridge | Only ~11 fresh orgs are Tier 2; **12 are Tier 0** including the two largest (ufi, kll). |
| Dimensions | all 4 (R,B,S,V) at ~100% | ~24 orgs have all four; the biggest org (ufi) has **none**. |
| Data hygiene | clean, fresh, no returns, no future dates | 15 stale, 2 future-dated, 1 $437B artifact, 28 with returns. |
| Size | $16M (rank ~31 of 55) | **Mid-pack, not large.** ufi/kll/cci/clc are 3.5–8× bigger and shaped completely differently. |

**Consequence for the program:** a hero built and demoed only on sarreid (concentration + named-rep + full-dim + clean) will **silently fail or degrade on the majority of the book**:
- The **single-account-risk** hero is *dramatic* on sarreid but a near-non-event on the diversified majority — it must degrade gracefully to "healthy diversification" copy, not imply everyone has a whale.
- The **per-rep** hero works on sarreid but is **impossible on ufi/kll** (the two biggest orgs) and name-less on 26 Tier-1 orgs — ship `rep_number` fallback + suppression, never names by default.
- **True Topline** (invoiced net) is the one hero that **travels to all 55** — it needs only `net_amount` + the RTD clamp + $5M cap, all of which are present everywhere. That is the safe universal v1.

**Pair sarreid (concentrated, Tier 2, full-dim) with a genuine opposite for every demo** — e.g. **ufi** (huge, Tier 0, dimension-poor) or **cci/pf** (huge, diversified, Tier 2) — so the design proves it reads real org shape, not a template.

---

## Handoff

Paste to **05-ORCHESTRATOR** for review. Feasibility tags this matrix supports:
- **True Topline** → works on **55 of 55** (with clamp + $5M cap).
- **Concentration / single-account risk** → computable on 55, *material* on ~2–3 live orgs.
- **Per-rep (named)** → **17 of 55** Tier 2 (~11 fresh real); **12 of 55 impossible** (Tier 0, incl. the 2 largest).
- **Returns / net-vs-gross** → **28 of 55**.
- **Territory rollups (master-table-backed)** → **23 of 55** (32 have no territories rows).
- **SERV-2178 comma fix** → material latent exposure on **5 of 55**; live only on ctest today.
