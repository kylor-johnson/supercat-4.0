# Closeout — Client Segmentation v4.0 propagation into Insightful Product 4.0

> **Date:** 2026-07-20 · **Scope:** thin consumption layer only (Workstream A → Insightful
> interpretation layer). Companion CHANGELOG entry: `../CHANGELOG.md` (2026-07-20).

## What this was

Stamp SuperCat's **Client Segmentation v4.0** (the ~109 client orgs classified by **selling
motion** — Luxury Specification / Premium Trade Brand / Mid-Market Multi-Channel / Volume
Distribution; `Customer Segmentation/current/`, stamped Kjael 2026-07-09) into Insightful's
per-client profiles and interpretation-layer docs.

This is **Workstream A** (how the client org goes to market). It is deliberately **not** Workstream B
(the frozen in-client customer segmentation — behavior clusters of buyers *inside* one client's book,
`../foundation/segmentation_derivation.md` / Q-SEG-DERIVE, Spine §8). The prior profile wording
"segmentation is 🧊 FROZEN per Spine §8" on the **client-segment** line misapplied Spine §8 (which
governs Workstream B) and has been corrected.

## Source of truth

`Customer Segmentation/current/SuperCat_Customer_Segmentation_v4.0_MASTER.csv` (109 rows, stamped
2026-07-09). Join key = org shortname, verified against profile `organization_id` == MASTER `org_id`.
Table below was rebuilt live from the CSV on 2026-07-20 (not from memory).

## Files changed

Profiles (§2 stamped; §5 where noted):
- `../profiles/profile_template.md` — §2 schema + Workstream A vs B note
- `../profiles/sarreid.md` — §2
- `../profiles/cci.md` — §2
- `../profiles/hfg.md` — §2 (kept descriptive "Price point" line)
- `../profiles/kal.md` — §2
- `../profiles/sca.md` — §2
- `../profiles/ali.md` — §2 + §5
- `../profiles/ali.draft.md` — §2 (DRAFT status retained)
- `../profiles/bri.md` — §2 + §5
- `../profiles/bri.draft.md` — §2 (DRAFT placeholders otherwise retained)
- `../profiles/da.md` — §2 + §5
- `../profiles/da.draft.md` — §2 (DRAFT placeholders otherwise retained)
- `../profiles/bsc.md` — §2 + §5
- `../profiles/clc.md` — §2 + §5
- `../profiles/bmc.md` — §2 gap note (unassigned)

Docs + pipeline doc-string:
- `../knowledge/industry_context.md` — new "Selling-motion segments … (context, not findings)" section
- `../pipeline/run_report.py` — auto-derive profile §2 **draft doc-string** only (stamp-from-MASTER
  instruction replacing the "dealer-distribution manufacturer" default)
- `../CHANGELOG.md` — newest-first entry
- this file

## Per-org before → after (§2 client segment)

| org | org_id (verified) | before (§2 wording) | after — Client segment (v4.0) | how / what / who | best_price | §5 change |
|---|---|---|---|---|---|---|
| sarreid | 1 | "dealer-distribution furniture … FROZEN per Spine §8" | **Luxury Specification** | Specification / Decor/Art / Trade (Designers/Architects) | $968 | no (already aligned) |
| cci | 161 | "dealer-distribution lighting/decor … FROZEN per Spine §8" | **Luxury Specification** | Specification / Lighting / Trade (Designers/Architects) | $624 | no (already aligned) |
| hfg | 165 | "dealer-distribution lighting/architectural … FROZEN per Spine §8" | **Premium Trade Brand** | Brand-Building / Lighting / Wholesale (Broad Dealer Network) | $846 | no (already aligned) |
| kal | 146 | "dealer-distribution lighting … FROZEN per Spine §8" | **Premium Trade Brand** | Brand-Building / Lighting / Wholesale (Dealers) | $647 | no (already aligned) |
| sca | 90 | "dealer-distribution lighting/décor … FROZEN per Spine §8" | **Mid-Market Multi-Channel** | Multi-Channel / Decor/Art / Wholesale (Dealers/Retailers) | $260 | no (ratified eCat-only prose) |
| ali | 127 | "Default: dealer-distribution manufacturer" | **Mid-Market Multi-Channel** | Multi-Channel / Lighting / Mixed (Trade + Retail) | $64 | yes (MMC framing) |
| ali (draft) | 127 | "Segment: Lighting" | **Mid-Market Multi-Channel** | Multi-Channel / Lighting / Mixed (Trade + Retail) | $64 | no (draft already aligned) |
| bri | 222 | "Default: dealer-distribution manufacturer" | **Volume Distribution** | Volume Distribution / Lighting / Wholesale (Retailers) | $12 | yes (VD framing) |
| bri (draft) | 222 | DRAFT-NEEDS-RATIFICATION | **Volume Distribution** | Volume Distribution / Lighting / Wholesale (Retailers) | $12 | no (draft) |
| da | 62 | "Default: dealer-distribution manufacturer" | **Premium Trade Brand** | Brand-Building / Lighting / Wholesale (Dealers) | $118 | yes (PTB framing) |
| da (draft) | 62 | DRAFT-NEEDS-RATIFICATION | **Premium Trade Brand** | Brand-Building / Lighting / Wholesale (Dealers) | $118 | no (draft) |
| bsc | 14 | "Default: dealer-distribution manufacturer" | **Premium Trade Brand** | Brand-Building / Furniture / Wholesale (Broad Dealer Network) | $411 | yes (PTB framing) |
| clc | 40 | "Default: dealer-distribution manufacturer" | **Mid-Market Multi-Channel** | Multi-Channel / Lighting / Wholesale (Dealers/Retailers) | $153 | yes (MMC framing) |
| bmc | 11 | "Default: dealer-distribution manufacturer" | **unassigned (gap)** | — | — | no |

