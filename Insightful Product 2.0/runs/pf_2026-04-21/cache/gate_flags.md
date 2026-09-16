# Gate Flags — Palecek (pf, org_id=32)
- **Run date**: 2026-04-21
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | true | org_summary.has_clicky_portal = true |
| HAS_CART | false | 0 server orders LTM; recurring_services has no "B2B Cart" |
| HAS_PORTAL_ORDERS | true | 2,093 LTM portal_orders |
| HAS_INVENTORY | true | 1,520 inventory rows |
| HAS_SALES_DATA | true (qty only) | 56,771 rows; amount_invoiced is NULL for all rows — only quantity_invoiced populated |
| HAS_SALES_SECTION | true | 31 qualifying reps with ≥10 iPad orders LTM |
| HAS_PEER_DATA | true | Peer benchmark CSV from 2026-04-14 (7 days old) |
| BENCHMARK_ELIGIBLE | True | From benchmark CSV |
| BENCHMARK_CONFIDENCE | low | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | tier2 | Internal only — not in delivered HTML |
| PEER_GROUP_N | 32 | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | Furniture | Source for plain-language cohort framing |
| CLICKY_PREFIX | palecek_eol_trial | Confirmed via BigQuery table list |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | FAIL | eCat GMV $19,714,233.93 > ERP GMV $12,044,191.91 — ERP sync is partial |
| VM45_GATE_2 | N/A | Gate 1 already failed |
| VM45_RENDER | false | Gate 1 failed — ERP sync partial, capture rate not interpretable |
| QUALIFYING_REP_COUNT | 31 | Reps with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | true | Q-01 Step 1 returned 154 rows |
| SHOWROOM_EXCLUSIONS | 6 | See showroom_scan_results.md for names + evidence |
| MIXPANEL_ORDER_TRACKING_GAP | false | Postgres LTM iPad orders: 2,890; Mixpanel total submit_order: 4,291 |
| USER_GROUP_SPLIT_AVAILABLE | false | See user_group_mapping.md; ambiguous_rate > 0 (118/197 unclassified) — split not reliable |
| USER_GROUP_JOIN_RATE | — | Computed in user_group_mapping.md |
| USER_GROUP_SHOWROOM_EVENT_SHARE | — | Computed in user_group_mapping.md |
| SALES_DATA_AMOUNT_GAP | true | sales_data has 56,771 rows but amount_invoiced is NULL for all — Q-37, Q-39 by-amount empty |
| HAS_NEW_ITEMS | true | 540 products with new_item = true |
| HAS_PORTAL_ORDER_ITEMS | true | 4,241 portal_order_items rows |

## Org Identity

- **Client name**: Palecek
- **Shortname**: pf
- **Org ID**: 32
- **Bundle**: iPad+Catalog
- **Bundle label for report**: iPad + Online Product Catalog
- **Vertical**: Furniture
- **Segment (internal only)**: Platform-Embedded
- **ARR**: $39,660
- **Feature depth**: 5
- **Peer standing (internal reference)**: Top Performer

## Validation Log

- portal_orders: Present (2,093 LTM), but ERP GMV ($12.0M) < eCat GMV ($19.7M) — indicates partial ERP sync. HAS_PORTAL_ORDERS = true for Q-16/Q-18B, but VM-45 skipped (Gate 1 fail).
- Showroom scan: 6 confirmed showroom accounts (PALECEK + city/location pattern). See showroom_scan_results.md.
- VM-45: SKIP — eCat GMV exceeds ERP GMV, denominator is invalid.
- sales_data: 56,771 rows present but amount_invoiced is NULL for all rows (0 rows with amount > 0). quantity_invoiced is populated (138,792 total). Q-37 and Q-39 by-amount return empty. Q-42 new item shows quantity sold but $0 revenue.
- Mangled rep names merged: "Jenna Rene  Fischer - candice " + "Jenna Rene  Fischer " → "Jenna Rene Fischer"; "Lacey Guerrero" + "Lacey  Guerrero" → "Lacey Guerrero"; "Jessica - Ricci sales Mason" flagged as mangled (see showroom_scan_results.md).
- Whitespace normalized: "Jessica  Flack " → "Jessica Flack", "Barbara Erlichman " → "Barbara Erlichman", "Tony Westley " → "Tony Westley", "John  Smith" → "John Smith", "Susan  Whitworth" → "Susan Whitworth", "Karen  Stewart" → "Karen Stewart", "Carol  Harris" → "Carol Harris"
- Non-person entities flagged: "Doeren Sales" (1 order, $25,834, 0 unique customers) — ambiguous, flagged for CSM review. "Doeren Carsten" (1 order, $10,460, 0 unique customers) — likely person from Doeren agency, included.
