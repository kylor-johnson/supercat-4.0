# Report Editorial Rules v4 — Insightful 4.0

> **Status**: Active (merge build, 2026-06-29)
> **Lineage**: The **3.0 `shared_rules.md`** editorial system (`Insightful Product 3.0/authority/shared_rules.md`) —
> the narrative arc, the specificity standard, client-facing language, the competitive-hypothesis requirement, and
> the what-this-means discipline — **kept almost verbatim** (it is the dope voice that makes clients say *"I need
> this"*). The **only** substantive change is §D: 3.0's dollar-tag system is replaced by the 4.0 **three-tag**
> provenance stamp. Everything else here is the 3.0 ruleset, adopted.
> **Embed**: include this file in every section context bundle (as 3.0 did with `shared_rules.md`).
> **Scope vs. the other voice docs** (per [`CANON.md`](../CANON.md)): this file is the **report-structure**
> voice — narrative arc, specificity standard, client-facing language, the three-tag dollar rules. Two
> companion knowledge-layer docs sit beside it: [`industry_context.md`](../knowledge/industry_context.md) decides
> whether a pattern is even a *finding* (seasonality, concentration, channel mix are industry-normal),
> and [`communication_guideline.md`](../knowledge/communication_guideline.md) is the cross-cutting voice test (the
> "no shit" rule, anti-cute, Failure Modes 1–5). Where this file overlaps the comms guideline on tone,
> the comms guideline's test governs.

---

## A0. Editorial voice — the North Star *(kept from 3.0)*

**This is an intelligence report, not a risk report.** The reader should finish thinking *"I didn't know that about
my business — I need to pay for this,"* not *"everything is broken, I should churn."*

**Narrative arc (MANDATORY), every section and the whole report:**
1. **MOMENTUM** — what's working; name the reps/accounts/products driving growth. The credibility foundation.
2. **INTELLIGENCE** — what's interesting; data-dense, cross-customer, behavioral — the "holy shit" layer.
3. **OPPORTUNITY** — what could be better; framed as growth, not repair.
4. **RISK** — what to watch; **last**, contextualized within the positive narrative.

**Tone rules (kept):** lead with strength; always contextualize risk ("you drove $Y; $X of that is at risk
from [pattern]"); frame negatives as opportunities; ban doom headlines ("ALERT/DETECTED/WARNING" reserved for true
P0 operational issues — stock-outs, staleness); celebrate specific wins by name.

**Report-level balance test (kept):** ≥3 of 7 Signal-Summary findings positive; **Finding #1 must be positive**;
≥1 of the priority actions must be a growth action.

> **4.0 note:** the balance rule is now *protected by* the provenance layer, not threatened by it. Even when
> economics confidence is only PARTIAL, the momentum opener can ship as a **directional / eCat-labeled** win
> (SIG-MOM-01), so honest confidence never forces a doom-first report.

---

## A1. Client-facing language *(kept from 3.0, verbatim intent)*

Audience = a VP of Sales / owner at a lighting, furniture, or home-decor manufacturer. They think in reps, dealers,
showrooms, orders, products — not platform metrics. Banned → use instead:

| Banned (SaaS/tech) | Use instead |
|---|---|
| "capture rate" / "platform capture rate" | "digital ordering share" / "share of orders placed through eCat" |
| "platform GMV" | "eCat sales" / "orders placed through eCat" |
| "collaborative filtering" / "Next Best Product" | "products your customers buy together" / "Products Frequently Bought Together" |
| "activation" (accounts) | "onboarding" / "getting them ordering through the app" |
| "behavioral data reveals" | "your team's usage patterns show" |
| "platform" (standalone) | "eCat" / "the app" / "your digital catalog" |
| "addressable revenue" | "potential" / "available" |

**Fine** (sales-leader vocabulary): conversion rate, YoY, trailing 12 months, reorder velocity, AOV, LTM, QoQ,
fill rate, pipeline, territory, funnel.

**4.0 addition to the banned list (internal-only terms — never client-facing):** `COMMERCE_CONFIDENCE`,
`FEED_COMPLETENESS`, `Q-ECON-00`, `house_suspect`, `rep_number` tier, `CORROBORATED/PROVABLY-INCOMPLETE`,
"booked vs invoiced." These are how we *decide* what to print; they are not how we *talk to the client.* Translate
them (see §D3).

---

## A. Specificity standard (the #1 rule) *(kept from 3.0)*

Every claim must name a specific customer/item/rep **and** include a dollar **and** state an action **and** carry a
time qualifier. Fail one → rewrite or delete.

- **BAD:** "Consider re-engaging dormant accounts to recover lost revenue."
- **GOOD:** "Call Ticking Stripe — $227K invoiced LTM, last ordered Oct 16 2025 (244 days). Rep: Sheryl Lowe."

---

## B. Signal hierarchy *(kept)*

P0 = must surface in Signal Summary if detected. P1 = surface if top 10 by `SIGNAL_RANK`, else section detail.
P2 = section detail / collapsed only. Diversity: **max 4 of 7** Signal-Summary slots from one section.

---

## C. Fragment contract (HTML) *(kept)*

Standalone HTML fragments using only template classes; section `id ∈ {signals, accounts, product, commerce, team,
platform}`; every section ends with a `.what-this-means` block (≤3 sentences); tables show top 5 + `<details>`
collapse; ≤4 metric cards per row; coaching cards only for reps with >$50K estimated upside.

---

## D. Dollar math — **the one rule that changed** (3.0 → 4.0)

3.0 tagged dollars `[HYPOTHETICAL]` / `[ESTIMATED]` / `[eCat ONLY]` / `[ALL-CHANNEL]`. **4.0 replaces that with the
three-tag provenance stamp from the Spine.** No bare numbers, ever.

### D1. Every money number carries THREE tags internally, or it does not ship
`[source]` (invoiced / booked / eCat) · `[confidence]` (STRONG / PARTIAL / LIMITED / NONE — **FULL retired**) ·
`[completeness]` (CORROBORATED / UNVERIFIED-SINGLE-FEED / PROVABLY-INCOMPLETE / STALE / DEAD).

### D2. Confidence is capped, never asserted
`signal_confidence = LEAST(signal_ceiling, COMMERCE_CONFIDENCE)`. A composite is never more confident than its
weakest input. When the rule says suppress, **suppress — do not approximate.**

### D3. How the three tags become client-facing language (translation table)
The client never sees the tag words. They see the *consequence*:

| Internal stamp | Client-facing rendering |
|---|---|
| `invoiced · STRONG · CORROBORATED` | plain dollar, "across all channels" — e.g. "$15.6M in total business (last 12 months)" |
| `invoiced · STRONG · UNVERIFIED-SINGLE-FEED` | plain dollar + "based on your invoiced sales" (no "complete/total business" claim) |
| `eCat · LIMITED · —` | "$X in orders placed through eCat" (channel statement, never total) |
| `… · PROVABLY-INCOMPLETE / DEAD` | **suppress the number**; render the "with connected data" callout instead |
| projection (behavior change assumed) | the word **"estimated"** in the sentence (drops the bracket tag) |

### D4. Retained 3.0 rules
eCat figures are eCat-channel unless stated; `portal_orders` (booked) only as a labeled fallback or completeness
cross-check, **never the topline**; never claim broader than the data supports.

---

## E. Semantic rules (locked) *(kept from 3.0 + 4.0 reinforcements)*

1. `portal_orders` = booked orders across channels — **never** "buyer self-service." Topline is invoiced net.
2. If a behavioral feed is absent, its section does not exist — don't reference it elsewhere.
3. **Health score is INTERNAL only**; it inherits the lowest input's confidence (cap or decompose).
4. **Segment labels are 🧊 FROZEN** — never internal *or* external (Spine §8). *(Stricter than 3.0, which allowed
   internal segment labels.)*
5. **Peer benchmarking EXCLUDED entirely** — no quartiles, medians, cohort comparisons. Peer data is unreliable.
6. **Rep naming obeys the identity tier** (Spine §7.1): Tier 2 named; Tier 1 `rep_number`; Tier 0 behavior-only,
   no rep→revenue. Never silently drop an unmapped rep from a ranking.

---

## F. Time-qualifier rule *(kept)*
Every metric needs a time qualifier. "$4.7M in eCat orders (May 2025–May 2026)," not "$4.7M." And every total also
carries its clamped `report_through_date` window.

---

## G. Signal Summary construction *(kept)*
Built **last** from section highlights. 5–7 findings sorted into narrative arc (not raw rank); Finding #1 positive;
≥3 positive; risk in slots 5–7; ≥1 immediate ("this week") action; diversity max-4-from-one-section. 2–4 priority
actions tagged HIGH/MED/LOW each with a dollar; 2–3 conversation questions.

---

## H. What-this-means blocks *(kept, with self-check)*
End every section with a ≤3-sentence `.what-this-means`: sentence 1 = the strength to protect / opportunity to
capture; sentence 2 = the specific growth-framed action; sentence 3 (optional) = what more data would enable, or
the cost of inaction **after** the positive framing. Never restate the table; never lead with doom. Apply the
3-question self-check (restatement / action / specificity) before saving any fragment.

---

## I. "With connected data" callouts *(kept — now also the hard-gap home)*
When a section would be dramatically better with data the client could provide, render one `.callout.opportunity`:
*"If [data] were connected, this section would show [intelligence] — [estimated value]."* Max 1/section. **This is
where 4.0's suppressed hard gaps live** (true margin/COGS, AR/DSO, channel attribution, carrier/claims, parent
rollup) — surfaced as the upsell, never faked (see `signal_catalog_v4.md` SIG-EXT-*).

