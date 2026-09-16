# §5 Commerce Analytics — Highlights

## Summary
- **Subsections rendered:** 4 of 7
- **Subsections skipped:** 3 (Channel Breakdown → HAS_CART=false; ERP Context → HAS_PORTAL_ORDERS=false; Capture Rate → VM45_RENDER=false)
- **Period:** Apr 2025–Apr 2026 (13 months; Apr 2026 is partial through Apr 20)

## Key Stats
- **291 iPad orders** with **$821.8K GMV** and **$2,824 AOV**
- **Top-5 buyer concentration: 30.4%** of eCat GMV — exceeds 25% threshold → alert callout rendered
- **Top-10 buyer concentration: 44.4%** of eCat GMV ($364.7K)
- **Top buyer:** Reeds Furniture Inc. — $62,233 (7.6% of GMV) on 3 orders
- **100% confirmed orders** — no quotes, drafts, or pending orders in the system
- **Peak month:** July 2025 (38 orders, $161.0K GMV)
- **Strongest recent month:** February 2026 (34 orders, $110.5K GMV)

## Notable Decisions
1. **Concentration pct uses row-derived math (30.4%), not Q-13 summary line (28.4%).** The Q-13 summary states "Top 5 = 28.4%" but the individual row GMV values ($249,814) over the Q-20 total ($821,800) yield 30.4%. Used 30.4% for consistency with the visible table data a reader could verify.
2. **Omitted eCat Online and Quote rows** from AOV subsection — both were zero (iPad-only bundle).
3. **Cleaned internal prefixes from buyer names:** removed "MEGA0 - " from Schwartz & Company Ltd. and Colemans Countrywide.
4. **Shortened "JRJT Trading Inc David Kirsch"** to "JRJT Trading Inc." for table readability.
5. **No channel attribution statement** — HAS_CART = false per operator guide.
6. **No ERP/portal_orders references anywhere** — HAS_PORTAL_ORDERS = false.
7. **April 2026 flagged as MTD** with muted badge in trend table.
8. **Row-highlighted** Feb 2026 and Jul 2025 as standout months in the trend table.
