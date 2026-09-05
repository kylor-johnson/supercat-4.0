# Segmentation v4.0 STAMPED — Fresh-Agent Handoff

> **Use this prompt to start a fresh session for post-stamp propagation work.**

---

## What happened

1. **v3.2** (July 2, 2026) established a 4-segment model of SuperCat's 109 clients by selling motion. Kylor stamped it.

2. **v4.0** (July 9, 2026) tested v3.2 against every available Postgres dimension — product catalogs, customer structure, order behavior, invoice revenue, rep activity, taxonomy diversity. **Result: the 4-segment model holds.** The 5th segment (Specialty/Non-Traditional) was dissolved. Kjael stamped it.

3. **Key deliverables (all in `Customer Segmentation/v4/v4.0_archive/`):**
   - `SuperCat_Client_Segmentation_v4.0.md` — full analysis with segment definitions, enrichment findings, price-as-dimension analysis
   - `SuperCat_Customer_Segmentation_v4.0_MASTER.csv` — 109 rows × 24 columns, all enrichment dimensions + three-axis classification
   - `build_v4.py` — reproducible build script (all Postgres data embedded)

## The stamped model

| # | Segment | Count | Selling Motion |
|---|---------|-------|----------------|
| 1 | Luxury Specification | 33 | Designers put it in a project |
| 2 | Premium Trade Brand | 38 | Dealers carry the line on brand reputation |
| 3 | Mid-Market Multi-Channel | 24 | Trade + retail + online distribution |
| 4 | Volume Distribution | 14 | Commodity distribution, high volume |

**Three enrichment axes (dimensions, not segments):**
- **What they sell:** Furniture (33), Lighting (44), Accessories (14), Decor/Art (9), Outdoor (7), Rugs (1), Textiles (1)
- **Who they sell to:** Trade/Designers (33), Wholesale/Dealers (28), Wholesale/Retailers (20), Volume Retail (14), Broad Network (7), Mixed (7)
- **Median price:** continuous variable within each segment (not a boundary)

## Key findings to carry forward

1. **Price is a correlate, not a classifier** — the Spec/Brand-Building overlap zone ($300–$700) is where selling motion determines placement
2. **Product vertical doesn't segment** — Lighting is in all 4 segments
3. **Buyer type is redundant** with selling motion — it's predicted, not independent
4. **The Specialty segment is dissolved** — those 5 accounts were placed in existing segments

## What needs doing next (pick one or more)

### A. Propagate to Insightful Product 4.0
- Update `Insightful Product 4.0/foundation/segmentation_derivation.md` to reference v4.0 as the canonical client segmentation
- The per-client customer segmentation (buying behavior within a client's customer base) is a DIFFERENT thing — that uses the derivation pipeline. Don't conflate.
- Update any reference to "5 segments" or "Specialty" in the Insightful Product foundation docs

### B. Update the "current" folder
- Copy the stamped CSV to `Customer Segmentation/current/` as the active reference
- Archive the old v3.2 comprehensive there

### C. Feed into ICP / who-we-serve work
- `SuperCat 4.0/foundation/02_who_we_serve.md` is the older Digital Selling Maturity ICP — it needs updating to reflect the stamped segmentation
- The three axes (how/what/who) + median price as continuous dimension are the inputs for any ICP refresh

### D. Validate the 5 unmatched accounts
- 5 accounts have `??` as shortname (no Postgres org match): Gabriella White, Legrand US, Silver One, Tomlinson Companies, Ideal Living
- Confirm with Kjael whether these are active or should be removed from the universe

## Do NOT

- Modify the provenance_spine.md or segmentation_derivation.md methodology (those are Tier 0/1 docs)
- Re-run the segmentation from scratch — it's stamped
- Use any legacy Insightful Product folders (2.0, 3.0) — see workspace rule `insightful-legacy-frozen`
- Conflate CLIENT segmentation (this work — 109 orgs) with CUSTOMER segmentation (per-client buying behavior clusters)
