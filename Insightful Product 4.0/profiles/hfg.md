# Client Profile — Hubbardton Forge (`hfg`)

> **What this is.** Reading-contract input #2 (see [`../CANON.md`](../CANON.md)): the cached, human-ratified
> statement of Hubbardton Forge's **stable context**. Loaded after `foundation/provenance_spine.md`, before
> `knowledge/industry_context.md`. **Facts and scope decisions only — no findings, no framing.** See
> [`README.md`](README.md) for the allowed/forbidden rule and the derive→ratify→cache workflow.
>
> **Status:** RATIFIED 2026-06-30 — §8 open questions resolved as: Illuminating Expressions = Unknown
> (PASS3's go-investigate framing stands); e-commerce cluster = `individual` (auto-rule holds, matches kal —
> Q-CHAN-00 = NONE blocks a §10 channel render); NENOREP = Unknown-but-exclude-held; DTC exclusions
> confirmed; rep-bridge gap = investigation item not a profile decision. Tier-2 carry-over deferred to the
> canon-level rep_copilot_operator §1 work. §1–§7 sanity-checked against the hfg PASS3 output and accepted
> as live-derived facts. See Ratification log.

---

## 1. Identity (the hard key — prevents running the wrong org)

| Field | Value | How derived |
|---|---|---|
| Client name | Hubbardton Forge | confirmed via `organizations.name` |
| `organization_id` (Postgres) | `165` | `Q-ECON-00` preflight |
| Shortname | `hfg` | confirmed via `organizations.shortname` |
| Home base | Castleton, Vermont (USA-made, hand-forged lighting) | public knowledge; not in DB |
| Same-name disambiguation | none flagged in cohort | preflight |
| `report_through_date` policy | `LEAST(MAX(invoice_date), CURRENT_DATE)` | gate-computed (2026-06-29, 1 day fresh) |
| Rep-identity tier | **Tier 1** (`rep_number`-only; name-bridge **79.3%** — 46 of 58 invoice reps, inside the 78–82% deadband, no declared carry-over) | RP-2 hysteresis gate (`../operators/rep_copilot_operator.md` §1, Spine §7.1) |

## 2. Business model / segment

- **Model:** premium hand-forged American lighting manufacturer (pendants, sconces, outdoor fixtures,
  large-scale decorative, occasional hospitality/architectural custom). USA-made; the Vermont
  manufacturing posture is brand-relevant.
- **Client segment (SuperCat v4.0, stamped):** Premium Trade Brand
- **How they sell (axis):** Brand-Building
- **What they sell (axis):** Lighting
- **Who they sell to (axis):** Wholesale (Broad Dealer Network)
- **Price (continuous, not a boundary):** best available unit price ≈ $846 (from Client Segmentation v4.0 MASTER; price is a correlate within segment, not the classifier)
- **Source:** `Customer Segmentation/current/SuperCat_Customer_Segmentation_v4.0_MASTER.csv` · stamped 2026-07-09 · join org=hfg · org_id=165 (verified)
- **Price point (descriptive):** mid-to-high premium (catalog SKUs invoice predominantly $200–$2,000 each; large-scale
  / custom items reach five figures per unit).
- _Client segment above = SuperCat's stamped **selling-motion** class (Workstream A). It is distinct from the 🧊 FROZEN in-client customer segmentation (Q-SEG-DERIVE, Spine §8), which stays out of scope and is not a profile field._

## 3. Channel model (how they sell)

- Sells through a **mixed multi-channel network**: independent lighting specialty showrooms (Lightology,
  CAI Designs, Connecticut Lighting Center, City Lights, Beautiful Things, Lighting First, etc.) +
  electrical distributors (Ferguson, Graybar, F.W. Webb, Shanor Electric, Franklin Empire) +
  national e-commerce / marketplace (Lumens, Wayfair, Build.com, Lighting New York, Lamps Plus,
  1800Lighting, Houzz Shop) + Hubbardton Forge's own DTC (Handmade In Vermont.com, Shop Hubbardton Forge)
  + occasional architectural / hospitality custom projects.
- **eCat (rep iPad) is a small channel for hfg** — ~$1.97M LTM on $41.16M invoiced (~4.8% of invoiced);
  dollars only, never shown as a share of business.
- This overrides any industry-default channel weighting in `../knowledge/industry_context.md`.

## 4. House / sample / internal accounts to screen

Excluded from the leaderboard, from the at-risk watchlist, and from the leakage / dispersion math:

- House/sample bill-to patterns: `ZZ*`, `HOUSE*`, `ACCOM*`, `SAMPLE*`, `DISPLAY*`, `SHOWROOM*`, `TEST*`,
  `MODEL*`, `PHOTO*`, `MISC*`, `NOCHARGE*`, `NO CHARGE*`, `COMP *` (per RS-01 §3 inline list).
