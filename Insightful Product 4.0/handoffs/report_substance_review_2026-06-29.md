# Report Substance Review — 3.0 → 4.0 (for the agent building the 4.0 report)

> **Status**: For review · 2026-06-29
> **Audience**: The agent picking up the 4.0 org-report build.
> **What this is**: A findings doc, not a spec. It says *what substance to bring from 3.0,
> what 4.0 is missing, the structure the report must take, and where the 3.0 example breaks
> the rules we've already written.* Review it, push back, then turn the agreed parts into the
> spec (`report_product_architecture.md` + `query_library_v2.md`).

---

## 0. The decision in one paragraph

4.0 was started from the **commerce, sales-rep, and customer** query stacks — those are strong.
The gap is **substance**, concentrated in **Product Intelligence** ("the products that sell")
and in the **behavioral depth of Team Intelligence**. 3.0's org report has that substance and a
proven shape (signal-first headlines → per-section headline → collapsible deep tables). **Bring
the substance and the shape; do NOT bring 3.0's framing** — the 3.0 example leads on eCat/digital
share and pitches app adoption, which is the exact "CEO doesn't care about the channel" failure. Two
files now govern that correction: the channel-is-a-minority reality lives in `industry_context.md`
("How they sell"), and the don't-narrate-your-own-machinery voice rule is **Failure Mode 3** in
`communication_guideline.md`. Re-anchor every dollar to invoiced truth and re-sort every headline to
money/accounts/products before it ships.

**Reference example** (synthetic, 3.0): `~/Downloads/example-co-intelligence-report-3.0.html`.
Read it for substance and structure — not for tone or framing.

---

## 1. The structure the report must take (canonical shape)

This refines, but does not replace, the section model in `report_product_architecture.md`.

1. **Signal Summary first** — the actionable headlines. N findings (target 5–7) ordered by
   strategic weight (`SIGNAL_RANK`), each a single sentence with **$ + name + the move**, each
   linking to the section that carries its depth. Followed by **Priority Actions**
   (High / Medium / Growth, every line dollar-tagged) and **Questions for your next leadership
   meeting**.
2. **Each section opens on its own headline** — one finding, then a one-line metric strip
   (the "section-sub"), then the deep tables.
   - **Tie-breaker (new rule, needs your sign-off):** a section headlines a *fresh* finding only
     if it has a fired P0/P1 signal not already in the top Signal Summary; otherwise it restates
     its strongest Signal-Summary line. This stops Product/Team from echoing the summary when they
     have depth, without inventing filler when they don't.
