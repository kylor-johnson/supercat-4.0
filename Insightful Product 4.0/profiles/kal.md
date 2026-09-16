# Client Profile — Kalco Lighting / Allegri Crystal (`kal`)

> **What this is.** Reading-contract input #2 (see [`../CANON.md`](../CANON.md)): the cached, human-ratified
> statement of Kalco / Allegri's **stable context**. Loaded after `foundation/provenance_spine.md`, before
> `knowledge/industry_context.md`. **Facts and scope decisions only — no findings, no framing.** See
> [`README.md`](README.md) for the allowed/forbidden rule and the derive→ratify→cache workflow.
>
> **Status:** RATIFIED 2026-06-30 — §8 cluster question resolved (`individual` / auto-rule holds — the
> cluster lives in §1/§5 as the house-routed-book routing-and-coverage question, not a duplicate channel
> block; differs from cci because kal's booked-orders origin field is uniformly blank → `Q-CHAN-00 = NONE`,
> so a §10 channel block has no data to render). §1–§7 sanity-checked against the kal PASS3 output and
> accepted as live-derived facts. See Ratification log.

---

## 1. Identity (the hard key — prevents running the wrong org)

| Field | Value | How derived |
|---|---|---|
| Client name | Kalco Lighting / Allegri Crystal | confirmed via `organizations.name` |
| `organization_id` (Postgres) | `146` | live identity probe |
| Shortname | `kal` | confirmed via `organizations.shortname` |
| Same-name disambiguation | none flagged in cohort | preflight |
| `report_through_date` policy | `LEAST(MAX(invoice_date), CURRENT_DATE)` | gate-computed (2026-06-29, fresh — same day as run) |
| Rep-identity tier | **Tier 2** (named; date-aligned name bridge **91.5%** — 43 of 47 invoice reps) | RP-2 gate (`../operators/rep_copilot_operator.md` §1) |

## 2. Business model / segment

- **Model:** lighting + crystal-chandelier manufacturer operating two brands under one entity (Kalco Lighting
  for the general decorative line; Allegri Crystal for the high-end crystal range).
- **Client segment (SuperCat v4.0, stamped):** Premium Trade Brand
- **How they sell (axis):** Brand-Building
- **What they sell (axis):** Lighting
- **Who they sell to (axis):** Wholesale (Dealers)
- **Price (continuous, not a boundary):** best available unit price ≈ $647 (from Client Segmentation v4.0 MASTER; price is a correlate within segment, not the classifier)
- **Source:** `Customer Segmentation/current/SuperCat_Customer_Segmentation_v4.0_MASTER.csv` · stamped 2026-07-09 · join org=kal · org_id=146 (verified)
- _Client segment above = SuperCat's stamped **selling-motion** class (Workstream A). It is distinct from the 🧊 FROZEN in-client customer segmentation (Q-SEG-DERIVE, Spine §8), which stays out of scope and is not a profile field._

## 3. Channel model (how they sell)

- Sells through **independent lighting/showroom dealers** plus a meaningful **online / e-commerce dealer
  cluster** (Lumens, Build.com, Lighting New York, Lamps Plus, Wayfair, Shades of Light, Lightology, Capitol
  Lighting, Designer Lighting & Fan/Decor, Belami / 1Stop Lighting, Bisonoffice). The Ferguson family
  (FEI Ferguson Main Account) is the single largest customer.
- **eCat is a minority channel for kal** — strict eCat-SALE LTM capture ~$0.56M (~6% of invoiced LTM);
  dollars only, never shown as a "share of business."
- Booked-orders origin tagging is **uniformly blank** (1 distinct `order_origin` value across all 10,066 LTM
  booked rows); the channel section therefore suppresses per `Q-CHAN-00` §O.1.
- This overrides any industry-default channel weighting in `../knowledge/industry_context.md`.

## 4. House / sample / marketplace accounts to screen

Excluded from leakage and leadership-facing same-SKU dispersion:

- House/sample bill-to patterns: `ZZ*`, `HOUSE*`, `ACCOM*`, `SAMPLE*`, `DISPLAY*`, `SHOWROOM*`, `TEST*`,
  `MODEL*`, `PHOTO*`, `MISC*`, `NOCHARGE*`, `NO CHARGE*`, `COMP *` (per RS-01 §3 inline list).
- **`House Account` rep (`rep_number = 0999`) is excluded from the rep leaderboard render** — auto-rule
  (`rep_label ILIKE 'house%'`) per [`../config/house_rep_exclusions.md`](../config/house_rep_exclusions.md);
  the bucket is $1.60M LTM / 72 accounts (surfaced beneath the leaderboard, cannot anchor a finding).
  **kal is not in the per-org EXCLUDE table** — the auto-rule alone catches it; the per-org row is not
  required unless an additional non-`house*`-named rep label appears.
- Configuration / option pricing handled by the same-SKU dispersion engine (finish is encoded in
  `item_number`).
- _Scope decision: this sets which rows the leakage math runs on; the dollar itself is computed live and
  ships DIRECTIONAL._

## 5. Buyer-type context

- The active dealer base skews toward **frequent reorder lighting dealers** — 213 dealers placed 6+ invoices
  this year and carry **89% of LTM revenue**. The one-time tail (140 dealers, $202K, 2.2% of revenue) is
  small in dollars and small as a share.
- The new-dealer cohort is small (118 first-time dealers in LTM, $437K total revenue, avg $3.7K each); the
  prior-LTM first-timer cohort (71 dealers) returned at **25.4% second year** — the lower half of the
  industry-normal 25–45% band for a lighting wholesaler with a frequent-reorder dealer mix.

