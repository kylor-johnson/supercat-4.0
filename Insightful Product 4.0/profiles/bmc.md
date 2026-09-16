# Client Profile — Bassett Mirror (`bmc`)

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
| Client name | Bassett Mirror | `cache.resolve_org_name()` |
| `organization_id` (Postgres) | `11` | Q-ECON-00 preflight |
| Shortname | `bmc` | live |
| `report_through_date` policy | `LEAST(MAX(invoice_date), CURRENT_DATE)` | gate-computed → 2025-11-28 |

## 2. Business model / segment

- **Model:** mirror / home-décor manufacturer (accent furniture and wall décor).
- **Client segment:** **unassigned** — org `bmc` / org_id 11 (Bassett Mirror) is **not** on the stamped Client Segmentation v4.0 109-org roster. Do not infer a selling-motion segment. Escalate for roster inclusion or deliberate exclusion.
- **Source:** checked against `Customer Segmentation/current/SuperCat_Customer_Segmentation_v4.0_MASTER.csv` (stamped 2026-07-09) — no row for org=bmc / org_id=11.
- _When bmc is added to the roster, stamp the schema (Client segment + how/what/who axes + continuous best_price + verified org_id) like every other profile. This "Client segment" line is SuperCat's stamped **selling-motion** class (Workstream A); it is distinct from the 🧊 FROZEN in-client customer segmentation (Q-SEG-DERIVE, Spine §8), which stays out of scope and is not a profile field._

## 3. Channel model (how they sell)

Preflight surface (live, 2025-11-28):
- `channel_posture` = `NONE` (0 distinct origins on 1,604 booked rows)
- eCat confirmed GMV LTM = $635,404 (9.1% of invoiced)

## 4. House / sample / marketplace accounts to screen

No per-org exclusions on file for `bmc` — auto-rules only (name patterns: `house%`, `% house account%`).

## 5. Buyer-type context

Default editorial standard: treat one-time buyers as a **conversion opportunity**, not assumed churn.

## 6. Structural concentration (context, NOT a finding)

Top-1 customer = **11.7%** of LTM invoiced net (top-10 = 38.9%, HHI 302). Confirm whether this reflects a known-structural account (e.g. a marketplace/drop-ship partner) before treating it as a finding.

## 7. Report mode default + scope exclusions

- **Default mode (live gate):** `Mode 1 - Tier-1 degraded` — the gate resolved this at preflight.
- **Hard-gap suppressions:** Detected from live side-channel flags: no returns data; no net-revenue freight adjustment data; no channel attribution data. Always suppressed (never in the ERP feed): margin/COGS, AR/DSO aging, competitive-loss reasons.

## 8. Sensitive callouts — per-client scrubbing policy

None configured — review output and add overrides if needed.

---

### Ratification log

- 2026-07-09 — AUTO-DERIVED by `pipeline/run_report.py` — pipeline
