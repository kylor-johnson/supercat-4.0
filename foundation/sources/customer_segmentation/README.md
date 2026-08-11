# Customer Segmentation — canonical home

> **Last updated**: 2026-07-10 · **Owner**: CEO · **Status**: v4.0 stamped (2026-07-09), imported here 2026-07-10.

This folder is the canonical workspace home for SuperCat's **selling-motion** segmentation
(Client Segmentation v4.0). It exists so that `foundation/` can cite it and the
`brand_to_customer` capability can consume it without depending on a Downloads copy or an
external build project.

## Files

- [`SuperCat_Client_Segmentation_v4.0.md`](SuperCat_Client_Segmentation_v4.0.md) — the stamped
  narrative + methodology (preserved verbatim; see its import banner about non-resolving legacy links).
- [`SuperCat_Customer_Segmentation_v4.0_MASTER.csv`](SuperCat_Customer_Segmentation_v4.0_MASTER.csv) —
  the **109-row roster**. One row per org with the three classification axes plus catalog / price /
  customer-structure / order-activity / invoiced-revenue / iPad-activity columns.
- [`account_buyer_type_reads.csv`](account_buyer_type_reads.csv) — the append-only index of
  evidence-based account buyer-type reads. **Live, coverage 8 / ~109 orgs · 19 reads** (as of
  2026-07-22). Seed triad (Anna Hislop / Viva / Cartwright) plus Phase A dual-socialize
  website verifies — including first **trade-led showroom** (A. Hoke, CAI Designs, Gorrod Gallery)
  and **designer / trade** (Michelle Gerson) goldens.
- **Design-partner dual-package queue** (moved 2026-07-23): lives under agent research —
  [`../agent_research/design_partners/DESIGN_PARTNER_COHORT.md`](../agent_research/design_partners/DESIGN_PARTNER_COHORT.md).
  Org packs + Batch tracker are production ops for copilot + B2C, not part of the v4 model home.

## Two complementary lenses (this is the important part)

SuperCat segments the *same* install base on **two orthogonal, first-party axes**. They are not
competitors; they answer different questions and feed different work.

- **Lens 1 — Digital Selling Maturity** (3 segments: Catalog-Focused / Commerce-Active /
  Platform-Embedded). Axis = *how digitally enabled their commercial operation is.* Predicts product
  need, willingness-to-pay, tier, and expansion path. This is the **pricing / monetization lens**.
  Source: `skills/monetization_refresh_2026/11_synthesis/PRICING_CONSTITUTION.md` (D-001a, stamped
  2026-01-28); summarized in [`../../foundation/02_who_we_serve.md`](../../foundation/02_who_we_serve.md).
- **Lens 2 — Selling Motion v4.0** (this folder; 4 segments: Luxury Specification / Premium Trade
  Brand / Mid-Market Multi-Channel / Volume Distribution). Axis = *how they go to market.* Predicts
  product-identity vocabulary, buyer mix, and taste. This is the **GTM / product-identity / buyer
  lens**, and the axis that powers `brand_to_customer` profiling.

Both lenses **reject revenue band and industry vertical as classifiers** (each was tested and found
non-predictive). They cross-tabulate: a Platform-Embedded account can be Premium Trade Brand or
Volume; a Luxury Specification brand can be Catalog-Focused or Platform-Embedded.

## The three classification axes (v4.0)

The v4.0 enrichment tested three axes and found **selling motion is the classifier**; the other two
are *dimensions within* segments, not cuts:

1. **How they sell** — the primary segmenting axis (the 4 selling motions above).
2. **What they sell** — product vertical (furniture, lighting, outdoor, accessories, decor, rugs,
   textiles). A *tag*, not a segment — lighting spans all four segments; furniture spans three.
3. **Who they sell to** — buyer type (trade/designers, wholesale/dealers, mixed, retail, contract).
   Almost perfectly predicted by selling motion at the *brand* level — but the **account-level**
   buyer type must be resolved from account evidence, not inherited (see `brand_to_customer`).

## Count caveat

This roster is **n=109** (the v4.0 universe). The Digital Selling Maturity segmentation baseline is
**n=104** (master data v3, M1 segmentation). Other valid sources cite 110 / 118 / 132 under different
inclusion rules and dates. None is wrong; there is no single canonical "as-of now" count. Use the one
matching your data window and say which. See the count caveat in
[`../../foundation/02_who_we_serve.md`](../../foundation/02_who_we_serve.md).

## Who consumes this

- [`../../foundation/02_who_we_serve.md`](../../foundation/02_who_we_serve.md) — cites this as the
  source for the Selling Motion lens and the deepened "our customers' customers" model.
- [`../../foundation/CEO_SYSTEM_CONTEXT.md`](../../foundation/CEO_SYSTEM_CONTEXT.md) — carries a
  condensed version of both lenses into the 10 CEO System prompts that read foundation context at runtime.
  This runtime file (not `02`) is the customer ontology the prompts actually see.
- [`../agent_research/brand_to_customer/PROFILE_SYNTHESIS.md`](../agent_research/brand_to_customer/PROFILE_SYNTHESIS.md)
  Step 0a — looks up the brand's `v4_segment` + how/what/who here to set catalog vocabulary.

## Feedback loop (how this sharpens over time)

`brand_to_customer` runs produce two facts per account: **0a** the brand's v4 segment (from this
roster) and **0b** the account's *actual* buyer type, resolved from the customer's own web evidence
(consumer/omnichannel retailer vs trade-led showroom/dealer vs designer/trade vs distributor). Each run
appends a row — `{date, org, org_id, customer_num, customer_name, brand_segment, vertical,
account_buyer_type, sales_channel, channel_posture, resolution_confidence, ecat_vs_invoiced_ratio,
evidence, identity_sentence, run_file}` — to [`account_buyer_type_reads.csv`](account_buyer_type_reads.csv).
The quarterly `02_who_we_serve.md` refresh reads that index to move the "our customers' customers" view
from general classification toward evidence-based per-account truth — this is the mechanism by which the
system's view of our customers' customers gets radically sharper as more presentations are produced.

**Coverage is honest, not aspirational.** The index is live with **3 reads** (of ~109 orgs); it is a
seed, not a census. Do not describe it as a completed per-account buyer census until coverage is
materially higher — say "3 evidence reads so far" and cite the file.
