# Shared Rules — Insightful Product 3.0

Rules governing all report generation. Every section builder, the signal summary
constructor, and the final assembler MUST comply. No exceptions, no soft guidance.

> **Embedding note**: This file is included in every context bundle via
> `build_context.py`. Section guides do not need to restate its rules —
> they can reference sections by ID (e.g., "per shared_rules A1").

---

## A0. Editorial Voice — The North Star

**This is an intelligence report, not a risk report.**

The reader should finish this report thinking: *"I didn't know that about my
business — I need to pay for this."* NOT: *"Everything is broken, I should
churn."*

### Narrative Arc (MANDATORY)

Every section, and the report as a whole, follows this arc:

1. **MOMENTUM** — What's working. Celebrate wins, name the reps/accounts/products
   driving growth. This is NOT filler — it's the credibility foundation. If the
   reader doesn't trust that you understand their business, they won't act on risks.
2. **INTELLIGENCE** — What's interesting. Data-dense tables, penetration views,
   category breakdowns, behavioral patterns — the stuff they can't get from their
   own ERP. This is the "holy shit, I didn't know that" layer.
3. **OPPORTUNITY** — What could be better. Cross-sell whitespace, activation
   targets, coaching upside, conversion improvements. Frame as growth, not repair.
4. **RISK** — What to watch. Decay signals, displacement, contraction. These
   come LAST and are contextualized within the positive narrative. A $50K decay
  signal is alarming in isolation but manageable when prefaced by "$8.6M in eCat
  sales driven by 37 active reps."

### Tone Rules

- **Lead with strength.** The first subsection in every section should be the
  most impressive finding — the thing that makes the client proud of their business.
- **Risk findings are always contextualized.** Never "you're losing $X" in
  isolation. Always "you drove $Y through the platform; $X of that is at risk
  from [specific pattern]."
- **Frame negatives as opportunities.** "6 accounts show eCat share declining
  while total business grows — re-engaging them through the platform could
  recapture an estimated $Z" beats "COMPETITIVE DISPLACEMENT DETECTED — $X
  shifting away."
- **Ban doom headlines.** The words "ALERT", "DETECTED", "WARNING" in callout
  titles are reserved for genuine P0 operational issues (stock-outs affecting
  top customers, data staleness). Behavioral patterns, pricing shifts, and
  channel migration use `.callout.insight` not `.callout.alert`.
- **Celebrate specific wins by name.** "[Rep] converts at 26.8% — the highest
  on your team." "[Account] grew from $824 to $78.9K in 4 quarters on the
  platform." These are the findings that make clients say "I need this."

### Report-Level Balance Test (run before finalizing)

Count the findings across the Signal Summary:
- **Minimum 3 of 7 findings must be positive** (momentum, opportunity, or
  intelligence). If fewer than 3 are positive, demote the weakest risk finding
  and promote the next-best positive finding.
- **The FIRST finding must be positive.** The reader's first impression sets the
  tone for the entire report. Lead with the win.
- **Priority Actions balance:** At least 1 of 4 priority actions must be a GROWTH
  action (not a "fix this" or "re-engage that"). E.g., "Expand [product line]
  into [N] accounts that buy similar categories — estimated $X addressable."

---

## A1. Client-Facing Language — Write for Sales Leaders, Not SaaS PMs

The audience is a VP of Sales or owner at a lighting, furniture, or home decor
manufacturer. They think in reps, dealers, showrooms, orders, and products —
not platform metrics. Every term in the left column is **banned from client-facing
HTML**. Use the right column instead.

| Banned (SaaS / tech) | Use instead |
|---|---|
| "platform capture rate" / "capture rate" | "digital ordering share" or "share of orders placed through eCat" |
| "Capture Rate Economics" | "Digital Ordering Opportunity" |
| "platform GMV" | "eCat sales" or "orders placed through eCat" |
| "platform-attributed revenue" | "orders placed through eCat" or "eCat volume" |
| "collaborative filtering" | Describe the behavior: "customers who buy X also buy Y" |
| "cross-sell engine" | "products your customers buy together" or "companion products" |
| "Next Best Product" (as a title) | "Products Frequently Bought Together" or "Companion Product Opportunities" |
| "activation" (for accounts) | "onboarding" or "getting them ordering through the app" |
| "signal density" | Never in client-facing text — internal only |
| "behavioral data reveals" | "your team's usage patterns show" |
| "platform engagement" | "app usage" or "digital catalog activity" |
| "[assumes behavioral change]" | "[estimated]" — or drop if "estimated" already appears in the sentence |
| `[eCat ONLY]` / `[ALL-CHANNEL]` inline with dollar figures | Move these labels to **column headers** or **metric card labels** instead. In prose, say "eCat orders" or "total business across all channels" — never bracket-tags mid-sentence. |
| "platform" (standalone, as in "the platform") | "eCat" or "the app" or "your digital catalog" |
| "addressable" (as in "addressable revenue") | "potential" or "available" |