- **Hubbardton Forge's own DTC and internal accounts** (eight bill-to codes, totaling ~$1.52M LTM):
  - `10505` Handmade In Vermont.com (~$716K LTM) — HF's own DTC site
  - `35639` Shop Hubbardton Forge (~$559K LTM) — HF's own retail site
  - `17190` HF Internal — Commercial Accomodation (~$88K)
  - `17236` HF Internal — Residential Accommodation (~$59K)
  - `11877` HF Internal — Employee Friends & Family (~$54K)
  - `1250` HF Internal — Employee Purchases (~$22K)
  - `17198` HF Internal — Trade Accommodation (~$21K)
  - `13003` HF Internal — Bunker Hill Capital (~$0)
- **`rep_number = NENOREP`** ($1.35M LTM / 21 accounts) — a no-rep placeholder bucket on the invoice
  feed. Its top accounts are the two DTC sites and the HF Internal codes above. Excluded from the
  rep leaderboard for the same reason house labels are. Open question for the ratifier — is `NENOREP`
  intended as a permanent house-route, or as an interim placeholder to be backfilled with a real
  rep code on the customer-direct book?
- **Blank `rep_number`** ($8.43M LTM / 739 accounts) — unattributed invoices. ~31% is one large custom
  project at Illuminating Expressions ($2.65M); the rest is a long tail of distributor / hospitality /
  small accounts that did not get a rep tag. Excluded from the rep leaderboard, surfaced as the
  "unassigned book" bucket beneath it.
- **Rep 42586** ($5.24M LTM / 11 accounts) — sole-coverage book of national e-commerce / marketplace
  (Lumens, Wayfair, Build.com, Lighting NY, Lamps Plus, 1800Lighting, Houzz Shop, Belami, Net
  Retailers, Carve Media, Kathy Kuo Home). Surfaced in the leaderboard at `rep <n>` grain like every
  other rep. Open question for the ratifier — should this book be re-labeled as the "e-commerce
  channel book" for §5 narrative purposes?
- _Scope decision: this sets which rows the dispersion / decline math runs on; the dollar itself is
  computed live and ships DIRECTIONAL on a leakage figure._

## 5. Buyer-type context

- The active dealer base splits roughly **673 frequent (6+ invoices LTM) / 946 occasional / 801 one-time**
  (LTM totals: $32.5M / $6.4M / $2.3M, respectively). The frequent dealers carry **79% of invoiced LTM**
  on **28% of the dealer count** — a heavy specialty-showroom tail.
- The new-dealer cohort (1,252 first-timers prior LTM) returned this LTM at **39.1%** — within the
  industry-normal 25–45% second-year band for a hand-forged premium lighting wholesaler. Treat the
  61% non-return as a mix of designer-resource / project / one-time-by-intent buyers (per
  industry-context guidance), not as flat churn.

## 6. Structural concentration (context, NOT a finding)

- **Top customer share is moderate on the base** — Illuminating Expressions $2.66M LTM = **6.46% of
  LTM** (top-1, single custom project at zero prior); top-10 share **25.72%**; HHI **110**.
  Per the §R thresholds (top-1 ≥25% / top-10 ≥40% / HHI ≥1500), the $-base is **NOT** broadly
  concentrated.
- **The same-base YoY lift IS heavily concentrated, however** — Illuminating Expressions alone is
  **27.09% of the $9.74M same-base positive lift**, and ex-Illuminating-Expressions the same-base
  comes in **−8.21% YoY** ($35.10M LTM vs $35.37M prior). This is a top-1 ≥25% on the **lift**
  denominator — the §R "broad-based" framing is FORBIDDEN for the lift; the §R.5 canonical template
  is used in §5 Layer 1.
- **No single-rep concentration on the field team** — top named-rep book (rep 42586, the e-commerce
  book) is $5.24M = 12.7% of company; the top six rep_numbers each sit below 13%.

## 7. Report mode default + scope exclusions

- **Default mode:** **1 — Standard**, **Tier-1 degraded** (clean invoice feed, fresh, internally
  consistent — but the rep-name bridge sits in the 78–82% deadband, so §2 coaching cards do NOT
  render and the leaderboard / decline list run at `rep <n>` grain per §O.4 of the editorial rules;
  the gate still resolves mode live each run and overrides this if data changes).
- **Channel section:** `Q-CHAN-00 = NONE` (the booked-orders feed carries one value — `Not specified` —
  on 100% of 22,250 LTM rows / $42.4M). Channel section is suppressed per §O.1; eCat is overlaid
  from in-app order data, dollars only.
- **Confirmed hard-gap suppressions** (no faking — surface as upsell only):
  - **Gross/true margin** — no cost/COGS feed.
  - **AR / DSO / collections** — no AR feed; `terms` field is itself 0% populated on hfg's invoice feed.
  - **Returns** — 0 credit memos visible in the LTM feed; either returns are processed off-feed or
    the field isn't populated here.
  - **Freight / carrier** — `freight_amount` and `tracking_carrier` are both 0% populated on hfg's
    invoice feed; freight-economics subsections do not run.
  - **Lead time** — `ship_date` 0% populated on the order feed.
  - **Channel split** — see Q-CHAN-00 NONE above.
  - **Stock-outs, market/showroom ROI, segmentation, confirmed competitive loss** — not in feed.

