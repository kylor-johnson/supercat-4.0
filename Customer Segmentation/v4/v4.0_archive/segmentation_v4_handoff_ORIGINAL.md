# Segmentation v4 Handoff — Fresh-Agent Prompt (ARCHIVED ORIGINAL)

> **Archived 2026-07-09.** This is the original v4.0 brief that over-rotated.
> Use `Customer Segmentation/handoffs/segmentation_v4.1_handoff.md` instead.

---

## Who you are

You are picking up a strategic workstream for **SuperCat**, a SaaS company serving furniture, lighting, and home-goods manufacturers with iPad-based sales tools (eCat). SuperCat has ~109 active client organizations ("orgs") in its Postgres database. You work for Kylor (CTO) and Kjael (CEO).

## What happened so far (v3.1 → v3.2)

1. **v3.1** (July 1, 2026) introduced a 4-segment model classifying SuperCat's 109 clients by **business model** — not by digital maturity or revenue band. Segments: Luxury Specification, Premium Trade Brand, Mid-Market Multi-Channel, Volume Distribution, plus a Specialty catch-all.

2. **v3.2** (July 2, 2026) validated v3.1 against 4 Postgres data layers (catalog price, realized invoice price, order behavior, price-code complexity). It resolved every flagged account and moved 7 accounts. **Kylor stamped v3.2** — it is now the baseline.

3. **Key finding from v3.2:** Price is a *correlate*, not a *classifier*. The segments don't cleanly separate on price alone. The Luxury/Premium boundary is selling motion (specification vs. brand-building). The Premium/Mid-Market boundary is channel strategy. Only the Mid-Market/Volume boundary is cleanly numeric.

## What this session needs to do

We are shifting the lens. The v3.1/v3.2 work was about proving or disproving segment boundaries and eliminating eCat platform bias from the classification. That's done. **Now we need to build the definitive segmentation of eCat clients** grounded in first-party data:

### The three classification axes (from Kjael)

1. **How they sell** — specification (designer puts it in a project), brand-building (dealers carry the line on brand reputation), multi-channel distribution (trade + retail + online), volume/commodity distribution
2. **What they sell** — furniture, lighting, outdoor, accessories/giftware, decor/art, rugs, specialty. Also: price tier as a continuous dimension, not a categorical boundary.
3. **Who they sell to** — interior designers/architects (trade-only), dealers/retailers (wholesale), end consumers (DTC), hospitality/contract buyers, or mixed

### Median price as a continuous data point

v3.2 showed price doesn't create clean segment boundaries. But **median realized price (or scrubbed catalog median where no realized data exists)** is still the single most informative continuous variable. Use it as a *dimension* within each segment — not as the segmenting axis.

### What "review ALL possible data" means

You have access to:

#### Postgres (read-only via MCP tool `user-supercat-postgres-vpn` → `execute_sql`)

Key tables and what they tell you:

| Table | Useful columns | What it reveals |
|-------|---------------|-----------------|
| `organizations` | `shortname`, `name`, `id` | Org identity, join key |
| `products` | `net_price`, `organization_id`, `deleted`, `item_number`, `category_code`, `collection_code`, `trade_name_code` | What they sell, at what price, how their catalog is structured |
| `customers` | `default_price_code`, `organization_id`, `territory_code` | Who they sell to (proxy: how many price tiers = how complex the trade relationship) |
| `orders` | `organization_id`, `is_submitted`, `total`, `created_at` | Order volume, AOV, activity level |
| `portal_invoice_items` | `unit_price`, `organization_id` | Realized transaction prices (ground truth) |
| `portal_invoices` | `net_amount`, `organization_id` | Invoiced revenue (the commercial-truth axiom per provenance_spine.md) |
| `users` | `organization_id` | Rep/user count — proxy for sales force size |
| `distribution_centers` | `organization_id` | Shipping/fulfillment footprint |

**MCP SQL limitations:** The validator blocks `PERCENTILE_CONT`, `STDDEV`, `ROUND`, `::numeric` casts. Use simple aggregates (COUNT, AVG, MIN, MAX, ARRAY_AGG) and do complex stats in Python.

#### CSVs on disk

