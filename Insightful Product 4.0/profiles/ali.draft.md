# Client Profile — Access Lighting (`ali`)

> **What this is.** Reading-contract input #2 (see [`../CANON.md`](../CANON.md)): derived draft profile for cohort-validation run.
>
> **Status:** DRAFT (derived inline 2026-06-17, not ratified) — human ratification required before client-facing use.

---

## 1. Identity (the hard key — prevents running the wrong org)

| Field | Value | How derived |
|---|---|---|
| Client name | Access Lighting | `organizations.name` (org 127) |
| `organization_id` (Postgres) | 127 | `Q-ECON-00` preflight |
| Shortname | `ali` | ratified input |
| Same-name disambiguation | None identified — `ali` resolves uniquely to Access Lighting (org 127) | preflight |
| `report_through_date` policy | `LEAST(MAX(invoice_date), CURRENT_DATE)` → **2026-06-26** (live) | gate-computed |

## 2. Business model / segment

- **Model:** Decorative/architectural **lighting manufacturer** (wholesale B2B).
- **Client segment (SuperCat v4.0, stamped):** Mid-Market Multi-Channel
- **How they sell (axis):** Multi-Channel
- **What they sell (axis):** Lighting
- **Who they sell to (axis):** Mixed (Trade + Retail)
- **Price (continuous, not a boundary):** best available unit price ≈ $64 (from Client Segmentation v4.0 MASTER; price is a correlate within segment, not the classifier)
- **Source:** `Customer Segmentation/current/SuperCat_Customer_Segmentation_v4.0_MASTER.csv` · stamped 2026-07-09 · join org=ali · org_id=127 (verified)
- _Client segment above = SuperCat's stamped **selling-motion** class (Workstream A). It is distinct from the 🧊 FROZEN in-client customer segmentation (Q-SEG-DERIVE, Spine §8), which stays out of scope and is not a profile field. (Draft otherwise still pending human ratification.)_

## 3. Channel model (how they sell)

- Independent **rep agencies** carry the field book; **online retailers / marketplaces** (Lamps Plus, Lumens, Ferguson, Home Depot, Lowe's, Belami/1 Stop Lighting, Zoro) are a material share of invoiced volume, largely on rep **29 / BRAND JUMP LLC**.
- **eCat capture is negligible** (~$410 LTM confirmed GMV, 2 orders) — the business runs through ERP invoicing, not the iPad app.
- `order_origin` is a **single bucket** (100% attributed, 1 distinct value, eCat not tagged) — channel split suppressed per `Q-CHAN-00 = NONE`.

## 4. House / sample / marketplace accounts to screen

- **House rep label:** `HOUSE ACCOUNTS` (rep 36) — auto-excluded via `house%` screen (~$515K LTM invoiced; not coached).
- **House bill-to patterns (standard):** `ZZ*`, `ACCOM*`, `SAMPLE*`, `HOUSE*`, `DISPLAY*`, `SHOWROOM*`, `TEST*`.
- **Marketplace / drop-ship accounts (context — screen from per-dealer dispersion, not from rep leaderboard):** Lamps Plus Online, Lumens, FergusonHome.com, Home Depot, Lowe's, 1 Stop Lighting/Belami, Zoro, Lighting NY E-COM — large, structurally different from stocking dealers; treat concentration as context unless paired with decay or rep-specific risk.
- **Data-quality bucket:** **blank `customer_bill_to_number`** (~$745K LTM, 371 invoices, 43 rep codes) — not a single account; ERP hygiene issue. Exclude from customer-facing concentration claims until reconciled.
- **Named exclusions (per-org EXCLUDE table):** none yet — owner should confirm whether `HOUSE ACCOUNTS` rep label and blank bill-to handling are complete.

## 5. Buyer-type context

- Mix of **electrical distributors / wholesalers**, **online retailers**, and **design-trade / project** buyers (e.g., Ignite Concepts Lighting Design, Power Design Inc).
- Marketplace and project buyers have **different cadence** than stocking dealers — silence thresholds must respect buyer type; do not call a completed project "churn."

## 6. Structural concentration (context, NOT a finding)

- **Rep-agency concentration:** BRAND JUMP LLC (~$2.43M, ~33% of invoiced LTM) is structurally large because it carries the online-retailer book — expected for a lighting manufacturer with marketplace presence, but worth monitoring if the agency relationship changes.
- **Customer concentration (named accounts):** top named bill-to (Lamps Plus Online) ~6.5% of positive invoiced revenue; top-10 named accounts ~44% — normal for lighting with marketplace mix once the blank bill-to bucket is excluded.
- **Product concentration:** LED drivers/modules and filament/vanity SKUs dominate the top of the item list — typical for an LED-forward lighting line.

## 7. Report mode default + scope exclusions

- **Default mode:** 1 Standard — gate confirms `COMMERCE_CONFIDENCE = STRONG`, invoice feed present (since **2025-07-01** only; no prior-year YoY window yet).
- **Confirmed hard-gap suppressions for this org:**
  - **Price-realization leakage (Q-ECON-LEAK / C2):** suppressed — only **6.5%** priced invoice lines (`leakage_dispersion_ok = false`).
  - **Channel decomposition:** suppressed — `Q-CHAN-00 = NONE` (single `order_origin` bucket; eCat not tagged).
  - **YoY momentum:** not available — feed < 24 months (first invoice 2025-07-01).
  - **Margin/COGS, AR/DSO, carrier analytics, segmentation:** schema gaps per Spine §6.9.
  - **eCat quote→purchase rate:** suppressed — eCat share < 20% of commerce.

---

### Ratification log
- 2026-06-17 — Inline draft derived from Step-1 preflight (`Q-ECON-00`, `Q-CHAN-00`, RP-2, concentration queries) under `--cohort-validation` — pending human ratification.
