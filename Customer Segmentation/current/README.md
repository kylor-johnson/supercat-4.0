# Customer Segmentation — current

**Active baseline:** stamped **v4.0** (Kjael, 2026-07-09) — supersedes v3.2.

| What | Where |
|---|---|
| Stamped analysis | `./SuperCat_Client_Segmentation_v4.0.md` |
| Stamped roster (109 rows, all dimensions) | `./SuperCat_Customer_Segmentation_v4.0_MASTER.csv` |
| Stamp-ready HTML (regenerated post Round 3) | `./SuperCat_Client_Segmentation_v4.0.html` |
| HTML builder | `./build_segmentation_html.py` |
| Build script (reproducible CSV) | `../v4/v4.0_archive/build_v4.py` |
| Unmatched-account validation (errata, applied post-stamp) | `../v4/v4.0_archive/unmatched_accounts_validation_2026-07-09.md` |
| Prior baseline (superseded) | `../v3/v3.2/` |
| TAM off-platform client fields | `../data/TAM_enriched_Customers.csv` |
| Propagation handoff | `../handoffs/segmentation_v4.0_stamped_handoff.md` |

## Status

**v4.0 is the current stamped model — 4 segments, 109 accounts** (Luxury Specification 33 /
Premium Trade Brand 38 / Mid-Market Multi-Channel 24 / Volume Distribution 14 — these totals
exactly match what Kjael originally stamped). Three rounds of post-stamp correction happened
(identity fix for Gabriella White / Summer Classics, then an independent Round 3 audit that
confirmed Round 2 and backfilled enrichment for five Round-1 matches) — see the errata note in
`SuperCat_Client_Segmentation_v4.0.md` and `unmatched_accounts_validation_2026-07-09.md`.

**The `v4.1` handoff (`../handoffs/segmentation_v4.1_handoff.md`) is stale/superseded.** It was
written earlier the same day (2026-07-09, ~10:28) as a plan to re-do the off-platform
selling-motion validation from scratch, on the assumption that v4.0's first pass was insufficient.
Before that plan was acted on, a further v4.0 pass (same day, ~11:09–11:17) added the three-axis
enrichment (how/what/who they sell) directly against v3.2 and Kjael reviewed and stamped it. **Do
not start a `v4.1` rebuild** — if a future revalidation is wanted, start from stamped v4.0, not v3.2.

**Next step (per the stamped model's own recommendation):** personas within segments.
