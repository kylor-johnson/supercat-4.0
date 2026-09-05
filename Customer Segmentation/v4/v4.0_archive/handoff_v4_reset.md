# Customer Segmentation v4.0 — Reset Handoff

**Date:** 2026-07-07
**Status:** v4.0 went off-track. This prompt gets you back on the rails.
**Goal:** Produce a stamped v4.0 that does what Kjael actually asked for.

---

## What happened

v3.2 was stamped by Kylor on July 2 after a team review call with Kjael, Brent, Jon, and Emery. On that call, Kjael reviewed the 4-segment model and said (direct quotes):

> "let's spend a few hours on this. Let's tune it to scrub out the outliers. Come back. I imagine it's going to be the same view. It's just going to be a little bit tighter. And let's stamp it for now."

> "our job ideally is just to establish three buckets and distinguish between those buckets to provide a kind of quasi-Northstar to get the thing going"

> "it doesn't need to be perfect. In three to four buckets that distill the market down from one giant thing"

> "our grasp on how these firms sell and what distinguishes how they sell from each other, putting them in groups is going to accelerate everything we're trying to do"

The purpose is **rep co-pilot context** — Kjael's words:

> "if I'm a sales rep co-pilot, if I'm Savoy House and I jump in there and it gives me a bunch of stuff that's totally catered towards trade dealers or whatever, it's going to be like, hey, you should pitch this kind of stuff. And it's like, what? Like we need to give – we need this level of – so we need to be able to drop customers into a bucket so we can drop their reps into a bucket so that we serve up stuff that's not tone deaf."

And from Kylor on the same call:

> "if you only look at it through the rails of eCat, it's just the data picture just does not work. And so a way to round that out, if we don't have full extended ERP data as well, is to look at their actual customers."

**What v4.0 did instead:** Built a three-axis classification framework, reclassified 8 orgs based on eCat operational data (customer counts, online ordering groups, territory structures), declared "price is a correlate not a classifier" as a thesis, and produced a 400+ line analytical document. This was a framework overhaul when Kjael asked for a refinement and stamp.

**Key problems with v4.0:**
1. Reclassified 8 orgs using eCat-only signals (how many customers loaded into eCat, how many online ordering groups configured) — but these signals only describe how the company uses eCat, not how they actually sell in the market
2. Treated "price is a correlate not a classifier" as a reason to remove price as a dimension — Kjael never said that; he said to CLEAN the price data, not abandon it
3. Overengineered what should have been a simple deliverable — Kjael wanted something he could read and stamp, not a methodology document

---

## What v4.0 got RIGHT (salvage these)

- **fms AOV correction:** The $92K AOV in v3.2 was caused by 23 corrupt duplicate orders in Postgres. Clean AOV = $3,649. This correction is real and should carry forward.
- **T12M order counts:** Trailing-12-month order counts were queried for all 109 orgs. This is useful recency data — keep it as an enrichment column.
- **Qualitative segment descriptions:** The prose descriptions of each segment's selling motion are good and align with the meeting discussion. The problem was making them the organizing principle instead of just descriptions.
- **SC customer count validation:** Summer Classics really does have 92K+ customers. sc and sccon are separate orgs with zero customer overlap.

---

## What to do now

### Start from v3.2 as the baseline

v3.2 is the Kylor-stamped, Kjael-reviewed version. Files:
- `SuperCat 4.0/Customer Segmentation/v3/v3.2/SuperCat_Client_Segmentation_v3.2.md`
- `SuperCat 4.0/Customer Segmentation/v3/v3.2/SuperCat_Customer_Segmentation_v3.2_COMPREHENSIVE.csv`

v3.2 already has:
- 2σ-scrubbed catalog prices
- Realized prices from portal_invoices (39/109 orgs)
- "Best price" = realized when available, else scrubbed catalog median
- 4 data layers (catalog price, realized price, order behavior, price code complexity)
- 7 account moves from v3.1, all resolved
- The 4 segments: Luxury Specification (34), Premium Trade Brand (31), Mid-Market Multi-Channel (26), Volume Distribution (13), Specialty (5)

### Produce a v4.0 that is v3.2 + Postgres enrichment

The enrichment should ADD operational context within each segment. It should NOT reclassify orgs based on eCat configuration data.