**Terms that are fine** — standard business vocabulary a sales leader uses daily:
conversion rate, year-over-year, trailing 12 months, reorder velocity, AOV,
LTM, quarter-over-quarter, fill rate, pipeline, territory, funnel.

**Inline data tags**: The `[eCat ONLY]` and `[ALL-CHANNEL]` bracket tags must
NOT appear inline with dollar figures in prose or table cells. Instead:
- In **metric cards**: put the scope in `.metric-note` (e.g., "eCat orders only")
- In **table headers**: append scope (e.g., "GMV (eCat)" or "GMV (all channels)")
- In **prose**: write it out ("$8.6M in eCat orders" or "$88M across all channels")
- These bracket tags ARE used in the **appendix labeling convention** and in
  **guide-internal documentation** to mark which data source applies — that is
  fine. The prohibition applies to client-facing rendered HTML only.

---

## A. Specificity Standard (The #1 Rule)

Every claim in the report must pass the **specificity test**. A claim qualifies
only if it satisfies ALL of the following:

- **Names a specific customer, item, or rep**
- **Includes a dollar figure**
- **States a specific action someone can take**
- **Includes a time qualifier on every metric**

If a sentence fails even one criterion, rewrite or delete it.

### Examples

**BAD:** "Consider re-engaging dormant accounts to recover lost revenue."

**GOOD:** "Call Ticking Stripe — $227K in historical eCat spend, last ordered
Oct 16 2025 (244 days). Rep: Sheryl Lowe."

---

**BAD:** "Your top items are experiencing stock-outs that may impact revenue."

**GOOD:** "HAY-1417-AG (Hayes 50'' Aged Brass Linear Chandelier) — $20.7K LTM,
0 available, next receipt July 14. Top customer impacted: Lamps Plus (463), who
ordered 17 units LTM."

---

## B. Signal Hierarchy and Rendering Priority

| Level | Rendering rule |
|-------|---------------|
| **P0** | MUST surface in Signal Summary if detected. Non-negotiable. |
| **P1** | Surface if in top 10 by `SIGNAL_RANK`. Otherwise section detail only. |
| **P2** | Section detail or collapsed sections only. Never Signal Summary. |

Additional constraints:

- A section renders if ANY of these are true: (a) ≥ 1 fired P0/P1 signal, (b) its section guide's alternate include gate passes, or (c) it contains a query-driven subsection with data that passes the guide's specificity test. A section is suppressed only when ALL are false.
- When a section has **> 5 entities** to show, top 5 visible, rest collapsed.

---

## C. Fragment Contract (HTML output rules)

Each section builder produces a **standalone HTML fragment**. Rules:

1. Fragment uses only classes defined in `html_report_template.html`.
2. Section `id` attribute matches one of: `signals`, `accounts`, `product`,
   `commerce`, `team`, `platform`.
3. Every section ends with a `what-this-means` block (max 3 sentences,
   action-focused — see Section H).
4. **Tables:** top 5 rows visible, remainder in `<details>` collapse.
5. **Metric cards:** max 4 per grid row.
6. **Coaching cards:** only for reps with > $50K estimated upside.

---

## D. Dollar Math Rules

- **`[HYPOTHETICAL]`** on all projections (any dollar figure not directly
  measured from source data).
- **`[ESTIMATED]`** on extrapolations (figures derived from incomplete data
  via scaling or inference).
- Inline tag + sentence = complete disclosure. No separate Appendix entry needed.
- eCat figures are **eCat-channel only** unless explicitly stated otherwise.
- `portal_orders` figures = **total ERP business across all channels**.
- Never claim broader than data supports.

---

## E. Semantic Rules (Locked)

1. `portal_orders` = "total business across all channels" / "orders synced from
   your ERP". **Never** "portal ordering" or "buyer self-service."
2. If `has_clicky = false`, the Portal/Demand section **does not exist**. Do not
   reference it in any other section.
3. Health score is **INTERNAL only** — never appears in external report output.
4. Segment labels (`Platform-Embedded`, `Commerce-Active`, `Catalog-Focused`)
   **NEVER** appear in external output.
5. **Peer benchmarking is EXCLUDED entirely.** Do not reference peer comparisons,
   quartile positioning, peer medians, or cohort benchmarks in any section.
   The peer data is unreliable. If a signal or subsection references peer
   comparison, skip that comparison silently.
