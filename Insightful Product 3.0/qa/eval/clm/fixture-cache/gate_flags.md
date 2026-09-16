# Gate Flags — Crystorama (clm, org_id=64)
- **Run date**: 2026-06-12
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | true | org_summary has_clicky_portal = true; daily_metrics table confirmed (crystorama_clm_ecat_online_daily_metrics) |
| HAS_CART | false | enable_online_ordering = false; recurring_services has no B2B Cart; 0 server-source orders LTM |
| HAS_PORTAL_ORDERS | true | 73,983 LTM portal_orders; LTM ERP GMV $40.13M |
| HAS_INVENTORY | true | 1,899 inventory rows confirmed |
| HAS_SALES_DATA | true | 68,984 sales_data rows confirmed |
| HAS_SALES_SECTION | true | 5 reps with ≥10 iPad orders LTM |
| HAS_PEER_DATA | true | Peer CSV dated 2026-04-14 (59 days old, not stale) |
| BENCHMARK_ELIGIBLE | True | peer_benchmark_2026-04-14.csv |
| BENCHMARK_CONFIDENCE | medium | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier1 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 5 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Lighting / iPad+Catalog+Portal | Source for plain-language cohort framing |
| CLICKY_PREFIX | crystorama_clm_ecat_online | Used for BigQuery clicky_analytics table names |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | PASS | portal_orders_gmv ($40.13M) > ecat_gmv ($553K) |
| VM45_GATE_2 | FAIL | ecat_gmv ($553,100.36) < 5% of portal_orders_gmv ($2.006M threshold); eCat = 1.38% of ERP total |
| VM45_RENDER | false | Gate 2 failed — eCat capture rate not interpretable as activation signal |
| QUALIFYING_REP_COUNT | 5 | Reps with ≥10 iPad orders LTM: Katy McCully (38), Jeff Nicholson (20), Chas Lassoff (11), Matt Sullivan (11), Zachary Rapp (11) |
| MIXPANEL_USER_DATA_PRESENT | true | Q-01 Step 1 returned 100 users |
| SHOWROOM_EXCLUSIONS | 1 | See showroom_scan_results.md (HighPoint Showroom — $8,084 GMV, 2 orders LTM) |
| MIXPANEL_ORDER_TRACKING_GAP | false | Postgres LTM iPad orders: 166; Mixpanel org-wide submit_order: 2 (effectively untracked, but not strictly 0 — gate=false per literal rule; §2 archetype logic should not rely on submit_order) |
| USER_GROUP_SPLIT_AVAILABLE | false | 90/100 Mixpanel users matched to org-64 user groups (Sales Reps=80, z-SuperCat=6, Internal Employees=4); join_rate=0.90, ambiguous_rate=0 (no matched user in `other` bucket), BUT admin_internal event share = 5,206/79,674 = 6.5% < 10% threshold → no meaningful rep-vs-internal split. §8 renders without split. |
| USER_GROUP_JOIN_RATE | 0.90 (not a required-parity gate) | 90/100 Q-01 Step 1 Mixpanel users matched org-64 org_users; 10 unmatched belong to other orgs/global (calebr, chermclelland, danapoe, jlindquist, khale1, mayerbrian, pmorris, rhiggins, robertgarcia, vwalker1) |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 0.065 | admin_internal (z-SuperCat + Internal Employees) events 5,206 / matched events 79,674 = 6.5% (< 10% threshold; showroom usernames dunnlighting/hpshow/dalshow/sourceltg/lightingvision matched as Sales Reps, not a distinct showroom group) |

## Org Identity

- **Client name**: Crystorama
- **Shortname**: clm
- **Org ID**: 64
- **Bundle**: iPad+Catalog+Portal
- **Bundle label for report**: iPad + eCat Online + Sales Portal

## Validation Log

- portal_orders: 141,409 total rows; 73,983 LTM (after excluding ~13 corrupt-date outlier rows with order_date years like 9380/2080/6021 — 1 order each); all rows have buyer_name and customer_bill_to_number populated (141,409 / 141,409).
- Showroom scan: 1 confirmed exclusion ("HighPoint Showroom" — $8,084 GMV, 2 orders LTM). "Dunn Lighting" flagged ambiguous (non-person naming pattern, contains "Lighting") — retained in leaderboard per name-alone-insufficient rule.
- Rep name normalization: collapsed double-spaces in "Vince  Hall" → "Vince Hall", "Megan  Trosclair" → "Megan Trosclair", "Kevin  Taylor" → "Kevin Taylor". No case-dup or mangled-name merges required.
- VM-45: Gate 2 FAIL — eCat GMV ($553K) is 1.38% of ERP total ($40.13M), below 5% threshold. Capture-rate subsection skipped.
- Q-43 (Territory): customer territory_codes populated in JSON-array format (`["C-14"]`) → JSON path used; `territories` lookup table empty (0 rows) so territory_name is NULL throughout. Step 1 (territory-name join) skipped; Step 3 gap summary used.
- MIXPANEL_ORDER_TRACKING_GAP: org-level submit_order tracking is effectively absent (org-wide total = 2 events vs 166 Postgres LTM iPad orders). Literal gate = false because not strictly zero; downstream archetype logic still avoids submit_order as a signal.
- Q-CI-04 (Growth Trajectory): segment_benchmarks_monthly now has 3 snapshots (Apr/May/Jun 2026) for segment "Catalog-Focused". Not run per Stage 1 plan (kept baseline-consistent); availability noted for future enablement.
