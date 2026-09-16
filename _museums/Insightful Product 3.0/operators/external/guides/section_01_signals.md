# Section Guide: Signal Summary
> **v3.0** — signal-first architecture. Built LAST, rendered FIRST.

## Section Identity

- **id**: `signals`
- **title**: Signal Summary
- **section number**: 1 (rendered first in report)
- **build order**: LAST — after all other section fragments are complete
- **include when**: Always (every report has a Signal Summary)
- **skip when**: Never

## PRE-BUILD GATE CHECK
> Follow `section_shared_contract.md` §1 for the gate check process.

Signal Summary always renders. No conditional gates.

## Query Inputs

Read these files:

- `cache/signal_rank.md` — ranked signal manifest (produced by signal detection pass)
- `cache/section_02_highlights.md` — Account Intelligence candidates
- `cache/section_03_highlights.md` — Product Intelligence candidates
- `cache/section_04_highlights.md` — Commerce Patterns candidates
- `cache/section_05_highlights.md` — Team Intelligence candidates
- `cache/section_06_highlights.md` — Platform Context candidates

Do NOT read raw query results. The Signal Summary synthesizes from section outputs and the signal rank — it never touches cache/Q-* files directly.

---

## Fragment Structure

The Signal Summary does NOT use the standard `<details class="section-collapse">` wrapper. It renders as an open `<section>` at the top of the report:

```html
<section class="section" id="signals">
  <h2 class="section-title"><span class="section-num">§1</span> Signal Summary</h2>
  {{CONTENT}}
</section>
```

---

## Content Blocks (render in this exact order)

### 1. Numbered Findings (MANDATORY)

**ABSOLUTELY NO PROSE before this list.** The first rendered element after the section title is the highlights list.

Select 5–7 findings from `cache/signal_rank.md` and section highlight files.
**Sort by narrative arc** (momentum → intelligence → opportunity → risk), NOT
raw SIGNAL_RANK. Within each tier, sort by SIGNAL_RANK descending.

Render as:

```html
<ol class="highlights">
  <li><strong>{{HEADLINE}}</strong> — {{ONE_SENTENCE_CONTEXT}}. ${{DOLLAR_FIGURE}}. <a href="#{{SECTION_ID}}">→ §{{N}}</a></li>
  ...
</ol>
```

**Each finding MUST include:**
- Bold headline phrase naming a specific entity (customer, item, rep)
- One sentence of context explaining why this is surprising or actionable
- A dollar figure (LTM revenue, dollar impact, or estimated opportunity)
- A section link to the relevant detail section

**Composition rules (CRITICAL — these override raw SIGNAL_RANK):**
- **Finding #1 MUST be positive** — momentum, growth, or intelligence. This is
  the first thing the client reads. It sets the tone. E.g., "37 reps drove
  $8.6M through the platform with 1,112 new buyers in 12 months."
- **Minimum 3 of 7 findings must be positive** (momentum, opportunity, or
  intelligence). If the raw top 7 has fewer than 3 positives, demote the
  weakest risk finding and promote the next-best positive finding.
- **Risk findings go in slots 5–7, never 1–3.** A client should read good news
  before bad news.
- At least ONE action the client can take this week
- Never repeat the same entity in two findings
- **Positive headline style**: Celebrate specifically. "Stacey Chiavetta converts
  at 26.8% — your team's model closer." "Bay Design grew from $824 to $78.9K
  in 4 quarters on the platform."
- **Risk headline style**: Contextualize, don't alarm. "6 accounts show eCat
  share declining while total business grows — $1.2M may be shifting to other
  channels" NOT "COMPETITIVE DISPLACEMENT — $1.2M at risk."
- **eCat / commerce findings — digital enablement, NOT eCat market share.** eCat is ONE
  digital order channel alongside the client's own B2B web, EDI, and rep/back-office entry.
  Frame any commerce finding around **digitizing the rep-/phone-/email-entered order flow**
  (less manual entry, fewer errors) — with eCat AND the client's own web as valid digital paths.
  **NEVER** write "each point of eCat ordering share is worth $X," "grow/lift eCat from A% to B%,"
  "capture rate," or "adoption stage." NEVER imply orders outside eCat are manual/offline/non-digital
  as a certainty. Celebrate real eCat growth as "more orders digitized," and never frame eCat as
  obsolete — name its specific strength (rep-assisted/field/showroom/visual selling).

### 2. Priority Actions (MANDATORY)

2–4 items in a `.priorities` container. Each action is tagged HIGH / MEDIUM / LOW urgency with a dollar impact estimate.

```html
<div class="priorities">
  <div class="priority">
    <span class="priority-badge high">HIGH</span>
    <div>
      <div class="priority-title">{{ACTION_TITLE}}</div>
      <div class="priority-desc">{{SPECIFIC_ACTION_WITH_NAMED_ENTITIES}}</div>
    </div>
    <div class="priority-impact">{{DOLLAR_IMPACT}}</div>
  </div>
  ...
</div>
```