---

## J. Output prohibitions *(kept + 4.0)*
Never improvise around missing data (gate not met = skip silently or suppress). "ERP" banned in client HTML except
one appendix attribution row. Internal/debug language banned. Generic recommendations banned. **No insight a client
could get from their own ERP dashboard** — our value is cross-customer patterns, behavioral data, inventory×demand
crossovers, products-bought-together, and **defensible leakage/revenue-at-risk dollars**. **4.0 add:** never print
a booked, capped, or incomplete number in a way a reader could mistake for a hard invoiced fact (the fourth test).

---

## K. Highlight-file contract *(kept)*
Each section emits `cache/section_NN_highlights.md` with 2–4 candidates (headline + dollar + `surprise_score` +
`signal_id` + **the three-tag stamp**). The Signal Summary builder reads all highlight files, selects top 5–7 by
`SIGNAL_RANK` under the diversity constraint, and re-sorts into narrative arc.

---

## L. Collapse behavior *(kept)*
Progressive disclosure: section-level (P2-only sections collapse), sub-tables (top 5 + details), account
mini-briefs (top 5 full, 6–10 collapsed), rep leaderboard (top 5 + two collapse tiers), low-priority actions
collapsed.

---

## M. Competitive-hypothesis requirement *(kept from 3.0, verbatim)*
When any account shows YoY decline > 25% **and** LTM (or prior-year) invoiced revenue > $50K, the report MUST give
2–3 investigative hypotheses (channel consolidation / competitive displacement / internal change / price
sensitivity / seasonal-project), never stating a competitor as fact ("we can see the decline, not the cause"), and
close with a specific investigative action for the assigned rep. Render via the `.callout.insight` "Decline
Investigation" block. This fires on SIG-DECAY-04 and SIG-ANOMALY-03.

