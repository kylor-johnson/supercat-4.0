# Client Profile — Sarreid, Ltd. (`sarreid`)

> **What this is.** Reading-contract input #2 (see [`../CANON.md`](../CANON.md)): the cached, human-ratified
> statement of Sarreid's **stable context**. Loaded after `foundation/provenance_spine.md`, before
> `knowledge/industry_context.md`. **Facts and scope decisions only — no findings, no framing.** See
> [`README.md`](README.md) for the allowed/forbidden rule.
>
> **Status:** RATIFIED 2026-06-29 (initial seed reverse-engineered from an earlier dry-run; re-ratified
> later the same day against the regenerated, gate-determined worked example at
> [`../outputs/Sarreid_CEO_intelligence_report_2026-06-29.md`](../outputs/Sarreid_CEO_intelligence_report_2026-06-29.md),
> which now stands as the canon-compliant Sarreid run — both earlier outputs superseded into `_archive/`). Facts here
> still hold: identity, channel model, house/sample/Wayfair screen, designer-project buyer note, Wayfair/single-rep
> structural concentration, Standard mode, hard-gap suppressions. Re-ratify only if the business structure changes.

---

## 1. Identity (the hard key — prevents running the wrong org)

| Field | Value | How derived |
|---|---|---|
| Client name | Sarreid, Ltd. | ratified |
| `organization_id` (Postgres) | `1` | `Q-ECON-00` preflight |
| Shortname | `sarreid` | ratified |
| Same-name disambiguation | `fal` is a **different** company (Fine Art Handcrafted Lighting) — not this org | ratified |
| `report_through_date` policy | `LEAST(MAX(invoice_date), CURRENT_DATE)` | gate-computed |
| Rep-identity tier | **Tier 2** (named; name-bridge 100%) | RP-2 gate (`../operators/rep_copilot_operator.md` §1) |

## 2. Business model / segment

- **Model:** furniture manufacturer selling into a dealer/retail base.
- **Client segment (SuperCat v4.0, stamped):** Luxury Specification
- **How they sell (axis):** Specification
- **What they sell (axis):** Decor/Art
- **Who they sell to (axis):** Trade (Designers/Architects)
- **Price (continuous, not a boundary):** best available unit price ≈ $968 (from Client Segmentation v4.0 MASTER; price is a correlate within segment, not the classifier)
- **Source:** `Customer Segmentation/current/SuperCat_Customer_Segmentation_v4.0_MASTER.csv` · stamped 2026-07-09 · join org=sarreid · org_id=1 (verified)
- _Client segment above = SuperCat's stamped **selling-motion** class (Workstream A). It is distinct from the 🧊 FROZEN in-client customer segmentation (Q-SEG-DERIVE, Spine §8), which stays out of scope and is not a profile field._

## 3. Channel model (how they sell)

- Sells through **independent dealers** plus **one drop-ship marketplace account (Wayfair)**.
- **eCat is a minority channel (historically under ~20%, booked intent only)** — dollars only, never shown as a "share."
  This overrides any industry-default channel weighting in `../knowledge/industry_context.md`.

## 4. House / sample / marketplace accounts to screen

Excluded from leakage and leadership-facing same-SKU dispersion:

- House/sample bill-to patterns: `ZZ*`, `HOUSE*`, `ACCOM*`, `SAMPLE*`, `DISPLAY*`, `SHOWROOM*`, `TEST*`.
- **Wayfair** handled separately: screened from per-dealer price-dispersion (marketplace drop-ship, not a comparable dealer).
- Configuration is **already excluded** from dispersion by construction (finish is encoded in the item number, so
  same-item compares are like-for-like).
- _Scope decision: this sets which rows the leakage math runs on; the dollar itself is computed live and ships DIRECTIONAL._

## 5. Buyer-type context

- A meaningful share of one-time buyers are **designer / project purchases** — treat the one-time tail as a
  **conversion test, not assumed churn**. (Frame the pattern; do not pre-judge it.)

## 6. Structural concentration (context, NOT a finding)

- The **Wayfair** marketplace account is a **structurally large share** of the company (roughly a third, historically)
  and runs through a **single rep** (`rep_number = '099'`, Charles Hoffman). This is **known, structural** — the
  report should not "discover" it as a surprise.
- The exact share, growth, and rep-book percentage are **recomputed live each run**; no number is fixed here.

## 7. Report mode default + scope exclusions

- **Default mode:** **1 — Standard** (clean invoiced feed; the gate still resolves mode live and overrides this if data changes).
- **Confirmed hard-gap suppressions** (no faking — surface as upsell only):
  - **Gross/true margin** — no cost/COGS feed (the headline upsell, given Wayfair).
  - **Returns** — no credit memos in feed (disclosed, not read as zero).
  - **Collections / AR / DSO** — terms billed, not collected.
  - **Stock-outs** — backorder field unpopulated.
  - **Confirmed competitive loss** — needs a second booking feed.
  - **Carrier/damage, inventory aging, market ROI, segmentation** — not in feed / out of scope.

---

### Ratification log
- 2026-06-29 — Initial ratification; facts read off the live-pulled dry-run appendix (identity, channel model,
  house/sample + Wayfair screen, designer-project buyer note, Wayfair/single-rep structural concentration, Standard
  mode, hard-gap suppressions). No dollar findings carried into the profile. — Kylor
- 2026-06-29 (later) — **Re-ratified** against the regenerated, gate-determined Sarreid worked example
  (`../outputs/Sarreid_CEO_intelligence_report_2026-06-29.md`). No profile facts changed. Pointer was updated because
  the earlier two outputs (the original and the rerun) were superseded into `_archive/` during the same-day Sarreid
  reconciliation pass (see `../CHANGELOG.md` 2026-06-29 entry). — Kylor
