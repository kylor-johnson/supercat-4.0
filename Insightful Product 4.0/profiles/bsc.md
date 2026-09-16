# Client Profile — Butler Specialty Company (`bsc`)

> **Status:** AUTO-DERIVED 2026-07-14 — review output and correct any section that needs it.
>
> This profile was auto-populated by `pipeline/run_report.py` from live
> preflight/cache data (see `handoffs/profile_gate_removal.md`). It is
> treated as a ratified profile for pipeline purposes — SHIP output is not
> gated on human review. Edit any section below and re-run to correct it.

---

## 1. Identity (the hard key — prevents running the wrong org)

| Field | Value | How derived |
|---|---|---|
| Client name | Butler Specialty Company | `cache.resolve_org_name()` |
| `organization_id` (Postgres) | `14` | Q-ECON-00 preflight |
| Shortname | `bsc` | live |
| `report_through_date` policy | `LEAST(MAX(invoice_date), CURRENT_DATE)` | gate-computed → 2026-07-14 |

## 2. Business model / segment

- **Model:** accent / occasional furniture manufacturer.
- **Client segment (SuperCat v4.0, stamped):** Premium Trade Brand
- **How they sell (axis):** Brand-Building
- **What they sell (axis):** Furniture
- **Who they sell to (axis):** Wholesale (Broad Dealer Network)
- **Price (continuous, not a boundary):** best available unit price ≈ $411 (from Client Segmentation v4.0 MASTER; price is a correlate within segment, not the classifier)
- **Source:** `Customer Segmentation/current/SuperCat_Customer_Segmentation_v4.0_MASTER.csv` · stamped 2026-07-09 · join org=bsc · org_id=14 (verified)
- _Client segment above = SuperCat's stamped **selling-motion** class (Workstream A). It is distinct from the 🧊 FROZEN in-client customer segmentation (Q-SEG-DERIVE, Spine §8), which stays out of scope and is not a profile field._

## 3. Channel model (how they sell)

Preflight surface (live, 2026-07-14):
- `channel_posture` = `NONE` (0 distinct origins on 0 booked rows)
- eCat confirmed GMV LTM = $40,876 (0.0% of invoiced)

## 4. House / sample / marketplace accounts to screen

No per-org exclusions on file for `bsc` — auto-rules only (name patterns: `house%`, `% house account%`).

## 5. Buyer-type context

- Premium Trade Brand selling motion: **stocking-dealer reorder** is the default mental model for the base. The one-time tail is still a **conversion test**, not automatic churn.
- Default editorial standard still holds: treat one-time buyers as a **conversion opportunity**, not assumed churn.

## 6. Structural concentration (context, NOT a finding)

No `Q-ECON-CONC` data cached for this run — concentration context unavailable.

## 7. Report mode default + scope exclusions

- **Default mode (live gate):** `Gate-STOP` — the gate resolved this at preflight.
- **Hard-gap suppressions:** Detected from live side-channel flags: no returns data; no carrier / shipping-method mix data; no payment terms data; no lead-time data; no net-revenue freight adjustment data; no leakage dispersion data; no channel attribution data. Always suppressed (never in the ERP feed): margin/COGS, AR/DSO aging, competitive-loss reasons.

## 8. Sensitive callouts — per-client scrubbing policy

None configured — review output and add overrides if needed.

---

### Ratification log

- 2026-07-14 — AUTO-DERIVED by `pipeline/run_report.py` — pipeline