## 8. Sensitive callouts — per-client scrubbing policy *(gold-stamp 2026-06-30)*

**Automatic top-1-share rule resolved per Step 1 concentration probe (2026-06-29 LTM):**

| Account (bill-to) | Top-1 share of LTM | Auto-rule render policy | Per-run override |
|---|---|---|---|
| **Illuminating Expressions** | 6.46% (5–20% band) | `body` — named in body prose; flagged as a single-project win | — _(human ratifier may override)_ |
| Lumens, Inc. | 5.46% | `exclude_only` from headline; body-named in the e-commerce cluster narrative | — |
| Ferguson Enterprises | 2.64% | `exclude_only` | — |
| Wayfair | 1.82% | `exclude_only` | — |
| Build.com | 1.79% | `exclude_only` | — |
| Handmade In Vermont.com (HF DTC) | 1.74% | excluded from leaderboard / at-risk via DTC house-screen above; body-disclosed | — |
| Shop Hubbardton Forge (HF DTC) | 1.36% | excluded from leaderboard / at-risk via DTC house-screen above; body-disclosed | — |

**Per-account overrides:** none set.

**Ratified resolutions (2026-06-30):**

1. **Illuminating Expressions = Unknown.** The $2.64M one-account lift (4 custom DL-series oil-rubbed
   bronze architectural fixtures, $19K prior) is NOT pinned as one-time-vs-recurring. PASS3's framing
   stands: §1 callout #1 surfaces both reads (one-time → catalog softer than headline; multi-property →
   year-one of a pipeline to defend and extend), §3 "this week" play schedules the investigation call,
   §5 sub-section pressure-tests the question. Re-ratify when HF leadership confirms the buyer's pipeline.
2. **E-commerce cluster = `individual` (auto-rule holds).** Matches kal for the same reason: hfg's
   booked-orders origin field carries one value (`Not specified`) on 100% of 22,250 LTM rows
   (`Q-CHAN-00 = NONE`, suppression branch enforced); a `cluster_section` override could not produce a
   real §10 channel block. Rep 42586's 11-account book is surfaced at `rep <n>` grain on the leaderboard
   under the Tier-1 degraded shape; per-account treatment follows the auto-rule table above.
3. **HF DTC + Internal exclusions confirmed.** Handmade In Vermont.com (10505), Shop Hubbardton Forge
   (35639), and the six HF Internal codes (17190, 17236, 11877, 1250, 17198, 13003) stay excluded from
   the leaderboard / at-risk watchlist / leakage dispersion math. Body-disclosure permitted.
4. **NENOREP = Unknown, exclusion held.** The $1.35M / 21-account bucket's top accounts ARE the DTC
   sites and HF Internal codes above (so the exclusion holds correctly regardless of whether NENOREP
   is intended as a permanent house-route or an interim placeholder). Re-ratify if HF backfills the
   bucket with real rep codes.
5. **Rep-name bridge gap = investigation item, not a profile decision.** The 12 unbridged
   `portal_orders.rep_name` rows that would push hfg from 79.3% to ~99% are a feed-engineering question
   (data integration), not a scope decision. Profile stays Tier-1 degraded until the bridge clears.
   PASS3 §3 "this week" already routes the call: backfill those 12 rep names on the booked feed.

**Deferred to canon-level work (NOT a profile decision):** whether hfg should be added to the
`rep_copilot_operator.md` §1 Tier-2 carry-over list given the 79.3% deadband position. Tracked in handoff
§7 Phase 5; bcf is the only declared Tier-2 carry-over currently.

**Cascade rule** (orphaned-hero-hedge fix): any §1 / §5 / §10 reference to a callout that's been
toggled out of `full_section` must drop or auto-substitute in the same render pass.

_Forbidden here: any judgment about whether the Illuminating Expressions project is good or bad for
the client. The policy is a scope decision (which surface renders this account), not a finding
(whether this concentration is risk)._

---

### Ratification log
- 2026-06-30 — Inline-DRAFT derived during PASS3 `--cohort-validation` run. Identity / mode / hard-gap
  suppressions / house-and-DTC screen / lift-concentration / open questions captured from Step-1
  preflight + Step-2 gather. — Kylor (via agent)
- 2026-06-30 (PM) — **RATIFIED.** Five §8 open questions resolved (see "Ratified resolutions" above):
  Illuminating Expressions = Unknown / PASS3 framing held; e-commerce cluster = `individual` (matches kal,
  Q-CHAN-00 = NONE); NENOREP = Unknown-but-exclude-held; DTC + HF Internal exclusions confirmed; rep-bridge
  gap = investigation item not a profile decision. Tier-2 carry-over deferred to canon-level
  rep_copilot_operator §1 work (handoff §7 Phase 5). §1–§7 sanity-checked against the hfg PASS3 output and
  accepted as live-derived facts (no per-account overrides set). Renamed `hfg.draft.md` → `hfg.md`. Standing
  leakage gut-check held: no leadership-facing dollar in hfg PASS3 was authored against an account the
  policy screens out. — Kylor