All org_ids matched (profile `organization_id` == MASTER `org_id`). **No BLOCKED orgs.**

## bmc gap

`bmc` / org_id 11 (Bassett Mirror) is **not** on the stamped v4.0 109-org roster. §2 is marked
**Client segment: unassigned** with an escalation note; no segment was inferred. Action for a human:
add bmc to the roster (then stamp the schema) or deliberately exclude it.

## §3 tensions flagged (NOT rewritten — ratified channel prose preserved)

Per contract, §3 was not rewritten from MASTER. Tensions to be aware of:

1. **cci** — stamped **Luxury Specification / Trade (Designers/Architects)**, but ratified §3 describes
   a broad multi-channel mix with a large named **e-commerce / marketplace cluster** (Wayfair, Ferguson,
   Lumens, etc.) that renders as its own channel (`cluster_section`, ratified 2026-06-30). The selling-motion
   stamp (designer-specification) and the heavy e-commerce channel presence coexist; the stamp is by selling
   motion, not by channel breadth. Noted in the cci §2 clarifier. **No silent reconciliation.**
2. **sarreid** — ratified Model/§3 read as "furniture manufacturer … independent dealers + Wayfair
   marketplace," while MASTER records **what_they_sell = Decor/Art** and **who = Trade (Designers/Architects)**.
   Sarreid genuinely does reproduction/accent furniture *and* decor; the ratified facts were preserved, the
   segment/axes stamped, and the tension noted here rather than overwriting §3.
3. **sca** — stamped **Mid-Market Multi-Channel** from catalog/order-behavior data, but sca has **no ERP
   invoice feed** (Tier-0 / behavior-only, permanent Mode-2 lock). The stamp is a fact about the org's selling
   motion; it does not change sca's report-mode routing. Noted in the sca §2 clarifier.
4. Minor / no conflict: **hfg** (Broad Dealer Network vs its e-commerce/DTC breadth) and **kal** (Wholesale
   Dealers vs its online-dealer cluster) are consistent enough with their Premium Trade Brand stamp; left as-is.

## OUT OF SCOPE (deliberately deferred / not touched)

- Re-running or "improving" Client Segmentation v4.0 / starting v4.1
- Unfreezing or altering Q-SEG-DERIVE / `../foundation/segmentation_derivation.md` method body
- Editing `../foundation/provenance_spine.md` rules (read-only here)
- Selling-motion **peer medians** / BigQuery peer rebuild / `segment_peer_comparison`
- Personas into Rep Copilot or prose
- Emitting client segment labels in HTML / templates / communication guideline as client-facing copy
- `../../foundation/02_who_we_serve.md` / ICP refresh (separate workstream)
- Legacy Insightful 2.0 / 3.0
- Jira writes; git commits (none made)
- SHIP HTML, prose JSON fact numbers, golden checksums (`config/golden_set.json`)
- Inventing a segment for bmc or any unmatched org

## Verification run (2026-07-20)

- `grep "FROZEN per Spine §8"` across `../profiles/` on client-segment lines → **0** (the remaining
  matches, if any, are the §7 hard-gap "segmentation — not in feed" lines, which correctly refer to
  Workstream B absence and were intentionally left).
- `grep "5 segments" / "Specialty"` across `../foundation/` → only the existing scope-note guard in
  `segmentation_derivation.md` (no contradiction with v4.0's 4-segment model).
- `python3 -m py_compile pipeline/run_report.py` → OK.
- Not modified: `provenance_spine.md` method, `segmentation_derivation.md` method body,
  `query_library_v2.md`, `signals.py`, Jinja templates, golden HTML, `config/golden_set.json` checksums.
- Because only profiles/docs/CHANGELOG + the run_report.py draft doc-string changed, **no golden
  rebaseline was run** (none required).
