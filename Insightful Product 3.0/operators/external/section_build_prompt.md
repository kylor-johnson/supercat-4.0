# Section Build Prompt — Insightful Product 3.0

You are building **ONE** section fragment for an Insightful 3.0 intelligence
report. You have a fresh context window devoted entirely to this section.

## Your Inputs

**Context bundle:** `{BUNDLE_PATH}`
This single file contains EVERYTHING you need:
- The section guide (subsection specs, HTML templates, rendering rules)
- **TARGET STRUCTURE — Gold Standard**: the canonical markup for THIS section.
  This is the source of truth for HTML structure. Where it disagrees with the
  prose guide's templates, the TARGET STRUCTURE wins.
- Shared rules excerpt (editorial voice, banned terms, what-this-means quality)
- Section shared contract (confidence header process, gate check process)
- Gate flags (data availability)
- Section confidence tier
- All cache data files for this section

**Do NOT read any other files.** The bundle is self-contained.

## Your Outputs

Save these files to `{FRAGMENTS_DIR}`:

1. `section_{NN}_plan.md` — Pre-build manifest
2. `section_{NN}.html` — The HTML fragment

Save this file to `{CACHE_DIR}`:

3. `section_{NN}_highlights.md` — 2–4 highlight candidates

## Process

### 1. Read the context bundle

Read `{BUNDLE_PATH}` in full. Identify:
- Which section this is (number, ID, title)
- The PRE-BUILD GATE CHECK table in the section guide
- The confidence tier from section_confidence
- Which cache files have data vs "(not present)"

### 2. Write the pre-build manifest

Write `{FRAGMENTS_DIR}/section_{NN}_plan.md`:

```
# Section {NN} Build Plan — {SECTION_TITLE}

| Subsection | MANDATORY/CONDITIONAL | Gate Status | Will Render |
|---|---|---|---|
| [exact name from guide] | MANDATORY | MET (reason) | YES |
| [exact name from guide] | CONDITIONAL | NOT MET (reason) | NO |
...
```

Use the EXACT subsection names from the section guide. Do not invent names.
Every MANDATORY subsection where the gate is MET must say "Will Render: YES".

### 3. Build the HTML fragment

**Anchor on the TARGET STRUCTURE block in the bundle.** Open it side-by-side with
the section guide. The TARGET STRUCTURE governs **form**: tag nesting, class
names, subsection order, which subsections carry a `what-this-means` block, and
the `<thead>`/`<tbody>`/`row-highlight` patterns. Where the guide's inline
template and the TARGET STRUCTURE disagree on form, the TARGET STRUCTURE wins.

The guide governs **content**: which subsections render (per the gate checks),
and which columns/metrics you actually have data for. The TARGET STRUCTURE's
specific column sets and numbers are illustrative — do NOT invent a column the
guide's data source doesn't provide just because the gold shows it. Match the
gold's structural shape using the columns and data the guide specifies for this
client.

Follow the section guide's Content Blocks specification exactly:

- Render subsections in the **narrative arc order** specified by the guide
  (Strength → Intelligence → Opportunity → Risk).
- Use the EXACT HTML structure shown in the guide templates.
- Use the EXACT subsection-title text from the guide.
- Build the confidence header per the shared contract process (§2–§5 only).
- Every rendered subsection must end with a `<div class="what-this-means">`
  block UNLESS the guide explicitly exempts that subsection (e.g., coaching
  cards, and pure ranking tables such as the Rep Leaderboard). When the guide
  says a subsection has no what-this-means, do NOT add one.
- Every dollar figure must have a time qualifier.
- Every finding must name a specific entity (customer, item, rep).

**CRITICAL**: After building, scan your plan. If ANY subsection marked
"Will Render: YES" is missing from the HTML you just wrote, add it NOW.
Do not save a fragment with missing mandatory subsections.

Save to `{FRAGMENTS_DIR}/section_{NN}.html`.

### 4. Write highlights

Save `{CACHE_DIR}/section_{NN}_highlights.md`:

- 2–4 candidate highlights from this section's strongest signals
- Each: **bold headline** + one sentence context + dollar figure +
  `surprise_score` + `signal_id` + section deep-link
- At least 1 highlight MUST be positive (momentum, opportunity, intelligence)
- 0–1 priority action candidates with urgency level

### 5. Exit

Report back: section built successfully, subsection count rendered,
fragment file size.

## Rules

- **Do NOT improvise subsection names or structure.** Use exactly what the
  section guide specifies. If the guide says "Top 10 Mini-Briefs", your
  subsection-title must be "Top 10 Mini-Briefs" — not "Top Accounts" or
  "Account Signal Summary".
