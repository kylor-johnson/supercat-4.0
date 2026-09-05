# EBR Deck Prompt — HYBRID: Best Judgment Synthesis

**Account:** Gabby / Summer Classics (4 entities: gh, scw, sccon, sc)
**Output:** `Gabby_SC_EBR_HYBRID.html`
**Slides:** 15

---

## Task

Build a presentation-ready HTML slide deck for an Executive Business Review with Gabby / Summer Classics using a hybrid structure that takes the best elements from all three EBR templates. This is the recommended deck — the one we'd actually present. First-ever structured review, executive audience, unknown attendees.

Build as a single self-contained HTML file — one section per slide, full-viewport, scroll-snap navigation. No external dependencies except Google Fonts.

## Data Source — DO NOT QUERY DATABASES

Read these workspace files for all data:

- **Gabby_SC_Intelligence_Brief.md** — Full B1-B8
- **Gabby_SC_Account_Snapshot.md** — A1-A6
- **ebr_frameworks.md** — All three templates for reference

## Hybrid Philosophy

This deck takes from each template what it does best:

- **From Template A (Discovery-Led):** The opening discovery questions and the collaborative closing. Discovery is non-negotiable for a first meeting — we need to listen before we prescribe.
- **From Template B (Intelligence-Led):** The rep intelligence and customer data sections. This is a $35M ordering account — the data story IS the value story. Lead with it after the brief orientation.
- **From Template C (Benchmark-Forward):** The cross-entity comparison framing. We can't benchmark against the portfolio yet, but 4 entities on one platform IS a benchmark universe.

**Sequence logic:** Orient → Listen briefly → Deliver the value story (data) → Go deep on cross-entity intelligence → Open full discovery anchored to data → Recommend → Commit.

The meeting should feel like: "We respect your time, we know your account deeply, we have insights you can't get anywhere else, and we want to know what matters to you."

## Design Direction

Same palette and fonts as all other decks. This one should feel like the polished final version — slightly tighter layouts, more confident use of whitespace, every slide earns its place.

## Slide Structure — 15 Slides

### Slide 1: Title

- Dark background (1E3A2F)
- "Executive Business Review" large white Georgia
- "Gabby / Summer Classics — The Gabriella White Family of Brands" subtitle
- "March 2026 · SuperCat Solutions"

### Slide 2: Partnership & Entity Overview (from A1 + C1)

- Title: "13 Years. Four Divisions. One Platform."
- Top: Partner since 2013 · $8,975/mo · 250 active users · 5 products
- 4 entity cards (compact): name | model | users | orders (2mo) | revenue (2mo)
- Bottom framing: "This is the first time we've brought all four divisions together in one conversation. Our goal is to share what we see across the full picture, and hear what matters to you."
- Presenter note: "2 minutes. Set the 'first-ever, full-picture' framing."

### Slide 3: Opening Discovery (from A2)

- Title: "Before the Data — What's on Your Mind?"
- 3 questions only (not 5 — keep it tight for a first meeting):
  1. "How are the four divisions evolving — more shared operations, or more independent?"
  2. "What's driving the growth we're seeing in SCW and SC retail?"
  3. "What would make this hour most valuable for you?"
- Presenter note: "3-5 minutes. This earns permission to go deep on data. The third question lets them steer."

### Slide 4: The Value Story (from B2 overview)

- Title: "What Your Team Accomplished in Two Months"
- 4 massive stat callouts (dominate the slide):
  - $35.2M in orders
  - 7,436 transactions
  - 250 active users
  - 95.4% platform adoption
- One line beneath: "More transaction volume through eCat than nearly any account in our portfolio."
- Presenter note: "This is the moment. Let the numbers breathe. Don't rush past this slide."

### Slide 5: Entity Performance Comparison (from C2 + B2)

- Title: "Four Divisions, Four Patterns"
- Clean comparison table: entity | orders | revenue | AOV | MoM growth | self-service
  - gh: 2,215 | $6.9M | $3,384 | +1.2% | 35.8%
  - scw: 1,646 | $6.4M | $5,182 | +45.6% | 26.2%
  - sccon: 849 | $10.7M | $15,240 | +33% | 1.8%
  - sc: 2,726 | $11.2M | $4,224 | +53.3% | 0% (retail)
- Insight line: "Every entity is growing. SCW and SC are surging. SCCON dominates per-order value. GH leads digital self-service."

### Slide 6: Cross-Entity Rep Intelligence (from B2 + C3)

- Title: "Your People Work Across Divisions"
- Cross-entity power user table (top 4 with orders per entity)
- Feature breadth comparison: power users avg 16-19 vs org avg 9.8
- Concentration note: SCW at 19.7% on Ryan Casabella — approaching threshold
- Presenter note: "Name names, show specifics. This is intelligence they can't get anywhere else."

### Slide 7: Feature Adoption — What's Working vs. What's Dark (from B2 + C2)