**Add these columns/data to the CSV and document:**
- `customer_count` — from Postgres `customers` table
- `distinct_territories` — from Postgres `territories` table
- `org_users` — from Postgres `org_users` table
- `t12m_orders` — trailing-12-month order count (already queried in v4.0, data is in the v4.0 MASTER CSV)
- `distribution_centers` — from Postgres

**Apply these corrections:**
- fms AOV: change from $92,048 to $3,649 (23 corrupt orders excluded)
- Do NOT include `total_invoiced_revenue` — the portal_invoices lifetime sums are garbage (not time-windowed, not deduplicated)

**Keep the v3.2 segment membership.** If any of v4.0's 8 reclassifications are actually warranted, they should be flagged for Kjael's review with a one-line rationale — not moved unilaterally. The reclassification decision should be based on "how does this company actually sell in the real world" (their website, their dealers, their go-to-market), not "how many customers they loaded into eCat."

### Keep it simple

The document should be something Kjael can read in 5 minutes and go "yep, stamp it." That means:
- 4 segments with clear one-sentence descriptions
- A roster table per segment with the enrichment data
- A short section flagging any accounts that might be in the wrong bucket (for Kjael to decide)
- A short section on what the enrichment data reveals about each segment
- NO methodology sections, NO cross-tabulation matrices, NO three-axis frameworks
- The qualitative segment descriptions from v4.0 are good — use them as prose, not as a formal framework

### The end state

After this, the segmentation is done and the next step is **personas within each segment** for co-pilot initialization. Kjael said this explicitly:

> "once you crack the code on customer profile, then you move into Personas. And then that's when you've got it licked."

---

## File locations

| File | Path | Role |
|---|---|---|
| v3.2 analysis (BASELINE) | `Customer Segmentation/v3/v3.2/SuperCat_Client_Segmentation_v3.2.md` | Start here |
| v3.2 CSV (BASELINE) | `Customer Segmentation/v3/v3.2/SuperCat_Customer_Segmentation_v3.2_COMPREHENSIVE.csv` | 109 orgs, 4 data layers |
| v4.0 analysis (OFF-TRACK) | `Customer Segmentation/current/SuperCat_Client_Segmentation_v4.0.md` | Reference only — salvage descriptions, discard framework |
| v4.0 HTML (OFF-TRACK) | `Customer Segmentation/current/SuperCat_Client_Segmentation_v4.0.html` | Will need to be rebuilt from the corrected v4.0 |
| v4.0 MASTER CSV (OFF-TRACK) | `Customer Segmentation/current/SuperCat_Customer_Segmentation_v4.0_MASTER.csv` | Salvage t12m_orders column, fms AOV fix |
| v3.2→v4.0 changelog (OFF-TRACK) | `Customer Segmentation/current/v3.2_to_v4.0_changelog.md` | Rewrite after corrections |
| v3.2 business model CSV | `Customer Segmentation/v3/v3.2/SuperCat_Customer_Segmentation_v3.2_Business_Model.csv` | Additional v3.2 reference |
| Segmentation backstory | `Customer Segmentation/briefs/SuperCat_Segmentation_How_We_Got_Here.md` | Context on v1→v3 evolution |
| v4 original handoff | `Customer Segmentation/handoffs/segmentation_v4_handoff.md` | What kicked off the v4 work |

## Postgres access

Use the `supercat-postgres-vpn` MCP server with `execute_sql` for any queries. Schema is `public`. Key tables: `organizations`, `customers`, `territories`, `orders`, `products`, `org_users`, `user_types`, `distribution_centers`, `price_levels`. Join on `organization_id` (not `org_id`).

## Important context from the July 2 meeting

- **Jon Vanderberg** (10 years in the market) suggested looking at price levels — do they have stocking dealers, non-stocking dealers, and designers? Companies with all three behave similarly.
- **Brent Sanders** said the one answer they need is "how you sell" — and that the dollar per unit analysis should throw out outliers because $5 accessories drag down the median.
- **Emery Rust** suggested price point is the simplest segmentation axis. Kjael's response was to clean the price data, not to abandon it.
- **Kjael** said furniture vs. lighting is "generally pretty misguided" as a distinction — "it's more to do with segment of the market as a function of price point."
- **Kjael** emphasized these firms sell through channels far beyond eCat — the segmentation must reflect how they sell broadly, not just their eCat configuration.
