# Client Profile — Currey & Company (`cci`)

> **What this is.** Reading-contract input #2 (see [`../CANON.md`](../CANON.md)): the cached, human-ratified
> statement of Currey & Company's **stable context**. Loaded after `foundation/provenance_spine.md`, before
> `knowledge/industry_context.md`. **Facts and scope decisions only — no findings, no framing.** See
> [`README.md`](README.md) for the allowed/forbidden rule and the derive→ratify→cache workflow.
>
> **Status:** RATIFIED 2026-06-30 — §8 cluster question resolved (`cluster_section` for the e-commerce /
> marketplace cluster, revisit after first client-facing run); §1–§7 sanity-checked against the cci PASS3
> output and accepted as live-derived facts. See Ratification log.

---

## 1. Identity (the hard key — prevents running the wrong org)

| Field | Value | How derived |
|---|---|---|
| Client name | Currey & Company | confirmed via `organizations.name` |
| `organization_id` (Postgres) | `161` | `Q-ECON-00` preflight |
| Shortname | `cci` | confirmed via `organizations.shortname` |
| Same-name disambiguation | none flagged in cohort | preflight |
| `report_through_date` policy | `LEAST(MAX(invoice_date), CURRENT_DATE)` | gate-computed (2026-06-29, 1 day fresh) |
| Rep-identity tier | **Tier 2** (named; name-bridge 100.0% — 54 of 54 invoice reps) | RP-2 gate (`../operators/rep_copilot_operator.md` §1) |

## 2. Business model / segment

- **Model:** lighting + home-decor manufacturer (chandeliers, pendants, sconces, lamps, mirrors, case goods).
- **Client segment (SuperCat v4.0, stamped):** Luxury Specification
- **How they sell (axis):** Specification
- **What they sell (axis):** Lighting
- **Who they sell to (axis):** Trade (Designers/Architects)
- **Price (continuous, not a boundary):** best available unit price ≈ $624 (from Client Segmentation v4.0 MASTER; price is a correlate within segment, not the classifier)
- **Source:** `Customer Segmentation/current/SuperCat_Customer_Segmentation_v4.0_MASTER.csv` · stamped 2026-07-09 · join org=cci · org_id=161 (verified)
- _Client segment above = SuperCat's stamped **selling-motion** class (Workstream A). The stamped Trade/Specification motion coexists with cci's broad §3 channel mix (incl. the named e-commerce/marketplace cluster) — see §3; segment is not re-derived from channel breadth. It is distinct from the 🧊 FROZEN in-client customer segmentation (Q-SEG-DERIVE, Spine §8), which stays out of scope and is not a profile field._

## 3. Channel model (how they sell)

- Sells through a **broad multi-channel mix**: independent lighting/furniture dealers + designer/trade
  buyers + e-commerce/marketplace accounts (Wayfair, Lumens, Ferguson family, Lamps Plus, Lighting New York,
  Pottery Barn, etc.) + market/showroom programs (High Point, Atlanta, Las Vegas, Dallas).
- **eCat is a minority channel for cci** — ~9–11% of invoiced LTM (booked-share 9.1% / capture share 11.4%);
  dollars only, never shown as a "share of business."
- This overrides any industry-default channel weighting in `../knowledge/industry_context.md`.

## 4. House / sample / marketplace accounts to screen

Excluded from leakage and leadership-facing same-SKU dispersion:

- House/sample bill-to patterns: `ZZ*`, `HOUSE*`, `ACCOM*`, `SAMPLE*`, `DISPLAY*`, `SHOWROOM*`, `TEST*`,
  `MODEL*`, `PHOTO*`, `MISC*`, `NOCHARGE*`, `NO CHARGE*`, `COMP *` (per RS-01 §3 inline list).
- **HOUSE ACCOUNT rep (`rep_number = HOUS`) is excluded from the rep leaderboard render** — auto-rule
  (`rep_label ILIKE 'house%'`) per [`../config/house_rep_exclusions.md`](../config/house_rep_exclusions.md);
  the bucket is $10.19M LTM / 112 accounts (surfaced beneath the leaderboard, cannot anchor a finding).
- Configuration / option pricing handled by the same-SKU dispersion engine (finish is encoded in
  `item_number`).
- _Scope decision: this sets which rows the leakage math runs on; the dollar itself is computed live and
  ships DIRECTIONAL._

## 5. Buyer-type context

- A meaningful share of the active dealer base are **designer / project / trade buyers** — the LTM
  one-time tail is 2,942 accounts spending $6.1M (8% of revenue). Treat the one-time tail as a
  conversion test, not assumed churn.
- The new-dealer cohort (3,295 first-timers prior LTM) returns at the **upper end of the industry-normal
  25–45% second-year band** (41.1%) — frame the gap as conversion opportunity, not failure.

## 6. Structural concentration (context, NOT a finding)

