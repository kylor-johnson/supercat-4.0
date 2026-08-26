---
id: ASSUMPTIONS
title: Assumptions register and open findings
version: 0.1
status: draft
date: 2026-08-25
owner: Kylor Johnson
source_lineage: [taxonomy/account-segments.md, taxonomy/prospect-archetypes.md, taxonomy/segment-archetype-mapping.md]
depends_on: [TAX-A, TAX-B, TAX-MAP]
---

# Assumptions register and open findings

`[ASSUMED]` items have no support and are load-bearing. Findings are `[MEASURED]`/`[OBSERVED]`
facts that are not acted on in Phase 1.

---

## A. Assumptions (no support — challenge these first)

| ID | Assumption | Where it bites | Basis |
|---|---|---|---|
| AS-01 | The four defining fields (AOV, price codes, customer count, order volume) are the *intended* definition of v4.0 | All of Layer A §4 | `[ASSUMED]` — carried from the brief as an established input. The stamped doc names a wider set and calls price a correlate, not a classifier |
| AS-02 | A person with a browser can observe everything the crawler observed, plus the 7 manual-only sites | Layer B collection model, Phase 4 field kit | `[ASSUMED]` — untested until the field kit runs |
| AS-03 | Web channel signals are a reasonable proxy for go-to-market channel structure | All of Layer B | `[ASSUMED]` — and §5 of the mapping doc is evidence against it |
| AS-04 | The 87-org back-test set is not systematically biased vs the 22 excluded orgs | Every accuracy number | `[ASSUMED]` — the excluded set skews toward orgs with no domain or dead domains, which plausibly skews older/smaller |
| AS-05 | Archetype evaluation order (ARCH-01 → 03 → 02 → 04) is the right precedence | Layer B §3 | `[ASSUMED]` — reasoned, not tested against alternative orders |

---

## B. Data-quality items

| ID | Item | Detail | Action |
|---|---|---|---|
| DQ-01 | Malformed `organizations.company_website` | `kal` = `www.kalco.com \| www.allegricrystal.com`; `sbmh` = `http://www.modernhistoryhome.com,http:// www.somersetbayhome.com`; `wac` = `https://www.waclighting.com & https://www.modernforms.com/` | Fixed **in working copy only**. Postgres not written to. Three orgs carry a real second brand domain that the schema has nowhere to put |
| DQ-02 | 9 roster orgs have no `company_website` | `all`, `dals`, `hf`, `hvl`, `ilc`, `mlg`, `ssi`, `ufi`, `yw` | Unfixed. Blocks Layer B entirely for these orgs |
| DQ-03 | 6 roster domains are dead | `arl`, `cl`, `pw`, `soi`, `tl`, `uhc` (DNS fail or 404) | Unfixed. May indicate churned or renamed entities |
| DQ-04 | 4 domains serve multiple roster orgs | `visualcomfort.com` ×4, `eglo.com` ×2, `interludehome.com` ×2 | Layer B cannot distinguish sibling brands. Structural, not fixable |

---

## C. Findings carried forward, not acted on