## 6. Structural concentration (context, NOT a finding)

- **Top customer share is low** — FEI Ferguson Main Account $610K LTM = **6.89% of the company** (top-1);
  top-10 share 36.66%; top-25 share 51.30%; HHI 187. Per §8 below this surfaces in body prose, not a
  standalone decision block. No single account is structurally dominant.
- **The named e-commerce / online-dealer cluster is a meaningful channel slice** — Ferguson + Lumens +
  Build.com + Lighting NY + Lamps Plus + Wayfair + Shades of Light + Lightology + Designer Lighting +
  Capitol + Belami + Bisonoffice account for a substantial share of the top-15 dealer book; several reach
  through `rep_number = 0999` (the auto-screened house bucket). This is known and structural; the share
  is recomputed live each run.
- No single-rep concentration on the field team (top rep Pacific Liteforce Sales LLC $1.04M = 11.8% of
  invoiced LTM; top-2 reps sum ~20%).

## 7. Report mode default + scope exclusions

- **Default mode:** **1 — Standard** (clean invoice feed, fresh, internally consistent; the gate still
  resolves mode live and overrides this if data changes). **Channel decomposition suppressed** under
  `Q-CHAN-00 = NONE` (1 distinct origin); use §O.1 template verbatim.
- **Confirmed hard-gap suppressions** (no faking — surface as upsell only):
  - **Gross/true margin** — no cost/COGS feed.
  - **AR / DSO / collections** — terms billed, not collected.
  - **Returns** — 907 credit memos visible in the LTM feed (~$0.6M absolute), but no SKU-level
    return-reason attribution; disclosed, not deep-analyzed.
  - **Stock-outs** — backorder field unpopulated.
  - **Confirmed competitive loss** — needs a second booking feed.
  - **Carrier / damage, inventory aging, market/showroom ROI, segmentation, channel attribution** — not
    in feed (booked-orders origin tagging is uniformly blank).

## 8. Sensitive callouts — per-client scrubbing policy *(gold-stamp 2026-06-30)*

**Automatic top-1-share rule resolved per Step 1 concentration probe (2026-06-29 LTM):**

| Account (bill-to) | Top-1 share of LTM | Auto-rule render policy | Per-run override |
|---|---|---|---|
| **FEI Ferguson Main Account** (0010023) | 6.89% (5–20% band) | `body` — named in body prose; no standalone decision block | — _(human ratifier may override; default holds)_ |
| Lumens Light & Living (0003937) | 5.73% (5–20% band) | `body` — named in body prose | — |
| Build.com (0004575) | 4.53% | `exclude_only` from headline; body when relevant | — |
| Lighting New York (Internet) (0004961) | 4.10% | `exclude_only` | — |
| Lamps Plus (0001416) | 3.42% | `exclude_only` | — |
| Wayfair LLC (0005456) | 3.04% | `exclude_only` | — |
| Shades of Light (0003299) | 2.78% | `exclude_only` | — |
| Lightology LLC (0005685) | 2.73% | `exclude_only` from leaderboard prose; appears in the at-risk list as the top cadence-cliff dollar | — |

**Per-account overrides:** none set.

**Online-dealer cluster — `individual` (auto-rule holds) RATIFIED 2026-06-30:** the named online-dealer book
(Ferguson + Lumens + Build.com + Lighting NY + Lamps Plus + Wayfair + Shades of Light + Lightology + Capitol +
Belami + Bisonoffice + Designer Lighting & Fan/Decor — the §6 list) is NOT promoted to a dedicated §3
decision block. Why: kal's booked-orders origin field is uniformly blank across all LTM rows
(`Q-CHAN-00 = NONE`, suppression branch enforced); a `cluster_section` override could not produce a real
§10 channel block from this feed, and the cluster's leadership-facing question is already correctly framed
in §1 / §2 / §5 as a **routing-and-coverage question** ("who covers the 72-account `rep 0999` house-routed
book?") rather than as a channel-mix question. A dedicated cluster §3 block would duplicate the existing
house-routed-book play. Cluster $ and YoY remain computed live; per-account treatment follows the auto-rule
in the table above (Ferguson + Lumens at `body`, others `exclude_only`).

_Differs from cci's `cluster_section` decision because cci has a populated origin tag and a real e-commerce
share to render; kal does not. Re-ratify here only if the booked feed adds a working origin tag, or if kal
leadership reframes the cluster as a marketplace strategy question rather than a coverage / routing question._

**Cascade rule** (orphaned-hero-hedge fix): any §1 / §5 / §10 reference to a callout that's been toggled
out of `full_section` must drop or auto-substitute in the same render pass.

_Forbidden here: any judgment about whether the account is good or bad for the client. The policy is a
scope decision (which surface renders this account), not a finding (whether this concentration is risk)._

---

### Ratification log
- 2026-06-30 — Inline-DRAFT derived during PASS3 `--cohort-validation` run. Identity / mode / hard-gap
  suppressions / house-screen / online-dealer-cluster concentration captured from Step-1 preflight +
  Step-2 gather. — Kylor (via agent)
- 2026-06-30 (PM) — **RATIFIED.** §8 cluster question resolved: `individual` (auto-rule holds) — kal's empty
  channel-origin tag and the existing house-routed-book routing-question framing in §1 / §2 / §5 make a
  dedicated cluster §3 block duplicative rather than additive. §1–§7 sanity-checked against the kal PASS3
  output and accepted as live-derived facts (no per-account overrides set). Renamed `kal.draft.md` → `kal.md`.
  Standing leakage gut-check held: no leadership-facing dollar in kal PASS3 was authored against an account
  the policy screens out. — Kylor

