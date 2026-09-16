# Client Profile — Access Lighting (`ali`)

> **Status:** AUTO-DERIVED 2026-07-09 — review output and correct any section that needs it.
>
> This profile was auto-populated by `pipeline/run_report.py` from live
> preflight/cache data (see `handoffs/profile_gate_removal.md`). It is
> treated as a ratified profile for pipeline purposes — SHIP output is not
> gated on human review. Edit any section below and re-run to correct it.

---

## 1. Identity (the hard key — prevents running the wrong org)

| Field | Value | How derived |
|---|---|---|
| Client name | Access Lighting | `cache.resolve_org_name()` |
| `organization_id` (Postgres) | `127` | Q-ECON-00 preflight |
| Shortname | `ali` | live |
| `report_through_date` policy | `LEAST(MAX(invoice_date), CURRENT_DATE)` | gate-computed → 2026-06-29 |

## 2. Business model / segment

- **Model:** decorative / architectural lighting manufacturer (wholesale B2B).
- **Client segment (SuperCat v4.0, stamped):** Mid-Market Multi-Channel
- **How they sell (axis):** Multi-Channel
- **What they sell (axis):** Lighting
- **Who they sell to (axis):** Mixed (Trade + Retail)
- **Price (continuous, not a boundary):** best available unit price ≈ $64 (from Client Segmentation v4.0 MASTER; price is a correlate within segment, not the classifier)
- **Source:** `Customer Segmentation/current/SuperCat_Customer_Segmentation_v4.0_MASTER.csv` · stamped 2026-07-09 · join org=ali · org_id=127 (verified)
- _Client segment above = SuperCat's stamped **selling-motion** class (Workstream A). It is distinct from the 🧊 FROZEN in-client customer segmentation (Q-SEG-DERIVE, Spine §8), which stays out of scope and is not a profile field._

## 3. Channel model (how they sell)

Preflight surface (live, 2026-06-29):
- `channel_posture` = `NONE` (1 distinct origins on 29,678 booked rows)
- eCat confirmed GMV LTM = $410 (0.0% of invoiced)

## 4. House / sample / marketplace accounts to screen

No per-org exclusions on file for `ali` — auto-rules only (name patterns: `house%`, `% house account%`).

## 5. Buyer-type context

- Mid-Market Multi-Channel selling motion: the book mixes **trade + retail + online** buyers — do NOT assume a single buyer type. Cadence findings must respect the channel mix (a marketplace/online buyer, a stocking dealer, and a designer/project buyer are not the same silence).
- Default editorial standard still holds: treat one-time buyers as a **conversion opportunity**, not assumed churn.

## 6. Structural concentration (context, NOT a finding)

Top-1 customer = **7.6%** of LTM invoiced net (top-10 = 39.4%, HHI 225). Confirm whether this reflects a known-structural account (e.g. a marketplace/drop-ship partner) before treating it as a finding.

## 7. Report mode default + scope exclusions

- **Default mode (live gate):** `Mode 1 - Standard` — the gate resolved this at preflight.
- **Hard-gap suppressions:** Detected from live side-channel flags: no carrier / shipping-method mix data; no net-revenue freight adjustment data; no leakage dispersion data; no channel attribution data. Always suppressed (never in the ERP feed): margin/COGS, AR/DSO aging, competitive-loss reasons.

## 8. Sensitive callouts — per-client scrubbing policy

None configured — review output and add overrides if needed.

---

### Ratification log

- 2026-07-09 — AUTO-DERIVED by `pipeline/run_report.py` — pipeline
