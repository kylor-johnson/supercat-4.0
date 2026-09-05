# SuperCat Segmentation v4.0 Stamp Packet

**Prepared for:** Kylor stamp decision
**Date:** July 7, 2026
**Recommendation:** Stamp v4.0 as a reset/refinement of v3.2, with the 8 candidates retained as review flags and no segment moves applied.

## Stamp Decision

- **Stamp candidate:** `Customer Segmentation/current/SuperCat_Client_Segmentation_v4.0.html`
- **Source document:** `Customer Segmentation/current/SuperCat_Client_Segmentation_v4.0.md`
- **Data file:** `Customer Segmentation/current/SuperCat_Customer_Segmentation_v4.0_MASTER.csv`
- **Persona starter:** `Customer Segmentation/current/SuperCat_Segment_Personas_v4.0_STARTER.md`

## What You Are Stamping

- v3.2 segment membership is preserved across all 109 orgs.
- Segment counts remain `34 / 31 / 26 / 13 / 5`.
- Postgres enrichment is added as context, not used as classifier logic.
- `fms` AOV is corrected from `$92,048` to `$3,649`.
- Lifetime invoiced revenue is excluded because it is not time-windowed or deduplicated.

## Review Candidate Decision

Keep the 8 candidates in the package as a review watchlist. They should not block stamping because corrected v4.0 does not move them; they are only a reminder that a future real-world selling-motion review could revisit them.

| Company | org | Current Segment | Default Decision |
|---|---|---|---|
| Currey & Company | cci | 1. Luxury Specification | Hold in Luxury Specification unless Kylor chooses to move it |
| Hooker Furnishings | hf | 1. Luxury Specification | Hold in Luxury Specification unless Kylor chooses to move it |
| Rowe Furniture | rf | 1. Luxury Specification | Hold in Luxury Specification unless Kylor chooses to move it |
| Sarreid, Ltd. | sarreid | 1. Luxury Specification | Hold in Luxury Specification unless Kylor chooses to move it |
| Charleston Forge | cfg | 1. Luxury Specification | Hold in Luxury Specification unless Kylor chooses to move it |
| Four Seasons Furniture | fsf | 1. Luxury Specification | Hold in Luxury Specification unless Kylor chooses to move it |
| Alden Home | ap | 1. Luxury Specification | Hold in Luxury Specification unless Kylor chooses to move it |
| Magnussen Home | mh | 3. Mid-Market Multi-Channel | Hold in Mid-Market Multi-Channel unless Kylor chooses to move it |

## Stamp Checklist

- [ ] HTML reads as a 5-minute review artifact.
- [ ] Segment counts match v3.2.
- [ ] Candidate flags are acceptable as notes, not moves.
- [ ] Persona work can start from these segment definitions.

## Recommended Stamp Note

> Stamped by Kylor as corrected v4.0: v3.2 membership preserved, Postgres enrichment added, fms AOV corrected, no revenue layer, and review candidates held as flags only.
