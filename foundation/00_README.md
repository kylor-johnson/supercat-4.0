# SuperCat — Foundation

> **What this is**: The shared, socializable foundational context for SuperCat. Seven Markdown files at the root of `foundation/` that every team member, advisor, partner, and incoming hire can read in under an hour to ground themselves in what we do, who we serve, how we make money, what market we're in, where we're going, and how we operate.
>
> **Last updated**: 2026-09-16 · **Owner**: CEO · **Review cadence**: Quarterly (or when a foundational fact changes)
>
> *2026-09-16: **Persona product rehomed** to [`../personas/00-PERSONA-GROUPS.md`](../personas/00-PERSONA-GROUPS.md). Lens 2 roster stays in `Customer Segmentation/current/`. `foundation/sources/customer_segmentation/` is no longer the persona home.*
>
> *2026-09-15: **Persona groups restored.** Selling motion × seat (PG-01…08 + HQ), not 7 login seats. Withdrawn: "build once / only 4 of 31 jobs vary / do not condition on segment." [`02_who_we_serve.md`](02_who_we_serve.md), [`01_what_we_do.md`](01_what_we_do.md), [`CEO_SYSTEM_CONTEXT.md`](CEO_SYSTEM_CONTEXT.md) updated. Canonical source: [`../personas/00-PERSONA-GROUPS.md`](../personas/00-PERSONA-GROUPS.md). Prior versions in [`_archive/`](_archive/). Lens 1, Lens 2 roster, D-001a and T1/T2/T3 unchanged.*
>
> *2026-08-26: Lens 2 (Selling Motion) lineage corrected in [`02_who_we_serve.md`](02_who_we_serve.md) and [`CEO_SYSTEM_CONTEXT.md`](CEO_SYSTEM_CONTEXT.md) — the v4.0 segments are stamped judgment corroborated by Postgres, not derived from it, and cannot be assigned to a prospect. Prior versions preserved in [`_archive/`](_archive/). Lens 1, D-001a and T1/T2/T3 unchanged.*

---

## Identity

- **Core Purpose** — Turn catalogs into revenue.
- **Core Values** — Customer-Obsessed · Ship Fast · Own the Outcome · Learn Loudly.
- **10-Year Target** — Be the commercial operating system home furnishings manufacturers can't run without.

> **Marketing niche** *(the line we use externally — outside-in framing)*: Mid-market furniture, lighting & home-décor manufacturers ($10–250M) selling through reps, dealers, showrooms, and designers. **This is the elevator pitch, not the analytical ICP** — see [`02_who_we_serve.md`](02_who_we_serve.md) for the substantive segmentation, which leads on **digital selling maturity** rather than revenue band or vertical.

---

## SuperCat at a glance