- **Top customer share is moderate** — Wayfair $4.59M LTM = **6.04% of the company** (top-1); top-5 share
  12.39%; top-10 share 16.34%; HHI 55. No single account is structurally dominant. Per §8 below this
  surfaces in body prose, not a standalone decision block.
- **The named e-commerce / marketplace cluster is a structurally large channel** — Wayfair, Ferguson
  Enterprises, Ferguson Home, Lumens, Lamps Plus, Lighting New York, Pottery Barn, Lulu and Georgia,
  Lightology, Lightopia, Lighting Star sum to a meaningful share of the dealer base; several reach
  through `rep_number = HOUS` (house account routing). This is known and structural; the share is
  recomputed live each run.
- No single-rep concentration on the field team (top rep Robbins $3.97M = 5.7% of company; top-2 reps
  sum ~11%).

## 7. Report mode default + scope exclusions

- **Default mode:** **1 — Standard** (clean invoice feed, fresh, internally consistent; the gate still
  resolves mode live and overrides this if data changes).
- **Confirmed hard-gap suppressions** (no faking — surface as upsell only):
  - **Gross/true margin** — no cost/COGS feed.
  - **AR / DSO / collections** — terms billed, not collected.
  - **Returns** — 4,736 credit memos visible in the LTM feed (~$3.5M absolute), but no SKU-level
    return-reason attribution; disclosed, not deep-analyzed.
  - **Stock-outs** — backorder field unpopulated.
  - **Confirmed competitive loss** — needs a second booking feed.
  - **Carrier / damage, inventory aging, market/showroom ROI, segmentation** — not in feed.

## 8. Sensitive callouts — per-client scrubbing policy *(gold-stamp 2026-06-30)*

**Automatic top-1-share rule resolved per Step 1 concentration probe (2026-06-29 LTM):**

| Account (bill-to) | Top-1 share of LTM | Auto-rule render policy | Per-run override |
|---|---|---|---|
| **WAYFAIR** | 6.04% (5–20% band) | `body` — named in body prose; no standalone decision block | — _(human ratifier may override; default holds)_ |
| Ferguson Enterprises | 1.88% | `exclude_only` from headline; appears in body when relevant | — |
| Lumens (BENNING) | 1.86% | `exclude_only` | — |
| Ferguson Home | 1.50% | `exclude_only` | — |
| Lamps Plus | 1.40% | `exclude_only` | — |
| Lighting New York | 1.44% (via HOUS routing) | `exclude_only` from coaching cards (HOUS rep); body-named for the e-commerce cluster narrative | — |

**Per-account overrides:** none set.

**E-commerce / marketplace cluster — `cluster_section` override RATIFIED 2026-06-30:** the named e-commerce /
marketplace book (Wayfair, Ferguson Enterprises, Ferguson Home, Lumens, Lamps Plus, Lighting New York,
Pottery Barn, Lulu and Georgia, Lightology, Lightopia, Lighting Star — the §6 list) renders as **one named
channel** with its own §3 decision block and a dedicated §10 channels block. Cluster membership comes from
the §6 list; cluster $ and YoY are computed live each run. Per-account treatment within the cluster: Wayfair
named in body prose at its actual share inside the cluster narrative; the others named when they materially
move the cluster $. Standalone Wayfair (or other single-account) §3 blocks remain forbidden unless a single
account crosses the 20% top-1 auto-rule threshold on a live run.

_Revisit clause: lock holds until the first client-facing cci run; if the dedicated §3 + §10 cluster blocks
read as too heavy against the rest of the report (or if cci leadership treats these accounts as five separate
strategic accounts rather than one channel), re-ratify back to `individual` and update the log._

**Cascade rule** (orphaned-hero-hedge fix): any §1 / §5 / §10 reference to a callout that's been toggled
out of `full_section` must drop or auto-substitute in the same render pass.

_Forbidden here: any judgment about whether the account is good or bad for the client. The policy is a
scope decision (which surface renders this account), not a finding (whether this concentration is risk)._

---

### Ratification log
- 2026-06-30 — Inline-DRAFT derived during PASS3 `--cohort-validation` run. Identity / mode / hard-gap
  suppressions / house-screen / e-commerce concentration captured from Step-1 preflight + Step-2 gather.
  — Kylor (via agent)
- 2026-06-30 (PM) — **RATIFIED.** §8 cluster question resolved: `cluster_section` override for the named
  e-commerce / marketplace book (the §6 list), with a revisit clause after the first client-facing run.
  §1–§7 sanity-checked against the cci PASS3 output and accepted as live-derived facts (no per-account
  overrides set; auto-rule defaults stand for the 6 enumerated accounts). Renamed `cci.draft.md` → `cci.md`.
  Standing leakage gut-check held: no leadership-facing dollar in cci PASS3 was authored against an account
  the policy screens out. — Kylor
