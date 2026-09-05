# Segmentation v4.1 — Fresh-Agent Prompt

> **STALE — superseded 2026-07-09, same day, a few hours after this was written.** This prompt
> assumed v4.0 was insufficient and needed a from-scratch rebuild off v3.2. Before it was acted on,
> a further v4.0 pass added the three-axis (how/what/who they sell) enrichment this prompt asked
> for, tested it against every Postgres dimension, and **Kjael stamped it**. See
> [`segmentation_v4.0_stamped_handoff.md`](segmentation_v4.0_stamped_handoff.md) and
> `Customer Segmentation/current/README.md`. **Do not run this prompt** unless a genuine
> further revalidation is wanted — and if so, start from stamped v4.0, not v3.2.

> Paste this entire file as your opening prompt in a new agent session.
> Do **not** continue from prior v4.0 chat history. Start clean.

---

## Who you are

You are picking up SuperCat client segmentation for Kylor (CTO). SuperCat sells eCat (iPad sales tools) to furniture, lighting, and home-goods manufacturers. The universe is ~108–109 active client orgs in Postgres.

Your job is to produce a **stampable v4.1** that Kjael can read in ~5 minutes. This is for **rep co-pilot initialization**: drop a client into a bucket so recommendations are not tone-deaf. It is also useful for GTM/onboarding, but co-pilot is the north star.

---

## Critical framing (read twice)

**We are segmenting SuperCat's clients by how they sell in the market — not by how they use eCat.**

Almost every client does **not** run all (often not most) of their selling on eCat rails. Orders, customers, users, and feature flags in Postgres describe platform configuration and partial activity. They are incomplete pictures of the business.

Classify by three questions (stamped since v3):

1. **What do they sell?** — product type + price point
2. **How do they sell it?** — specification / brand-building / multi-channel / volume replenishment
3. **Who buys from them?** — designers/architects, dealers, retail chains, category managers, hospitality, etc.

**Price is supporting evidence, not the sole boundary.** Kjael's July 2 ask was to *scrub* dollar-per-unit outliers so clusters tighten — not to abandon price, and not to invent a new framework.

Furniture vs lighting as a primary cut is **misguided**. Same market segment can include both.

---

## What already happened (do not redo)

| Version | What it did | Status |
|---|---|---|
| v3.1 | 4-segment business-model model from website/selling-motion research | Superseded by v3.2 |
| **v3.2** | Multi-layer Postgres validation; 2σ price scrub; 7 account moves; stamped by Kylor July 2 | **BASELINE — start here** |
| v4.0 (first pass) | Over-rotated into framework + eCat-config reclassifications | Off-track; archived |
| v4.0 (reset) | Froze v3.2 membership; added enrichment columns; fixed fms/shl AOV; removed Gabriella White duplicate | Useful salvage, but **did not** re-validate selling motion with off-platform evidence |

**v4.0 reset is not the finish line.** It preserved buckets and cleaned metrics. v4.1 must re-check *who/what/how they sell* using off-platform evidence + cleaned price, then propose any moves for human stamp — not unilaterally reclassify from eCat config.

---

## July 2 meeting directive (source of truth for intent)

Kjael (paraphrased + key quotes):

- Buckets are directionally right; don't over-slice.
- Scrub dollar/unit (start at ~2σ) so quantitative clusters tighten; expect same view, maybe a few moves; then stamp.
- Purpose: co-pilot jumpstart — 3–4 buckets so Savoy House doesn't get luxury-spec prompts (and vice versa).
- "It doesn't need to be perfect."
- Next after stamp: **personas within segments**.

Brent: throw out $5 accessory outliers dragging medians down; anchor on who they sell to / how they sell.

Jon: price levels (stocking dealer / non-stocking / designer) are a useful behavioral signal; Wayfair/Ferguson/Costco-type channels skew metrics — treat as channel evidence, not noise to ignore blindly.

Emery: price is the simplest axis. Kjael's response: clean the price data, don't abandon the model.