| Dimension | Today |
|---|---|
| **What we are** | B2B SaaS — a five-surface commercial operating system (iPad eCat field-sales app, eCat Online catalog, B2B Cart, Sales Portal, Admin Console) for wholesale manufacturers in the home-furnishings adjacencies |
| **Substantive ICP** | A behavioral posture, not a revenue band — **digital selling maturity** (per [`PRICING_CONSTITUTION.md`](../skills/monetization_refresh_2026/11_synthesis/PRICING_CONSTITUTION.md) D-001a stamped 2026-01-28). Three segments: **Catalog-Focused (54%)**, **Commerce-Active (27%)**, **Platform-Embedded (19%)**. Revenue band, vertical, organizational scale, digital surface readiness, and tech sophistication were each tested as primary segmentation axes and **explicitly rejected**. |
| **Install base** | ~104 paying accounts (master data v3 baseline used in M1 segmentation); ~110 in Q425 pricing readout; trending toward 120 year-end FY26. Different inclusion rules; all internally valid; an as-of-quarter source-of-truth is a foundation backlog item. |
| **GMV running through us** | $768M / quarter from Platform-Embedded segment alone (20 accounts on $47K MRR — extraordinary value-to-price ratio). $6.46M annually for our reference customer BCF — and BCF is *median* Platform-Embedded, not the top of the segment. |
| **Revenue today** | Median MRR $1,192.50 / median implied ARR $16,123; **$2.12M FY26 subscription revenue target (+15.2% over FY25)**; **$2.27M implied ARR target (+23.4%)**; year-end ACV $20,166 (+14.0%) |
| **Pricing model in transition** | Modular five-product menu → stamped **T1 $749 / T2 $1,295 / T3 $2,295** Good/Better/Best tiers, billable users on a step-declining curve. Tiers map to behavioral segments (T1 ↔ Catalog-Focused, T2 ↔ Commerce-Active, T3 ↔ Platform-Embedded), but the segment-vs-tier mapping is intentionally not 1:1 — the gap is the upgrade-opportunity signal. |
| **Market context** | Wholesale home furnishings — TAM ~4,651 firms (Furniture 68%, Lighting 17%, Home & Décor 7%); 71% run the dealer + trade + (eCom) selling motion. The TAM industry mix is **inverted from the install base** (heavily Lighting today) — per M1, the segmentation generalizes across verticals, so growth into the Furniture-heavy TAM is not a different segmentation question. |
| **Competitive set** | 5 direct competitors (AmpTab, Pepperi, WizCommerce, MarketTime, RepZio); 8 adjacent; "we'll build it / status quo" is the most common loss path |
| **Differentiator** | Deepest CPQ in the competitive set + **50+ value moments across 13 domains** packaged as the Insights Layer (cross-customer intelligence only SuperCat can do) |
| **How we operate** | Autonomous CEO System — **13 weekly artifacts** running Mon–Fri at 6:00 AM, deploying to [ceosystem.io](https://ceosystem.io); editorial-feedback protocol that turns CEO critique into runtime memory |

---

## Why we win — five bullets

1. **Vertical depth in furniture / lighting / home-décor that no horizontal platform matches.** Configurable products with option sets, mappings, riser pricing, matrix options, and kits — built for SKU complexity that defeats Pepperi, WizCommerce, RepZio, and Shopify B2B.
2. **The full commercial stack on one spine.** iPad rep app + buyer-facing online catalog + B2B cart + closed dealer site + sales portal + admin console — sharing one catalog, one customer file, one user file. Competitors who match a single surface lose on the integration story.
3. **Total cost of ownership at scale.** With setup fees amortized, SuperCat's Y1-effective cost is at or below AmpTab at every tier; SuperCat T3 ($2,545 at 50 users) is **15% below AmpTab Pro** ($3,000) — and includes Insights Layer.
4. **The Insights Layer — cross-customer intelligence only SuperCat can produce.** 50+ value moments across 13 domains, validated against live customer data, with the cross-instance BigQuery infrastructure already built and live. The defining T3 differentiator and the strongest analytical-intelligence answer to WizCommerce's AI-first positioning.
5. **Price transparency and discipline in a market dominated by quote-only competitors.** Stamped pricing in [`PRICING_CONSTITUTION.md`](../skills/monetization_refresh_2026/11_synthesis/PRICING_CONSTITUTION.md), CEO-approved 10%/12-month discount cap, no annual prepay discount that erodes the rate. 78% of B2B buyers demand upfront pricing per industry research; we are one of the few who provide it.

---

## The seven docs (read in order)

| # | File | What it covers | When you'd read it |
|---|---|---|---|
| 00 | **[`00_README.md`](00_README.md)** *(this file)* | At-a-glance + identity + navigation | First — orient |
| 01 | **[`01_what_we_do.md`](01_what_we_do.md)** | The five product surfaces, the five-layer gating model, **the build-once-parameterise-on-org-structure rule**, the 42-value-moment framework, BCF as the reference deployment | Anyone trying to understand the product |
| 02 | **[`02_who_we_serve.md`](02_who_we_serve.md)** | The substantive ICP — digital selling maturity (Catalog-Focused / Commerce-Active / Platform-Embedded), why revenue band/vertical/scale were rejected as segmentation axes, the marketing niche we use externally, market context (4,651-firm TAM), the four buyer roles, **persona groups (selling motion × seat — who is in the room, what job, what to build)**, BCF as the reference deployment | Anyone trying to understand the market and customers |
| 03 | **[`03_how_we_make_money.md`](03_how_we_make_money.md)** | Today's economics (the modular menu), the 2026 T1/T2/T3 model, the install-base baseline, the migration plan | Anyone touching pricing, ACV, or revenue planning |
| 04 | **[`04_market_and_competitors.md`](04_market_and_competitors.md)** | The competitive universe, the buyer-friction language we sell against, where we win and where we're vulnerable, the per-competitor response playbook | Anyone in a sales conversation, competitive analysis, or product positioning |
| 05 | **[`05_strategic_direction.md`](05_strategic_direction.md)** | The four active bets (Monetization Refresh, Insightful Product, FY26 Target Scenario, ROI Calculator), the 10-year target, the deliberate exclusions | Anyone trying to understand where we're going and why |
| 06 | **[`06_how_we_operate.md`](06_how_we_operate.md)** | The data spine, the CEO System weekly cadence, the editorial-feedback protocol, the operating discipline (and the seven gaps for v2) | Anyone trying to understand how the company runs |

**Total reading time**: ~45 minutes for the full set; ~10 minutes for `00` + `01` + `05`.

---

## Reading paths by role

| If you are | Read in this order |
|---|---|
| **A new hire orienting** | 00 → 01 → 02 → 03 → 06 → 04 → 05 |
| **An advisor or board member** | 00 → 05 → 03 → 04 → 02 → 01 → 06 |
| **A prospective customer** *(or anyone preparing a customer pitch)* | 00 → 01 → 02 → 04 (especially "where we win") |
| **A pricing / GTM partner** | 00 → 03 → 04 → 05 |
| **An engineer joining the team** | 00 → 01 → 06 → 05 |
| **A potential acquirer or investor** | 00 → 03 → 05 → 04 → 02 → 06 → 01 |
| **An AI agent operating in this workspace** | [`AGENTS.md`](../AGENTS.md) is the canonical map; this set is the strategic context behind it |

---

## What this set is not

- **Not the operational manual.** Detailed prompts, query libraries, brand specs, migration mechanics, scorecard SQL, and operator playbooks live in their respective `skills/<workstream>/` folders. The foundation set summarizes and points; it does not duplicate.
- **Not the AI-agent orientation.** That role is owned by [`AGENTS.md`](../AGENTS.md) at the workspace root. The two docs deliberately overlap on subject matter but serve different audiences (humans vs. agents).
- **Not the customer-facing pitch deck.** This is internal — fluent, candid about gaps, names sensitive details (named churn, customer concentration, Fathom call evidence). External narratives draw *from* this set but are not the same artifact.
- **Not finished.** Every doc has an explicit "Open intelligence questions" section. Those gaps are the next quarter's work.

---

## Maintenance

- **When a foundational fact changes** (ICP definition, stamped pricing decision, primary segment counts, FY26 model version, named competitor universe), update the relevant doc and bump its `Last updated` date — and bump this file's date too.
- **When a doc is rewritten meaningfully** (not edited in place), preserve the prior version under `foundation/_archive/` so the lineage is recoverable.
- **The Open Intelligence Questions section in each doc is the foundation backlog.** When a question is closed, remove it and update the relevant section with the new figures. When a new question surfaces, add it.
- **The follow-on workstreams in the foundation backlog** close meaningful gaps in this set: M1 customer validation (JTBD + WTP interviews per segment), retention/expansion history by segment, win/loss mining by named competitor, status-quo / "we'll build it" competitor analysis, ERP-encroachment scan (NetSuite, Acumatica, Salesforce B2B Commerce, Shopify B2B), competitor scale & motion table, and the v2 of `06_how_we_operate.md` (team/org, decision rhythm, financial cadence, hiring/perf, governance, capital structure, customer-facing operating motions). Run them in priority order; refresh the affected docs when each lands.

---

## Source citation discipline

Every figure in every doc cites its source file with a workspace-relative link. If you find a number without a citation, that's a bug — flag it. The truth lives in the source files; the foundation set is the synthesis layer.

The single most-cited source files across the set are:

- [`PRICING_CONSTITUTION.md`](../skills/monetization_refresh_2026/11_synthesis/PRICING_CONSTITUTION.md) — every pricing decision (T1/T2/T3, user expansion, implementation tiers, discount policy)
- [`skills/insightful_product/01_bcf_instance_profile.md`](../skills/insightful_product/01_bcf_instance_profile.md) — the reference customer, source for any "what it looks like deployed" claim
- [`skills/insightful_product/04_value_moment_catalog.md`](../skills/insightful_product/04_value_moment_catalog.md) — the value moments framework (canonical count in the catalog)
- [`../personas/00-PERSONA-GROUPS.md`](../personas/00-PERSONA-GROUPS.md) and [`../personas/analytics/jtbd-register.md`](../personas/analytics/jtbd-register.md) — SuperCat personas (who consumes which product) and jobs; source for any "who uses it / what job / what to build" claim. Do not use PER-00…08 as that source. Roster for selling motion is `Customer Segmentation/current/`.
- [`reports/state_of_industry/state_of_industry_benchmarks_2026-01-21.md`](../reports/state_of_industry/state_of_industry_benchmarks_2026-01-21.md) — the TAM and industry-shape benchmarks
- [`skills/monetization_refresh_2026/10_exec/2026-01-29__q425_customer_base_readout.md`](../skills/monetization_refresh_2026/10_exec/2026-01-29__q425_customer_base_readout.md) — the install-base baseline (n=110)
- [`skills/monetization_refresh_2026/11_synthesis/2026-01-28__competitive_packaging_audit__m3_input__v1.md`](../skills/monetization_refresh_2026/11_synthesis/2026-01-28__competitive_packaging_audit__m3_input__v1.md) and [`2026-02-25__competitive_price_benchmarking__d004a_exercise2__v1.md`](../skills/monetization_refresh_2026/11_synthesis/2026-02-25__competitive_price_benchmarking__d004a_exercise2__v1.md) — competitive analysis
- [`skills/fy26_target_scenario/SKILL.md`](../skills/fy26_target_scenario/SKILL.md) — the FY26 plan
- [`Supercat_CEO_system_README.md`](../Supercat_CEO_system_README.md) and [`skills/ceo_system/ARTIFACT_CATALOG.md`](../skills/ceo_system/ARTIFACT_CATALOG.md) — the operating cadence