- **Do NOT skip mandatory subsections.** If the plan says YES, it must exist
  in the HTML.
- **Do NOT read files outside the context bundle.** Everything you need is there.
- **Do NOT add inline verification steps.** Build the fragment, check it against
  your plan once, save, and exit. An audit agent handles full verification later.
- **Banned terms** (from shared rules in the bundle): ERP, Mixpanel, Clicky,
  health score, segment labels, internal IDs, platform (standalone),
  portal orders, platform-attributed revenue. Use the approved replacements
  listed in the bundle's shared rules excerpt.

## HTML Quality Rules (ENFORCE — these override guide template shorthand)

Guide templates sometimes omit structural HTML tags for brevity. You MUST add
them. These rules apply to every section, every table, every metric block.

### Tables MUST use `<thead>` and `<tbody>`

Even if the guide template shows `<tr><th>` directly inside `<table>`, you MUST
wrap header rows in `<thead>` and data rows in `<tbody>`:

```html
<table>
  <thead>
    <tr><th>Column 1</th><th>Column 2</th></tr>
  </thead>
  <tbody>
    <tr><td>data</td><td>data</td></tr>
  </tbody>
</table>
```

Without `<thead>`, the CSS rule `thead { background: var(--panel) }` never fires
and table headers are visually indistinguishable from data rows.

### Top rows in leaderboards use `row-highlight` and bold names

The top 5 rows (or top N as specified by the guide) use `class="row-highlight"`
and bold the entity name:

```html
<tr class="row-highlight"><td>1</td><td><strong>Entity Name</strong></td><td>$value</td></tr>
```

### Never wrap what-this-means content in `<p>` tags

```html
<!-- WRONG -->
<div class="what-this-means">
  <p><strong>Action:</strong> Some text here.</p>
</div>

<!-- RIGHT -->
<div class="what-this-means">
  <strong>Action:</strong> Some text here.
</div>
```

### Metric card containers use `class="metrics"` not `class="metric-row"`

If a guide template shows `<div class="metric-row">`, render it as
`<div class="metrics">` instead. The CSS grid layout only applies to `.metrics`.

### Signal Summary findings use `<ol>` not `<ul>`

```html
<ol class="highlights">
  <li><strong>Headline</strong> — context. <a href="#section">→ §N</a></li>
</ol>
```

---

## Data Presentation Rules (ENFORCE — raw data must be polished)

Cache data comes from database queries and may contain raw formatting. You MUST
normalize it for a client-facing executive report.

### Title-case ALL entity names

Customer names, account names, and product descriptions from cache data are often
ALL-CAPS (e.g., "LIGHTING DESIGN LLC", "WILLIAMS-SONOMA INC"). Convert to title
case before rendering: "Lighting Design LLC", "Williams-Sonoma Inc".

Exceptions: Keep known acronyms uppercase (LLC, INC, CO, LTD, USA, LED).
Keep brand-specific casing when recognizable (e.g., "eBay", "iPhone").

### Suppress empty columns

If a column (e.g., State, Region) is "—" or empty for EVERY row in the table,
remove the column entirely rather than displaying a column of dashes. An empty
column signals broken data and wastes horizontal space.

### Handle thin data gracefully

If a subsection would render with only 1 data row (e.g., a geographic breakdown
with "All regions" as the only row), either:
- Skip the subsection and note the gap in the data confidence header
- Or render it as a single metric card or inline stat, not a full table

A 1-row table surrounded by a subsection title, callout, and what-this-means
block creates a bad ratio of chrome to content.

---

## Text Brevity (ENFORCE — these are hard limits, not guidelines)

The report is read by VPs who scan. Every text block must be tight.

| Element | Hard Limit |
|---------|-----------|
| Confidence header | Max 2 sentences. Strip methodology/exclusion details to a footnote or omit entirely. |
| `what-this-means` block | ALWAYS start with `<strong>Action:</strong>`. Max 3 sentences total. |
| Callout titles (`.callout-title`) | Max 12 words. Data belongs in the body, not the title. |
| Coaching card body | Max 2 sentences before the coaching action line. |
| Subsection lead-in paragraphs | Max 2 sentences before the table/chart. |

**Anti-patterns to avoid:**
- Titles that are full sentences with embedded dollar figures and percentages
- Multi-paragraph what-this-means blocks that repeat data already in the table
- Confidence headers that explain the methodology instead of stating the coverage
- Coaching card narratives with parenthetical data dumps mid-sentence
