# Client Profile — Bulbrite (`bri`)

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
| Client name | Bulbrite | `cache.resolve_org_name()` |
| `organization_id` (Postgres) | `222` | Q-ECON-00 preflight |
| Shortname | `bri` | live |
| `report_through_date` policy | `LEAST(MAX(invoice_date), CURRENT_DATE)` | gate-computed → 2026-07-01 |

## 2. Business model / segment

- **Model:** lighting / lamp (bulb) manufacturer-distributor.
- **Client segment (SuperCat v4.0, stamped):** Volume Distribution
- **How they sell (axis):** Volume Distribution
- **What they sell (axis):** Lighting
- **Who they sell to (axis):** Wholesale (Retailers)
- **Price (continuous, not a boundary):** best available unit price ≈ $12 (from Client Segmentation v4.0 MASTER; price is a correlate within segment, not the classifier)
- **Source:** `Customer Segmentation/current/SuperCat_Customer_Segmentation_v4.0_MASTER.csv` · stamped 2026-07-09 · join org=bri · org_id=222 (verified)
- _Client segment above = SuperCat's stamped **selling-motion** class (Workstream A). It is distinct from the 🧊 FROZEN in-client customer segmentation (Q-SEG-DERIVE, Spine §8), which stays out of scope and is not a profile field._

## 3. Channel model (how they sell)

Preflight surface (live, 2026-07-01):
- `channel_posture` = `NONE` (1 distinct origins on 117,082 booked rows)
- eCat confirmed GMV LTM = $3,478,845 (16.4% of invoiced)

## 4. House / sample / marketplace accounts to screen

No per-org exclusions on file for `bri` — auto-rules only (name patterns: `house%`, `% house account%`).

## 5. Buyer-type context

- Volume Distribution selling motion: a **replenishment / retailer-procurement** cadence. Extreme account concentration and a very low unit price are **structurally common** for this segment — do NOT "discover" commodity concentration as a surprise without a second fact (it's growing dangerously, declining, or tied to a single rep/relationship).
- Default editorial standard still holds: treat one-time buyers as a **conversion opportunity**, not assumed churn.

## 6. Structural concentration (context, NOT a finding)

Top-1 customer = **3.5%** of LTM invoiced net (top-10 = 26.6%, HHI 112). Confirm whether this reflects a known-structural account (e.g. a marketplace/drop-ship partner) before treating it as a finding.

## 7. Report mode default + scope exclusions

- **Default mode (live gate):** `Mode 1 - Tier-1 degraded` — the gate resolved this at preflight.
- **Hard-gap suppressions:** Detected from live side-channel flags: no payment terms data; no lead-time data; no net-revenue freight adjustment data; no channel attribution data. Always suppressed (never in the ERP feed): margin/COGS, AR/DSO aging, competitive-loss reasons.

## 8. Sensitive callouts — per-client scrubbing policy

None configured — review output and add overrides if needed.

---

### Ratification log

- 2026-07-09 — AUTO-DERIVED by `pipeline/run_report.py` — pipeline