**Rules:**
- Every action names a specific customer, item, or rep
- Every action includes a dollar impact estimate (hedged with "estimated" or "potential")
- HIGH = act this week. MEDIUM = act this month. LOW = strategic, act this quarter.
- At least 1 HIGH priority action
- **At least 1 GROWTH action** (not all "fix/re-engage" — include an "expand/
  coach/activate" action). E.g., "Expand [product line] into [N] accounts that
  buy similar categories" or "Coach bottom-quartile reps to median conversion."
- Max 1 LOW — if everything is low priority, the report isn't finding strong enough signals

### 3. This Week's Outreach List (MANDATORY when 3+ actionable accounts exist)

A prioritized table of accounts that need immediate attention — the "Monday morning call list." This is the single most actionable artifact in the report: named accounts, assigned reps, specific actions, and talking points.

**Gate**: Render when at least 3 accounts have fired signals that warrant immediate outreach (decay, displacement, stock-out impact, reorder stretch, dormancy).

```html
<div class="outreach-list">
  <div class="outreach-title">This Week's Outreach List</div>
  <table>
    <tr>
      <th>#</th>
      <th>Account</th>
      <th>Rep</th>
      <th>Action</th>
      <th>Talking Point</th>
      <th>By When</th>
    </tr>
    {{ROWS — max 7, sorted by urgency × dollar impact}}
  </table>
</div>
```

**Column construction rules:**

| Column | Source | Format |
|--------|--------|--------|
| # | Priority rank (1 = most urgent) | Integer |
| Account | Customer name from fired signal | Name only, never internal codes |
| Rep | Assigned rep from Q-43 territory data; "Unassigned" if no mapping | Rep display name |
| Action | Specific verb: Call, Email, Visit, Schedule review | One action verb + context |
| Talking Point | The opening line for the conversation — references the specific signal | One sentence in quotes, conversational tone |
| By When | "This week" for HIGH, "This month" for MEDIUM | Relative timing |

**Priority ranking algorithm:**
1. Accounts with active stock-out impacting them + reorder decay = highest priority (relationship at risk NOW)
2. Accounts with >25% YoY decline and >$50K LTM = second tier (investigation needed)
3. Accounts with reorder stretch >2.5x normal cadence = third tier (early warning)
4. Dormant high-value accounts = fourth tier (re-engagement)
5. Unactivated high-value accounts (non-enterprise) = fifth tier (activation opportunity)

**Talking Point examples:**
- "Your eCat share dropped 15% while your total business grew — what changed in how you're ordering?"
- "I noticed [item] is out of stock and you've ordered it 6 times this year. I wanted to flag [alternative] and let you know restock is expected [date]."
- "It's been 147 days since your last order — is there anything we can help with? Your historical cadence is every 45 days."
- "You do $2.7M in total business with us but nothing through eCat yet — would a 15-minute demo be useful?"

**If rep assignment data (Q-43) is unavailable**: Still render the table but use "—" in the Rep column and note below: "Rep assignments would strengthen this list — territory mapping enables direct routing to the right salesperson."

### 4. Patterns That Warrant a Conversation (MANDATORY)

A `.callout.insight` block with 2–3 numbered questions designed to provoke executive discussion.

```html
<div class="callout insight">
  <div class="callout-title">Patterns That Warrant a Conversation</div>
  <ol>
    <li>{{QUESTION_1}}</li>
    <li>{{QUESTION_2}}</li>
    <li>{{QUESTION_3}}</li>
  </ol>
</div>
```

**Rules:**
- These are QUESTIONS, not statements — they require the client's own context to answer
- Each question references specific data from the report (dollar figures, entity names, patterns)
- Frame as "We see X — is this because Y, or is something else happening?"
- Never answer the questions yourself — the value is in prompting the conversation

---

## Section-Specific Rules

1. **No What-This-Means block.** The Signal Summary is itself the "what this means" for the entire report. Do not add a `.what-this-means` div.
2. **No data confidence footer.** Signal Summary synthesizes from other sections' outputs — confidence is disclosed at the section level, not here.
3. **No prose preamble.** The highlights list IS the opening. No "This report analyzes..." or "We reviewed..." introductory paragraphs.
4. **No subsection wrappers.** The three content blocks (findings, priorities, conversation) render directly inside the section — no `.subsection` divs.

---

## Highlight File Output

This section does NOT produce a `cache/section_01_highlights.md` file. It consumes highlights from all other sections.

---

## Conditional Subsection Checklist (verify before saving fragment)

- [ ] Fragment starts with `<section class="section" id="signals">`, NOT `<details>`
- [ ] First rendered element after `<h2>` is `<ol class="highlights">` — no prose before it
- [ ] 5–7 findings in the highlights list, each with: bold headline, context sentence, dollar figure, section link
- [ ] Finding #1 is POSITIVE (momentum, growth, or intelligence)
- [ ] At least 3 of 7 findings are positive (momentum, opportunity, intelligence)
- [ ] Risk findings are in slots 5–7, not 1–3
- [ ] At least 1 "act this week" finding included
- [ ] 2–4 priority actions rendered, each with urgency badge and dollar impact
- [ ] At least 1 HIGH priority action
- [ ] At least 1 GROWTH action (expand/coach/activate, not only fix/re-engage)
- [ ] This Week's Outreach List rendered (if 3+ actionable accounts exist): max 7 rows, each with account/rep/action/talking point/timing
- [ ] Outreach list talking points are conversational and specific (not generic "re-engage this account")
- [ ] 2–3 conversation questions in `.callout.insight`, all framed as actual questions
- [ ] No prose before the highlights list
- [ ] No `.what-this-means` block
- [ ] No data confidence footer
- [ ] Forbidden terms check passed (see section_shared_contract.md §6)
- [ ] Every dollar figure has a time qualifier
- [ ] Every entity reference uses a specific name (customer, item, rep) — no generic "your accounts"