| File | Path | What it contains |
|------|------|------------------|
| v3.2 comprehensive (109 rows, all data layers) | `SuperCat 4.0/Segmentation/SuperCat_Customer_Segmentation_v3.2_COMPREHENSIVE.csv` | Company, org shortname, segment, v3 avg price, catalog scrub median, realized mean, best price, orders, AOV, price codes, product count |
| v3.2 analysis doc | `SuperCat 4.0/Segmentation/SuperCat_Client_Segmentation_v3.2.md` | Full methodology, rosters, flag resolutions |
| v3.1 original CSV | `~/Downloads/SuperCat_Customer_Segmentation_v3_Business_Model.csv` | Original 109-row classification with selling motion and buyer type text fields |
| v3.1 original doc | `~/Downloads/SuperCat_Client_Segmentation_v3.md` | Original 4-segment definitions and hypotheses |
| Master account data | `SuperCat 4.0/Pricing Migration V2/data/_master-account-data-v6.3.csv` | Company-to-org shortname mapping, pricing migration status, account metadata |
| Provenance spine | `SuperCat 4.0/Insightful Product 4.0/foundation/provenance_spine.md` | Canonical rules for data truth, confidence tiers, identity resolution |
| Segmentation derivation | `SuperCat 4.0/Insightful Product 4.0/foundation/segmentation_derivation.md` | Methodology for deriving segments from first-party data |

#### Foundation docs (read for context, don't modify)

- `SuperCat 4.0/foundation/02_who_we_serve.md` — older Digital Selling Maturity ICP (being superseded by this work)
- `SuperCat 4.0/Insightful Product 4.0/foundation/provenance_spine.md` — data truth rules
- `SuperCat 4.0/Insightful Product 4.0/foundation/segmentation_derivation.md` — derivation methodology

### Your task, specifically

1. **Pull every useful dimension from Postgres** for all 109 orgs. Suggested queries:
   - Category/collection/tradename distribution per org (what do they sell?)
   - Customer count + distinct territory codes per org (how big is their dealer network?)
   - User/rep count per org (how big is their sales force?)
   - Distribution center count per org (how complex is their fulfillment?)
   - Order recency — most recent order date per org (are they active?)
   - Invoice revenue where available — `SUM(portal_invoices.net_amount)` per org (how big are they on the platform?)

2. **Combine with the v3.2 comprehensive CSV** to create a master enrichment table: one row per org, every dimension available.

3. **Classify each of the 3 axes** for every account where data supports it:
   - **How they sell**: specification / brand-building / multi-channel / volume — use price code count, order patterns, AOV, customer structure as signals
   - **What they sell**: furniture / lighting / outdoor / accessories / decor / rugs / specialty — use `category_code` and `trade_name_code` distributions
   - **Who they sell to**: trade-only / wholesale / mixed / DTC / contract — use customer structure, territory complexity, price tier count

4. **Test whether the 4-segment model still holds** under these richer axes, or whether a different cut emerges naturally. Don't force a predetermined answer — let the data speak.

5. **Use median price as a continuous variable**, not a boundary. Show where it correlates with segment and where it doesn't. The v3.2 finding ("price is a correlate, not a classifier") should be tested, not assumed.

6. **Produce a v4.0 segmentation document** with:
   - Methodology (all data sources, all dimensions)
   - Segment definitions grounded in data, not just qualitative judgment
   - Full roster with all enrichment columns
   - Any accounts that remain ambiguous and why
   - Recommendation for Kjael: stamp, adjust, or rethink

### Constraints

- **Do not modify any foundation docs** (provenance_spine, segmentation_derivation, etc.)
- **Postgres is read-only** — you cannot write to the database
- **No imposed labels** — per the provenance spine, segments should emerge from first-party data, not be imposed externally
- **109 accounts is the universe** — the v3.2 comprehensive CSV is the canonical list
- **The v3.2 4-segment model is the null hypothesis** — you are testing whether it holds, not starting from scratch

### Output location

Save all output to `SuperCat 4.0/Segmentation/`:
- `SuperCat_Client_Segmentation_v4.0.md` — the analysis document
- `SuperCat_Customer_Segmentation_v4.0_MASTER.csv` — the enriched data file