6. Benchmark metadata (`benchmark_confidence`, `peer_group_level`,
   `peer_group_n`) are **banned from all output** — neither internal nor external.

---

## F. Time Qualifier Rule

Every metric requires a time qualifier. No bare numbers. Ever.

| Bad | Good |
|-----|------|
| "373 active eCat buyers." | "373 active eCat buyers in the trailing 12 months." |
| "$4.7M in platform GMV." | "$4.7M in platform GMV (May 2025–May 2026)." |
| "Last ordered recently." | "Last ordered June 3, 2026 (13 days ago)." |

---

## G. Signal Summary Construction

Built **LAST** from all section outputs. Never drafted before sections complete.

### Numbered Findings

- **5–7 numbered findings**, sorted by narrative arc (momentum → intelligence →
  opportunity → risk), NOT raw `SIGNAL_RANK` descending.
- Each finding: **bold headline phrase** + one sentence context + dollar figure +
  section link.
- **Finding #1 MUST be positive** — the single most impressive momentum or
  intelligence finding. This sets the tone for the entire report.
- **Minimum 3 of 7 findings must be positive** (momentum, opportunity, or
  intelligence). If the raw SIGNAL_RANK top 7 has fewer than 3 positives,
  demote the weakest risk finding and promote the next-best positive.
- At least **one action the client can take immediately** (this week).
- Risk findings appear in slots 5–7, never slots 1–3.

### Diversity Constraint

**Maximum 4 of the 7 Signal Summary slots may come from a single section.** If one section (e.g. Account Intelligence) holds 6 of the top 7 by raw SIGNAL_RANK, slots 5–7 go to the next-highest-ranked signals from OTHER sections. This guarantees at minimum 3 non-account findings reach the Signal Summary when data exists across multiple sections.

### Priority Actions

- **2–4 priority actions**, each tagged `HIGH` / `MEDIUM` / `LOW` urgency.
- Every action includes a dollar impact estimate.

### Patterns That Warrant a Conversation

- **2–3 questions** framed to provoke executive discussion.
- Not statements — actual questions that require the client's own context to
  answer.

---

## H. What-This-Means Blocks

End every **section** (not subsection) with a `.what-this-means` div. Subsections also get their own `.what-this-means` per section guide specs.

- **Max 3 sentences.**
- **First sentence:** the strength to protect or the opportunity to capture
  (what's WORKING and how to build on it).
- **Second sentence:** the specific action that unlocks the next level of
  performance (growth-framed, not risk-framed).
- **Third sentence (optional):** what additional data would enable (data extension
  opportunity) OR the cost of inaction (but ONLY after the positive framing).
- **Never restate the statistics.** The reader already saw the table.
- **Never lead with doom.** "Your 37-rep team drove $8.6M through the platform —
  coaching the bottom quartile to median would add an estimated $1.2M" beats
  "10 reps convert below 10% — $1.2M at risk if nothing changes."

### H1. Self-Check (MANDATORY before saving any fragment)

After writing EVERY `.what-this-means` block, apply this 3-question test:

1. **Restatement test**: Could this sentence be produced by reading the first row of the table above it? If yes → REWRITE. The reader already read the table — your job is interpretation, not narration.
2. **Action test**: Does this block tell the reader what to DO or what it MEANS for their business? If it only tells them what the data SAYS → REWRITE.
3. **Specificity test**: Does this block reference at least one specific entity (rep name, account name, dollar figure, percentage) from THIS org's data? If it could apply to any org → REWRITE.

**FAILING EXAMPLES** (any of these patterns = automatic rewrite):
- "Your top performer generates $765K in iPad orders across 131 customers." ← This literally reads the table back.
- "This table shows your top 10 reps by GMV." ← Narrates the obvious.
- "Your top accounts are driving the majority of your revenue." ← Generic, applies to every org.
- "These accounts show declining order patterns." ← Restates without interpreting WHY or WHAT TO DO.

**PASSING EXAMPLES**:
- "The $485K gap between #1 and #10 suggests significant room to elevate mid-tier reps through coaching on customer targeting — if your bottom 5 matched your #5's AOV, that's an estimated $290K in annual incremental revenue."
- "Your most active rep presented to 49 accounts but only 3.6% converted to orders — high effort, lower yield. Meanwhile, your most efficient closer converts at 26.8% with far fewer presentations, suggesting targeted demos outperform high-volume prospecting for your product category."
- "The 63.8% decline at Lighting Connection ($926K→$335K) warrants immediate investigation: at that velocity, this was likely a deliberate channel shift rather than gradual drift. Three hypotheses: (1) they consolidated vendors, (2) they're sourcing this category direct-import, or (3) a competitor captured the relationship."

---

## I. "With Connected Data" Callouts

When a section's intelligence would be **dramatically** better with data the
client could provide:

- Use `.callout.opportunity` class.
- Format: *"If [specific data] were connected, this section would show [specific
  intelligence] — [estimated value]."*