---

## N. Render-time editorial enforcement *(NEW 2026-06-30 — PASS1 validation findings)*

These checks fire during `operators/report_operator.md` Step 10 (provenance + static check). Each one is
a **deterministic regex / structural check** the operator runs against the assembled markdown BEFORE writing
the file. A check that fires either DELETES the offending fragment or HALTS the render with a named error —
**never patches the output text in place** (the Sarreid lesson: defects patched in output recur in the next
org because the canon that produced them never changed).

Every check below closes one or more PASS1 defect register entries; the closure tag is in the heading.

### N.1 — `HOUSE-LEAK` check *(closes cci §C.1, cci §E.1, kal §C.1, kal §C.2)*

**Fires if any rendered §2 leaderboard row, §2 coaching card, §3 mini-brief rep cell, "This Week's Outreach
List" row, or Appendix Traceability line contains a `rep_label` that matches the auto-rule
`ILIKE 'house%'` OR `ILIKE '% house account%'` OR appears in the per-org EXCLUDE list of
[`../config/house_rep_exclusions.md`](../config/house_rep_exclusions.md) for the current org.**

**Action.** HALT the render and surface the offending row with the message *"HOUSE-LEAK: rep_label
`{label}` was rendered in `{section}` despite the house-rep screen. Re-check `rep_copilot_operator.md` §3
RS-01 SQL and `rung4_option_a_operator.md` §2 O1/O2 SQL — both must apply the AUTO-RULE and the per-org
EXCLUDE rows. Do not patch the output; fix the operator invocation."* See §5a.0 invocation contract.

### N.2 — `FM9-CHANNEL-LEAD` check *(closes cci §B.1, kal §B.1)*

**Fires if any §2 leaderboard "What it is" cell, or any §3 watchlist "Notes" cell, contains a pre-judging
narration phrase that the editorial layer is supposed to suppress.** Banned phrases (case-insensitive,
applied to those cells only):

- "top growing" / "top-growing" / "largest YoY decline" / "largest year-over-year decline"
- "breakout year" / "breakout book" / "soft decline" / "concentrated book"
- "widest coverage" / "high coverage" / "selectively growing minority"
- Any sentence that **renders judgment of the rep before the human sees the dollar** ("declining sharply",
  "growing on a concentrated book", "biggest decline on a top-10 book").