| ID | Finding | Why it matters | Status |
|---|---|---|---|
| F-01 | **The stamped v4.0 §4 signatures do not reproduce.** SEG-01 "$5,000+ AOV" holds for 14/33; SEG-03 "7–35 price codes" holds for 6/24 against a median of 2 | Layer A thresholds had to be authored, not transcribed | Correction drafted in `FOUNDATION-CORRECTIONS.md`, held for approval. Stamped doc **not** edited |
| F-02 | **v4.0 is not a computable function of its four fields.** Authored rule 38.5% vs 34.9% majority baseline; best-fit ceiling 50.0% | Layer A's authority is the stamped roster as a lookup, not a rule | Recorded in Layer A §4.3 |
| F-03 | **13 roster orgs cannot be stood behind by Layer A** — 9 with zero AOV and order count, plus the stamped §5 ambiguous five (overlap = `fal` only) | Excluded from any Layer A distribution; never silently dropped (principle 6) | Recorded in Layer A §5 |
| F-04 | **Volume Distribution's 89% predictability did not reproduce.** ARCH-04 → SEG-04 at 31.2%; SEG-04's web profile is pure absence | Direct discrepancy with an established input in the brief | **Unresolved.** Likely the prior run used catalog-scale/unit-price features that are Layer A fields |
| F-05 | **ARCH-03 inverts.** Consumer pricing/cart points at SEG-02 (53.8%), not SEG-03 (15.4%) | Counterintuitive; would improve the back-test if adopted | **Not adopted** — that would be fitting to the answer key. Phase 4 hypothesis |
| F-06 | **Three brief-named candidate features do not exist observably**: rep recruiting pages (0/87), MAP policy (1/87), SKU depth (Layer A field) | Shrinks the Layer B feature space materially | Pruned with evidence in Layer B §2.3 |
| F-07 | **HPMKT footprint and LinkedIn headcount were not collected.** Both are real, both are manual-only, neither is populated | The archetypes rest on web channel signals alone | Open — Phase 4 field kit is the collection mechanism |
| F-08 | **The 79-domain denominator is unreproducible.** Roster 109 / 100 non-blank / 95 distinct / 93 manually reachable / 87 auto-observable. No artifact recording the 79-org run exists anywhere in the repo | Prior 53% figure cannot be recomputed or audited | **Closed by decision** — the prior conclusion is accepted as an established input and is not re-derived |
| F-09 | **`foundation/sources/customer_segmentation/` was a broken canonical home.** Its README named 3 files it did not contain and linked to an `agent_research/` tree that was never imported | Agents routed here by `supercat-foundation` SKILL found dead links | Links repaired to point at `Customer Segmentation/current/`. **No file copied in** — one answer key, at the path `build_v4.py` writes |
| F-10 | **`Customer Segmentation 2` is a byte-identical duplicate** of `Customer Segmentation` (`diff -rq` returns nothing) | A second copy of the answer key | **Ignore list. Do not read, cite, or write to it.** Kylor will delete it |
| F-11 | **Overlapping v4.0 signature ranges have no tie-breaker** in the stamped doc — AOV bands and price-code bands overlap across three segments with no stated precedence | Forced the authoring of a precedence rule | Precedence rule authored and justified in Layer A §4.1 |
| F-12 | **Sales Portal Territory Dashboard is enabled for zero organisations** — `:portal_portal` resolves to 9 internal SuperCat usernames only | There is no incumbent rep analytics surface | Carried to Phase 3 `product/surface-mapping.md` as a first-class result |
| F-13 | **Anatomy vs spec persona conflict.** `PLATFORM_ANATOMY_CURRENT_STATE.md` assigns Sales Portal to "sales leadership and CS"; `00-SALES-PORTAL-SYSTEM-SPEC.md` lists sales representatives first | Two stamped docs, same surface, different primary persona | **Flagged, not resolved.** Phase 3 decision |
| F-14 | **The buyer is the Sales Portal's primary population.** 78,046 enabled / 17,532 active in 90 days vs 15,987 / 2,274 rep-or-internal — 7.7:1 on active logins, across 52 orgs with `enable_sales_portal` `[MEASURED 2026-08-25]` | Buyer persona added to Phase 2 scope | Confirmed; axis to be tagged as our-customer's-customer |

---

## D. Scope boundaries honoured

- Established inputs 1–4 from the brief were **not** re-litigated or re-tested.
- The stamped v4.0 document, `build_v4.py`, and the MASTER CSV were **read only**.
- `foundation/CEO_SYSTEM_CONTEXT.md` and `foundation/02_who_we_serve.md` were **not edited**;
  corrections are held in `FOUNDATION-CORRECTIONS.md`.
- Insightful profiles (`kal.md`, `da.md`, `hfg.md`, `bsc.md`) and `industry_context.md` were **not
  touched**; the "Brand-Building" alias was not swept.
- Postgres was **read-only** throughout. No writes, including the DQ-01 malformed values.
- Lens 1 (Digital Selling Maturity) and T1/T2/T3 pricing were **not touched**.