- Only include when the improvement is genuinely dramatic (not minor enrichment).
- **Max 1 per section.**

---

## J. Output Rules (Prohibitions)

1. Never improvise around missing data. Gate not met = skip silently.
2. Section rendering: see Section B (relaxed gates). The strict "< 2 P0/P1" rule
   is replaced by the multi-path gate in Section B.
3. **ERP** as a term is forbidden in all client-facing HTML except one Appendix
   attribution row.
4. Internal/debug language forbidden: "package defect," "pending engineering,"
   "query returned zero rows," "runtime workaround," "validation note,"
   "Gate 2 failed," "per documented requirement."
5. HTML comments stripped from delivered output.
6. Generic recommendations forbidden. Every action must name a specific entity.
7. No insight that a client could get from their own ERP dashboard. If their ERP
   shows it, we don't need to show it. **Our value = cross-customer patterns,
   behavioral data, inventory × demand crossovers, collaborative filtering —
   things ONLY our data position enables.**

---

## K. Highlight File Contract

After building each section fragment, output `cache/section_NN_highlights.md`:

- **2–4 candidate highlights** per section.
- Each highlight: one-line headline + dollar figure + `surprise_score` +
  `signal_id`.
- Signal Summary builder reads **ALL** highlight files and selects top 5–7 by
  `SIGNAL_RANK`, subject to the diversity constraint (max 4 from any one section).
- `[HYPOTHETICAL]` tags appear in highlight files only — never in final HTML
  fragment.

---

## L. Collapse Behavior

Progressive disclosure for information density:

| Context | Rule |
|---------|------|
| **Section-level** | Sections with only P2 signals render as collapsed `<details class="section-collapse">`. |
| **Sub-table** | Tables with > 5 rows show top 5, rest in `<details>`. |
| **Account mini-briefs** | Top 5 accounts fully rendered, accounts 6–10 in collapsed block. |
| **Rep leaderboard** | Top 5 reps visible, reps 6–10 in first collapsed `<details>`, remaining in second collapsed `<details>`. |
| **Low-priority actions** | Wrapped in `<details>` below the main priority actions. |

---

## M. Competitive Hypothesis Requirement

When ANY account shows a year-over-year decline exceeding 25% AND the account's LTM revenue exceeds $50K, the report MUST include 2–3 investigative hypotheses explaining the decline. This applies in:
- Account mini-briefs (subsection F: Competitive Displacement)
- Velocity Deceleration subsection (section 2, subsection 7)
- Spending Contraction subsection (section 2, subsection 12)

### Rules

1. **We cannot see competitors.** Never state "they are buying from [competitor]" as fact. Always frame as hypothesis.
2. **Provide 2–3 plausible explanations**, ordered by likelihood based on available evidence:
   - Channel consolidation ("may have consolidated vendors or shifted to direct-import sourcing")
   - Competitive displacement ("a competitor may have captured this relationship with better pricing or service")
   - Internal change ("the account may have exited a market segment, lost a key project, or changed buying committee")
   - Pricing sensitivity ("if your prices increased, the volume drop may reflect a price elasticity response")
   - Seasonal/cyclical ("if this account is project-driven, the decline may reflect normal project completion rather than relationship loss")
3. **Always close with a specific investigative action**: "The rep assigned to this account should ask directly — a 63% decline is almost never accidental, and the cause determines the response."
4. **Acknowledge the limitation explicitly** when relevant: "We can see the decline but not the cause — here are the most likely explanations based on the pattern."

### Format

```html
<div class="callout insight">
  <div class="callout-title">Decline Investigation: {{ACCOUNT_NAME}}</div>
  <p><strong>The pattern:</strong> {{PRIOR_GMV}} → {{LTM_GMV}} ({{DECLINE_PCT}}% decline, ${{DOLLAR_DECLINE}} in lost annual volume)</p>
  <p><strong>Hypotheses:</strong></p>
  <ol>
    <li>{{HYPOTHESIS_1}}</li>
    <li>{{HYPOTHESIS_2}}</li>
    <li>{{HYPOTHESIS_3_IF_APPLICABLE}}</li>
  </ol>
  <p><strong>Next step:</strong> {{SPECIFIC_INVESTIGATIVE_ACTION}}</p>
</div>
```

### Threshold

Only render competitive hypotheses when BOTH conditions are met:
- YoY decline > 25%
- Account LTM revenue > $50K (or prior-year revenue > $50K if current is lower)

Below these thresholds, the standard what-this-means framing is sufficient.