Kylor: eCat-only data picture does not work; round out with actual customers / market selling motion.

---

## What went wrong in v4.0 (do not repeat)

1. Reclassified orgs from eCat operational signals (customer file size, online ordering groups, territory config).
2. Treated "price is a correlate" as permission to de-emphasize the scrub Kjael asked for.
3. Overbuilt methodology / three-axis frameworks instead of a stampable roster.
4. The *reset* v4.0 fixed membership freeze + enrichment but still skipped the off-platform re-validation pass.

**Salvage from archived v4.0 (carry forward):**

- `fms` AOV: $92,048 → **$3,649** (23 corrupt duplicate orders excluded)
- `shl` AOV: $75,722 → **$6,942** ($5M ORDER_CAP; one $464M corrupt order excluded)
- T12M order counts (enrichment column)
- Gabriella White (`??` / duplicate of Summer Classics `sc`) removed from Luxury — keep that cleanup
- Qualitative segment prose (selling-motion descriptions) — reuse as short blurbs, not a new framework

---

## Baseline files (read these first)

| Role | Path |
|---|---|
| **Baseline analysis** | `Customer Segmentation/v3/v3.2/SuperCat_Client_Segmentation_v3.2.md` |
| **Baseline CSV (109 rows)** | `Customer Segmentation/v3/v3.2/SuperCat_Customer_Segmentation_v3.2_COMPREHENSIVE.csv` |
| Business-model text (v3.1) | `Customer Segmentation/v3/v3.1/SuperCat_Customer_Segmentation_v3_Business_Model.csv` |
| TAM enriched clients | `Customer Segmentation/data/TAM_enriched_Customers.csv` |
| Archived v4.0 (salvage only) | `Customer Segmentation/v4/v4.0_archive/` |
| This prompt | `Customer Segmentation/handoffs/segmentation_v4.1_handoff.md` |

v3.2 comprehensive columns: `Company`, `org`, `segment`, `v3_avg_price`, `catalog_scrub_median`, `realized_mean_price`, `best_price`, `total_orders`, `avg_order_value`, `distinct_price_codes`, `n_products`.

Segments in v3.2:

| Segment | N |
|---|---:|
| 1. Luxury Specification | 34 |
| 2. Premium Trade Brand | 31 |
| 3. Mid-Market Multi-Channel | 26 |
| 4. Volume Distribution | 13 |
| 5. Specialty/Non-Traditional | 5 |

After Gabriella White dedupe, expect **108** orgs / Luxury **33** unless you find another identity issue.

---

## Evidence hierarchy (mandatory)

### Tier A — may support classification / proposed moves

1. **Off-platform selling motion** from TAM + v3.1 business-model fields:
   - `Product Type`, `How They Sell`, `Who They Sell To`
   - `Channels Detected`, `Channel Count`
   - `Has Direct Sales`, `Has Dealer Network`, `Has Trade Program`, `Has Contract Sales`, `Has eCommerce`
2. **Cleaned unit economics:** best price (realized mean when available, else 2σ-scrubbed catalog median), cleaned AOV
3. **Selective website checks** (see below) when Tier A conflicts with v3.2 placement
4. **Human market judgment flags** already raised (Currey, Hooker, Rowe, Sarreid, Charleston Forge, Four Seasons, Alden, Magnussen, etc.) — propose, don't auto-move

### Tier B — enrichment only (never sole reason to move)