- Title: "Platform Capabilities: Used vs. Available"
- Two-column split:
  - Left: Heavy Adoption (green accent) — Kits 78K, Configured Items 13K, Portal 11K, Camera Scan 14K, PDF Catalogs 2.2K
  - Right: Zero Adoption (gold accent) — Flipbook 0, Placements 0, Commitments 0, SmartPicks 138, Maybe Lists 12
- Bottom: "All four divisions hit all six levels of our Activity Ladder. The opportunity is in the features you haven't tried yet."

### Slide 8: Customer Intelligence (from B3 + C4)

- Title: "Your Customer Base Through the Platform Lens"
- Per-entity customer cards (compact): customers | active | activation % | top concentration
- Reactivation opportunity callout: "100 reactivated SCW accounts × $5,182 AOV = ~$518K"
- SCCON concentration flag: OMNI Hotels 8.3%, Direct Supply 7.3%

### Slide 9: Growth Momentum (from C4)

- Title: "Where the Momentum Is"
- Visual emphasis on MoM growth: SCW +45.6% and SC +53.3% as large callouts
- Revenue trajectory: SCW Jan $2.61M → Feb $3.54M, SC Jan $4.77M → Feb $6.42M
- Bottom: "Two of your four divisions are in significant growth surges right now."

### Slide 10: Data-Anchored Discovery (from B5 + A2)

- Title: "What We're Curious About"
- 4 discussion questions anchored to specific data:
  1. "Ryan Casabella drives 2,100+ orders across gh and scw — is dual-entity selling intentional?"
  2. "SC Contract's $15,240 AOV is 3-4x other divisions — are large hospitality projects your growth engine?"
  3. "Your team uses Kit workflows 78,000+ times but hasn't tried Flipbook — is that a training gap or a fit issue?"
  4. "GH leads self-service at 35.8% — what would it take to bring SCW to the same level?"
- Presenter note: "Now we've earned the discovery conversation. Both sides have shared context. Listen for which gaps they care about."

### Slide 11: Opportunities (from A6 + B6 + C7)

- Title: "Where We See Growth Potential"
- 3 recommendation cards (prioritized):
  1. **Flipbook pilot → SCCON** — Replace static PDFs for 52.9% self-service buyers. Then roll to SCW and GH.
  2. **SmartPicks pilot → SCW** — AI recommendations during +45.6% growth surge. Highest AOV entity = highest impact.
  3. **Territory configuration → SC** — Map 42 codes, unlock Portal analytics for $11.2M revenue entity.
- Presenter note: "Only present what they validated in the discovery. If they didn't engage with it in slide 10, skip it here."

### Slide 12: Cross-Entity Best Practices (from C7 + B6)

- Title: "What One Division Does Well, Others Can Learn"
- 3 transfer arrows:
  1. GH Portal adoption (5,695) → teach SC (577) and SCCON (557)
  2. GH self-service (35.8%) → playbook for SCW (26.2%)
  3. SC Camera Scan (13,332) → test at trade shows for GH and SCW
- Plus: B2B Cart for SC (missing module, incremental MRR)

### Slide 13: Support Status & Engagement (from A5 + B4)

- Title: "Housekeeping"
- Compact: 4 pending tickets (commit to resolve), payment current, MRR stable, data healthy
- Key callout: "This is the first structured review in 13 years of partnership. We're committed to quarterly going forward."

### Slide 14: Commitments (from A7)

- Title: "What We'll Do Next"
- Pre-filled:
  1. Resolve 4 pending HelpScout tickets — SuperCat — 1 week
  2. Full rep activity CSV export — SuperCat — end of week
  3. Quarterly EBR cadence agreement — Both — today
  4. [From discussion] — ___ — ___
  5. [From discussion] — ___ — ___
- "Formalized summary within 48 hours."

### Slide 15: Closing

- Dark background
- "13 Years. Four Divisions. $35 Million. This Is Just the Beginning."
- "SuperCat Solutions · March 2026"

## Output

Save as `Gabby_SC_EBR_HYBRID.html`

## Implementation Requirements

- Single self-contained HTML file. All CSS embedded. Only external dependency: Google Fonts (DM Sans + DM Mono).
- Scroll-snap layout: each slide is a `<section>` at 100vh. Scroll or arrow keys to navigate. Subtle slide counter ("3 / 15") bottom-right.
- Print-friendly: `@media print` should render one slide per page.
- Tables: DM Mono headers, muted borders, compact padding.
- Stat callouts: large numbers (48-64pt equivalent) with small labels beneath.
- The deck should look like a real presentation, not a web page with sections. Full-bleed backgrounds, centered content blocks, generous whitespace.
- Presenter notes embedded as hidden `<div class="presenter-notes">` elements, toggled with N key. Not visible by default.

## Multi-Entity Adaptation Note

None of the three EBR templates were designed for multi-entity accounts. This hybrid intentionally adds entity overview/comparison sections and cross-entity analysis that doesn't exist in the single-entity framework. The multi-entity view IS the unique value for this account.

## Data Discipline

The Intelligence Brief contains ~28,000 words of data. This deck uses roughly 5-8% of it. The slide specs above specify exactly which data points go on which slides. Do not pull additional numbers from the brief that aren't specified — that's over-stuffing. Executive decks are sparse.