**Why.** Failure Mode 3 of `knowledge/communication_guideline.md` ("don't narrate the client's own machinery
back to them") + the §A specificity standard. The "What it is" cell should carry **a fact, not a verdict**:
the YoY % and customer count are already in the row; the cell either restates them in three words ("Flat",
"−12% YoY, 485 dealers") or is empty.

**Action.** DELETE the offending cell content; replace with the bare YoY % + customer count from the row's
own data, or `—` if neither adds information. Do not invent a softer phrasing — the cell goes empty.

### N.3 — `CROSS-ORG-LEAK` check *(closes cci §B.2, kal §B.4)*

**Fires if a customer-facing section (Signal Summary, §2–§6, Priority Actions, "What the data can't tell
you", Account watchlist, Outreach List) contains the literal name of any OTHER org from the validation
cohort or any prior worked example.** Banned literals (case-insensitive, in customer-facing copy only —
the Appendix Traceability is exempt):

- `Sarreid`, `sarreid`
- `Currey & Company`, `currey & company`, `cci` (when not the current org)
- `Kalco`, `Allegri`, `kal` (when not the current org)
- `Hubbardton Forge`, `hfg` (when not the current org)
- `Shadow Catchers`, `sca` (when not the current org)
- Any other org shortname from `foundation/provenance_spine.md` §7.1 Tier cohort tables (clc, mhc, wwjc,
  pf, ril, bcf, gh, scw, sc, clm, clli, bri, vic, shl, jyc, ufi, heb, kll, lpf, asi)

**Why.** A customer-facing report is a one-org artifact; benchmarking against another named client
violates the §E.5 peer-benchmarking exclusion and is a confidentiality leak besides. Cross-cohort
*context* belongs in internal validation notes, not in the customer file.

**Action.** DELETE the comparison sentence and the named-org literal. If the comparison carried a
substantive point (e.g. "our NRR is {X} vs the industry-normal {Y}"), rewrite without naming the other
client: "industry-normal NRR is roughly {Y}; this org's {X} is {above/below/at} that."

### N.4 — `CUTE-METAPHOR` check *(closes cci §B.4, kal §B.3)*

**Fires if the same metaphor appears more than once across §1–§6 of a single report**, or if any of the
following banned metaphors appear at all in customer-facing copy:

- "engine" (the metaphor that recurred 3× at cci, 2× at kal — banned outright; use the literal noun:
  "returning base", "Nottaway family", "Flint family")
- "leaking" (when not the literal `Q-ECON-LEAK` term in the Appendix)
- "bleeding" (Karen-style melodrama; use "declining" or "at risk")
- "war room" / "fire drill" / "moonshot" / "north star" / "single throat to choke"
- Any "is the X of Y" comparison ("Nottaway is the cci engine")

**Why.** The "no shit" test (`knowledge/communication_guideline.md`) plus the anti-cute rule: metaphors
substitute for specificity. The data speaks; the metaphor undermines the data by sounding like marketing.

**Action.** Replace the metaphor with the literal noun + the figure. "The Nottaway chandelier is the
single-SKU **engine** — $724K…" → "The Nottaway chandelier is the **single largest SKU** — $724K…"

### N.5 — `UNTRACEABLE-ARITHMETIC` check *(closes cci §A.4, cci §E.5, kal §A.4 — Step 10 DELETE rule)*

**Fires if any rendered dollar figure does NOT trace to a query named in the Appendix Traceability table.**
This is the canonical Step 10 rule, re-stated here because PASS1 found it was NOT being enforced on
**editorial arithmetic** — specifically the "$X per 5pt move on new-logo retention" sensitivity number.

The Sarreid lesson: this number ($300K at Sarreid, $420K at cci, $45K at kal) is **editorial arithmetic
done in the prose** (`5% × N_cohort × avg_reorder`), NOT a query result. It carries no source tag and
traces to no `Q-RET-SENSITIVITY` query (because none exists). **It must be deleted in Step 10.**

**Action.** DELETE any sentence of the form *"Every {N} {points|pp} moved … is **estimated** … {$X}"*
unless the figure traces to a named query in the Appendix Traceability block. The narrative reads
cleaner without it; the cohort-size finding (`{N_cohort} dealers, {Y%} second-year return rate`)
already carries the operational signal. Editorial arithmetic is not a finding.

**Same rule fires on** any "estimated $X" / "approximately $X" / "roughly $X" / "≈ $X" that has no
Trace line. The `estimated` word does not exempt a dollar from the three-tag rule (§D3 says the word
*replaces the bracket tag* — it does not replace the trace requirement).

### N.6 — `VISUAL-CUE` check *(closes cci §B.5, kal §B.5)*

**Fires if any emoji or visual cue glyph appears in a customer-facing section.** Banned glyphs:
⚠ ✅ ❌ 🟢 🟡 🔴 ✨ 🎯 🚨 (and any other emoji). Plain text only. The Appendix is exempt only for
internal provenance footers (`[from-live]`, etc.).

**Action.** DELETE the glyph; if the row needed flagging (e.g. house-rep row), the §N.1 `HOUSE-LEAK`
check should have caught it — re-run §N.1.

### N.7 — `CHANNEL-NONE-SUPPRESSION` check *(closes kal §C.8, hfg §C.2)*

**Fires if `Q-CHAN-00 = NONE` (suppress channel section) but the §4 commerce section either (a) renders
a channel decomposition table anyway, or (b) renders a custom hand-written suppression note that does
not match the canonical template in §O below.** This is the determinism failure where two validators
wrote two different "channel suppressed" sentences.

**Action.** Replace the section content with the canonical template from §O (Q-CHAN-00 NONE suppression
template). Same applies for `Q-CHAN-00 = PARTIAL` / `STRONG-CANDIDATE` — use the templated language
exactly, do not paraphrase.

### N.8 — Render-pipeline contract

`operators/report_operator.md` Step 10 runs §N.1 through §N.7 in order. **Each check that fires either
DELETES a fragment (N.2, N.3, N.4, N.5, N.6, N.7) or HALTS the render (N.1).** A HALT requires the
operator to be re-run after the upstream operator/config fix; the report does not patch around a HALT.

These checks are the structural enforcement of the rules already stated in §A–§M. They exist because
PASS1 found that voice-rule violations were not being caught at render time; the rules were aspirational,
not enforced.

---

## O. Canonical suppression templates *(NEW 2026-06-30 — closes kal §C.8, hfg §C.2, sca §A.2, sca §C.3)*

When a gate suppresses a section or subsection, the operator emits the **exact** template language below.
Validators MUST NOT paraphrase; deviations are caught by §N.7 and §N.8.

### O.1 — Q-CHAN-00 = NONE (channel section suppressed)

```
### Channel context — **suppressed**

`Q-CHAN-00` posture for {org}: **NONE — SUPPRESS channel section (insufficient origin signal).** {org} has
**{distinct_origins} distinct `order_origin` values** on ${booked_dollars} of booked LTM orders (the field
is {uniformly NULL or blank | uniformly the string "{single_value}"}). No channel decomposition can be
rendered. Per the Q-CHAN-00 gate, the channel section is suppressed.

eCat is overlaid from `orders` truth in §6 below.

`[Q-CHAN-00 · NONE — suppressed]`
```

### O.2 — Q-CHAN-00 = PARTIAL (eCat folded; partial channel render)

```
### Channel context — partial

`Q-CHAN-00` posture for {org}: **PARTIAL** — {distinct_origins} distinct origins; eCat tag {status}
({ratio}× reconciliation vs confirmed eCat GMV). Channel decomposition renders with eCat folded into
'Other' (where applicable); per the gate, eCat dollars are overlaid from `orders` truth, not the
origin column.

{render the channel table with eCat = "see §6 for capture (orders truth)"}

`[Q-CHAN-00 · PARTIAL · {ecat_tag_status}]`
```

### O.3 — `COMMERCE_CONFIDENCE = NONE` (truth-axis suppression — full Mode-2 / Tier-0 surfaces)

```
### {section} — **suppressed**

`COMMERCE_CONFIDENCE = NONE` for {org}: no `portal_invoices` rows on the LTM window (`n_inv = 0`,
`inv_ltm_net = $0`). Per the report operator (§5b.3) and the Spine (§1 — *"if there is no ERP feed,
there is no commercial outcome to report"*), {section} is suppressed. The org runs on the **Rep
Copilot operator** (`operators/rep_copilot_operator.md`) in its Tier-0 behavior-only branch; that
operator emits the R1–R4 behavior layer and does NOT make any rep → revenue claim.

`[COMMERCE_CONFIDENCE · NONE — section suppressed]`
```

### O.4 — `REP_IDENTITY_TIER < 2` (rep-name suppression for §2 coaching cards)

```
### Coaching cards — **not rendered at this rep-identity tier**

`REP_IDENTITY_TIER` for {org} is **{tier}** (bridge {pct}% < 80% boundary, or no `rep_number` key at all).
§2 falls back to the RS-01 leaderboard at **`rep <n>` grain** (no names); coaching cards do not render
below Tier 2 per `report_operator.md` §5a.1 / `rung4_option_a_operator.md` §1. See the Appendix for
which `rep_number` rows did not resolve to a name (they are NEVER silently dropped from the leaderboard
— Spine §7.1 red line).

`[REP_IDENTITY_TIER · {tier} — coaching cards suppressed]`
```

### O.5 — `FEED_COMPLETENESS = STALE / DEAD` (Reactivation mode header)

```
### Header note — **feed staleness**

`FEED_COMPLETENESS = {STALE | DEAD}` for {org}: last invoice {date} ({days} days stale). Per the
Reactivation mode (operator §3), every $-at-risk and forward-looking figure is rendered as
**historical**, never pushed as live. `report_through_date` pins to the last real invoice.

`[FEED_COMPLETENESS · {STALE | DEAD} — historical only]`
```

These five templates are the canonical wording for the five gate-suppression states. **The operator
emits them verbatim; validators do not paraphrase.** §N.7 enforces this at render time.

### O.6 — Narrative-form expansion permitted *(NEW 2026-06-30 — hfg cohort lesson)*

The §O.1–§O.5 templates above are intentionally terse (single-paragraph render-time fillers). When the
terse form would dilute the consultant-briefing voice — e.g. a Tier-1 fallback that needs to explain
**why the cards are held back + what the operational fix is + how that fix matters** — a narrative-form
expansion is permitted, **provided all three of**:

- **(a) The gate state is named verbatim** in the body — the exact tier number, the exact bridge
  percentage, the exact `Q-CHAN-00` posture, etc. The template's load-bearing facts cannot drift.
- **(b) The operational fix is given inline** — "backfill 12 rep-name rows on the booked-orders feed,"
  not just "see Appendix." A narrative expansion that omits the fix is a §N.7 violation.
- **(c) The verbatim canonical footer line is present** — `[REP_IDENTITY_TIER · {tier} — coaching cards
  suppressed]` (or the §O.1 / §O.2 / §O.3 / §O.5 equivalent) MUST appear at the end of the block,
  unaltered. The footer is what makes the render deterministic for downstream tooling.

**Worked example** *(use as the §O.4 narrative-form pattern)*: the hfg PASS3 §6 "Coaching cards — held
back in this report" block, which expanded the §O.4 terse template into a 12-line consultant-voice
explanation while preserving the footer line verbatim. Voice is better than the terse template; the
footer keeps determinism intact; (a), (b), (c) all satisfied.

**§N.7 enforcement update.** The check now passes when **either** the terse template is emitted
verbatim **or** the three §O.6 conditions are all met. A narrative expansion missing any of (a)/(b)/(c)
fails the check and is replaced with the terse template.

---

## P. Forbidden-vocabulary regex sweep *(NEW 2026-06-30 — gold-stamp absorption)*

> **Why this exists.** §A1 already lists a small "use instead" table of banned SaaS terms, and §N.2/§N.4/§N.6
> catch narrow narration / metaphor / glyph defects. The Sarreid gold-stamp audit (handoff §3a) showed the
> next defect class is broader: **a senior furniture-industry consultant does not write the words "NRR / cohort /
> playbook / new logos / ICP / motion / GTM / playbook / north-star / operator / preflight / portal_invoices".**
> §P is the hard render-time fail-list that catches every such hit across the entire output (HTML and MD).
>
> **The bar this gate enforces:** *if any sentence in the output reads like a SaaS analyst, a CRO, a revenue-ops
> PM, or a SuperCat engineer wrote it, the run fails.* See `knowledge/communication_guideline.md` "The bar".

### P.1 — The banned-token list (regex, case-insensitive)

The operator runs this sweep against the rendered HTML and the rendered MD **separately** in Step 10. Each list
below is the **literal banned phrasing in customer-facing copy**. Banned tokens may appear in the Appendix
Traceability footers (internal provenance) and **nowhere else**.

**A — SaaS / CRO / revenue-ops vocabulary** *(supersedes the §A1 use-instead table — this fires render-fail):*

- `NRR`, `net revenue retention`, `GRR`, `gross revenue retention`, `MRR`, `ARR`
- `new logo`, `new logos`
- `playbook`
- `cohort` *(in retention / customer-base contexts; allowed only as "buyer cohort" when domain-true)*
- `ICP`, `TAM`, `SAM`, `CAC`, `LTV`
- `AOV` *(only when context is non-furniture; allowed in furniture-order context per §A1)*
- `MoM`, `QoQ`, `YoY` as an acronym without a number adjacent
- `funnel`, `pipeline coverage`, `win rate`, `motion`, `GTM`, `expansion revenue`
- `land and expand`, `PLG`, `north-star`, `north star`, `DAU`, `MAU`

**B — Internal codes / system identifiers** *(any client-facing leak is an automatic fail):*

- `S1`, `C2`, `K7`, `VM-\d+`, `VM-[A-Z]+\d+`, `Q-ECON-\w+`, `Q-CHAN-\w+`, `Q-CI-\w+`, `Q-PROV-\w+`, `Q-ORG-\w+`
- `Rung-\d`, `operator-\d`, `RP-\d`, `RS-\d+`, `O1`, `O2` *(when context is the operator, not a literal letter+digit)*
- `FEED_COMPLETENESS`, `COMMERCE_CONFIDENCE`, `REP_IDENTITY_TIER`, `DATA_MASS_TIER`, `REPORT_INTELLIGENCE_TIER`
- `TIER-1`, `TIER-2`, `TIER-3` *(as raw labels; allowed only as plain-English phrasings like "named reps")*
- `Mode 1 Standard`, `Mode 2 Activation`, `Mode 3 Reactivation` *(internal mode names)*
- `preflight`, `feed posture`, `Gate-STOP`, `cohort-validation`

**C — System / pipeline / process language** *(belongs only in build docs, never in a client face):*

- `the operator`, `the run`, `this run`, `the pipeline`, `the renderer`, `the gate`
- `feed posture`, `single-feed posture`, `feed-posture` *(2026-06-30 cci canary lesson — use "one feed of your business" instead)*
- `delivered HTML`, `report stage badge`, `TODO`, `FIXME`, `XXX`
- `house_suspect`, `house-rep`, `house/sample/accom`, `shortname`, `org_id`, `organization_id`
- `portal_invoices`, `portal_orders`, `sales_data`, `users`, any other DB table name
- **DB column names used as customer-facing identifiers** *(2026-06-30 hfg cohort lesson)*: `rep_number`, `rep_name`, `rep_label`, `bill_to_number`, `ship_to_number`, `item_number`, `customer_num`, `customer_bill_to_number`, `org_user_id`, `organization_id`, `net_amount`, `order_origin`, `submit_date`, `is_submitted`, any other DB column name
- **Column-arrow compounds**: `rep_number → rep_name`, `rep_number→rep_name`, `customer_num → customer_code`, or any other `<col> → <col>` phrase. **Use plain English instead**: "rep-code-to-rep-name map," "the customer-code lookup," etc.
- `config/`, `operators/`, `authority/`, `foundation/`, `knowledge/`, `profiles/`, `outputs/`, any `_path/`

> **The Tier-fallback identifier leak** *(2026-06-30 hfg cohort lesson — load-bearing).* When `REP_IDENTITY_TIER`
> falls below 2 (rep names cannot render), the operator's natural fallback is to substitute the system column name
> (`rep_number`) as the identifier the field team uses to find the row. This leaks system vocabulary into
> customer-facing copy in a way the §A1 / §N.2 / §N.4 checks were not authored to catch. The §P.1.C ban now
> covers the entire family of DB column names; the substitute is **"rep code"** (plain English, same operational
> meaning, zero system-vocab leak). hfg PASS3 surfaced 7 such leaks across §1 / §2 / §3 / §5 / §6 / §11 — every
> one of them at a Tier-1 fallback site. The same pattern can fire on `customer_num` (when a customer code is
> rendered in place of a customer name) and `item_number` (when a SKU code is rendered in place of a product
> name). Plain-English substitutes for all three: **rep code**, **customer code**, **item code** (or **SKU**).

**D — Internal product names / version numbers** *(zero tolerance):*

- `Insightful Product`, `Insightful`
- `SuperCat` *(other than in the literal "About SuperCat" footer block if present)*
- `eCat` *(allowed only inside the literal Channels section where it is the channel label)*
- Any version number: `2\.0`, `3\.0`, `4\.0`, `v4`, `v4\.1`, `v4\.2`

### P.2 — Per-token allow-list (overrides P.1 in named contexts)

The operator carries a per-run allow-list keyed by token + context. A token survives the sweep only if it
appears in one of these contexts:

| Token | Allowed context |
|---|---|
| `cohort` | the literal phrase "buyer cohort" or "design cohort" *(domain-true; rare)* |
| `AOV` | a furniture-order context (allowed per §A1) |
| `YoY` | adjacent to a number (e.g. "+29% YoY"); banned standalone |
| `eCat` | inside the Channels section (gold §10) and the methodology disclosure block only |
| `Mixpanel` | inside the methodology disclosure block only (never in a finding) |
| `SuperCat` | the literal "About SuperCat" footer block if present |
| any system token | the Appendix Traceability footer (internal provenance only) |
| any DB column name (`rep_number`, `customer_num`, `item_number`, etc.) | the Appendix Traceability footer ONLY (where it appears as a real DB column referent, not as a customer-facing identifier) |
| `rep code` / `customer code` / `item code` / `SKU` | the plain-English substitutes — allowed everywhere, including customer-facing §1–§11 copy |

A token that hits P.1 and is **not** in an allowed context per P.2 fails the run.

### P.3 — Action on hit

**HALT the render** with the message *"P-VOCAB: token `{token}` matches the §P forbidden-vocabulary list in
`{file}` at `{line}`, not in any §P.2 allowed context. The pipeline does not patch the output — fix the
upstream prose source and re-render."* The operator does NOT silently substitute or strip; the human-readable
fix is logged and the renderer re-runs.

**Why HALT, not DELETE:** unlike §N.2/§N.4/§N.6 (cell-scoped fixes), a §P hit usually means the prose around
it is also off-voice; a silent token strip can leave dangling sentences that still read as SaaS. The HALT
forces a real prose pass.

---

## Q. Sensitivity-hedge gate *(NEW 2026-06-30 — gold-stamp absorption, the load-bearing voice move)*

> **What this enforces.** The Sarreid gold standard's defining voice move: **every Tier-A / Tier-S claim
> (the big-dollar callouts the CEO will plan around) carries one inline "what would change this read"
> sentence, adjacent to the claim.** Not in an appendix. Not in the methodology block. Adjacent.
>
> This is what makes the report read as a consultant briefing (anticipating the pushback) instead of a
> dashboard explanation (here is a number, good luck). Without it, the report's other rules can all pass
> and the output still reads thin.

### Q.1 — What constitutes a Tier-A / Tier-S claim

| Render site | Counts as Tier-A/S |
|---|---|
| §1 Signal Summary | every numbered finding |
| §1 "Three things you wouldn't have known" CEO-callouts | every callout |
| §2 "Do this week" call-list rows | every row |
| §2 §M Decline Investigation blocks | every block |
| §3 "Do this month" play upside chips | every play |
| §3 coaching cards | every card |
| §5 Growth engine subsection headlines | every subsection |
| §6 The team — coaching cards | every card |
| Priority Actions block | every row |

### Q.2 — The marker-phrase requirement

Within ±400 characters of the Tier-A/S claim, the prose **must** contain one of the following sensitivity-marker
phrasings (case-insensitive; voice variation allowed within the pattern):

- `What would change this read` / `What would flip this`
- `Worth pressure-testing`
- `Two non-decline explanations to rule out` / `Two reads to rule out`
- `If [condition], the addressable [denominator]` / `If [X], the [Y] sizes against`
- `Loosening / tightening [the rule] would`
- `Trim the list on the call if`
- `A single [risk] would pull [headline] back`
- `Pressure-test on the call`

The Sarreid HTML carries the six gold examples (Play 01 Lilac→Jupe, Play 02 second-order, Play 03 leak,
Growth Layer 2 Jupe, Card 2 Klein/France and Son, Card 4 Barnard cluster). Copy that pattern — these are
the worked examples for the gate.

### Q.3 — Action on miss

**HALT the render** with the message *"Q-HEDGE: Tier-A/S claim `{snippet}` at `{file}:{line}` has no
sensitivity-marker phrase within ±400 chars. Add an inline 'what would change this read' sentence adjacent
to the claim before re-render."*

The operator does NOT auto-write the hedge — the hedge is the load-bearing voice move and must be authored,
not templated. The HALT forces the agent (or human) to write one.

### Q.4 — Collective hedging permitted on table-format claim lists *(NEW 2026-06-30 — cci cohort lesson)*

When Tier-A/S claims are rendered as **rows in a single table** (the §2 7-row call list, the §6 5-card
coaching layer, the §3 plays table, the §7 watchlist tail), per-row hedging dilutes the table's
information density. A **collective hedge** is permitted instead, **provided all three of**:

- **(a) The collective hedge addresses the underlying systemic uncertainty** that applies across all
  rows of the table — e.g. *"Trim the list on the call if any of the seven has a known seasonal cycle
  (designer-services accounts in particular run on project cadences that can leave a 6-month window
  looking like a decline when nothing has actually changed)."* The hedge must name the uncertainty
  class, not just "verify before acting."
- **(b) The collective hedge is positioned within ±400 chars of the last row of the table** — typically
  in the explanatory paragraph immediately below. A hedge placed three sections later does not satisfy
  §Q.
- **(c) The table itself carries the "two-conversations" or equivalent split** when the rows represent
  two distinct call-shape patterns — see Sarreid §2 "Don't conflate the two conversations" callout and
  the cci / hfg / kal worked examples. Without the split, the collective hedge cannot do the work of
  a per-row hedge.

**Worked examples (gold patterns)**: cci §2 7-row call list (one collective "trim the list" hedge below
the table); hfg §2 7-row call list (one "two different conversations" callout + one collective trim
hedge); kal §2 7-row call list (one "growing account skipped a beat" split + one collective hedge).

§Q.3 enforcement updates to: HALT if per-row Tier-A/S claims **and** no satisfying collective hedge
within ±400 chars of the table's last row. The check passes when either form (per-row OR collective)
is present and satisfies the marker-phrase requirement.

---

## R. Concentration-check gate *(NEW 2026-06-30 — closes qa-lessons Finding 1; Sarreid lesson)*

> **What this prevents.** The Sarreid Growth Engine §5 Layer 1 shipped saying the same-dealer +29% growth was
> "broad-based" and "isn't concentrated in your largest account." A live concentration query showed the
> top 10 of 655 carried 94.9% of the lift and one marketplace account alone was 65% of it. The "broad-based"
> framing was directionally misleading — a CEO planning around "long-tail-is-healthy" would misallocate.
>
> §R makes that misframing impossible to ship again on any client.

### R.1 — Trigger

Fires if any sentence in customer-facing copy contains any of these tokens describing a $-base or $-lift:

- `broad-based`, `broadly distributed`, `broadly spread`
- `diversified`, `spread across`, `spread over`
- `concentrated` *(when followed by a negation: "isn't concentrated", "not concentrated", "rather than concentrated")*
- `well-distributed`, `evenly distributed`
- `the long tail is healthy` / `the broad middle` / `the bulk of dealers`

### R.2 — The concentration check the operator must have run

For any $-lift or $-base the prose describes, the operator's run log **must** contain a concentration probe
output with three figures:

- `top_1_share` = single largest contributor's share of the $-lift (or $-base)
- `top_10_share` = top-10 contributors' share of the $-lift
- `HHI` = sum of squared shares × 10,000 (Herfindahl-Hirschman Index on the lift)

If no such probe was run, the run is non-compliant — fix the operator invocation, do not ship.

### R.3 — The forbidden-framing thresholds

If **any one** of the following is true, the "broad-based" framing is **forbidden** and §R replaces it with
the canonical "concentrated in top N" template:

- `top_1_share ≥ 25%`
- `top_10_share ≥ 40%`
- `HHI ≥ 1500`

### R.4 — Action on hit

**HALT the render** with the message *"R-CONC: 'broad-based' framing at `{file}:{line}` claims diffuse
distribution, but the concentration probe returned top_1=`{x}%` / top_10=`{y}%` / HHI=`{z}`. The framing
is forbidden by §R. Replace with the canonical template below before re-render."*

### R.5 — Canonical replacement template (verbatim — do not paraphrase)

```
{N_total} {dealers|customers|accounts} {bought in both years|qualified for the base} and {spent +X%|grew $Y}
in aggregate — but the engine is concentrated, not spread. The top {N_top} of the {N_total} carried ${A} of
the ${B} lift; the next {N_mid} added ${C}; the remaining {N_tail}, in aggregate, came in ${D} {below|above}
prior year. The growth is real and the {base} is intact, but the {+X%|$Y} is being pulled by the top of the
{book|base}, not the broad middle. The play that follows is "invest where the {tail|lagging segment} is
fading," not "amplify what's already working everywhere."
```

**Why HALT not DELETE:** the framing change forces a different operating-play paragraph downstream (Card 1 /
Play 01 / Priority Action wording may all need to follow the new headline). Auto-delete would leave dangling
references; HALT forces a coherent re-render.

### R.6 — Polarity symmetry (loss-direction also covered) *(NEW 2026-06-30 — cci cohort lesson)*

§R.1–§R.5 above are written around a $-lift / growth direction (the Sarreid lesson was a "broad-based
+29%" misframing). **The same concentration math and the same thresholds apply to a $-loss / decline
direction.** A misframed "broad-based decline" / "broadly spread churn" / "the broad middle is fading"
sentence can equally lead a CEO to misallocate when the loss is actually concentrated in the top-1 or
top-10 lapsed accounts.

**Trigger extension.** §R.1 also fires on these tokens describing a $-loss or $-decline:

- `broad-based decline`, `broadly distributed decline`, `broadly spread churn`
- `diversified contraction`, `spread across the base`, `evenly distributed losses`
- `concentrated` *(when followed by a negation in a decline context: "the decline isn't concentrated",
  "the churn isn't in any one account")*
- `the broad middle is fading` / `the broad middle is softening` / `it's everywhere`

**Concentration check** runs identically — top-1 / top-10 / HHI on the **lapsed or contracting cohort
$-base**, with the same forbidding thresholds (top-1 ≥ 25%, top-10 ≥ 40%, HHI ≥ 1500).

**Canonical replacement template (loss-direction variant)**:

```
{N_total} {dealers|customers|accounts} {bought last year but not this year | spent less this year},
totaling −${B} in aggregate — but the contraction is concentrated, not spread. The top {N_top} of the
{N_total} carried −${A} of the −${B} loss; the next {N_mid} added −${C}; the remaining {N_tail}, in
aggregate, came in roughly flat. The decline is real and the base is intact, but the loss is being
pulled by the top of the {book|base}, not the broad middle. The play that follows is "defend or replace
the top {N_top} specifically," not "stabilize across the dealer base."
```

**Symmetry rationale.** A CEO planning around "everyone is fading a little" deploys differently than a
CEO planning around "five accounts walked out the door." The honest framing changes the play. Same
rule fires on both polarities for the same reason.

---

## S. Addressable-base rule for per-N-point upside math *(NEW 2026-06-30 — gold-stamp absorption)*

> **What this prevents.** A "+$X per N-pt move on rate Y" claim run against the full cohort denominator can
> overstate addressable upside by 2× when half the cohort is one-time-by-intent. The Sarreid Play 02 gold
> pattern shows the fix: state the addressable share inline, or express the figure as a range across
> full-cohort and addressable-cohort.

### S.1 — Trigger

Fires on any sentence containing per-N-point upside arithmetic:

- `+$X per N {pt|pts|point|points|pp}` / `+$X for every N pts`
- `Each N-pt move … +$X` / `$X per N-point lift`
- `Every N-pt improvement on {rate} … $X`
- `+N% → +$X` *(when N refers to a percentage-point move, not a $-delta)*

### S.2 — The requirement

The sentence must carry **one** of the following adjacent (within ±200 chars):

- **(a) An addressable-base footnote** naming the denominator the lever sizes against — *"the lever sizes
  against the ~{N_addr} addressable {dealers|customers}, not the full {N_total}"* — with the addressable
  figure traced to a query in the Appendix.
- **(b) An explicit range** expressing the figure across full and addressable cohorts — *"$X (full cohort)
  to $Y (addressable subset)"*.

### S.3 — Action on miss

**DELETE the claim** under the §N.5 `UNTRACEABLE-ARITHMETIC` rule (editorial arithmetic without addressable
trace = no provenance). The narrative reads cleaner without the figure; the cohort-size finding (`N dealers,
Y% reorder rate`) already carries the operational signal. Do not auto-write the addressable share — if the
operator can produce it, it should have produced it in the first place.

---

## Render-time enforcement contract (updated 2026-06-30)

Step 10 of [`../operators/report_operator.md`](../operators/report_operator.md) runs the full gate set in
this order against both the rendered MD and the rendered HTML:

1. §N.1 `HOUSE-LEAK` *(HALT)*
2. §N.2 `FM9-CHANNEL-LEAD` *(DELETE cell)*
3. §N.3 `CROSS-ORG-LEAK` *(DELETE sentence)*
4. §N.4 `CUTE-METAPHOR` *(DELETE + replace with literal)*
5. §N.5 `UNTRACEABLE-ARITHMETIC` *(DELETE)*
6. §N.6 `VISUAL-CUE` *(DELETE glyph)*
7. §N.7 `CHANNEL-NONE-SUPPRESSION` *(REPLACE with §O template)*
8. **§P `FORBIDDEN-VOCAB` *(HALT)*** — gold-bar superset of §A1 / §N.2 / §N.4 / §N.6
9. **§Q `SENSITIVITY-HEDGE` *(HALT)*** — Tier-A/S claims must carry an adjacent "what would change this read"
10. **§R `CONCENTRATION-CHECK` *(HALT)*** — "broad-based" framing forbidden when top-1 ≥25% / top-10 ≥40% / HHI ≥1500
11. **§S `ADDRESSABLE-BASE` *(DELETE via §N.5)*** — per-N-point math without addressable trace

Any HALT requires a real upstream fix and a re-render. The operator does not patch around a HALT, and
shipped output that has not passed every gate above is **non-compliant**.
