---
name: supercat-foundation
description: "SuperCat company context (L1) — ICP and the two segmentation lenses, T1/T2/T3 pricing, competitive set, strategic bets, FY26 headline targets, product surfaces, and how confident we're allowed to be before citing a figure. Use this BEFORE answering anything about what SuperCat is, who we serve, how we make money, where we're going, or how the company operates — including lazy phrasings like 'what's our ACV again', 'is X a T2', 'what's Platform-Embedded mean', or 'can I say $768M GMV in a deck', and including when drafting customer-, investor-, or board-facing material that leans on those facts. Trigger it even when the question sounds answerable from memory: the figures move quarterly. NOT for live org lookups (use supercat-data-routing), report runs (insightful-report-4), eCat file builds or import debugging (ecat-* skills), or workspace navigation (AGENTS.md)."
---

# SuperCat Foundation — L1 context router

## What this skill is

The **L1 context entry point**: it decides *what SuperCat is* and routes to the
authority. It holds no facts of its own.

That is deliberate. `foundation/` is a synthesis layer over stamped sources, and
`foundation/CEO_SYSTEM_CONTEXT.md` is already its agent-optimized condensation.
Restating figures or doctrine here would create a copy that no `git log` catches —
the failure mode `foundation/00_README.md` names ("the truth lives in the source
files"). **Read the doc, cite the doc, never answer SuperCat facts from memory.**

## Do this first

Read **`foundation/CEO_SYSTEM_CONTEXT.md`**. It condenses `foundation/01`–`07`,
opens with number discipline, and names the source doc at the end of each
section. It already contains the install-base count caveat, the selling-instrument
vs. order-consummation contract, and the marketing-niche vs. analytical-ICP
distinction — do not reconstruct those from elsewhere. For most questions it is
sufficient alone.

**If these paths don't resolve, you are not in the repo — or the workspace is out
of sync.** Say so plainly and ask for the doc or the relevant pasted section. Do
**not** fall back to memory. That failure is silent, sounds confident, and is the
entire reason this skill exists.

## Depth routing — `foundation/`

| The question is about | Read |
|---|---|
| Orientation, identity, at-a-glance | `foundation/00_README.md` |
| Product surfaces, gating layers, value-moment framework, BCF as deployed | `foundation/01_what_we_do.md` |
| "What is the platform?" — spine → actors → surfaces → capabilities, as shipped | `foundation/PLATFORM_ANATOMY_CURRENT_STATE.md` |
| ICP, both lenses, buyer types, our customers' customers, market context | `foundation/02_who_we_serve.md` |
| Pricing, tiers, ACV, MRR, revenue targets, migration plan | `foundation/03_how_we_make_money.md` |
| Competitors, buyer friction, where we win/lose, response playbooks | `foundation/04_market_and_competitors.md` |
| Active bets, 10-year target, deliberate exclusions | `foundation/05_strategic_direction.md` |
| Data spine, CEO System cadence, editorial-feedback protocol | `foundation/06_how_we_operate.md` |
| Whether a number can be stated at all | `foundation/07_how_we_establish_truth.md` + the `truth-discipline` skill |
| Shaping a bet, prototype-first, the five gates, decision rights | `foundation/08_how_we_build.md` |
| Building/running/certifying a commercializable agent, L0–L4 harness | `foundation/09_agent_factory.md` |

## Depth routing — stamped sources

`foundation/` summarizes and points. **On conflict, the stamped source wins.**

| Claim type | Authority |
|---|---|
| Any pricing decision (tiers, user expansion, discount policy, implementation) | `foundation/sources/monetization_refresh_2026/11_synthesis/PRICING_CONSTITUTION.md` |
| Pricing background, mechanics, rate context | `foundation/sources/monetization_refresh_2026/01_reference/MONETIZATION_REFERENCE.md` |
| Which tier an account maps to; willingness-to-pay | `foundation/sources/monetization_refresh_2026/11_synthesis/2026-02-25__install_base_tier_mapping_wtp__d004a_exercise1__v1.md` |
| Product surfaces, gating layers, adoption counts (code- and DB-verified) | `foundation/sources/monetization_refresh_2026/11_synthesis/2026-01-28__product_capability_map__m3_input__v1.md` |
| What the Insights Layer *is*, commercially | `foundation/sources/monetization_refresh_2026/01_reference/2026-01-30__insights_layer_definition__v1.md` |
| Competitor packaging and feature fences | `foundation/sources/monetization_refresh_2026/11_synthesis/2026-01-28__competitive_packaging_audit__m3_input__v1.md` |
| Competitor pricing comparisons | `foundation/sources/monetization_refresh_2026/11_synthesis/2026-02-25__competitive_price_benchmarking__d004a_exercise2__v1.md` |
| Install-base baseline | `foundation/sources/monetization_refresh_2026/10_exec/2026-01-29__q425_customer_base_readout.md` |
| Selling Motion (Lens 2) — model and methodology | `foundation/sources/customer_segmentation/README.md`, `Customer Segmentation/current/SuperCat_Client_Segmentation_v4.0.md` |
| Selling Motion (Lens 2) — per-org roster and buyer-type evidence | `Customer Segmentation/current/SuperCat_Customer_Segmentation_v4.0_MASTER.csv`, `foundation/sources/customer_segmentation/account_buyer_type_reads.csv` |
| "What it looks like deployed" / reference customer | `foundation/sources/insightful_product/01_bcf_instance_profile.md` |
| Value moments — the catalog itself | `Insightful Product 4.0/foundation/capability/value_moment_catalog.md` |
| Truth/confidence rules (Tier 0 — wins over `foundation/07`) | `Insightful Product 4.0/foundation/provenance_spine.md` |
| TAM and industry shape | `reports/state_of_industry/state_of_industry_benchmarks_2026-01-21.md` |
| FY26 plan | `foundation/sources/fy26_target_scenario/SKILL.md` |
| Operating cadence — artifact inventory | `foundation/sources/ceo_system/ARTIFACT_CATALOG.md`, `Supercat_CEO_system_README.md` |
| Agent Factory (Notion wins over `foundation/09`) | Touchstone Notion page linked in `foundation/09_agent_factory.md` |

## Route elsewhere — this skill is the wrong tool

Answer the context question, then hand off. Do not attempt these here.

| The ask | Goes to |
|---|---|
| Live org state — is X enabled, what is X paying, current counts | `supercat-data-routing` (Postgres / BigQuery) |
| Generating a customer report or CS brief | `insightful-report-4` |
| eCat file builds, import failures, customer/product load debugging | `ecat-*` skills |
| Support ticket triage and replies | `ecat-support-triage` |
| FY26 waterfall, scenario math, target modeling | `fy26_target_scenario` (this skill gives the headline only) |
| Where things live in the workspace; active vs. frozen; file conventions | `AGENTS.md` at workspace root |

**Mixed asks are common and are the main failure mode.** "What tier should we put
them on" needs this skill for the tier model *and* `supercat-data-routing` for the
account's actual behavior. Do both and say which half came from where — never
infer live account state from a foundation figure.

## When the docs disagree

They currently do. Prefer the later `Last updated` stamp, go to the source file
named in the citation, and **tell the user you found a conflict** rather than
picking silently. Drift is a bug to surface, not a detail to smooth over. Same
for a bare figure with no citation — `foundation/00_README.md`: "that's a bug —
flag it."

## Maintenance

This is a router; its only failure mode is a stale route. Update it when a doc is
added, renamed, or moved, or when a domain skill is added to the hand-off table.
It should not need updating when a figure changes — **if you are editing a number
in this file, the number does not belong here.**