- Customer count, territories, users, T12M orders, distribution centers
- Price-code *count* (useful correlate; Jon's stocking/non-stocking/designer *labels* are more interesting if you can infer them)
- Catalog category/collection distributions (what they sell — supporting)

### Tier C — forbidden as move reasons

- eCat feature flags, login volume, billable users, library size
- Mobile-site toggles, enrollment flags
- "Has online ordering group" / portal config alone
- Lifetime portal invoice revenue sums (not time-windowed / not deduped) — **do not use**
- ARR/MRR from TAM as segment classifier (commercial size ≠ selling motion)

### TAM file notes

- Path: `Customer Segmentation/data/TAM_enriched_Customers.csv`
- Row 0 is blank; **header is row 1**; data starts row 2. First column is empty — ignore it.
- This file is **SuperCat clients** (~110), not their end-customers.
- Join to v3.2 on `Company` name (normalize lightly: trim, casefold). Map to `org` shortname via v3.2 CSV. Flag unmatched names.
- Gabriella White and Summer Classics both appear — treat as same corporate family; `sc` is Summer Classics (fka Gabriella White). Do not double-count.

---

## Postgres (read-only)

MCP: `user-supercat-postgres-vpn` → `execute_sql`. Schema `public`. Join on `organization_id`.

**Allowed / expected pulls:**

| Need | Approach |
|---|---|
| Org identity | `organizations` (`shortname`, `name`, `id`) |
| Catalog prices for scrub | `products.net_price` where not deleted; scrub in Python (2σ per org); MCP may block `STDDEV`/`PERCENTILE_CONT` — pull raw or simple aggregates and compute locally |
| Realized prices | `portal_invoice_items.unit_price` (coverage ~39 orgs) |
| Orders / AOV | `orders` — apply known corrupt-order fixes for `fms` and `shl`; compute T12M |
| Price codes | distinct `customers.default_price_code` |
| Enrichment | customer counts, territories, users, DCs |

**Do not:**

- Write to the DB
- Use lifetime `portal_invoices` revenue as a segment axis
- Reclassify from customer_count / user_count alone

---

## Website scrub policy (selective)

Do **not** crawl all 108 sites.

**Required review set:**

1. Any org where TAM channel flags / `How They Sell` / `Who They Sell To` **conflict** with v3.2 segment
2. The known muddy Luxury/Premium boundary cases: `cci`, `hf`, `rf`, `sarreid`, `cfg`, `fsf`, `ap`, and Mid-Market `mh`
3. Orgs with missing/weak best price (e.g. `sbl`, `fal`, `cf`, `hh`, `kkc`, `wac`, ghosts with `??`)
4. Identity issues (Gabriella White / Summer Classics already known)

For each reviewed site, capture in ≤5 bullets: product positioning, channels visible (trade portal, dealer locator, DTC cart, contract/hospitality), who the site addresses. Prefer evidence over adjectives.

---

## Segment definitions (keep; refine prose only if needed)

1. **Luxury Specification** — Designer/architect/hospitality *specification* into projects. Trade-primary. eCat often presentation/project capture; fulfillment may finish in ERP later.
2. **Premium Trade Brand** — Brand-building through dealers/showrooms; often trade + some consumer; dealer protection vs brand pull tension.
3. **Mid-Market Multi-Channel** — Distribution arms race: trade + retail + ecommerce + contractor; compete on availability/breadth.
4. **Volume Distribution** — High-volume, low unit price; category managers / chains / replenishment; commodity-adjacent.
5. **Specialty/Non-Traditional** — Exception bucket only (retail/service/niche/incomparable data). Not a fifth strategic segment.

Boundaries (from stamped model):

| Boundary | Separator |
|---|---|
| Luxury ↔ Premium | Selling motion: specify-into-projects vs brand-through-dealers |
| Premium ↔ Mid-Market | Channel strategy: trade-primary brand-building vs omnichannel everywhere |
| Mid-Market ↔ Volume | Unit economics: roughly mid ($55+) vs commodity-adjacent (roughly ≤$33) — supporting, not sole |

Default decision rule: **hold v3.2 placement** unless Tier A evidence clearly supports a move.

---

## Your task (ordered)

1. **Load baseline** — v3.2 MD + comprehensive CSV. Confirm 109 rows and segment counts.
2. **Apply known cleanups** — Gabriella White dedupe; fms/shl AOV corrections from archive; note universe → 108.
3. **Join TAM** — attach Tier A channel/selling fields to each org; report match rate and unmatched companies.
4. **Refresh cleaned price layer** — recompute or verify best_price with 2σ scrub; keep realized-when-available rule; do not invent a new price methodology.
5. **Pull Tier B enrichment** from Postgres (customers, territories, users, T12M, DCs).
6. **Conflict scan** — for each org, compare v3.2 segment vs TAM `How They Sell` / `Who They Sell To` / channel flags / cleaned price. Produce a conflict list.
7. **Selective website review** on the required review set.
8. **Propose moves** — table only; do not silently rewrite membership. Each proposal needs: org, from, to, Tier A evidence (1–3 bullets), confidence (high/med/low).
9. **Write stampable v4.1 deliverables** (below).
10. **Stop.** Do not start personas unless asked. Do not expand to 8 segments.

---

## Deliverables (write here)

All outputs go under:

`Customer Segmentation/v4/v4.1/`

and when ready for review, also copy the stamped candidates into:

`Customer Segmentation/current/`

| File | Purpose |
|---|---|
| `SuperCat_Client_Segmentation_v4.1.md` | Stampable doc (see structure) |
| `SuperCat_Customer_Segmentation_v4.1_MASTER.csv` | One row per org, all columns |
| `SuperCat_Segmentation_v4.1_STAMP_PACKET.md` | 1-pager for Kjael: summary + proposed moves + ask to stamp |
| `v3.2_to_v4.1_changelog.md` | What changed and why |

### Required structure for `SuperCat_Client_Segmentation_v4.1.md`

Keep it short enough to stamp:

1. **Executive summary** (≤15 lines) — what v4.1 is, universe N, whether buckets held, how many proposed moves
2. **How we segment** — the three questions + boundary table (brief)
3. **Segment profiles** — one short blurb each (reuse good v4.0 prose if accurate)
4. **Segment summary table** — N, median best price, IQR, median AOV, median orders, plus 1–2 off-platform aggregates if useful (e.g. % with dealer network)
5. **Rosters** — per segment, columns at minimum: Company, org, Best Price, AOV, Orders, T12M, key TAM flags or a single `channels` summary, PCodes, Customers (enrichment)
6. **Proposed moves** — table for human decision (empty if none)
7. **Hold / muddy list** — boundary cases still uncertain
8. **What we explicitly did not do** — no eCat-usage segmentation; no lifetime invoice revenue; no framework overhaul
9. **Next step** — personas after stamp

**No** long methodology essays, cross-tab matrices, or three-axis formal frameworks.

---

## Constraints

- Do not modify Insightful Product foundation docs
- Do not delete `v4/v4.0_archive/`
- Do not treat the archived v4.0 reset as already finished
- Do not unilaterally move accounts in the roster without listing them under Proposed Moves (roster should show **recommended** segment only if you also show current v3.2 segment — preferred: roster stays on v3.2 membership; proposed moves are separate)
- Prefer: **roster = v3.2 membership + cleanups**; **proposed moves = separate decision table**
- Ask mode / read-only Postgres only for DB
- If VPN/MCP is down, proceed with CSVs + TAM + archived enrichment; note gaps

---

## Definition of done

- [ ] v4.1 MD + MASTER CSV + stamp packet + changelog written under `v4/v4.1/`
- [ ] Gabriella dedupe + fms/shl AOV fixes applied
- [ ] TAM Tier A fields joined; match report included in changelog
- [ ] Conflict scan completed; selective websites reviewed
- [ ] Proposed moves table present (even if zero moves)
- [ ] No org moved solely for eCat config / login / customer-file size
- [ ] Document is stampable in ~5 minutes
- [ ] Ready for Kylor/Kjael review → then personas

---

## First actions in the new session

1. Read this prompt fully.
2. Read `Customer Segmentation/v3/v3.2/SuperCat_Client_Segmentation_v3.2.md`.
3. Load the v3.2 comprehensive CSV + TAM CSV (header on row 1).
4. Skim `Customer Segmentation/v4/v4.0_archive/SuperCat_Customer_Segmentation_v4.0_MASTER.csv` only for salvage columns (t12m, corrected AOVs).
5. Begin the ordered task list above.
)