3. **Deep tables collapse** (`<details>`), but the **action / "what this means" stays visible** —
   only the supporting tables go behind the fold. (3.0 sometimes collapses whole P2-only sections;
   that's fine, but never collapse a P0/P1 action.)

---

## 2. Substance catalog — what to bring, by section

Verdict key: **have** = exists in 4.0 and is adequate · **enrich** = exists but thin ·
**build** = no real 4.0 equivalent.

### Product Intelligence — the headline gap (4.0 was not started here)

| 3.0 insight | 4.0 today | Verdict | Note |
|---|---|---|---|
| Ghost SKU Registry (invoice rev, likely cause, "make it discoverable" action) | `Q-ORG-GHOST` | **enrich** | add likely-cause + named-account columns |
| Stock-Out Impact Board (backorder-since, est. lost $, named affected accounts, status) | `Q-ORG-STOCKOUT` | **enrich** | add affected-account names + days-on-backorder |
| Velocity Signals — accelerating / decelerating SKUs, QoQ %, reposition action | none | **build** | the "products that sell / dying" story |
| New-Item Adoption Gaps — launch date, unique buyers, adoption rate, push-to-rep | none | **build** | partly available via copilot QUERY_REFERENCE / 2.0 lib |
| Category & Collection Performance — share, YoY ("Modern +28%, Traditional −9%") | none | **build** | the portfolio-shift narrative |

This is the priority. Three new org-grain queries (velocity, new-item adoption, category
performance) + two enrichments. Anchor dollars to invoiced where a feed exists; otherwise label
eCat and cap at `COMMERCE_CONFIDENCE`.

### Team Intelligence — bring the outcome depth, demote the vanity

| 3.0 insight | 4.0 today | Verdict | Note |
|---|---|---|---|
| Rep Leaderboard | rep stack / `Q-ORG`-rep | **have** | re-anchor to invoiced, rep-identity gated |
| Presentation-to-Close Conversion | partial (VM Domain 1 / Mixpanel) | **enrich** | predicts revenue — keep |
| Engagement Trajectory (accelerating / declining reps) | partial | **enrich** | keep — leading indicator |
| Coaching Opportunities (dollar-tagged) | partial (C2 leakage, S1) | **have/enrich** | only ships with a $ attached |
| Behavioral Archetypes | VM Domain 1 | **demote** | coaching-internal, never a CEO headline |
| Selling-vs-Admin Time | VM Domain 1 | **demote** | app-usage vanity for a manufacturer CEO |

### Account Intelligence — mostly have, confirm depth

Top-N named account mini-briefs + Competitive Displacement signal + reorder-decay. Largely covered
by the customer stack + `Q-ORG-CONTRACTION` + S1; confirm the org report renders the **mini-brief**
shape (one paragraph per top account with the one move), not just a table.

### Commerce Patterns — have (you started here)

Channel mix, seasonal, quote-to-order, AOV. Strong already. Apply the channel-first framing from
`industry_context.md` ("How they sell" — eCat is a minority of total business) plus the voice rules
in `communication_guideline.md` (already corrected in the Downloads examples).

---

## 3. Push-backs — do NOT copy the 3.0 example's framing

1. **Its Signal Summary leads on the channel.** Finding #1 in the example is *"eCat sales grew
   17.4% to $8.6M, digital share 23.1%."* That is the FM9 violation. Re-sort: the real #1 is the
   money/relationship/product finding (e.g., "Aurora Sconce backorder risks $1.82M in named
   accounts"). Digital share is a Commerce-section line, never the lead.
2. **Re-anchor every dollar.** The velocity/category "Revenue LTM" columns are eCat sales printed
   as the business. Invoiced where a feed exists; otherwise labeled eCat + capped. No bare numbers.
3. **Hedge the projections.** "$186K est. lost orders" is a model output — ship it `[ESTIMATED]` /
   directional in plain English per the guideline, not as a hard figure.
4. **Kill the adoption-pitch lines.** "7 reps haven't opened eCat → recover $320K in digital
   orders" and "each point = $372K shifting to trackable digital" are upsell framing. The substance
   (which reps are disengaging) stays; the framing (grow the app) goes.
5. **Rep identity is gated.** Named reps only at the verified tier; otherwise rep-number grain.

---

## 4. Suggested build order

1. Product Intelligence queries (velocity, new-item adoption, category performance) +
   enrich Ghost/Stock-Out. **← start here, this is the gap.**
2. Wire Team outcome metrics (conversion, trajectory) into the report; demote archetypes/time.
3. Lock the canonical structure (§1) into `report_product_architecture.md`.
4. Then scaffolding: operator + HTML shell (the wrapper around the substance, not the substance).

---

## 5. Open questions for the reviewing agent

- Sign off on the **section-headline tie-breaker** (§1.2) — fresh P0/P1 or restate?
- Do the **new product queries** belong in `query_library_v2.md` as `Q-ORG-VELOCITY` /
  `Q-ORG-NEWITEM` / `Q-ORG-CATEGORY`, or is some of this already in the copilot QUERY_REFERENCE /
  2.0 library and just needs lifting to org grain?
- Confirm the **invoiced anchor** for velocity/category (most clients won't have item-grain invoice
  detail — does it fall back to eCat-labeled, or suppress?).
- Which Team metrics are CEO-grade vs coaching-internal in *your* read?

---

## Source files referenced

- 3.0 example report (substance/structure): `~/Downloads/example-co-intelligence-report-3.0.html`
- Voice rules: `Insightful Product 4.0/communication_guideline.md` (the "no shit" test, anti-cute, Failure Modes 1–5)
- Industry/channel framing: `Insightful Product 4.0/industry_context.md` (seasonality, channel mix, eCat-as-minority)
- Section model to refine: `Insightful Product 4.0/report_product_architecture.md`
- Query home: `Insightful Product 4.0/query_library_v2.md` (`Q-ORG-*`)
- Team substance source: `Insightful Product 4.0/value_moment_catalog.md` (Domain 1 / Mixpanel)
- Combined example outputs (already FM9-corrected):
  `~/Downloads/Insightful_combined_report_v1_lighthouse.md`, `..._v2_harbordale.md`
